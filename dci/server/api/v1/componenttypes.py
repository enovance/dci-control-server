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
from sqlalchemy import exc as sa_exc
import sqlalchemy.sql

from dci.server.api import exceptions
from dci.server.api.v1 import api
from dci.server.db import models_core as models
from dci.server import utils


@api.route('/componenttypes', methods=['POST'])
def create_componenttypes():
    name = str(flask.request.form.get('name', ''))
    if not name:
        raise exceptions.InvalidAPIUsage(
            message="Parameters missing: name='%s'" % name)

    query = models.COMPONENTYPES.insert().values(name=name)
    try:
        result = flask.g.db_conn.execute(query)
    except sa_exc.IntegrityError:
        raise exceptions.InvalidAPIUsage(
            "Componenttype '%s' already exist." % name)
    except sa_exc.DBAPIError as e:
        raise exceptions.InternalError(str(e))
    result = {'id': result.inserted_primary_key[0]}
    result = json.dumps(result)
    return flask.Response(result, 201, content_type='application/json')


@api.route('/componenttypes', methods=['GET'])
def get_all_componenttypes():
    query = sqlalchemy.sql.select([models.COMPONENTYPES])
    try:
        rows = flask.g.db_conn.execute(query).fetchall()
        result = [dict(row) for row in rows]
    except sa_exc.DBAPIError as e:
        raise exceptions.InternalError(str(e))

    result = {'componenttypes': result}
    result = json.dumps(result, default=utils.json_encoder)
    return flask.Response(result, 200, content_type='application/json')


@api.route('/componenttypes/<ct_id>', methods=['GET'])
def get_componenttype_by_id_or_name(ct_id):
    query = sqlalchemy.sql.select([models.COMPONENTYPES]).where(
        sqlalchemy.sql.or_(models.COMPONENTYPES.c.id == ct_id,
                           models.COMPONENTYPES.c.name == ct_id))
    try:
        result = flask.g.db_conn.execute(query).fetchone()
    except sa_exc.DBAPIError as e:
        raise exceptions.InternalError(str(e))

    if result is None:
        raise exceptions.NotFound("Component type '%s' not found." % ct_id)

    result = dict(result)
    result = json.dumps(result, default=utils.json_encoder)
    return flask.Response(result, 200, content_type='application/json')


@api.route('/componenttypes/<ct_id>', methods=['DELETE'])
def delete_componenttype_by_id_or_name(ct_id):
    query = sqlalchemy.sql.select([models.COMPONENTYPES]).where(
        sqlalchemy.sql.or_(models.COMPONENTYPES.c.id == ct_id,
                           models.COMPONENTYPES.c.name == ct_id))
    try:
        result = flask.g.db_conn.execute(query).fetchone()
    except sa_exc.DBAPIError as e:
        raise exceptions.InternalError(str(e))

    if result is None:
        raise exceptions.NotFound("Component type '%s' not found." % ct_id)

    query = models.COMPONENTYPES.delete().where(
        sqlalchemy.sql.or_(models.COMPONENTYPES.c.id == ct_id,
                           models.COMPONENTYPES.c.name == ct_id))

    try:
        result = flask.g.db_conn.execute(query)
    except sa_exc.DBAPIError as e:
        raise exceptions.InternalError(str(e))

    if result.rowcount == 0:
        raise exceptions.ConflictError("Conflict on component type '%s'." %
                                       ct_id)

    return flask.Response(None, 204, content_type='application/json')
