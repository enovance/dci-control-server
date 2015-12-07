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

import flask
from flask import json

from dci.server.api.v1 import api
from dci.server import auth2
from dci.server.common import schemas


@api.route('/search', methods=['POST'])
@auth2.requires_auth()
def search(user_info):
    values = schemas.search.post(flask.request.json)

    if user_info.role != auth2.SUPER_ADMIN:
        res = flask.g.es_conn.search_content(values['pattern'], user_info.team)
    else:
        res = flask.g.es_conn.search_content(values['pattern'])

    return flask.Response(json.dumps({'logs': res}), 200,
                          content_type='application/json')
