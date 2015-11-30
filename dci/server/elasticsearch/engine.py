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

from elasticsearch import Elasticsearch


class DCIESEngine(object):

    def connect(self, conf):
        self.conn = Elasticsearch(conf['ES_HOST'], port=conf['ES_PORT'])
        return self

    def get(self, id):
        res = self.conn.get(index="global-index", doc_type='log', id=id)
        return res

    def index(self, values):
        self.conn.index(index="global-index", doc_type='log', id=values['id'],
                        body=values)

    def search_content(self, pattern, team_id=None):
        return self.conn.search(index="global-index", body={"query":
                                {"match": {"content": pattern}}})
