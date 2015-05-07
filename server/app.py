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

import os

from pprint import pprint

import server.db.api as api
from server.db.models import Base
from server.db.models import engine
from server.db.models import Job
from server.db.models import Notification
from server.db.models import session

from eve import Eve
from eve_sqlalchemy import SQL
from eve_sqlalchemy.validation import ValidatorSQL
from flask import jsonify

import bcrypt
from eve.auth import BasicAuth

from pprint import pprint


class adminOnlyCrypt(BasicAuth):
    def check_auth(self, name, password, allowed_roles, resource, method):
        # use Eve's own db driver; no additional connections/resources are used
        User = Base.classes.users
        user = session.query(User).filter_by(name=name).one()
        roles = set([ur.role.name for ur in user.user_roles])
        if not user:
            return False
        if bcrypt.hashpw(password, user.password) != user.password:
            return False
        if allowed_roles:
            if not roles & set(allowed_roles):
                return False
        return True


app = Eve(validator=ValidatorSQL, data=SQL, auth=adminOnlyCrypt)
db = app.data.driver
Base.metadata.bind = engine
db.Model = Base


def site_map():
    for rule in app.url_map.iter_rules():
        pprint(rule)

site_map()


@app.route('/jobs/get_job_by_remoteci/<remoteci_id>')
def get_job_by_remoteci(remoteci_id):
    return jsonify(api.get_job_by_remoteci(remoteci_id))


def get_ssh_key_location():
    if 'OPENSHIFT_DATA_DIR' in os.environ:
        ssh_key = os.environ['OPENSHIFT_DATA_DIR'] + '/id_rsa'
    else:
        ssh_key = os.environ['HOME'] + '/.ssh/id_rsa'
    return ssh_key


@app.route('/id_rsa.pub')
def id_rsa_pub():
    ssh_key_pub = get_ssh_key_location() + '.pub'
    return open(ssh_key_pub, 'r').read()


# TODO(Gonéri): Move that somewhere else
def post_jobstates_callback(request, payload):
    job_id = request.form['job_id']
    status = request.form['status']
    if status not in ('success', 'failure'):
        return
    job = session.query(Job).get(job_id)
    pprint(job.id)
    for notification in job.version.notifications.filter(
            Notification.sent == False):  # NOQA
        if notification.struct['type'] == 'stdout':
            print("job %s has been built on %s with status %s" %
                  (job.id,
                   job.remoteci.name,
                   status))
        elif notification.struct['type'] == 'gerrit':
            print("Sending notification to Gerrit")
            if status == 'success':
                score = "+1"
                message = "Distributed CI job has failed on  %s" % (
                    job.remoteci.name)
            else:
                score = "-1"
                message = "Distributed CI job has succeed on remoteci %s" % (
                    job.remoteci.name)
            ssh_key = get_ssh_key_location()
            import subprocess  # TODO(Gonéri)
            subprocess.call(['ssh', '-i', ssh_key,
                             '-oBatchMode=yes', '-oCheckHostIP=no',
                             '-oHashKnownHosts=no',
                             '-oStrictHostKeyChecking=no',
                             '-oPreferredAuthentications=publickey',
                             '-oChallengeResponseAuthentication=no',
                             '-oKbdInteractiveDevices=no',
                             '-oUserKnownHostsFile=/dev/null',
                             '%s@%s' % (
                                 notification.struct['account'],
                                 notification.struct['server']
                             ),
                             '-p', str(notification.struct['port']),
                             'gerrit review --verified %s %s --message "%s"' % (
                                 score,
                                 notification.struct['gitsha1'],
                                 message)])
        notification.sent = True
        session.commit()
    print('A get on "jobevents" was just performed!')


app.on_post_POST_jobstates += post_jobstates_callback

if __name__ == "__main__":
    app.run(debug=True)
