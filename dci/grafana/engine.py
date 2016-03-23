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

import requests


class DCIGrafanaEngine(object):

    def __init__(self, conf):
        self.__host = conf['GRAFANA_HOST']
        self.__port = conf['GRAFANA_PORT']
        self.__user = conf['GRAFANA_USER']
        self.__password = conf['GRAFANA_PASS']
        self.__influxdb_host = conf['INFLUXDB_HOST']
        self.__influxdb_port = conf['INFLUXDB_PORT']
        self.__influxdb_admin_user = conf['INFLUXDB_USER']
        self.__influxdb_admin_password = conf['INFLUXDB_PASS']
        self.__url = 'http://%s:%s@%s:%s' % (self.__user, self.__password,
                                             self.__host, self.__port)

    def create_datasource(self, name):

        payload = {
            'name': name,
            'type': 'influxdb',
            'url': 'http://%s:%s' % (self.__influxdb_host,
                                     self.__influxdb_port),
            'access': 'direct',
            'database': name,
            'user': self.__influxdb_admin_user,
            'password': self.__influxdb_admin_password
        }

        requests.post('%s/api/datasources' % self.__url, data=payload)
