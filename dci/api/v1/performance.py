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

import flask

from dci.api.v1 import api
from dci.api.v1 import utils as v1_utils
from dci.api.v1 import files
from dci.api.v1 import transformations
from dci.common.schemas import (
    check_json_is_valid,
    performance_schema
)
from dci.db import models
from dci import decorators

import logging
from sqlalchemy import sql

LOG = logging.getLogger(__name__)


def _add_delta_to_tests(base_tests, testscases):
    res = []
    for t in testscases:
        res_test = {}
        res_test['classname'] = t.get('classname')
        res_test['name'] = t.get('name')
        key = "%s/%s" % (t.get('classname'), t.get('name'))
        if t.get("time") is None or base_tests.get(key) is None:
            continue

        base_time = float(base_tests.get(key))
        t_time = float(t.get('time'))
        diff = t_time - base_time
        percentage = (diff * 100.) / base_time
        res_test['time'] = t_time
        res_test['delta'] = percentage
        res.append(res_test)
    return res


def _keytify_test_cases(test_cases):
    """Traverse the test cases list and return a dictionnary
    which associate test case name to its duration. This is used for
    fast access to tests cases duration.
    """
    res = {}
    for tc in test_cases:
        key = "%s/%s" % (tc.get('classname'), tc.get('name'))
        if tc.get('time') is None or float(tc.get('time')) == 0.0:
            continue
        res[key] = float(tc.get('time'))
    return res


def get_performance_tests(baseline_test, tests):

    res = []
    baseline_keytified_test_cases = _keytify_test_cases(baseline_test['testscases'])  # noqa

    for t in tests:
        test = transformations.junit2dict(t['fd'])
        test = _add_delta_to_tests(baseline_keytified_test_cases,
                                   test['testscases'])
        res.append({'job_id': t['job_id'],
                    'testscases': test})
    return res


def _get_tests_filenames(job_id):
    query = sql.select([models.FILES.c.name]). \
        where(models.FILES.c.job_id == job_id). \
        where(models.FILES.c.mime == 'application/junit')
    res = flask.g.db_conn.execute(query).fetchall()
    if res is None:
        return []
    else:
        return [r[0] for r in res]


def _get_jobs_tests_with_fds(jobs_ids, test_filename):
    """"for each job get the associated file corresponding to the
    provided filename"""

    def _get_file(job_id):
        query = sql.select([models.FILES]). \
            where(models.FILES.c.job_id == job_id). \
            where(models.FILES.c.name == test_filename)
        return flask.g.db_conn.execute(query).fetchone()

    res = []
    for j_id in jobs_ids:
        j = v1_utils.verify_existence_and_get(j_id, models.JOBS, _raise=False)
        if j is None:
            LOG.error("job %s not found" % j_id)
            continue
        file = _get_file(j_id)
        if file is None:
            logger.error("file %s from job %s not found" % (test_filename, j_id))  # noqa
            continue
        fd = files.get_file_descriptor(file)
        res.append({'fd': fd, 'job_id': j_id})
    return res


def _get_base_mean_job(base_job_ids, test_file):
    _nb_jobs = float(len(base_job_ids))
    base_jobs_tests_with_fd = _get_jobs_tests_with_fds(base_job_ids, test_file)

    # tmp dict will keytify and sum up all the tests cases
    tmp = {}
    for bjt in base_jobs_tests_with_fd:
        testsuite = transformations.junit2dict(bjt['fd'])
        for tc in testsuite['testscases']:
            _key = "%s/%s" % (tc.get('classname'), tc.get('name'))
            if tc.get('time') is None or float(tc.get('time')) == 0.0:
                continue
            if _key in tmp:
                tmp[_key] += float(tc.get('time'))
            else:
                tmp[_key] = float(tc.get('time'))

    testscases = []
    for k, v in tmp.items():
        classname, name = k.split('/')
        testcase = {'classname': classname,
                    'name': name,
                    'time': v / _nb_jobs}  # compute the mean
        testscases.append(testcase)

    return {'testscases': testscases}


@api.route('/performance', methods=['POST'])
@decorators.login_required
def compare_performance(user):
    values = flask.request.json
    check_json_is_valid(performance_schema, values)
    base_jobs_ids = values["base_jobs_ids"]
    jobs_ids = values["jobs"]
    tests_filenames = _get_tests_filenames(base_jobs_ids[0])
    res = []
    for tf in tests_filenames:
        base_mean_job = _get_base_mean_job(base_jobs_ids, tf)
        jobs_tests_with_fd = _get_jobs_tests_with_fds(jobs_ids, tf)
        perf_res = get_performance_tests(base_mean_job, jobs_tests_with_fd)
        res.append({tf: perf_res})

    return flask.jsonify({"performance": res}), 200
