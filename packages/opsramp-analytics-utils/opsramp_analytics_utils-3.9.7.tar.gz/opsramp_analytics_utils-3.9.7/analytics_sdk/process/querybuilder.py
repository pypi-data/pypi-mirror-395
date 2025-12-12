import json

from analytics_sdk.utilities import (
    API_PAGE_SIZE,
    OPSQL_OBJECT_TYPES,
    OPSQL_JOIN_API_PAGE_SIZE
)

"""
This Class is used for maintaining all the query fields
"""
class QueryBuilder:


    def __init__(self, tenant_id, query_params):
        self.tenant_id = tenant_id
        self.object_type = None
        self.filter_criteria = None
        self.fields = None
        self.group_by = None
        self.agg_function = None
        self.sort_by = None
        self.sort_order = 'ASC'
        self.page_no = 1
        self.page_size = 100
        self.prepare_builder(tenant_id, query_params)

    def prepare_builder(self, tenant_id, query_params):
        if query_params is None:
            return
        if tenant_id is not None:
            self.tenant_id = tenant_id
        if 'object_type' in query_params and query_params['object_type'] is not None:
            self.object_type = query_params['object_type']
        if 'filter_criteria' in query_params and query_params['filter_criteria'] is not None:
            self.filter_criteria = query_params['filter_criteria']
        if 'fields' in query_params and query_params['fields'] is not None:
            self.fields = query_params['fields']
        if 'group_by' in query_params and query_params['group_by'] is not None:
            self.group_by = query_params['group_by']
        if 'agg_function' in query_params and query_params['agg_function'] is not None:
            self.agg_function = query_params['agg_function']
        if 'sort_by' in query_params and query_params['sort_by'] is not None:
            self.sort_by = query_params['sort_by']
        if 'sort_order' in query_params and query_params['sort_order'] is not None:
            self.sort_order = query_params['sort_order']
        if 'page_no' in query_params and query_params['page_no'] is not None:
            self.page_no = query_params['page_no']
        if 'page_size' in query_params and query_params['page_size'] is not None:
            self.page_size = query_params['page_size']


    def set_property(self, props):
        self.props = props

    def get_property(self, key, default_value):
        if key is None:
            return default_value
        if key and self.props and key not in self.props:
            return default_value
        if self.props is None and self.props[key] is None:
            return default_value
        if self.props[key] and self.props[key]:
            return self.props[key]

    def get_query(self):
        query = {}
        if self.object_type is not None:
            query['objectType'] = self.object_type
        if self.filter_criteria is not None:
            query['filterCriteria'] = self.filter_criteria
        if self.fields is not None:
            query['fields'] = self.fields
        if self.group_by is not None:
            query['groupBy'] = self.group_by
        if self.agg_function is not None:
            query['aggregateFunction'] = self.agg_function
        if self.sort_by is not None:
            query['sortBy'] = self.sort_by
        if self.sort_order is not None:
            query['sortByOrder'] = self.sort_order
        if self.page_no is not None:
            query['pageNo'] = self.page_no
        if self.page_size is not None:
            query['pageSize'] = self.page_size
        query['pageSize'] = self.get_opsql_page_size()
        return query
    
    def get_count_query(self):
        query = {}
        if self.object_type is not None:
            query['objectType'] = self.object_type
        if self.filter_criteria is not None:
            query['filterCriteria'] = self.filter_criteria
        if self.agg_function is not None:
            query['aggregateFunction'] = 'count'
        if self.sort_by is not None:
            query['sortBy'] = self.sort_by
        if self.sort_order is not None:
            query['sortByOrder'] = self.sort_order
        return query

    def set_page_no(self, page_no):
        self.page_no = page_no

    def set_page_size(self, page_size):
        self.page_size = page_size

    def get_opsql_page_size(self):
        page_size = self.page_size
        if self.fields and self.fields is not None and len(self.fields) > 0:
            page_size = int(API_PAGE_SIZE)
            for field in self.fields:
                if "." in field:
                    page_size = int(OPSQL_JOIN_API_PAGE_SIZE)
                    return page_size
        if self.filter_criteria and self.filter_criteria is not None and len(self.filter_criteria) > 0:
            page_size = int(API_PAGE_SIZE)
            if OPSQL_OBJECT_TYPES is not None and len(OPSQL_OBJECT_TYPES) > 0:
                obj_types = OPSQL_OBJECT_TYPES.split(',')
                for obj_type in obj_types:
                    obj_type = obj_type + "."
                    if obj_type in self.filter_criteria:
                        page_size = int(OPSQL_JOIN_API_PAGE_SIZE)
                        return page_size
        return page_size

    def settingLatestQueryBuilderValues(self, data, query):
        if not data:
            return query
        param = {}
        if 'filterCriteria' in data and data['filterCriteria'] is not None:
            param['filter_criteria'] = data['filterCriteria']
        if 'objectType' in data and data['objectType'] is not None:
            param['object_type'] = data['objectType']
        if 'fields' in data and data['fields'] is not None:
            param['fields'] = data['fields']
        if 'groupBy' in data and data['groupBy'] is not None:
            param['group_by'] = data['groupBy']
        if 'aggregateFunction' in data and data['aggregateFunction'] is not None:
            param['agg_function'] = data['aggregateFunction']
        if 'sortBy' in data and data['sortBy'] is not None:
            param['sort_by'] = data['sortBy']
        if 'sort_order' in data and data['sort_order'] is not None:
            param['sort_order'] = data['sortByOrder']
        if 'page_no' in data and data['page_no'] is not None:
            param['page_no'] = data['pageNo']
        if 'page_size' in data and data['page_size'] is not None:
            param['page_size'] = data['pageSize']
        if param:
            self.query = QueryBuilder(query.tenant_id, param)
        return self.query
