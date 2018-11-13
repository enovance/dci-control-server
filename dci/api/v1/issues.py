# -*- coding: utf-8 -*-
#
# Copyright (C) 2015-2016 Red Hat, Inc
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

import datetime
import flask

from flask import json
from sqlalchemy import sql
from sqlalchemy import exc as sa_exc
from dci.api.v1 import api
from dci.api.v1 import utils as v1_utils
from dci.common import exceptions as dci_exc
from dci.common import schemas
from dci.common import utils
from dci.db import models
from dci import decorators
from dci.trackers import github
from dci.trackers import bugzilla


_TABLE = models.ISSUES
_I_COLUMNS = v1_utils.get_columns_name_with_objects(_TABLE)


def _create_issue(values):

    if 'github.com' in values['url']:
        type = 'github'
    else:
        type = 'bugzilla'

    issue_id = utils.gen_uuid()
    values.update({
        'id': issue_id,
        'created_at': datetime.datetime.utcnow().isoformat(),
        'tracker': type,
    })

    # First, insert the issue if it doesn't already exist
    # in the issues table. If it already exists, ignore the
    # exceptions, and keep proceeding.
    query = _TABLE.insert().returning(*_TABLE.columns).values(**values)
    try:
        return flask.g.db_conn.execute(query).fetchone()
    except sa_exc.IntegrityError:
        # It is not a real failure it the issue have been tried
        # to inserted a second time. As long as it is once, we are
        # good to proceed
        query = (sql.select([_TABLE])
                 .where(_TABLE.c.url == values['url']))
        return flask.g.db_conn.execute(query).fetchone()


def get_issues_by_resource(resource_id, table):
    """Get all issues for a specific job."""

    v1_utils.verify_existence_and_get(resource_id, table)

    # When retrieving the issues for a job, we actually retrieve
    # the issues attach to the job itself + the issues attached to
    # the components the job has been run with.
    if table.name == 'jobs':
        JJI = models.JOIN_JOBS_ISSUES
        JJC = models.JOIN_JOBS_COMPONENTS
        JCI = models.JOIN_COMPONENTS_ISSUES

        # Get all the issues attach to all the components attach to a job
        j1 = sql.join(
            _TABLE,
            sql.join(
                JCI,
                JJC,
                sql.and_(
                    JCI.c.component_id == JJC.c.component_id,
                    JJC.c.job_id == resource_id,
                ),
            ),
            _TABLE.c.id == JCI.c.issue_id,
        )

        query = sql.select([_TABLE]).select_from(j1)
        rows = flask.g.db_conn.execute(query)
        rows = [dict(row) for row in rows]

        # Get all the issues attach to a job
        j2 = sql.join(
            _TABLE,
            JJI,
            sql.and_(
                _TABLE.c.id == JJI.c.issue_id,
                JJI.c.job_id == resource_id
            )
        )
        query2 = sql.select([_TABLE]).select_from(j2)
        rows2 = flask.g.db_conn.execute(query2)
        rows += [dict(row) for row in rows2]

    # When retrieving the issues for a component, we only retrieve the
    # issues attached to the specified component.
    else:
        JCI = models.JOIN_COMPONENTS_ISSUES

        query = (sql.select([_TABLE])
                 .select_from(JCI.join(_TABLE))
                 .where(JCI.c.component_id == resource_id))

        rows = flask.g.db_conn.execute(query)
        rows = [dict(row) for row in rows]

    for row in rows:
        if row['tracker'] == 'github':
            l_tracker = github.Github(row['url'])
        elif row['tracker'] == 'bugzilla':
            l_tracker = bugzilla.Bugzilla(row['url'])
        row.update(l_tracker.dump())

    return flask.jsonify({'issues': rows,
                          '_meta': {'count': len(rows)}})


def unattach_issue(resource_id, issue_id, table):
    """Unattach an issue from a specific job."""

    v1_utils.verify_existence_and_get(issue_id, _TABLE)
    if table.name == 'jobs':
        join_table = models.JOIN_JOBS_ISSUES
        where_clause = sql.and_(join_table.c.job_id == resource_id,
                                join_table.c.issue_id == issue_id)
    else:
        join_table = models.JOIN_COMPONENTS_ISSUES
        where_clause = sql.and_(join_table.c.component_id == resource_id,
                                join_table.c.issue_id == issue_id)

    query = join_table.delete().where(where_clause)
    result = flask.g.db_conn.execute(query)

    if not result.rowcount:
        raise dci_exc.DCIConflict('%s_issues' % table.name, issue_id)

    return flask.Response(None, 204, content_type='application/json')


def attach_issue(resource_id, table, user_id):
    """Attach an issue to a specific job."""

    values = schemas.issue.post(flask.request.json)
    issue = _create_issue(values)

    # Second, insert a join record in the JOIN_JOBS_ISSUES or
    # JOIN_COMPONENTS_ISSUES database.
    if table.name == 'jobs':
        join_table = models.JOIN_JOBS_ISSUES
    else:
        join_table = models.JOIN_COMPONENTS_ISSUES

    key = '%s_id' % table.name[0:-1]
    query = join_table.insert().values({
        'user_id': user_id,
        'issue_id': issue['id'],
        key: resource_id
    })

    try:
        flask.g.db_conn.execute(query)
    except sa_exc.IntegrityError:
        raise dci_exc.DCICreationConflict(join_table.name,
                                          '%s, issue_id' % key)

    result = json.dumps({'issue': values})
    return flask.Response(result, 201, content_type='application/json')


# CRUD /issues
@api.route('/issues', methods=['POST'])
@decorators.login_required
@decorators.check_roles
def create_issue(user):
    values = schemas.issue.post(flask.request.json)
    issue = _create_issue(values)
    result = json.dumps({'issue': issue})
    return flask.Response(result, 201, content_type='application/json')


@api.route('/issues', methods=['GET'])
@decorators.login_required
@decorators.check_roles
def get_all_issues(user):
    args = schemas.args(flask.request.args.to_dict())

    query = v1_utils.QueryBuilder(_TABLE, args, _I_COLUMNS)
    nb_rows = query.get_number_of_rows()
    rows = query.execute(fetchall=True)
    rows = v1_utils.format_result(rows, _TABLE.name)

    return flask.jsonify({'issues': rows, '_meta': {'count': nb_rows}})


@api.route('/issues/<uuid:issue_id>', methods=['GET'])
@decorators.login_required
@decorators.check_roles
def get_issue(user, issue_id):
    issue = v1_utils.verify_existence_and_get(issue_id, _TABLE)
    return flask.jsonify({'issue': issue})


@api.route('/issues/<uuid:issue_id>', methods=['DELETE'])
@decorators.login_required
@decorators.check_roles
def delete_issue_by_id(user, issue_id):
    v1_utils.verify_existence_and_get(issue_id, _TABLE)
    query = _TABLE.delete().where(_TABLE.c.id == issue_id)
    result = flask.g.db_conn.execute(query)

    if not result.rowcount:
        raise dci_exc.DCIDeleteConflict('Issue', issue_id)

    return flask.Response(None, 204, content_type='application/json')
