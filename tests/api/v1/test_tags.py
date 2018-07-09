# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 Red Hat, Inc
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


from __future__ import unicode_literals


def test_create_tags(admin):
    pt = admin.post('/api/v1/tags', data={'name': 'my tag'})
    assert pt.status_code == 201
    assert pt.data['tag']['name'] == 'my tag'


def test_get_tags(admin):
    gt = admin.get('/api/v1/tags')
    count = gt.data['_meta']['count']
    for x in range(3):
        admin.post('/api/v1/tags', data={'name': 'my tag %s' % x})

    gt = admin.get('/api/v1/tags')
    assert gt.status_code == 200
    assert len(gt.data['tags']) == count + 3


def test_delete_tag_by_id(admin):
    gt = admin.get('/api/v1/tags')
    count = gt.data['_meta']['count']

    pt = admin.post('/api/v1/tags',
                    data={'name': 'my tag to delete'})
    pt_etag = pt.headers.get("ETag")
    pt_id = pt.data['tag']['id']
    assert pt.status_code == 201

    deleted_t = admin.delete('/api/v1/tags/%s' % pt_id,
                             headers={'If-match': pt_etag})
    assert deleted_t.status_code == 204

    gt = admin.get('/api/v1/tags')
    assert len(gt.data['tags']) == count


def test_create_tags_components(admin, components_ids):
    pt = admin.post('/api/v1/tags',
                    data={'name': 'my tag to delete'})
    tag_id = pt.data['tag']['id']
    assert pt.status_code == 201

    pt = admin.post('/api/v1/components/%s/tags' % (components_ids[0]),
                    data={'tag_id': '%s' % tag_id})
    assert pt.status_code == 204


def test_get_tags_components(admin, components_ids):
    gt = admin.get('/api/v1/components/%s/tags' % (components_ids[0]))
    count = gt.data['_meta']['count']

    for x in range(3):
        pt = admin.post('/api/v1/tags', data={'name': 'my tag %s' % x})
        admin.post('/api/v1/components/%s/tags' % (components_ids[0]),
                   data={'tag_id': pt.data['tag']['id']})
    gt = admin.get('/api/v1/components/%s/tags' % (components_ids[0]))
    assert gt.status_code == 200
    assert len(gt.data['tags']) == count + 3


def test_delete_tags_components(admin, components_ids):
    pt = admin.post('/api/v1/tags', data={'name': 'my tag to delete'})
    tag_id = pt.data['tag']['id']
    assert pt.status_code == 201

    pt = admin.post('/api/v1/components/%s/tags' % (components_ids[0]),
                    data={'tag_id': tag_id})
    assert pt.status_code == 204
    pt = admin.delete('/api/v1/components/%s/tags/%s' % (components_ids[0],
                                                         tag_id))
    assert pt.status_code == 204

    gt = admin.get('/api/v1/components/%s/tags' % (components_ids[0]))
    assert pt.status_code == 204
    count = gt.data['_meta']['count']
    assert count == 0
