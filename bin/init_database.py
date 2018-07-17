#!/usr/bin/env python
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

"""
This module will create the database if it does not exist and add initial data
mandatory for the control server and run alembic script to synchronize the db
"""

from sqlalchemy_utils import functions as sa_funcs

from dci import dci_config, auth
from dci.db import models
from dci.alembic import utils as dci_alembic


def init_db(conf):
    db_uri = conf['SQLALCHEMY_DATABASE_URI']
    if not sa_funcs.database_exists(db_uri):
        sa_funcs.create_database(db_uri)


def add_initial_data(conf):
    engine = dci_config.get_engine(conf).connect()

    def get_or_create(model, values):
        query = model.select().where(model.c.name == values['name'])
        get_result = engine.execute(query).fetchone()
        if get_result:
            return dict(get_result)
        engine.execute(model.insert().values(**values))
        return dict(engine.execute(query).fetchone())

    admin_team = get_or_create(models.TEAMS, {'name': 'admin'})
    roles = [
        {
            'name': 'Product Owner',
            'label': 'PRODUCT_OWNER',
            'description': 'Product Owner role',
        },
        {
            'name': 'Admin',
            'label': 'ADMIN',
            'description': 'Admin role',
        },
        {
            'name': 'User',
            'label': 'USER',
            'description': 'User role',
        },
        {
            'name': 'Read only user',
            'label': 'READ_ONLY_USER',
            'description': 'Read only user role',
        },
        {
            'name': 'RemoteCI',
            'label': 'REMOTECI',
            'description': 'RemoteCI role',
        },
        {
            'name': 'Feeder',
            'label': 'FEEDER',
            'description': 'Feeder role',
        }
    ]
    for role in roles:
        get_or_create(models.ROLES, role)
    super_admin_role = get_or_create(models.ROLES, {
        'name': 'Super Admin',
        'label': 'SUPER_ADMIN',
        'description': 'Super Admin role',
    })
    super_admin = {
        'name': 'admin',
        'password': auth.hash_password('admin'),
        'team_id': admin_team['id'],
        'role_id': super_admin_role['id'],
        'fullname': 'Admin',
        'email': 'admin@example.org'
    }
    get_or_create(models.USERS, super_admin)


def synchronize_alembic():
    dci_alembic.sync()


def main(conf):
    init_db(conf)
    synchronize_alembic()
    add_initial_data(conf)


if __name__ == '__main__':
    conf = dci_config.generate_conf()
    main(conf)
