# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 Red Hat, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


from dci.server.api import v1 as api_v1
from dci.server.common import exceptions
from dci.server.elasticsearch import engine as es_engine

import flask
from sqlalchemy import exc as sa_exc

from dci.dci_databrowser import dci_databrowser
from dci.server import dci_config


def handle_api_exception(api_exception):
    response = flask.jsonify(api_exception.to_dict())
    response.status_code = api_exception.status_code
    return response


def handle_dbapi_exception(dbapi_exception):
    dci_exception = exceptions.DCIException(str(dbapi_exception)).to_dict()
    response = flask.jsonify(dci_exception)
    response.status_code = 400
    return response


def create_app(conf):
    dci_config.TEAM_ADMIN_ID = dci_config.get_team_admin_id()

    dci_app = flask.Flask(__name__)
    dci_app.config.update(conf)
    dci_app.engine = dci_config.get_engine(conf)
    dci_app.es_engine = es_engine.DCIESEngine(conf)

    @dci_app.before_request
    def before_request():
        flask.g.db_conn = dci_app.engine.connect()
        flask.g.es_conn = dci_app.es_engine

    @dci_app.teardown_request
    def teardown_request(_):
        flask.g.db_conn.close()

    # Registering REST error handler
    dci_app.register_error_handler(exceptions.DCIException,
                                   handle_api_exception)
    dci_app.register_error_handler(sa_exc.DBAPIError,
                                   handle_dbapi_exception)

    # Registering REST API v1
    dci_app.register_blueprint(api_v1.api, url_prefix='/api/v1')
    dci_app.register_blueprint(dci_databrowser)

    return dci_app
