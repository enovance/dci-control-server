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
from server.db.models import User

from eve import Eve
from eve_sqlalchemy import SQL
from eve_sqlalchemy.validation import ValidatorSQL
from flask import jsonify
from flask import abort
from flask import request
import sqlalchemy.orm.exc

# WARNING(Gonéri): both python-bcrypt and bcrypt provide a bcrypt package
import bcrypt
from eve.auth import BasicAuth


class AdminOnlyCrypt(BasicAuth):
    def check_auth(self, name, password, allowed_roles, resource, method):
        try:
            user = session.query(User).filter_by(name=name).one()
        except sqlalchemy.orm.exc.NoResultFound:
            return False

        if bcrypt.hashpw(
                password.encode('utf-8'),
                user.password.encode('utf-8')
        ) == user.password.encode('utf-8'):
            return True
        return False

    def authorized(self, allowed_roles, resource, method):
        auth = request.authorization
        if not hasattr(auth, 'username') or not hasattr(auth, 'password'):
            abort(401, description='Unauthorized: username required')
        if not self.check_auth(auth.username, auth.password, None,
                               resource, method):
            abort(401, description='Unauthorized')

        user = session.query(User).filter_by(name=auth.username).one()
        roles = set([ur.role.name for ur in user.user_roles])

        if 'admin' in roles:
            return True

        # NOTE(Gonéri): We may find useful to store this matrice directly in
        # the role entrt in the DB
        acl = {
            'partner': {
                'remotecis': ['GET'],
                'jobs': ['GET'],
                'jobstates': ['GET', 'POST']
            }
        }

        for role in roles:
            try:
                if method in acl[role][resource]:
                    return True
            except KeyError:
                pass
        abort(403, description='Forbidden')


app = Eve(validator=ValidatorSQL, data=SQL, auth=AdminOnlyCrypt)
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

    for notification in job.testversion.version.notifications.filter(
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
                message = ("Distributed CI job has failed ",
                           "on environment %s" % job.environment.name)
            else:
                score = "-1"
                message = ("Distributed CI job has succeed ",
                           "on environment %s" % job.environment.name)
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
                             ('gerrit review --verified ',
                              '%s %s --message "%s"' % (
                                  score,
                                  notification.struct['gitsha1'],
                                  message))])
        notification.sent = True
        session.commit()
    print('A get on "jobevents" was just performed!')


app.on_post_POST_jobstates += post_jobstates_callback

if __name__ == "__main__":
    app.run(debug=True)
