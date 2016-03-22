# -*- coding: utf-8 -*-
#
# Copyright (C) 2016 Red Hat, Inc
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

from influxdb import InfluxDBClient


class DCIInfluxdbEngine(object):

    def __init__(self, conf):
        self.conn = InfluxDBClient(conf['INFLUXDB_HOST'],
                                   conf['INFLUXDB_PORT'],
                                   conf['INFLUXDB_USER'],
                                   conf['INFLUXDB_PASS'])

    def create_database(self, name):
        self.conn.create_database(name)

    def create_user(self, name, password):
        self.conn.create_user(name, password)

    def grant_privileges(self, username, databasename):
        self.conn.grant_privilege('all', databasename, username)
