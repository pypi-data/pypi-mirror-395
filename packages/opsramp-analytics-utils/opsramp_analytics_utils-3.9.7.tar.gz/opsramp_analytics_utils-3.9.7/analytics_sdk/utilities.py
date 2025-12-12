import os
import csv
import re
import time
import datetime
import logging
import random
from io import BytesIO
import json
import traceback
from datetime import datetime
import pytz
import yaml
from urllib.request import urlopen
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from flask.wrappers import Response
import socket

import boto3
import botocore
from botocore.exceptions import NoCredentialsError
import flask
import requests
from flask import request, session, redirect, Response
from .constants import *
from analytics_sdk.config.config import *
logger = logging.getLogger(__name__)
from google.cloud import storage

BASE_API_URL = load_value('data.api.base.url', APP, None)
API_RETRY = load_value('api.retry', APP, None)
API_TIME_STACKS = load_value('api.time.stacks', APP, 5)
LOG_LEVEL = load_value('log.level', APP, None)
PYTHONWARNINGS = load_value('python.warnings', APP, None)
NO_OF_API_THREADS = load_value('no.of.api.threads', APP, 2)
DISABLE_API_THREADS = load_value('disable.api.threads', APP, True)
API_PAGE_SIZE = load_value('api.page.size', APP, 500)
PDF_SERVICE = load_value('pdf.service', APP, None)
DASH_BOARD_PDF_SERVICE = load_value('dash.board.pdf.service', APP, None)
API_KEY = load_value('api.key', AUTH, None)
API_SECRET = load_value('api.secret', AUTH, None)
SPL_USER_IMP_API_KEY = load_value('spl.user.imp.api.key', AUTH, None)
SPL_USER_IMP_API_SECRET = load_value('spl.user.imp.api.secret', AUTH, None)
GLOBAL_API_KEY = load_value('api.key', AUTH, None)
GLOBAL_API_SECRET = load_value('api.secret', AUTH, None)
TOKEN_URL = load_value('token.url', AUTH, None)
DISABLE_JWT = load_value('disable.jwt', AUTH, 'False')
REQUIRE_AUTH_REDIRECT = load_value('require.auth.redirect', AUTH, 'True')
KAFKA_BROKERS = load_value('kafka.brokers', KAFKA, None)
WORKER_THREADS = load_value('worker.threads', KAFKA, None)
OPSQL_OBJECT_TYPES = load_value('opsql.object.types', APP, None)

APP_ID = load_value('APP_ID')
APP_DISPLAY_NAME = load_value('APP_DISPLAY_NAME', None, APP_ID)
PLATFORM_ROUTE = load_value("PLATFORM_ROUTE", None, '')
ENABLED_AUTO_RESCHEDULE_RUNS = load_value('ENABLED_AUTO_RESCHEDULE_RUNS', None, 'true')
EXCLUDE_RUN_IDS = load_value('EXCLUDE_RUN_IDS', None, '')
API_TASKS_BATCH_SIZE = load_value('api.tasks.batch.size', APP, 50)
OPSQL_JOIN_API_PAGE_SIZE = load_value('opsql.join.api.page.size', APP, 100)


from .renderer.excel import ExcelRenderer
from .renderer.pdf import PDF

class GCPCloudHandler:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.gcp_client = self._init_gcp_client()
        self._is_bucket_existed(bucket_name)
        self.bucket = self.gcp_client.bucket(bucket_name)

    def _init_gcp_client(self):
        try:
            client = storage.Client()
            return client
        except Exception as e:
            print(f"Failed to initialize GCP client : {e}")
            raise e

    def _is_bucket_existed(self, bucket_name):
        try:
            bucket = self.gcp_client.get_bucket(bucket_name)
        except Exception as e:
            print(f"Error verifying bucket {self.bucket_name} : {e}")
            raise e

storage_name = load_value('storage.name', STORAGE, None)

global ACCESS_KEY_ID, SECRET_ACCESS_KEY, REGION_NAME, BUCKET_NAME, ACCESS_HEADER, TOKEN_RETRIES
GCP_OBJ = None

if storage_name == 's3':
    ACCESS_KEY_ID = load_value('access.key.id', STORAGE, None)
    SECRET_ACCESS_KEY = load_value('secret.access.key', STORAGE, None)
    REGION_NAME = load_value('region.name', STORAGE, None)
    BUCKET_NAME = load_value('bucket.name', STORAGE, None)
    S3_ENDPOINT_URL = load_value('s3.endpoint.url', STORAGE, None)
    if S3_ENDPOINT_URL is not None:
        if 'http://' not in S3_ENDPOINT_URL and 'https://' not in S3_ENDPOINT_URL:
            S3_ENDPOINT_URL = 'https://'+S3_ENDPOINT_URL
elif storage_name == 'ceph':
    ACCESS_KEY_ID = load_value('access.key.id', STORAGE, None)
    SECRET_ACCESS_KEY = load_value('secret.access.key', STORAGE, None)
    BUCKET_NAME = load_value('bucket.name', STORAGE, None)
    ENDPOINT_URL = load_value('endpoint.url', STORAGE, None)
elif storage_name.lower() == 'gcp':
    BUCKET_NAME = load_value('bucket.name', STORAGE, None)
    GCP_OBJ = GCPCloudHandler(BUCKET_NAME)
else:
    logger.info("No storages are found")

TOKEN_RETRIES = 0
ACCESS_HEADER = None

def get_token():
    with requests.Session() as session:
        headers = {"Content-Type" : "application/x-www-form-urlencoded" , "Accept" : "application/json"};
        post_data = {"grant_type": "client_credentials", "client_id" : API_KEY, "client_secret" : API_SECRET};
        token_url = BASE_API_URL + "/tenancy/auth/oauth/token";
        response = session.post(token_url,data=post_data,headers=headers,verify=False);
        json = response.json();
        auth = str(json["access_token"])
        return auth


def get_jwt_token():
    try:
        jwt_token = flask.request.cookies.get('OPSRAMP_JWT_TOKEN', '')
    except:  # outside Flask
        jwt_token = os.getenv('OPSRAMP_JWT_TOKEN', '')

    return jwt_token


def get_headers():
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {get_token()}'
    }

    return headers


def login_get_headers():
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {get_jwt_token()}'
    }

    return headers


def get_auth_token(session=None):
    logging.info('invoking auth token call...')
    headers = {"Content-Type" : "application/x-www-form-urlencoded" , "Accept" : "application/json"}
    post_data = {"grant_type": "client_credentials", "client_id" : API_KEY, "client_secret" : API_SECRET}
    token_url = BASE_API_URL + "/tenancy/auth/oauth/token"
    response = session.post(token_url,data=post_data,headers=headers,verify=False)
    json = response.json()
    auth = str(json["token_type"]) + " " + str(json["access_token"])
    global ACCESS_HEADER
    ACCESS_HEADER = {"Content-Type" : "application/json" ,"Accept" : "application/json" , "Authorization" : auth}


def call_requests(method, url, params=None, session=None, data=None, json=None, verify=True):
    retry = 1
    resp = None
    if session is None:
        print("Utilities :: Session is Empty... So fallback to requests ::: ", url)
        session = requests
    if ACCESS_HEADER is None:
        get_auth_token(session=session)
        global TOKEN_RETRIES
        TOKEN_RETRIES = 0
    while retry <= API_RETRY:
        try:
            resp = session.request(method, url, params=params, data=data, json=json, headers=ACCESS_HEADER, verify=verify)
            logger.info(f'Params :: {params}  Data :: {data}')
            logger.info(f'Response = {resp}')
            if resp.status_code == 407:
                if TOKEN_RETRIES < 5:
                    logging.info(f'Token expired, re-generating token..{TOKEN_RETRIES}' )
                    TOKEN_RETRIES +=1
                    time.sleep(TOKEN_RETRIES * 2)
                    get_auth_token(session=session)
                    call_requests(method, url, params=params, session=session,  data=data, json=json, verify=verify)
                else:
                    TOKEN_RETRIES = 0
                    raise Exception(f'API Fetching failed {url}')
            if not resp.ok:
                time.sleep(retry * 2)
                retry+=1
                continue
        except requests.exceptions.ConnectionError:
            time.sleep(retry * 2)
            retry+=1
            continue

        TOKEN_RETRIES = 0
        return resp
    
    return resp


def login_call_requests(method, url, params=None, data=None, json=None, verify=True):
    headers = login_get_headers()
    retry = 1
    resp = None
    with requests.Session() as session:  # Use a session with a context manager
        while retry <= API_RETRY:
            print(f"Processing authentication request at {retry} iteration ")
            try:
                resp = session.request(method, url, params=params, data=data, json=json, headers=headers, verify=verify)
                print("authentication response is ", resp, url)
                if not resp.ok:
                    time.sleep(retry * 2)
                    retry+=1
                    print(f"Invalid response, going to {retry} iteration ")
                    continue
            except requests.exceptions.ConnectionError:
                time.sleep(retry * 2)
                retry+=1
                print(f"Got the exception, going to {retry} iteration ")
                continue
            print("Response is ", resp)
            return resp
        return resp


def call_get_requests(url, session=None, params=None, verify=True):
    return call_requests('GET', url, params, session=session, verify=verify)


def call_post_requests(url, session=None, params=None, data=None, verify=True):
    return call_requests('POST', url, params, session=session, data=data, verify=verify)


def call_put_requests(url, session=None, params=None, data=None, verify=True):
    return call_requests('PUT', url, params, session=session, data=data, verify=verify)


def login_call_get_requests(url, params=None, verify=True):
    return login_call_requests('GET', url, params, verify=verify)


def has_reports_view_permission(data):
    is_reports_view = False
    if data and data is not None and len(data)>0:
        if 'permissions' in data:
            permissions = data.get("permissions", [])
            is_reports_view = any(item.lower() == 'reports_view' for item in permissions)
    return is_reports_view


def is_authenticated():
    # REQUIRE_AUTH_REDIRECT = os.getenv('REQUIRE_AUTH_REDIRECT') == 'true'
    print("Getting authentication configuration value is ", REQUIRE_AUTH_REDIRECT)
    if not REQUIRE_AUTH_REDIRECT:
        print("authentication is not verifying,means bypassing authentication")
        return True
    if get_jwt_token():
        url = f'{BASE_API_URL}/api/v2/users/me'
        print("authentication is verifying, request URL is ",url)
        res = login_call_get_requests(url)
        if res.ok and res is not None and res.json() and res.json ()is not None and len(res.json())>0:
            json_resp = res.json()
            if has_reports_view_permission(json_resp):
                print("User has 'Reports View' permission. Access granted.")
                return True
            return "no_reports_view_permission"
        print("authentication is failed...", res)
        return False
        # return res.status_code == 200
    print("Invalid authentication, redirecting to login url")
    return False


def check_required_permissions(result):
    if not result:
        redirect_url = BASE_API_URL + f'/tenancy/web/login?cb=/loginResponse.do'
        logger.info("authentication is failed, redirecting to login url is %s", redirect_url)
        print("authentication is failed, redirecting to login url is ", redirect_url)
        return flask.redirect(redirect_url, code=302)
        # return Response("Unauthorized", 401)
    elif result == 'no_reports_view_permission':
        logger.info("Access denied: You are authenticated but lack the required reports permissions.")
        print("Access denied: You are authenticated but lack the required reports permissions.")
        return flask.Response('Access denied: You are authenticated but lack the required reports permissions.', status=403)


def check_auth_cache(path, auth_cache):
    if path not in auth_cache:
        # :x: Not cached — perform expensive auth check
        result = is_authenticated()
        # Cache result for this endpoint
        auth_cache[path] = result
        session["auth_cache"] = auth_cache
        return check_required_permissions(result)
    else:
        return check_required_permissions(auth_cache[path])


def login_required(view):
    '''Decorator that check authentication'''
  
    def wrap(*args, **kwargs):
        if not is_authenticated():
            return Response('Not authorized', status=401)
        result = view(*args, **kwargs)
        return result
    return wrap


def get_epoc_from_datetime_string(str_datetime):
    timestamp = datetime.strptime(str_datetime, DATETIME_FORMAT).timestamp()
    return timestamp


def _retrive_value_from_json(json_object, key, default_value=None):
    try:
        result = json.loads(json_object)
        if key:
            result = result.get(key, default_value)
        return result
    except Exception as e:
        raise e


def get_result_by_run(run_id, field=None, default_value=None):
    try:
        # run_id= f'{PLATFORM_ROUTE}/{run_id}/json/{run_id}'
        if storage_name == 's3':
            run_id= f'{PLATFORM_ROUTE}/{run_id}/json/{run_id}'
            s3 = get_s3_client()
            res_object = s3.get_object(Bucket=BUCKET_NAME,Key=run_id)
            serializedObject = res_object['Body'].read()
            result = _retrive_value_from_json(serializedObject, field, default_value)
            return result
        elif storage_name == 'ceph':
            run_id= f'{APP_ID.lower()}/{run_id}/json/{run_id}'
            s3 = get_ceph_resource()
            data = BytesIO()
            res_object = s3.Bucket(BUCKET_NAME).download_fileobj(Fileobj=data,Key=run_id)   
            res_object = data.getvalue()
            result = _retrive_value_from_json(res_object, field, default_value)
            return result
        elif storage_name.lower() == 'gcp':
            run_id= f'{PLATFORM_ROUTE}/{run_id}/json/{run_id}'
            blob = GCP_OBJ.bucket.blob(run_id)
            serializedObject = blob.download_as_string()
            result = _retrive_value_from_json(serializedObject, field, default_value)
            return result
        else:
            logger.info("No storages are found")
    except Exception as e:
        logger.error('An error occurred (NoSuchKey) when calling the GetObject operation: The specified key does not exist')
        traceback.print_stack()
        pass


def get_response(url, type, session=None, params=None):
    start_time = int(time.time())
    logging.info(f'api type: {type}, : url : {url}')
    res = call_get_requests(url, session=session, params=None, verify=True)
    duration = int(time.time()) - start_time
    if duration > API_TIME_STACKS:
        logging.info(f'Get {type} API response took %d (greater than %d) seconds, url : {url}', duration, API_TIME_STACKS)
    return res


def get_ses_client():
    return boto3.client('ses',
                        region_name=REGION_NAME,
                        aws_access_key_id=ACCESS_KEY_ID,
                        aws_secret_access_key=SECRET_ACCESS_KEY)


def get_s3_client():
    if ((ACCESS_KEY_ID is None or len(ACCESS_KEY_ID) <= 0) and (SECRET_ACCESS_KEY is None or len(SECRET_ACCESS_KEY) <= 0)):
       return boto3.client('s3',
                        region_name=REGION_NAME,
                        endpoint_url=S3_ENDPOINT_URL)
    return boto3.client('s3',
                        region_name=REGION_NAME,
                        aws_access_key_id=ACCESS_KEY_ID,
                        aws_secret_access_key=SECRET_ACCESS_KEY,
                        endpoint_url=S3_ENDPOINT_URL)

def get_s3_resource():
    if ((ACCESS_KEY_ID is None or len(ACCESS_KEY_ID) <= 0) and (SECRET_ACCESS_KEY is None or len(SECRET_ACCESS_KEY) <= 0)):
        return boto3.resource('s3',
                            region_name=REGION_NAME,
                            endpoint_url=S3_ENDPOINT_URL)
    return boto3.resource('s3',
                            region_name=REGION_NAME,
                            aws_access_key_id=ACCESS_KEY_ID,
                            aws_secret_access_key=SECRET_ACCESS_KEY,
                            endpoint_url=S3_ENDPOINT_URL)
    

def get_ceph_resource():
    return boto3.resource('s3',
                            endpoint_url=ENDPOINT_URL,
                            aws_access_key_id=ACCESS_KEY_ID,
                            aws_secret_access_key=SECRET_ACCESS_KEY)


def get_ceph_client():
    return boto3.client('s3',
                          endpoint_url=ENDPOINT_URL,
                          aws_access_key_id=ACCESS_KEY_ID,
                          aws_secret_access_key=SECRET_ACCESS_KEY)


def send_email(subject, from_email, to_emails, body, attachment=None):
    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = from_email
    message['To'] = to_emails

    # message body
    part = MIMEText(body, 'html')
    message.attach(part)

    if attachment:
        attachment_body = urlopen(attachment).read()
        part = MIMEApplication(attachment_body)
        part.add_header('Content-Disposition', 'attachment', filename=attachment)
        message.attach(part)

    resp = get_ses_client().send_raw_email(
        Source=message['From'],
        Destinations=to_emails.split(','),
        RawMessage={
            'Data': message.as_string()
        }
    )

    return resp


def upload_to_storage(content, location):
    '''
    :param: content: bytes
    :param: location: str
    '''
    if storage_name == 's3':
        s3 = get_s3_resource()
        object_url = f'https://{BUCKET_NAME}.s3.{REGION_NAME}.amazonaws.com/{location}'
        try:
            s3.Bucket(BUCKET_NAME).put_object(Body=content,
                                              Key=location)
            #return object_url
            return location
        except Exception as e:
            logger.error(f"Error uploading json file to S3: {e}")
            pass
    elif storage_name == 'ceph':
        try:
            s3 = get_ceph_resource()
            bucket_check = s3.Bucket(BUCKET_NAME) in s3.buckets.all()
            
            if bucket_check:
                logger.info(f'{BUCKET_NAME} Bucket already exists!')
            else:
                logger.info(f'{BUCKET_NAME} Bucket does not exist!')
                try:
                    bucket = s3.Bucket(BUCKET_NAME)
                    bucket.create()
                except botocore.parsers.ResponseParserError as error:
                    #Bucket is created is successfully, but throwing an error. So that we are catching and passing that error(But not throwing that error)
                    bucket_check = s3.Bucket(BUCKET_NAME) in s3.buckets.all()
                    if bucket_check:
                        logger.info(f'{BUCKET_NAME} bucket created...')
                    else:
                        logger.info(f'{BUCKET_NAME} bucket is not created...')
                    pass
            
            s3.Bucket(BUCKET_NAME).put_object(Bucket=BUCKET_NAME,
                                              Key=location,
                                              Body=content)
            #return object_url
            return location
        except Exception as e:
            logger.error(f"Error uploading json file to Ceph: {e}")
            pass
    elif storage_name.lower() == 'gcp':
        try:
            blob = GCP_OBJ.bucket.blob(location)
            blob.upload_from_string(content)
            #object_url = f'https://storage.googleapis.com/{BUCKET_NAME}/{location}'
            print("gcp file upload location is ", location)
            return location
        except Exception as e:
            logger.error(f"Error uploading json file to GCP: {e}")
            pass
    else:
        logger.info("No storages are found")


def generate_pdf(analysis_run):
    logger.info(f'{analysis_run} :: Entered into pdf generation process')
    try:
        url = PDF_SERVICE
        current_date = datetime.now()
        # file_name = APP_ID.lower() + '-' + pdf.analysis_run[:8] + '-' + current_date.strftime("%Y-%m-%d-%H-%M-%S") + '.pdf'
        report_path = ''
        if storage_name == 's3' or storage_name.lower() == 'gcp':
            report_path = PLATFORM_ROUTE
        elif storage_name == 'ceph':
            report_path = APP_ID.lower()
        pdf = PDF(analysis_run, url, report_path, current_date.strftime("%Y-%m-%d-%H-%M-%S"))
        file_name = pdf.prepare_file_name(APP_ID.lower(), 'pdf')
        file_path = pdf.report_path + '/' + pdf.analysis_run + '/pdf/' + file_name
        data = {
            'domain': BASE_API_URL,
            'report': PLATFORM_ROUTE,
            'run': pdf.analysis_run,
            'route': '/full-view',
            'token': get_token(),
            'app_id': APP_ID,
            'size': 'A4',
            'storage': storage_name,
            'file_name': file_name,
            'file_path': file_path
        }
        
        gen_retry = 1
        while gen_retry <= 2:
            logging.info(f'{pdf.analysis_run} :: pdf generation trying {gen_retry} time..')
            gen_retry += 1
            logging.info(f'b4 generation >> full file path : {file_path}')
            response = pdf.generate(data)
            logging.info(f'after generation >> full file path : {file_path}')
            if response == 504:
                storage_retry = 1
                file_found = False
                while storage_retry <= API_RETRY:
                    logging.info(f'{pdf.analysis_run} checking the file is existing in storage or not {storage_retry} time..')
                    file_found = is_file_in_storage(file_path)
                    if file_found == True:
                        logging.info(f'{pdf.analysis_run} the pdf file is found in storage')
                        return file_path
                    else:
                        time.sleep(storage_retry * 30)
                        storage_retry += 1
                        logging.info(f'{pdf.analysis_run} pdf not found in storage trying for {storage_retry} time..')
                        continue
            else:
                return response
        raise Exception(f'Generate_pdf:: pdf generation failed after max tries ({API_RETRY}), for run ::: {pdf.analysis_run}')
    except Exception as e:
        traceback.print_exc()
        err_msg = f'Generate_pdf:: Exeception - pdf generation failed after max tries({API_RETRY}), for run ::: {pdf.analysis_run}'
        raise Exception(err_msg)


def is_file_in_storage(file_path: str):
    try:
        if storage_name == 's3':
            s3 = get_s3_client()
            res_object = s3.get_object(Bucket=BUCKET_NAME,Key=file_path)
            return True
        elif storage_name == 'ceph':
            s3 = get_ceph_resource()
            data = BytesIO()
            res_object = s3.Bucket(BUCKET_NAME).download_fileobj(Fileobj=data,Key=file_path)
            return True
        elif storage_name.lower() == 'gcp':
            blob = GCP_OBJ.bucket.blob(file_path)
            if blob.exists():
                return True
        else:
            return False
    except Exception as e:
        return False


def generate_excel(analysis_run, orgId, client_name, excel_data, report_gen_start_time, report_gen_completed_time, file_name=None):
    try:
        excel_renderer = ExcelRenderer(analysis_run, orgId, client_name, excel_data, report_gen_start_time, report_gen_completed_time)
        workbook = excel_renderer.render()
    except Exception as ex:
        raise ex

    if file_name:
        output = None
        workbook.save(file_name)
    else:
        output = BytesIO()
        workbook.save(output)

    return output


def diff_sec(st, et):
    difference = int(et - st)
    return difference


def add_custom_headers(response):
    # Add CORS headers
    response.headers['Access-Control-Max-Age'] = 3600
    response.headers['Access-Control-Expose-Headers'] = 'Content-Length'
    response.headers['Access-Control-Allow-Headers'] = 'Range'
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, DELETE, PATCH'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['Content-Security-Policy'] = "script-src: 'self' 'unsafe-inline' https://www.google.com"
    response.headers['Strict-Transport-Security'] = "max-age=31536000 ; includeSubDomains;preload;"
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Xss-Protection'] = "1;mode=block"
    return response


# Cache Control Mechanism
def add_cache_control(response):
    # Check if the requested URL matches the _dash-component-suites route
    path = request.path
    if "/opsramp-analytics-utils/" in path or path.endswith("/_dash-layout") or path.endswith("/_dash-dependencies"):
        # Add Cache-Control header to the response for browser caching
        response.headers['Cache-Control'] = 'max-age=31536000'  # Cache for 365 days
    return response


def update_status_url(analysisRunId, tenantId, genStime, genEtime, status=None, session=None):

    url = BASE_API_URL + f'/reporting/api/v3/tenants/{tenantId}/runs/{analysisRunId}'
    pod_name = socket.gethostname()
    data={
            "status" : status,
            "runDurStartDate" : genStime,
            "runDurEndDate" : genEtime,
            "podName" : pod_name
        }
    
    api_proce_before_time = time.time()
    res = call_put_requests(url, session=session, data=json.dumps(data), verify=False);
    api_proce_after_time = time.time()
    api_proce_diff = diff_sec(api_proce_before_time, api_proce_after_time)
    if api_proce_diff > API_TIME_STACKS:
        logging.info('Status update response took %d (greater than %d) seconds', api_proce_diff, API_TIME_STACKS)
    logger.info('Status update response is %s', res)


def update_results_url(gen_start_time, analysisRunId, tenantId, json_result_url=None, gen_completed_time=None, excel_result_url=None, pdf_result_url=None, failure_reason=None, status=None, csv_result_url=None, session=None):

    url = BASE_API_URL + f'/reporting/api/v3/tenants/{tenantId}/runs/{analysisRunId}'
    pod_name = socket.gethostname()
    
    if storage_name == 'ceph':
        if excel_result_url is not None:
            excel_result_url = f'{BUCKET_NAME}/{excel_result_url}'
        if pdf_result_url is not None:
            pdf_result_url = f'{BUCKET_NAME}/{pdf_result_url}'
        if csv_result_url is not None:
            csv_result_url = f'{BUCKET_NAME}/{csv_result_url}'
    data={
            "status" : status,
            "resultUrl" : json_result_url,
            "pdfFilePath" : pdf_result_url,
            "xlsxFilePath" : excel_result_url,
            "csvFilePath" : csv_result_url,
            "repGenStartTime" : gen_start_time,
            "repGenEndTime" : gen_completed_time,
            "failureReason" : failure_reason,
            "podName" : pod_name
        }

    api_proce_before_time = time.time()
    res = call_put_requests(url , session=session, data=json.dumps(data), verify=False);
    api_proce_after_time = time.time()
    api_proce_diff = diff_sec(api_proce_before_time, api_proce_after_time)
    if api_proce_diff > API_TIME_STACKS:
        logging.info('Database update response took %d (greater than %d) seconds', api_proce_diff, API_TIME_STACKS)
    logger.info('Database update response is %s', res)
    
    
def upload_file(run_id, reportname, filepath):
    excel_file_location = f'{PLATFORM_ROUTE}/{run_id}/xls/' + reportname
    if storage_name == 's3':
        excel_url = upload_excel_s3(filepath, BUCKET_NAME, excel_file_location)
    elif storage_name == 'ceph':
        excel_file_location = f'{APP_ID.lower()}/{run_id}/xls/' + reportname
        excel_url = upload_excel_ceph(filepath, BUCKET_NAME, excel_file_location)
    elif storage_name.lower() == 'gcp':
        excel_url = upload_excel_gcp(filepath, BUCKET_NAME, excel_file_location)
        print("gcp upload file excel url : ", excel_url)
    else:
        logger.info("No storages are found")
    
    delete_excel_file(filepath)
    return excel_url


#Upload excel file to s3
def upload_excel_s3(local_file, bucket, s3_file):
    retry = 1
    s3 = get_s3_client()
    while retry <= API_RETRY:
        try:
            s3.upload_file(local_file, bucket, s3_file)
            url = f'https://{bucket}.s3.{REGION_NAME}.amazonaws.com/{s3_file}'
            logger.info('Upload successful, result url is %s', url)
        
            delete_excel_file(local_file)
            return s3_file
        except FileNotFoundError:
            logger.info('File was not found')
            return False
        except NoCredentialsError:
            logger.info('Invalid credentials')
            return False
        except Exception as e:
            time.sleep(retry * 2)
            retry+=1
            if retry > API_RETRY:
                raise e
            continue


#Upload excel file to ceph
def upload_excel_ceph(local_file, bucket, s3_file):
    retry = 1
    s3 = get_ceph_resource()
    while retry <= API_RETRY:
        try:
            s3.Bucket(BUCKET_NAME).upload_file(Filename = local_file, Key = s3_file)
            logger.info('Upload successful')
            delete_excel_file(local_file)
            return s3_file
        except FileNotFoundError:
            logger.info('File was not found')
            return False
        except NoCredentialsError:
            logger.info('Invalid credentials')
            return False
        except Exception as e:
            time.sleep(retry * 2)
            retry+=1
            if retry > API_RETRY:
                raise e
            continue


#Upload excel file to gcp
def upload_excel_gcp(local_file, bucket, s3_file):
    retry = 1
    while retry <= API_RETRY:
        try:
            blob = GCP_OBJ.bucket.blob(s3_file)
            blob.upload_from_filename(local_file)
            url = f"gs://{bucket}/{s3_file}"
            logger.info('Upload successful... result url is %s', url)
            delete_excel_file(local_file)
            return s3_file
        except FileNotFoundError:
            logger.info('File was not found')
            return False
        except Exception as e:
            time.sleep(retry * 2)
            retry+=1
            if retry > API_RETRY:
                raise e
            continue


#Delete excel_file from local path
def delete_excel_file(source_path):
    try:
        os.remove(source_path)
        logger.info('Excel file successfully deleted')
    except OSError as e:
        logger.info(f'Failed to delete: %s : %s % {source_path, e.strerror}')


# #Generate excel file
# def generate_excel_file(run_id, orgId, client_name, report_gen_start_time, report_gen_completed_time):
#     logger.info('Entered into excel generation process')
#     excel_data=get_result_by_run(run_id, 'excel-data', {})
#     reportname = f"{APP_ID.lower()}-{run_id[:8]}" + '-' + datetime.now().strftime('%Y-%m-%d-%I-%M-%S') + '.xlsx'
#     filepath = './' + reportname
#     generate_excel(run_id, orgId, client_name, excel_data, report_gen_start_time, report_gen_completed_time, filepath)
#     # excel_file_location = f'{PLATFORM_ROUTE}/{run_id}/xls/' + reportname
#     if storage_name == 's3':
#         excel_file_location = f'{PLATFORM_ROUTE}/{run_id}/xls/' + reportname
#         excel_url = upload_excel_s3(filepath, BUCKET_NAME, excel_file_location)
#     elif storage_name == 'ceph':
#         excel_file_location = f'{APP_ID.lower()}/{run_id}/xls/' + reportname
#         excel_url = upload_excel_ceph(filepath, BUCKET_NAME, excel_file_location)
#     else:
#         logger.info("No storages are found")
#     return excel_url


def upload_generated_file_to_storage(reportname, filepath, run_id, format):
    path = 'xls'
    if format and format is not None and format.lower() == 'csv': path = 'csv'
    file_location = f'{PLATFORM_ROUTE}/{run_id}/{path}/' + reportname
    if storage_name == 's3':
        # file_location = f'{PLATFORM_ROUTE}/{run_id}/{path}/' + reportname
        location_url = upload_excel_s3(filepath, BUCKET_NAME, file_location)
    elif storage_name == 'ceph':
        file_location = f'{APP_ID.lower()}/{run_id}/{path}/' + reportname
        location_url = upload_excel_ceph(filepath, BUCKET_NAME, file_location)
    elif storage_name.lower() == 'gcp':
        location_url = upload_excel_gcp(filepath, BUCKET_NAME, file_location)
        print("gcp upload_generated_file_to_storage location url : ", location_url)
    else:
        logger.info("No storages are found")
    return location_url


#Generate excel file
def generate_excel_file(run_id, orgId, client_name, report_gen_start_time, report_gen_completed_time):
    logger.info('Entered into excel generation process')
    excel_data=get_result_by_run(run_id, 'excel-data', {})
    reportname = f"{APP_ID.lower()}-{run_id[:8]}" + '-' + datetime.now().strftime('%Y-%m-%d-%I-%M-%S') + '.xlsx'
    filepath = './' + reportname
    generate_excel(run_id, orgId, client_name, excel_data, report_gen_start_time, report_gen_completed_time, filepath)
    # excel_file_location = f'{PLATFORM_ROUTE}/{run_id}/xls/' + reportname
    location_url = upload_generated_file_to_storage(reportname, filepath, run_id, None)
    return location_url


def generate_csv_report(processed_data, run_id, format=None):
    logger.info('Entered into csv generation process')
    try:
        reportname = f"{APP_ID.lower()}-{run_id[:8]}" + '-' + datetime.now().strftime('%Y-%m-%d-%I-%M-%S') + '.csv'
        filepath = './' + reportname
        def sanitize_for_csv(value):
            if value is None:
                return ""
            # Convert to string if not already
            value = str(value)
            if value.startswith(('=', '+', '@', '\t', '\r')):
                # Add a visible prefix that shows users this was modified for security
                value = "'" + value
            value = value.replace('"', '""')
            return value

        def get_csv_report(data, file_name):
            headers = ['SNo'] + data[0]
            # Sanitize headers to prevent formula injection
            # sanitized_headers = ['SNo'] + [sanitize_for_csv(header) for header in data[0]]

            # Process and sanitize each row
            sanitized_data = []
            for idx, row in enumerate(data[1:]):
                # Sanitize each cell in the row
                sanitized_row = [idx + 1] + [sanitize_for_csv(cell) for cell in row]
                sanitized_data.append(sanitized_row)

            with open(file_name, mode='w', newline='') as file:
                writer = csv.writer(file, quoting=csv.QUOTE_ALL)  # Quote all fields for extra safety
                writer.writerow(headers)
                writer.writerows(sanitized_data)

        if processed_data and processed_data is not None and len(processed_data)>0:
            get_csv_report(processed_data, reportname)
        else:
            prepared_data = [['', '', ''], ['', 'No Data Found', '']]
            get_csv_report(prepared_data, reportname)
        location_url = upload_generated_file_to_storage(reportname, filepath, run_id, format)
    except Exception as e:
        error_message = 'Failed to generate CSV Report'
        traceback.print_exc()
        logger.error(f'generate_csv_report : Error generating csv report, Error Cause is ::: {e}')
        raise Exception(f'{error_message}')
    return location_url


def init_mail(org_id, run_id, session=None):
    logger.info('Entered into init_mail method')
    try:
        # /tenants/{tenantId}/runs/{id}/sends
        url = BASE_API_URL + f'/reporting/api/v3/tenants/{org_id}/runs/{run_id}/sends'
        data = {}
        t1 = int(time.time())
        res = call_post_requests(url , session=session, data=json.dumps(data), verify=False)
        t2 = int(time.time())
        duration = t2-t1
        if duration > API_TIME_STACKS:
            logging.info('Status update response took %d (greater than %d) seconds', duration, API_TIME_STACKS)
        logger.info('Status update response is %s', res)
    except Exception as e:
        logger.error("Exception raised due to : " + repr(e))
        traceback.print_exc()
    logger.info('finished init_mail method')


def send_internal_failure_notification_mail(run_id, app_name, err_msg, partner_id, partner_name, client_id, client_name, session=None):
    logger.info('Entered into send_internal_failure_notification_mail method')
    try:
        url = BASE_API_URL + f'/reporting/api/v3/sendInternalFailureNotifications'
        data = {
            "runId": run_id,
            "appName": app_name,
            "exception": err_msg,
            "partnerId": partner_id,
            "partnerName": partner_name,
            "clientIds": client_id,
            "clientNames": client_name
        }
        t1 = int(time.time())
        res = call_post_requests(url, session=session, data=json.dumps(data), verify=False)
        t2 = int(time.time())
        duration = t2-t1
        if duration > API_TIME_STACKS:
            logging.info('Send internal failure notification mail response took %d (greater than %d) seconds', duration, API_TIME_STACKS)
        logger.info('Send internal failure notification mail response is %s', res)
    except Exception as e:
        raise e
        logger.error("Exception raised due to : " + repr(e))
        traceback.print_exc()
    logger.info('finished send_internal_failure_notification_mail method')


def send_user_failure_notification(run_id, org_id, session=None):
    logger.info('Entered into send_user_failure_notification method')
    try:
        url = BASE_API_URL + f'/reporting/api/v3/tenants/{org_id}/runs/{run_id}/failureNotification'
        data = {}
        t1 = int(time.time())
        res = call_post_requests(url, session=session, data=json.dumps(data), verify=False)
        t2 = int(time.time())
        duration = t2-t1
        if duration > API_TIME_STACKS:
            logging.info('Send internal failure notification to customer mail response took %d (greater than %d) seconds', duration, API_TIME_STACKS)
        logger.info('Send internal failure notification to customer mail response is %s', res)
    except Exception as e:
        raise e
        logger.error("Exception raised due to : " + repr(e))
        traceback.print_exc()
    logger.info('finished send_user_failure_notification method')
    

def upload_excel(analysis_run, excel_file):
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    s3_path = f'{analysis_run.analysis.app.slug}/excel/{timestamp}.xlsx'

    return upload_to_storage(excel_file, s3_path)


"""
Method to read summary response and get the required values to showcase in the summary / overview pages of the result files
Inpute values:
    param1: run_id - actual run id of the generated run
    param2: summary_key - this is the key which is stored with summary response of a run in the metafile(json) stored in the cloud
    param3: value_by - defines the which type information is requested by end user.
        values:
            client_logo
            partner_logo
            client_name
            partner_name
            description
            last_run
"""
def get_summary_details(run_id, summary_key, value_by):
    value = ''
    if value_by is None or summary_key is None:
        return value
    if (len(value_by) == 0 or len(summary_key) == 0):
        return value
    summary_response = get_result_by_run(run_id, summary_key, {})
    if len(summary_response) <= 0:
        return value

    if value_by == 'client_logo':
        return get_tenant_logo(summary_response, 'client')
    elif value_by == 'partner_logo':
        return get_tenant_logo(summary_response, 'partner')
    elif value_by == 'last_run':
        return get_last_run(summary_response)
    elif value_by == 'description':
        return get_app_description(summary_response)
    elif value_by == 'partner_name':
        return get_tenant_name(summary_response, 'partner')
    elif value_by == 'client_name':
        return get_tenant_name(summary_response, 'client')
    else:
        return value


def get_tenant_logo(summary_res, context):
    logo = ''
    if context == 'partner':
        logo = summary_res['partner_logo_path']
    else:
        logo = summary_res['client_logo_path']
    return logo


def get_tenant_name(summary_res, context):
    name = ''
    if context == 'client':
        name = summary_res['client_name']
    else:
        name = summary_res['partner_name']
    return name


def get_last_run(summary_res):
    return summary_res['create_date']


def get_app_description(summary_res):
    return summary_res['app_description']

def prepare_page_size_page_no(data, page_no, page_size):
    if data and data is not None:
        if "pageNo" in data:
            data["pageNo"] = page_no
        if "pageSize" not in data:
            data["pageSize"] = page_size
    return data


def add_page_no_page_size_for_url(add_page_no, url, page_no, page_size):
    uri = url
    if add_page_no:
        if "pageSize" not in url:
            uri = url + f'&pageNo={page_no}&pageSize={page_size}'
        else:
            uri = url + f'&pageNo={page_no}'
    return uri


def get_paginated_api_results(method, url, data, type, add_pageNo=True, session=None):
    resp = []
    page_no=1
    nextPage= True
    page_size= 100

    try:
        error_message = ''
        while (nextPage != False):
            data = json.loads(data)
            data = prepare_page_size_page_no(data, page_no, page_size)
            data=json.dumps(data)
            if method == 'POST':
                res = get_post_request_results(url, data, type, session=session)
            else:
                uri = add_page_no_page_size_for_url(add_pageNo, url, page_no, page_size)
                res = get_response(uri, type, session=session)
            if res == None or not res.ok or (res.json() is not None and "results" not in res.json()) or (res is not None and "nextPage" not in res.json()):
                error_message = f'Get {type} API is failed, url ::: {url}, response ::: {res}'
                logger.error('Get %s API is failed, url ::: %s, response ::: %s ', type, url, res)
                retry_count = 1
                while (retry_count <= API_RETRY):
                    data = json.loads(data)
                    data = prepare_page_size_page_no(data, page_no, page_size)
                    data=json.dumps(data)

                    time.sleep(1)
                    retry_count += 1
                    if method == 'POST':
                        res = get_post_request_results(url, data, type, session=session)
                    else:
                        uri = add_page_no_page_size_for_url(add_pageNo, url, page_no, page_size)
                        res = get_response(uri, type, session=session)
                    if res == None or not res.ok:
                        error_message = f'Get {type} API is failed, url ::: {url}, response ::: {res}, response_json ::: {res.json()}, API_Retry_Count ::: {retry_count}'
                        logger.error('Get %s API is failed, url ::: %s, response ::: %s, response_json ::: %s, API_Retry_Count ::: %s ', type, url, res, res.json(), retry_count)
                        res = None
                        if retry_count > 3:
                            raise Exception(error_message)
                    elif res.json() is not None and "results" not in res.json():
                        error_message = f"Get {type} results keyword is missing in API response, url ::: {url}, response ::: {res}, response_json ::: {res.json()}, API_Retry_Count ::: {retry_count}"
                        logger.error('Get %s results keyword is missing in API response, url ::: %s, response : %s, response_json ::: %s, API_Retry_Count ::: %s ', type, url, res, res.json(), retry_count)
                        res = None
                        if retry_count > 3:
                            raise Exception(error_message)
                    elif res.json() is not None and "nextPage" not in res.json():
                        error_message = f"Get {type} nextPage keyword is missing in API response, url : {url}, response ::: {res}, response_json ::: {res.json()}, API_Retry_Count ::: {retry_count}"
                        logger.error('Get %s nextPage keyword is missing in API response, url ::: %s, response : %s, response_json ::: %s, API_Retry_Count ::: %s ', type, url, res, res.json(), retry_count)
                        res = None
                        if retry_count > 3:
                            raise Exception(error_message)
                    else:
                        break
                if res == None or "results" not in res.json() or len(res.json()['results'])==0:
                    logger.error('After retrying for %s times, Get %s API results are empty, url is %s', API_RETRY, type, url)
                    return None
            #else:
            result = res.json()['results']
            resp.append(result)

            if "nextPage" not in res.json():
                error_message = f"Get {type} nextPage keyword is missing in API response, url ::: {url}, response : {res}, response_json ::: {res.json()},"
                logger.error('Get %s nextPage keyword is missing in API response, url ::: %s, response ::: %s, response_json ::: %s', type, url, res, res.json())
                raise Exception(error_message)

            nextPage=res.json()['nextPage']
            page_no+=1

        resp = [item for sublist in resp for item in sublist] # To eliminate list of list (ex: [[data:{}]] -> [data:{}])
    except Exception as e:
        traceback.print_exc()
        logger.error(f'get_paginated_api_results : Error while fetching apis, Error Cause is ::: {e}')
        raise Exception(f'{error_message}')
    return resp


def get_post_request_results(url, data, type, session=None):
    start_time = int(time.time())
    logging.info(f'api type: {type}, : url : {url}')

    res = call_post_requests(url, session=session, data=data, verify=False)
    duration = int(time.time()) - start_time
    if duration > API_TIME_STACKS:
        logging.info(f'Get {type} API response took %d (greater than %d) seconds, url : {url}', duration, API_TIME_STACKS)
    return res


def get_post_opsql_count_results(url, data, type, session=None):
    res = get_post_request_results(url, data, type, session=session)
    if res == None or not res.ok:
        logger.error('FAILED :' + type)
        return None
    elif "count" not in res.json() or len(res.json()) == 0:
        logger.error('Result are Empty for ' + type)
        return None
    else:
        resp = res.json()

    return resp

########################### Tenant and Logo Information #########################
def get_tenants(orgId, session=None):
    url = BASE_API_URL + f'/api/v2/tenants/{orgId}/clients/minimal'
    res = get_response(url, 'V2 Tenants', session=session)
    logger.info('Get tenants API response is %s', res)
    if res == None or not res.ok:
        logger.error('Get tenants API is failed')
    return res.json()


def get_tenant_list(org_id, level, tenant_list, session=None):
    tenant_id_list = []
    if level == 'partner':
        tenant_id_list.append(org_id)
    elif level == 'all-clients':
        tenants = get_tenants(org_id, session=session)
        for tenant in tenants:
            tenant_id_list.append(tenant['uniqueId'])
    elif level == 'specific_clients':
        for tenant in tenant_list:
            tenant_id_list.append(tenant['uniqueId'])
    else:
        tenant_id_list.append(org_id)
    return tenant_id_list


    
def prepare_tenant_list(form, parameters, session=None, all_clients=False):
    tenant_id_list = []
    if parameters is not None and len(parameters) > 0:
        if 'allClients' in parameters and (parameters['allClients'] == True or parameters['allClients'] == 'true'):
            tenant_id_list = fetch_all_clients(form.get_tenant_id(), form.get_tenant_context(), all_clients, session=session)
        elif 'client' in parameters and parameters['client'] is not None:
            clients = parameters['client']
            if clients is not None:
                if clients == 'All Clients' or clients == 'All Client' or clients == ['All Clients'] or clients == 'all client' or clients == 'all clients':
                    tenant_id_list = fetch_all_clients(form.get_tenant_id(), form.get_tenant_context(), all_clients, session=session)
                else:
                    if isinstance(clients, list):
                        tenant_id_list = clients
                    else:
                        for i in clients.split(','):
                            tenant_id_list.append(i)
        else:
            tenant_id_list = fetch_all_clients(form.get_tenant_id(), form.get_tenant_context(), all_clients, session=session)
    else:
        tenant_id_list = fetch_all_clients(form.get_tenant_id(), form.get_tenant_context(), all_clients, session=session)
    return tenant_id_list



def fetch_all_clients(tenant_id, context, all_clients, session=None):
    tenant_id_list = []
    if all_clients and context == 'partner':
        context = 'all-clients'
    tenant_id_list = get_tenant_list(tenant_id, context, None, session=session)
    return tenant_id_list



def get_tenant_info(tenant_id_list, keys, session=None):
    tenant_info = []
    for tenant_id in tenant_id_list:
        info={}
        url = BASE_API_URL + f'/tenancy/api/v7/tenants/{tenant_id}/getTenant'
        res = get_response(url, f'V7 tenants, tenant id is : {tenant_id}', session=session)
        if res == None or not res.ok:
            logger.error('Get tenant info API is failed')
            return tenant_info
        else:
            for key in keys:
                info[key] = res.json()[key]
            tenant_info.append({tenant_id: info})
    return tenant_info



def get_logo_path_url(id, session=None):
    url = BASE_API_URL + f'/api/v2/tenants/{id}/customBranding?cascade=true'
    res = get_response(url, f'V2 tenants logo, tenant id is : {id}', session=session)
    if res == None or not res.ok:
        logger.error('Get logo path url API is failed')
        return ''
    if ('logo' in res.json() and res.json()['logo']) and ('logoPath' in res.json()['logo'] and res.json()['logo']['logoPath']):
        return res.json()['logo']['logoPath']
    else:
        logger.error('Get logo path url is empty')
        return ''



def get_app_logo(id, context, parameters, session=None):
    if context == 'client':
        return get_logo_path_url(id, session=session)
    elif context == 'partner':
        if parameters is not None and len(parameters) > 0:
            if 'allClients' in parameters and (parameters['allClients'] == True or parameters['allClients'] == 'true'):
                return get_logo_path_url(id, session=session)
            elif 'client' in parameters and parameters['client'] is not None:
                clients = parameters['client']
                if clients is not None:
                    if clients == 'All Clients' or clients == 'All Client' or clients == ['All Clients'] or clients == 'all client' or clients == 'all clients':
                        return get_logo_path_url(id, session=session)
                    else:
                        if isinstance(clients, list):
                            if len(clients) == 1:
                                for cid in clients:
                                    return get_logo_path_url(cid, session=session)
                            else:
                                return get_logo_path_url(id, session=session)
                        else:
                            return get_logo_path_url(clients, session=session)
    return get_logo_path_url(id, session=session)


def generate_pie_chart_colors(num_colors):
    colors=["#0077C8", "#00A3E0", "#673AB7", "#9C27B0", "#E91E63", "#F47925"]
    random.seed(123)  # 123 Fixed seed value
    #colors = []
    for _ in range(num_colors):
        hex_color = '#{:06x}'.format(random.randint(0, 0xFFFFFF))
        colors.append(hex_color)
    return colors


def convert_datetime_tz_to_tz(date, format, fromTz, toTz):
    if date is None or date == '-' or format is None:
        return '-'
    if fromTz is not None:
        date = date.astimezone(fromTz)
    if toTz is None or len(toTz) <= 0:
        toTz = 'UTC'
    if toTz is not None:
        try:
            date_obj = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S%z")
            date = date_obj.astimezone(pytz.timezone(toTz))
            date = date.strftime(format)
            return date
        except Exception as e:
            logger.error(f"Error while converting date field to user timezone, Error Cause is : {e}")
            logger.error(f"bps value is : date")
            return date
    return '-'


def convert_date_time_with_format(date, format):
    try:
        date_obj = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z')
        formatted_date_str = date_obj.strftime(format)
        return formatted_date_str
    except Exception as e:
        return '-'


def update_run_progress(tenant_id, run_id, percent, message, session=None):
    url = BASE_API_URL + f'/reporting/api/v3/tenants/{tenant_id}/runs/{run_id}/progress'
    data = {
        "runningPercentage" : percent
    }
    res = call_put_requests(url, session=session, data=json.dumps(data), verify=False);
    if res == None or not res.ok:
        logger.error('Update run progress API is failed')
        return res
    else:
        logger.error('Update run progress result updated upto %d',  percent)
        return res
    #TODO : Implement logic here to update the run
    
       
# Report Builder Methods
def generate_dashboard_pdf(dashboard_id):
    logger.info(f'{dashboard_id} :: Entered into dashboard pdf generation process')
    try:
        url = DASH_BOARD_PDF_SERVICE
        jwt_token = os.getenv("OPSRAMP_JWT_TOKEN")
        current_date = datetime.now()
        # file_name = APP_ID.lower() + '-' + pdf.analysis_run[:8] + '-' + current_date.strftime("%Y-%m-%d-%H-%M-%S") + '.pdf'
        report_path = ''
        if storage_name == 's3' or storage_name.lower() == 'gcp':
            report_path = PLATFORM_ROUTE
        elif storage_name == 'ceph':
            report_path = APP_ID.lower()
        pdf = PDF(dashboard_id, url, report_path, current_date.strftime("%Y-%m-%d-%H-%M-%S"))
        file_name = pdf.prepare_file_name(APP_ID.lower(), 'pdf')
        file_path = pdf.report_path + '/' + pdf.analysis_run + '/pdf/' + file_name
        data = {
            'domain': BASE_API_URL,
            'report': PLATFORM_ROUTE,
            'run': pdf.analysis_run,
            'route': '/full-view',
            'token': get_token(),
            'app_id': APP_ID,
            'size': 'A4',
            'storage': storage_name,
            'file_name': file_name,
            'file_path': file_path,
            'dashboard_id': f'/{pdf.analysis_run}'
        }

        gen_retry = 1
        while gen_retry <= 2:
            logging.info(f'{pdf.analysis_run} :: pdf generation trying {gen_retry} time..')
            gen_retry += 1
            logging.info(f'b4 generation >> full file path : {file_path}')
            response = pdf.generate(data)
            logging.info(f'after generation >> full file path : {file_path}')
            if response == 504:
                storage_retry = 1
                file_found = False
                while storage_retry <= API_RETRY:
                    logging.info(f'{pdf.analysis_run} checking the file is existing in storage or not {storage_retry} time..')
                    file_found = is_file_in_storage(file_path)
                    if file_found == True:
                        logging.info(f'{pdf.analysis_run} the pdf file is found in storage')
                        return file_path
                    else:
                        time.sleep(storage_retry * 30)
                        storage_retry += 1
                        logging.info(f'{pdf.analysis_run} pdf not found in storage trying for {storage_retry} time..')
                        continue
            else:
                return response
        raise Exception(f'Generate_pdf:: pdf generation failed after max tries ({API_RETRY}), for run ::: {pdf.analysis_run}')
    except Exception as e:
        traceback.print_exc()
        err_msg = f'Generate_pdf:: Exeception - pdf generation failed after max tries({API_RETRY}), for run ::: {pdf.analysis_run}'
        raise Exception(err_msg)


def dashboard_init_mail(org_id, dashboard_id, toEmails, filePath, fileName):
    logger.info('Entered into init_mail method')
    try:
        # /tenants/{tenantId}/runs/{id}/sends
        url = BASE_API_URL + f'/reporting/api/v3/tenants/{org_id}/reportbuilder/sendmail'
        data={
                "recipients":toEmails,
                "filePath":filePath,
                "fileName":fileName
            }
        t1 = int(time.time())
        res = call_post_requests(url , data=json.dumps(data), verify=False)
        t2 = int(time.time())
        duration = t2-t1
        if duration > API_TIME_STACKS:
            logging.info('Status update response took %d (greater than %d) seconds', duration, API_TIME_STACKS)
        logger.info('Status update response is %s', res)
    except Exception as e:
        logger.error("Exception raised due to : " + repr(e))
        traceback.print_exc()
    logger.info('finished init_mail method')
    
    
def get_dashboard_result(dashboard_Id, path, field=None, default_value=None):
    try:
        # run_id= f'{PLATFORM_ROUTE}/{run_id}/json/{run_id}'
        #PLATFORM_ROUTE = 'report-builder'
        if storage_name == 's3':
            run_id= f'{PLATFORM_ROUTE}/{dashboard_Id}/json/{path}/{dashboard_Id}'
            print('locationnn',run_id)
            s3 = get_s3_client()
            res_object = s3.get_object(Bucket=BUCKET_NAME,Key=run_id)
            serializedObject = res_object['Body'].read()
            result = _retrive_value_from_json(serializedObject, field, default_value)
            return result
        elif storage_name == 'ceph':
            run_id= f'{APP_ID.lower()}/{dashboard_Id}/json/{path}/{dashboard_Id}'
            s3 = get_ceph_resource()
            data = BytesIO()
            res_object = s3.Bucket(BUCKET_NAME).download_fileobj(Fileobj=data,Key=run_id)
            res_object = data.getvalue()
            result = _retrive_value_from_json(res_object, field, default_value)
            return result
        elif storage_name == 'gcp':
            run_id= f'{PLATFORM_ROUTE}/{dashboard_Id}/json/{path}/{dashboard_Id}'
            blob = GCP_OBJ.bucket.blob(run_id)
            serializedObject = blob.download_as_string()
            result = _retrive_value_from_json(serializedObject, field, default_value)
            return result
        else:
            logger.info("No storages are found")
    except Exception:
        logger.error('An error occurred (NoSuchKey) when calling the GetObject operation: The specified key does not exist')
        pass

def prepare_chunk_data(data, _chunk_size):
    chunk_data = []
    for _record in data:
        chunk_data.append(_record)
        if len(chunk_data) >= _chunk_size:
            yield chunk_data
            chunk_data = []
    if chunk_data:
        yield chunk_data

def is_run_status_cancelled(summary_resp, form):
    if summary_resp and summary_resp is not None and summary_resp.ok:
        if summary_resp.json() is not None and 'analysisRun' in summary_resp.json() and 'status' in summary_resp.json()['analysisRun']:
            status = summary_resp.json()['analysisRun']['status']
            if status == 'cancelled':
                logger.info('Run was Cancelled for Run Id ::: %s, Tenant Id ::: %s', form.get_run_id(), form.get_tenant_id())
                return True
    return False

def auto_reschedule_on_restart(request_from):
    try:
        if ENABLED_AUTO_RESCHEDULE_RUNS == 'true':
            host_name = socket.gethostname()
            logger.debug('########### Started auto reschedule mechanism #########')
            logger.debug('Pod Name :: %s, Request From :: %s', host_name, request_from)
            url = BASE_API_URL + f'/reporting/api/v3/trigger_auto_reschedule_run_process'
            params = {
                "podName": host_name,
                "excludeRunIds": EXCLUDE_RUN_IDS
            }
            res = call_get_requests(url, session=None, params=params)
            logger.debug('Successfully triggerred the auto reschedule process :: %s', res)
    except KeyboardInterrupt as e:
        logger.error('KeyboardInterrupt: %s', str(e), exc_info=1)
    except BaseException as e:
        logger.error('Error : %s', str(e), exc_info=1)
    except:
        logger.error('Error', exc_info=1)


def has_required_permissions(required_permissions, user_permissions):
    missing_permissions = []
    if not required_permissions or not user_permissions:
        return False, None
    for req_perm in required_permissions:
        if req_perm not in user_permissions:
            missing_permissions.append(req_perm)
    return len(missing_permissions) == 0, missing_permissions


def get_permissions_display_names(permission_list):
    permissions = []
    for permission in permission_list:
        if permission and permission.strip() != "":
            permission = permission.replace("_", " ").replace("-", " ")
            permission = permission.lower()
            key_array = permission.split(" ")
            key_array = [word[0].upper() + word[1:] if word else "" for word in key_array]
            permission = " ".join(key_array)
            permissions.append(permission)
    return permissions


def prepare_permissions_error_message(required_permissions, missing_permissions):
    missing_per_err_msg , req_per_err_msg = '', ''
    if required_permissions is not None and len(required_permissions) > 0:
        req_per_err_msg = '(Required Permissions: ' + ', '.join(get_permissions_display_names(required_permissions)) + ")"
    if missing_permissions is not None and len(missing_permissions) > 0:
        missing_per_err_msg = 'Missing Permissions: ' + ', '.join(get_permissions_display_names(missing_permissions))
    return missing_per_err_msg + ' ' + req_per_err_msg