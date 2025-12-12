import os
import json
import logging
from functools import partial

import dash
import flask
import plotly
import pkgutil
import mimetypes
# import dash_renderer
#import dash_core_components as dcc
from dash import dcc
from dash import *

from dash.version import __version__
from dash._utils import (
    stringify_id,
    format_tag
)
from .utilities import is_authenticated
from .utilities import (
    BASE_API_URL,
    APP_ID
)

logger = logging.getLogger(__name__)

class OAPDash(dash.Dash):
    static_files = {
        'css': [
            'main.wrapper.css'
        ]
    }

    def __init__(self, **kwargs):
        self.route = kwargs.pop('route')
        app_id = APP_ID
        self.in_store_id = "_oap_data_in_" + app_id
        self.out_store_id = "_oap_data_out_" + app_id

        route_prefix = f'/{self.route}' if self.route else ''
        # assume this is not set by user
        kwargs['requests_pathname_prefix'] = f'{route_prefix}/'

        super(OAPDash, self).__init__(**kwargs)

    def init_app(self, app=None):
        """
        called when the app is initiated, called only once
        register api endpoints and custom static resources
        """
        super(OAPDash, self).init_app(app)

        # register manifest files
        self._add_url("opsramp-analytics-utils/<string:file_name>", self.serve_resource)

    def index(self, *args, **kwargs):  # pylint: disable=unused-argument
        logger.info("verifying authentication")
        print("verifying authentication")
        is_auth = is_authenticated()
        if ('path' in kwargs and 'server/status' in kwargs['path'] ):
            logger.info("server is up and running")
            print("server is up and running")
            return 'server is up and running', 200
        elif is_auth:
            if is_auth == 'no_reports_view_permission':
                logger.info("Access denied: You are authenticated but lack the required reports permissions.")
                print("Access denied: You are authenticated but lack the required reports permissions.")
                return flask.Response('Access denied: You are authenticated but lack the required reports permissions.', status=403)

            logger.info("authentication is successful")
            print("authentication is successful")
            # resp = self._index(args, kwargs)
            resp = super(OAPDash, self).index(*args, **kwargs)
            return resp
        else:
            # return flask.Response('Not authorized', status=401)
            redirect_url = BASE_API_URL + f'/tenancy/web/login?cb=/loginResponse.do'
            logger.info("authentication is failed, redirecting to login url is %s", redirect_url)
            print("authentication is failed, redirecting to login url is ", redirect_url)
            return flask.redirect(redirect_url, code=302)

    def serve_resource(self, file_name):
        if file_name == 'main.css':
            return self._serve_main_css()
        else:
            extension = "." + file_name.split(".")[-1]
            mimetype = mimetypes.types_map.get(extension, "application/octet-stream")

            return flask.Response(
                pkgutil.get_data('dash_core_components', file_name), mimetype=mimetype
            )

    def _serve_main_css(self):
        body = ''

        # TODO: external css files using requests
        external_links = self.config.external_stylesheets

        # oap css files
        for file_path in self.static_files['css']:
            body += pkgutil.get_data('analytics_sdk', 'analysis-wrapper/'+file_path).decode("utf-8")
        body = body.replace('url(/static/media', f'url({self.config.requests_pathname_prefix}wrapper-static/media')

        # custom css files
        for resource in self.css.get_all_css():
            file_name = resource['asset_path']
            body += open(self.config.assets_folder+'/'+file_name).read()

        response = flask.Response(body, mimetype='text/css')

        return response

    def get_component_ids(self, layout):
        component_ids = []
        for component in layout._traverse():
            component_id = stringify_id(getattr(component, "id", None))
            component_ids.append(component_id)

        return component_ids

    def _layout_value(self):
        """
        add custom stores
        """
        _layout = self._layout() if self._layout_is_function else self._layout                        

        component_ids = self.get_component_ids(_layout)
        
        if self.in_store_id not in component_ids:
            _layout.children.append(dcc.Store(id="dummy-store"))
            _layout.children.append(dcc.Store(id=self.out_store_id, storage_type="local"))
            _layout.children.append(dcc.Store(id=self.in_store_id, storage_type="local"))
            _layout.children.append(dcc.Store(id='op-filter-start-date', storage_type="local"))
            _layout.children.append(dcc.Store(id='op-filter-end-date'))

        return _layout

    def _generate_css_dist_html(self):
        return f'<link rel="stylesheet" href="{self.config.requests_pathname_prefix}opsramp-analytics-utils/main.css">'