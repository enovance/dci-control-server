# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 eNovance SAS <licensing@enovance.com>
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

from sqlalchemy.sql import text

from server.db.models import engine
from server.db.models import Job
from server.db.models import Jobstate
from server.db.models import Product
from server.db.models import RemoteCI
from server.db.models import Version
from server.db.models import session
from server.db.models import TestVersion


def get_job_by_remoteci(remoteci_id):
    """Return the first environment_id that has not be associated to this RemoteCI.
    """
    query = text(
        """
SELECT
    testversions.id
FROM
    testversions
WHERE testversions.id NOT IN (
    SELECT
        jobs.testversion_id
    FROM jobs
    WHERE jobs.remoteci_id=:remoteci_id
)
LIMIT 1""")

    r = engine.execute(query, remoteci_id=remoteci_id)
    record = r.fetchone()
    if record is None:
        return {}
    test_version = session.query(TestVersion).get(str(record[0]))
    remoteci = session.query(RemoteCI).get(remoteci_id)
    job = Job(
        remoteci_id=remoteci.id,
        testversion_id=test_version.id)
    session.add(job)
    session.commit()
    session.refresh(job)
    session.add(
        Jobstate(job_id=job.id, status='new')
    )
    session.commit()

    # NOTE(Gonéri): loop to get the father environments URL
#    url_list = [environment.url]
#    while environment.environment:
#        environment = environment.environment
#        url_list.insert(0, environment.url)

    return {'job_id': job.id}
