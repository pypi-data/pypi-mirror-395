import requests
import logging
import time
import os
import traceback
import json

from analytics_sdk.utilities import (
    BASE_API_URL,
    API_RETRY,
    API_TIME_STACKS,
    SPL_USER_IMP_API_KEY,
    SPL_USER_IMP_API_SECRET,
    GLOBAL_API_KEY,
    GLOBAL_API_SECRET,
    TOKEN_URL,
    DISABLE_JWT
)

DEFAULT_LEVEL = 'JWT'

logger = logging.getLogger(__name__)

class ApiClient:

    def __init__(self, user_id, run_id = None, session=None):
        self.user_id = user_id
        self.run_id = run_id
        self.global_access_header = None
        self.impersonate_access_header = None
        self.jwt_access_header = None
        self.session = session
        # self.generate_global_auth_token()
        # self.generate_impersonate_auth_token()
        # self.generate_jwt_token()

    def call_get_requests(self, url, params=None, verify=True, level=DEFAULT_LEVEL):
        return self.call_requests('GET', url, params, verify=verify, level=level)


    def call_post_requests(self, url, params=None, data=None, verify=True, level=DEFAULT_LEVEL):
        return self.call_requests('POST', url, params, data, verify=verify, level=level)


    def call_put_requests(self, url, params=None, data=None, verify=True, level=DEFAULT_LEVEL):
        return self.call_requests('PUT', url, params, data, verify=verify, level=level)


    def generate_global_auth_token(self):
        if GLOBAL_API_KEY is None or len(GLOBAL_API_KEY) <= 0 or GLOBAL_API_SECRET is None or len(GLOBAL_API_SECRET) <= 0:
            self.global_access_header = None
            return
        logging.info('invoking global auth token call...')
        headers = {"Content-Type" : "application/x-www-form-urlencoded" , "Accept" : "application/json"}
        post_data = {"grant_type": "client_credentials", "client_id" : GLOBAL_API_KEY, "client_secret" : GLOBAL_API_SECRET}
        token_url = BASE_API_URL + "/tenancy/auth/oauth/token"
        response = self.session.post(token_url,data=post_data,headers=headers,verify=False)
        json = response.json()
        auth = str(json["token_type"]) + " " + str(json["access_token"])
        self.global_access_header = {"Content-Type" : "application/json" ,"Accept" : "application/json" , "Authorization" : auth}


    def generate_impersonate_auth_token(self):
        if SPL_USER_IMP_API_KEY is None or len(SPL_USER_IMP_API_KEY) <= 0 or SPL_USER_IMP_API_SECRET is None or len(SPL_USER_IMP_API_SECRET) <= 0:
            self.impersonate_access_header = None
            return
        logging.info('invoking impersonate auth token call...')
        headers = {"Content-Type" : "application/x-www-form-urlencoded" , "Accept" : "application/json"}
        post_data = {"grant_type": "client_credentials", "client_id" : SPL_USER_IMP_API_KEY, "client_secret" : SPL_USER_IMP_API_SECRET}
        token_url = BASE_API_URL + "/tenancy/auth/oauth/token"
        response = self.session.post(token_url,data=post_data,headers=headers,verify=False)
        json = response.json()
        auth = str(json["token_type"]) + " " + str(json["access_token"])
        self.impersonate_access_header = {"Content-Type" : "application/json" ,"Accept" : "application/json" , "Authorization" : auth}


    def generate_jwt_token(self):
        self.jwt_access_header = None
        if TOKEN_URL and self.user_id is not None:
            url = BASE_API_URL + f'{TOKEN_URL}/{self.user_id}'
            response = self.call_get_requests(url, params=None, verify=True, level='IMPERSONATE')
            json = response.json()
            if 'token' in json:
                auth = 'bearer ' + json['token']
                self.jwt_access_header = {"Content-Type" : "application/json" ,"Accept" : "application/json" , "Authorization" : auth}

    def prepare_headers(self, level):
        headers = None
        if level == 'IMPERSONATE':
            if self.impersonate_access_header is None:
                self.generate_impersonate_auth_token()
            headers = self.impersonate_access_header
            return headers
        elif level == 'JWT':
            if self.jwt_access_header is None:
                self.generate_jwt_token()
            headers = self.jwt_access_header
        elif level == 'GLOBAL':
            if self.global_access_header is None:
                self.generate_global_auth_token()
            headers = self.global_access_header
        return headers


    def call_requests(self, method, url, params=None, data=None, json=None, verify=True, level=DEFAULT_LEVEL):
        # routing to global if flag is disable
        if DISABLE_JWT is not None and DISABLE_JWT == 'true':
            level = 'GLOBAL'

        retry = 1
        resp = None
        token_retries = 0  # Use local variable instead of undefined global
        
        headers = self.prepare_headers(level)

        if headers is None:
            return None

        if BASE_API_URL not in url:
            url = BASE_API_URL + url

        while retry <= API_RETRY:
            try:
                resp = self.session.request(method, url, params=params, data=data, json=json, headers=headers, verify=verify)
                logger.info(f'Params :: {params}  Data :: {data}')
                logger.info(f'Response = {resp}')
                if resp.status_code == 407:
                    if token_retries < 5:
                        logging.info(f'Token expired, re-generating token..{token_retries}' )
                        token_retries += 1
                        time.sleep(token_retries * 2)
                        self.reset_headers(level)
                        headers = self.prepare_headers(level)
                        continue  # Continue loop instead of recursive call
                    else:
                        raise Exception(f'API Fetching failed {url}')
                if resp.ok:
                    return resp
                else:
                    time.sleep(retry * 2)
                    retry += 1
            except Exception as e:
                logger.error(f'Error while fetching apis, Error Cause is ::: {e}')
                time.sleep(retry * 2)
                retry += 1

        # If we reach here, all retries failed
        error_msg = f'API Fetching failed url: {url}, params: {params}, data: {data}, after retrying for {retry-1} times'
        if resp is not None:
            try:
                error_msg += f' due to: {resp.text}'
            except:
                pass
        logger.error(error_msg)
        raise Exception(error_msg)


    def reset_headers(self, level):
        if level == 'IMPERSONATE':
            self.impersonate_access_header = None
        elif level == 'JWT':
            self.jwt_access_header = None
        elif level == 'GLOBAL':
            self.global_access_header = None


    def get_response(self, url, type, params=None):
        start_time = int(time.time())
        logging.info(f'api type: {type}, : url : {url}')
        res = self.call_get_requests(url, params=None, verify=True)
        duration = int(time.time()) - start_time
        if duration > API_TIME_STACKS:
            logging.info(f'Get {type} API response took %d (greater than %d) seconds, url : {url}', duration, API_TIME_STACKS)
        return res


    def prepare_page_size_page_no(self, data, page_no, page_size):
        if data and data is not None:
            if "pageNo" in data:
                data["pageNo"] = page_no
                if "pageSize" not in data:
                    data["pageSize"] = page_size
        return data
    
    
    def add_page_no_page_size_for_url(self, add_page_no, url, page_no, page_size):
        uri = url
        if add_page_no:
            if "pageSize" not in url:
                uri = url + f'&pageNo={page_no}&pageSize={page_size}'
            else:
                uri = url + f'&pageNo={page_no}'
        return uri
    
    
    def get_paginated_api_results(self, method, url, data, type, add_pageNo=True):
        resp = []
        page_no=1
        nextPage= True
        page_size= 100

        try:
            error_message = ''
            while (nextPage != False):
                data = json.loads(data)
                data = self.prepare_page_size_page_no(data, page_no, page_size)
                data=json.dumps(data)
                if method == 'POST':
                    res = self.get_post_request_results(url, data, type)
                else:
                    uri = self.add_page_no_page_size_for_url(add_pageNo, url, page_no, page_size)
                    res = self.get_response(uri, type)
                if res == None or not res.ok or (res.json() is not None and "results" not in res.json()) or (res is not None and "nextPage" not in res.json()):
                    error_message = f'Get {type} API is failed, run_id ::: {self.run_id}, url ::: {url}, response ::: {res}'
                    logger.error('Get %s API is failed, run_id : %s, url ::: %s, response ::: %s ', type, self.run_id, url, res)
                    retry_count = 1
                    while (retry_count <= API_RETRY):
                        data = json.loads(data)
                        data = self.prepare_page_size_page_no(data, page_no, page_size)
                        data=json.dumps(data)

                        time.sleep(1)
                        retry_count += 1
                        if method == 'POST':
                            res = self.get_post_request_results(url, data, type)
                        else:
                            uri = self.add_page_no_page_size_for_url(add_pageNo, url, page_no, page_size)
                            res = self.get_response(uri, type)
                        if res == None or not res.ok:
                            error_message = f'Get {type} API is failed, run_id ::: {self.run_id}, url ::: {url}, response ::: {res}, response_json ::: {res.json()}, API_Retry_Count ::: {retry_count}'
                            logger.error('Get %s API is failed, run_id ::: %s, url ::: %s, response ::: %s, response_json ::: %s, API_Retry_Count ::: %s ', type, self.run_id, url, res, res.json(), retry_count)
                            res = None
                            if retry_count > 3:
                                raise Exception(error_message)
                        elif res.json() is not None and "results" not in res.json():
                            error_message = f"Get {type} results keyword is missing in API response, run_id ::: {self.run_id}, url ::: {url}, response ::: {res}, response_json ::: {res.json()}, API_Retry_Count ::: {retry_count}"
                            logger.error('Get %s results keyword is missing in API response, run_id ::: %s, url ::: %s, response : %s, response_json ::: %s, API_Retry_Count ::: %s ', type, self.run_id, url, res, res.json(), retry_count)
                            res = None
                            if retry_count > 3:
                                raise Exception(error_message)
                        elif res.json() is not None and "nextPage" not in res.json():
                            error_message = f"Get {type} nextPage keyword is missing in API response, run_id ::: {self.run_id}, url : {url}, response ::: {res}, response_json ::: {res.json()}, API_Retry_Count ::: {retry_count}"
                            logger.error('Get %s nextPage keyword is missing in API response, run_id ::: %s, url ::: %s, response : %s, response_json ::: %s, API_Retry_Count ::: %s ', type, self.run_id, url, res, res.json(), retry_count)
                            res = None
                            if retry_count > 3:
                                raise Exception(error_message)
                        else:
                            break
                    if res == None or "results" not in res.json() or len(res.json()['results'])==0:
                        logger.error('After retrying for %s times, Get %s API results are empty, run_id ::: %s, url is %s', API_RETRY, type, self.run_id, url)
                        return None
                #else:
                result = res.json()['results']
                resp.append(result)

                if "nextPage" not in res.json():
                    error_message = f"Get {type} nextPage keyword is missing in API response, run_id ::: {self.run_id}, url ::: {url}, response : {res}, response_json ::: {res.json()},"
                    logger.error('Get %s nextPage keyword is missing in API response, run_id ::: %s, url ::: %s, response ::: %s, response_json ::: %s', type, self.run_id, url, res, res.json())
                    raise Exception(error_message)

                nextPage=res.json()['nextPage']
                page_no+=1

            resp = [item for sublist in resp for item in sublist] # To eliminate list of list (ex: [[data:{}]] -> [data:{}])
        except Exception as e:
            traceback.print_exc()
            logger.error(f'get_paginated_api_results : Error while fetching apis, Error Cause is ::: {e}')
            raise Exception(f'{error_message}')
        return resp

    def get_topn_api_results(self, method, url, data, type, add_pageNo=True):
        resp = []
        page_no=1
        nextPage= True
        page_size= 100
        try:
            error_message = ''
            # while (nextPage != False):
            data = json.loads(data)
            data = self.prepare_page_size_page_no(data, page_no, page_size)
            data=json.dumps(data)
            if method == 'POST':
                res = self.get_post_request_results(url, data, type)
            else:
                uri = self.add_page_no_page_size_for_url(add_pageNo, url, page_no, page_size)
                res = self.get_response(uri, type)
            if res == None or not res.ok or (res.json() is not None and "results" not in res.json()) or (res is not None and "nextPage" not in res.json()):
                error_message = f'Get {type} API is failed, run_id ::: {self.run_id}, url ::: {url}, response ::: {res}'
                logger.error('Get %s API is failed, run_id : %s, url ::: %s, response ::: %s ', type, self.run_id, url, res)
                retry_count = 1
                while (retry_count <= API_RETRY):
                    data = json.loads(data)
                    data = self.prepare_page_size_page_no(data, page_no, page_size)
                    data=json.dumps(data)

                    time.sleep(1)
                    retry_count += 1
                    if method == 'POST':
                        res = self.get_post_request_results(url, data, type)
                    else:
                        uri = self.add_page_no_page_size_for_url(add_pageNo, url, page_no, page_size)
                        res = self.get_response(uri, type)
                    if res == None or not res.ok:
                        error_message = f'Get {type} API is failed, run_id ::: {self.run_id}, url ::: {url}, response ::: {res}, response_json ::: {res.json()}, API_Retry_Count ::: {retry_count}'
                        logger.error('Get %s API is failed, run_id ::: %s, url ::: %s, response ::: %s, response_json ::: %s, API_Retry_Count ::: %s ', type, self.run_id, url, res, res.json(), retry_count)
                        res = None
                        if retry_count > 3:
                            raise Exception(error_message)
                    elif res.json() is not None and "results" not in res.json():
                        error_message = f"Get {type} results keyword is missing in API response, run_id ::: {self.run_id}, url ::: {url}, response ::: {res}, response_json ::: {res.json()}, API_Retry_Count ::: {retry_count}"
                        logger.error('Get %s results keyword is missing in API response, run_id ::: %s, url ::: %s, response : %s, response_json ::: %s, API_Retry_Count ::: %s ', type, self.run_id, url, res, res.json(), retry_count)
                        res = None
                        if retry_count > 3:
                            raise Exception(error_message)
                    elif res.json() is not None and "nextPage" not in res.json():
                        error_message = f"Get {type} nextPage keyword is missing in API response, run_id ::: {self.run_id}, url : {url}, response ::: {res}, response_json ::: {res.json()}, API_Retry_Count ::: {retry_count}"
                        logger.error('Get %s nextPage keyword is missing in API response, run_id ::: %s, url ::: %s, response : %s, response_json ::: %s, API_Retry_Count ::: %s ', type, self.run_id, url, res, res.json(), retry_count)
                        res = None
                        if retry_count > 3:
                            raise Exception(error_message)
                    else:
                        break
                if res == None or "results" not in res.json() or len(res.json()['results'])==0:
                    logger.error('After retrying for %s times, Get %s API results are empty, run_id ::: %s, url is %s', API_RETRY, type, self.run_id, url)
                    return None
            #else:
            result = res.json()['results']
            resp.append(result)

            # if "nextPage" not in res.json():
            #     error_message = f"Get {type} nextPage keyword is missing in API response, run_id ::: {self.run_id}, url ::: {url}, response : {res}, response_json ::: {res.json()},"
            #     logger.error('Get %s nextPage keyword is missing in API response, run_id ::: %s, url ::: %s, response ::: %s, response_json ::: %s', type, self.run_id, url, res, res.json())
            #     raise Exception(error_message)

            # nextPage=res.json()['nextPage']
            # page_no+=1

            resp = [item for sublist in resp for item in sublist] # To eliminate list of list (ex: [[data:{}]] -> [data:{}])
        except Exception as e:
            traceback.print_exc()
            logger.error(f'get_paginated_api_results : Error while fetching apis, Error Cause is ::: {e}')
            raise Exception(f'{error_message}')
        return resp

    def get_post_request_results(self, url, data, type):
        start_time = int(time.time())
        logging.info(f'api type: {type}, : url : {url}')

        res = self.call_post_requests(url, data=data, verify=False)
        duration = int(time.time()) - start_time
        if duration > API_TIME_STACKS:
            logging.info(f'Get {type} API response took %d (greater than %d) seconds, url : {url}', duration, API_TIME_STACKS)
        return res


    def get_post_opsql_count_results(self, url, data, type):
        res = self.get_post_request_results(url, data, type)
        if res == None or not res.ok:
            logger.error('FAILED :' + type)
            return None
        elif "count" not in res.json() or len(res.json()) == 0:
            logger.error('Result are Empty for ' + type)
            return None
        else:
            resp = res.json()

        return resp


    def get_post_request_results(self, url, data, type):
        start_time = int(time.time())
        logging.info(f'api type: {type}, : url : {url}')

        res = self.call_post_requests(url, data=data, verify=False)
        duration = int(time.time()) - start_time
        if duration > API_TIME_STACKS:
            logging.info(f'Get {type} API response took %d (greater than %d) seconds, url : {url}', duration, API_TIME_STACKS)
        return res


    def get_post_opsql_count_results(self, url, data, type):
        res = self.get_post_request_results(url, data, type)
        if res == None or not res.ok:
            logger.error('FAILED :' + type)
            return None
        elif "count" not in res.json() or len(res.json()) == 0:
            logger.error('Result are Empty for ' + type)
            return None
        else:
            resp = res.json()

        return resp
    

    def prepare_tenant_list(self, form, parameters, all_clients=False):
        def fetch_all_clients(tenant_id, context, all_clients):
            def get_tenant_list(org_id, level, tenant_list):
                def get_tenants(orgId):
                    url = BASE_API_URL + f'/api/v2/tenants/{orgId}/clients/minimal'
                    res = self.get_response(url, 'V2 Tenants')
                    logger.info('Get tenants API response is %s', res)
                    if res == None or not res.ok:
                        logger.error('Get tenants API is failed')
                    return res.json()

                tenant_id_list = []
                if level == 'partner':
                    tenant_id_list.append(org_id)
                elif level == 'all-clients':
                    tenants = get_tenants(org_id)
                    for tenant in tenants:
                        tenant_id_list.append(tenant['uniqueId'])
                elif level == 'specific_clients':
                    for tenant in tenant_list:
                        tenant_id_list.append(tenant['uniqueId'])
                else:
                    tenant_id_list.append(org_id)
                return tenant_id_list

            tenant_id_list = []
            if all_clients and context == 'partner':
                context = 'all-clients'
            tenant_id_list = get_tenant_list(tenant_id, context, None)
            return tenant_id_list
        tenant_id_list = []
        if parameters is not None and len(parameters) > 0:
            if 'allClients' in parameters and (parameters['allClients'] == True or parameters['allClients'] == 'true'):
                tenant_id_list = fetch_all_clients(form.get_tenant_id(), form.get_tenant_context(), all_clients)
            elif 'client' in parameters and parameters['client'] is not None:
                clients = parameters['client']
                if clients is not None:
                    if clients == 'All Clients' or clients == 'All Client' or clients == ['All Clients'] or clients == 'all client' or clients == 'all clients':
                        tenant_id_list = fetch_all_clients(form.get_tenant_id(), form.get_tenant_context(), all_clients)
                    else:
                        if isinstance(clients, list):
                            tenant_id_list = clients
                        else:
                            for i in clients.split(','):
                                tenant_id_list.append(i)
            else:
                tenant_id_list = fetch_all_clients(form.get_tenant_id(), form.get_tenant_context(), all_clients)
        else:
            tenant_id_list = fetch_all_clients(form.get_tenant_id(), form.get_tenant_context(), all_clients)
        return tenant_id_list

