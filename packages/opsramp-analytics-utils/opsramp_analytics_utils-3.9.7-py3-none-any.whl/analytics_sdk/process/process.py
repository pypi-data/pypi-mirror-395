import json
import requests

"""
This Class is used for maintaining all the required field to run
"""


class AppForm:

    def __init__(self, message):
        self.session = requests.Session()
        self.message = message
        self.additional_props = {}
        self.prepare_json(message)

    def prepare_json(self, message):
        self.json_msg = json.loads(message)

    def read_from_json(self, key, defalt_value):
        if self.json_msg is None or key not in self.json_msg or self.json_msg[key] is None:
            return defalt_value
        return self.json_msg[key]

    def set_field(self, field_name, field_value):
        if self.additional_props is None or len(self.additional_props) <=0:
            self.additional_props = {}

        if field_name is not None or field_value is not None:
            self.additional_props[field_name] = field_value

    def get_field(self, field_name, default_value):
        if self.additional_props is None:
            return default_value

        if field_name not in self.additional_props or self.additional_props[field_name] is None:
            return default_value

        return self.additional_props[field_name]

    def get_session(self):
        return self.session

    def get_run_id(self):
        self.run_id = self.read_from_json('analysisRunId', '')
        return self.run_id

    def set_run_id(self, run_id):
        self.run_id = run_id

    def get_gen_start_time(self):
        self.gen_start_time = self.read_from_json('genStime', 0)
        return self.gen_start_time

    def set_gen_start_time(self, start_time):
        self.gen_start_time = start_time

    def get_gen_end_time(self):
        self.gen_end_time = self.read_from_json('genEtime', 0)
        return self.gen_end_time

    def set_gen_end_time(self, end_time):
        self.gen_end_time = end_time

    def get_file_formats(self):
        self.file_formats = self.read_from_json('fileFormat', '')
        return self.file_formats

    def set_file_formats(self, formats):
        self.file_formats = formats

    def get_client_id(self):
        self.client_id = self.read_from_json('clientUniqueId', '')
        return self.client_id

    def set_client_id(self, client_id):
        self.client_id = client_id

    def get_partner_id(self):
        self.partner_id = self.read_from_json('mspUniqueId', '')
        return self.partner_id

    def set_partner_id(self, partner_id):
        self.partner_id = partner_id

    def get_tenant_id(self):
        self.get_client_id()
        self.get_partner_id()
        self.tenant_id = 0
        if self.client_id is not None and self.client_id != '':
            self.tenant_id = self.client_id
        elif self.partner_id is not None and self.partner_id != '':
            self.tenant_id = self.partner_id
        return self.tenant_id

    def set_tenant_id(self, tenant_id):
        self.tenant_id = tenant_id

    def get_tenant_context(self):
        self.get_client_id()
        self.get_partner_id()
        self.tenant_context = ''
        if self.client_id is not None and self.client_id != '':
            self.tenant_context = 'client'
        elif self.partner_id is not None and self.partner_id != '':
            self.tenant_context = 'partner'
        return self.tenant_context

    def set_tenant_context(self, tenant_context):
        self.tenant_context = tenant_context

    def get_created_user_id(self):
        self.created_user_id = self.read_from_json('triggeredBy', '')
        return self.created_user_id

    def set_created_user_id(self, user_id):
        self.created_user_id = user_id

    def get_updated_user_id(self):
        self.update_user_id = self.read_from_json('triggeredBy', '')
        return self.update_user_id

    def set_updated_user_id(self, user_id):
        self.update_user_id = user_id

    def get_user_tz(self):
        self.user_tz = self.read_from_json('schTimeZone', 'UTC')
        return self.user_tz

    def set_user_tz(self, tz):
        self.user_tz = tz

    def get_recipeints(self):
        self.recipients = self.read_from_json('sendToRecipients', False)
        return self.recipients

    def set_recipeints(self, recipients):
        self.recipients = recipients

    def get_integration_id(self):
        self.integration_id = self.read_from_json('intId', '')
        return self.integration_id

    def set_integration_id(self, integration_id):
        self.integration_id = integration_id

    def get_analysis_id(self):
        self.analysis_id = self.read_from_json('analysisId', '')
        return self.analysis_id

    def set_analysis_id(self, analysis_id):
        self.analysis_id = analysis_id

    def get_app_description(self):
        self.app_description = self.read_from_json('appDescription', '')
        return self.app_description

    def set_app_description(self, app_description):
        self.app_description = app_description

    def set_query_builder(self, query_builder):
        self.query_builder = query_builder
    
    def get_query_builder(self):
        return self.query_builder
    
    # Report Builder Methods
    def get_dashboard_id(self):
        self.dashboard_id = self.read_from_json('dashboardId', '')
        return self.dashboard_id

    def set_dashboard_id(self,dashboard_id):
        self.dashboard_id = dashboard_id
    
    def get_partnerId(self):
        self.partner_id = self.read_from_json('tenantId', '')
        return self.partner_id
    
    def set_partnerId(self, partner_id):
        self.partner_id = partner_id
    
    def get_tenantId(self):
        self.get_client_id()
        self.get_partnerId()
        self.tenant_id = 0
        if self.client_id is not None and self.client_id != '':
            self.tenant_id = self.client_id
        elif self.partner_id is not None and self.partner_id != '':
            self.tenant_id = self.partner_id
        return self.tenant_id
    
    def get_app_id(self):
        self.app_id = self.read_from_json('appId', None)
        return self.app_id
    