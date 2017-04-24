# -*- encoding: utf-8 -*-
#
# Copyright 2015-2016 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import base64
import collections
import flask
import shutil

import six

import dci.auth as auth
import dci.common.utils as utils
import dci.db.models as models
import dci.dci_config as config

# convenient alias
memoized = utils.memoized
conf = config.generate_conf()


def rm_upload_folder():
    shutil.rmtree(conf['FILES_UPLOAD_FOLDER'], ignore_errors=True)


def generate_client(app, credentials):
    attrs = ['status_code', 'data', 'headers']
    Response = collections.namedtuple('Response', attrs)

    token = (base64.b64encode(('%s:%s' % credentials).encode('utf8'))
             .decode('utf8'))
    headers = {
        'Authorization': 'Basic ' + token,
        'Content-Type': 'application/json'
    }

    def client_open_decorator(func):
        def wrapper(*args, **kwargs):
            headers.update(kwargs.get('headers', {}))
            kwargs['headers'] = headers
            content_type = headers.get('Content-Type')
            data = kwargs.get('data')
            if data and content_type == 'application/json':
                kwargs['data'] = flask.json.dumps(data, cls=utils.JSONEncoder)
            response = func(*args, **kwargs)

            data = response.data
            if response.content_type == 'application/json':
                data = flask.json.loads(data or '{}')
            if type(data) == six.binary_type:
                data = data.decode('utf8')

            return Response(response.status_code, data, response.headers)

        return wrapper

    client = app.test_client()
    client.open = client_open_decorator(client.open)

    return client


def provision(db_conn):
    def db_insert(model_item, **kwargs):
        query = model_item.insert().values(**kwargs)
        return db_conn.execute(query).inserted_primary_key[0]

    user_pw_hash = auth.hash_password('user')
    user_admin_pw_hash = auth.hash_password('user_admin')
    admin_pw_hash = auth.hash_password('admin')

    # Create teams
    team_admin_id = db_insert(models.TEAMS, name='admin')
    team_user_id = db_insert(models.TEAMS, name='user')

    # Create the three mandatory roles
    super_admin_role = {
        'name': 'Super Admin',
        'label': 'SUPER_ADMIN',
        'description': 'Admin of the platform',
        'team_id': team_admin_id,
    }

    admin_role = {
        'name': 'Admin',
        'label': 'ADMIN',
        'description': 'Admin of a team',
        'team_id': team_admin_id,
    }

    user_role = {
        'name': 'User',
        'label': 'USER',
        'description': 'User',
        'team_id': team_admin_id,
    }

    admin_role_id = db_insert(models.ROLES, **admin_role)
    user_role_id = db_insert(models.ROLES, **user_role)
    super_admin_role_id = db_insert(models.ROLES, **super_admin_role)

    # Create basic permissions
    allrights_permission = {
        'name': 'Allrights',
        'label': 'ALLRIGHTS',
        'description': 'Super Admin Permission',
    }

    admin_permission = {
        'name': 'Admin Level',
        'label': 'ADMIN_LEVEL_RIGHT',
        'description': 'Admin Level Permission',
    }

    user_permission = {
        'name': 'User Level',
        'label': 'USER_LEVEL_RIGHT',
        'description': 'User Level Permission',
    }

    allrights_permission_id = db_insert(models.PERMISSIONS,
                                        **allrights_permission)
    admin_permission_id = db_insert(models.PERMISSIONS, **admin_permission)
    user_permission_id = db_insert(models.PERMISSIONS, **user_permission)

    db_insert(models.JOIN_ROLE_PERMISSIONS, role_id=super_admin_role_id,
              permission_id=allrights_permission_id)
    db_insert(models.JOIN_ROLE_PERMISSIONS, role_id=super_admin_role_id,
              permission_id=admin_permission_id)
    db_insert(models.JOIN_ROLE_PERMISSIONS, role_id=super_admin_role_id,
              permission_id=user_permission_id)

    db_insert(models.JOIN_ROLE_PERMISSIONS, role_id=admin_role_id,
              permission_id=admin_permission_id)
    db_insert(models.JOIN_ROLE_PERMISSIONS, role_id=admin_role_id,
              permission_id=user_permission_id)

    db_insert(models.JOIN_ROLE_PERMISSIONS, role_id=user_role_id,
              permission_id=user_permission_id)

    # Create users
    db_insert(models.USERS,
              name='user',
              role_id=user_role_id,
              password=user_pw_hash,
              team_id=team_user_id)

    db_insert(models.USERS,
              name='user_admin',
              role_id=admin_role_id,
              password=user_admin_pw_hash,
              team_id=team_user_id)

    db_insert(models.USERS,
              name='admin',
              role_id=super_admin_role_id,
              password=admin_pw_hash,
              team_id=team_admin_id)
