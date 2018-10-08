# -*- coding: utf-8 -*-
#
# Copyright (C) Red Hat, Inc
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


def test_create_tag(admin, user, job_user_id):
    admin.post('/api/v1/tags', data={'name': 'kikoo'})
    tag = user.post('/api/v1/jobs/%s/tags' % job_user_id,
                    data={'name': 'kikoo'})
    assert tag.status_code == 201


def test_get_all_tags(admin, user, job_user_id):
    admin.post('/api/v1/tags', data={'name': 'kikoo'})
    admin.post('/api/v1/tags', data={'name': 'kikoo2'})

    user.post('/api/v1/jobs/%s/tags' % job_user_id,
              data={'name': 'kikoo'})
    user.post('/api/v1/jobs/%s/tags' % job_user_id,
              data={'name': 'kikoo2'})

    all_tags = user.get('/api/v1/jobs/%s/tags' % job_user_id).data
    assert len(all_tags['tags']) == 2


def test_delete_tag(admin, user, job_user_id):
    tag = admin.post('/api/v1/tags', data={'name': 'kikoo'})
    tag_id = tag.data['tag']['id']

    user.post('/api/v1/jobs/%s/tags' % job_user_id,
              data={'name': 'kikoo'})

    all_tags = user.get('/api/v1/jobs/%s/tags' % job_user_id).data
    assert len(all_tags['tags']) == 1

    tag_deleted = user.delete('/api/v1/jobs/%s/tags/%s' % (job_user_id,
                                                           tag_id))
    assert tag_deleted.status_code == 204

    all_tags = user.get('/api/v1/jobs/%s/tags' % job_user_id).data
    assert len(all_tags['tags']) == 0
