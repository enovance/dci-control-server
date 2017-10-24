# -*- encoding: utf-8 -*-
#
# Copyright 2015-2016 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import datetime

import dci.auth_mechanism as authm
from dci.common import exceptions as dci_exc

import flask
import mock
import pytest
import uuid


class MockRequest(object):
    def __init__(self, auth=None):
        self.authorization = auth


class AuthMock(object):
    def __init__(self):
        self.username = 'test'
        self.password = 'password'


def test_basic_auth_mecanism_authenticate_fail_if_no_auth():
    basic_auth_mecanism = authm.BasicAuthMechanism(MockRequest())
    with pytest.raises(dci_exc.DCIException):
        basic_auth_mecanism.authenticate()


def test_bam_authenticate_fail_if_not_authenticated():
    def return_is_authenticated(*args):
        return {}, False

    basic_auth_mecanism = authm.BasicAuthMechanism(MockRequest(AuthMock()))
    basic_auth_mecanism.get_user_and_check_auth = return_is_authenticated
    with pytest.raises(dci_exc.DCIException):
        basic_auth_mecanism.authenticate()


def test_bam_authenticate():
    def return_is_authenticated(*args):
        return {}, True

    def return_get_user_teams(*args):
        return []

    basic_auth_mecanism = authm.BasicAuthMechanism(MockRequest(AuthMock()))
    basic_auth_mecanism.get_user_and_check_auth = return_is_authenticated
    basic_auth_mecanism.get_user_teams = return_get_user_teams
    basic_auth_mecanism.authenticate()


class MockSignedRequest(object):
    def __init__(self, headers={}):
        self.headers = headers


class RemoteCiMock(object):
    def __init__(self, id, api_secret='dummy'):
        self.id = id
        self.api_secret = api_secret
        self.team_id = uuid.uuid4()

    def __iter__(self):
        yield 'team_id', self.team_id


sam_headers = {
    'DCI-Client-Info': '2016-12-12 03:03:03Z/remoteci/Morbo',
    'DCI-Auth-Signature': 'DOOOOOOOM!!!',
}


def return_get_remoteci(*args):
    return RemoteCiMock(args[0])


def _test_client_info_value(client_info_value):
    mech = authm.SignatureAuthMechanism(
        MockSignedRequest({
            'DCI-Client-Info': client_info_value,
            'DCI-Auth-Signature': None,
        }))
    return mech.get_client_info()


def test_get_client_info_bad():
    bad_format_message = \
        'DCI-Client-Info should match the following format: ' + \
        '"YYYY-MM-DD HH:MI:SSZ/<client_type>/<id>"'

    with pytest.raises(dci_exc.DCIException) as e_info:
        _test_client_info_value('pif!paf!pouf!')
    assert e_info.value.message == bad_format_message

    with pytest.raises(dci_exc.DCIException) as e_info:
        _test_client_info_value('pif/paf')
    assert e_info.value.message == bad_format_message

    with pytest.raises(dci_exc.DCIException) as e_info:
        _test_client_info_value('pif/paf/pouf/.')
    assert e_info.value.message == bad_format_message

    with pytest.raises(dci_exc.DCIException) as e_info:
        _test_client_info_value('p/p/')
    assert e_info.value.message == bad_format_message

    with pytest.raises(dci_exc.DCIException) as e_info:
        _test_client_info_value('p//p')
    assert e_info.value.message == bad_format_message

    with pytest.raises(dci_exc.DCIException) as e_info:
        _test_client_info_value('pif/paf/pouf')


def test_get_client_info_good():
    expected = {
        'timestamp': datetime.datetime(2016, 3, 21, 15, 37, 59),
        'type': 'foo',
        'id': '12890-abcdef',
    }
    client_info_value = '2016-03-21 15:37:59Z/foo/12890-abcdef'

    assert _test_client_info_value(client_info_value) == expected


def test_sam_authenticate_fail_if_no_signature():
    mech = authm.SignatureAuthMechanism(MockSignedRequest())
    with pytest.raises(dci_exc.DCIException):
        mech.authenticate()


def test_sam_authenticate_fail_if_not_authenticated():
    def raise_not_authenticated(*args):
        raise dci_exc.DCIException("None shall pass!")

    mech = authm.SignatureAuthMechanism(MockSignedRequest(sam_headers))
    mech.verify_remoteci_auth_signature = raise_not_authenticated
    mech.get_remoteci = return_get_remoteci
    with pytest.raises(dci_exc.DCIException):
        mech.authenticate()


def test_sam_authenticate():
    def return_is_authenticated(*args):
        return True

    mech = authm.SignatureAuthMechanism(MockSignedRequest(sam_headers))
    mech.verify_remoteci_auth_signature = return_is_authenticated
    mech.get_remoteci = return_get_remoteci
    mech.authenticate()


@mock.patch('jwt.api_jwt.datetime', spec=datetime.datetime)
def test_sso_auth_verified(m_datetime, admin, app, engine, access_token):
    m_utcnow = mock.MagicMock()
    m_utcnow.utctimetuple.return_value = datetime.datetime. \
        fromtimestamp(1505564918).timetuple()
    m_datetime.utcnow.return_value = m_utcnow
    sso_headers = mock.Mock
    sso_headers.headers = {'Authorization': 'Bearer %s' % access_token}
    nb_users = len(admin.get('/api/v1/users').data['users'])
    with app.app_context():
        flask.g.db_conn = engine.connect()
        mech = authm.OpenIDCAuth(sso_headers)
        mech.authenticate()
        assert mech.identity['team_id'] is None
        assert mech.identity['name'] == 'dci'
        assert mech.identity['sso_username'] == 'dci'
        assert mech.identity['email'] == 'dci@distributed-ci.io'
        nb_users_after_sso = len(admin.get('/api/v1/users').data['users'])
        assert (nb_users + 1) == nb_users_after_sso


@mock.patch('jwt.api_jwt.datetime', spec=datetime.datetime)
def test_sso_auth_not_verified(m_datetime, admin, app, engine, access_token):
    m_utcnow = mock.MagicMock()
    m_utcnow.utctimetuple.return_value = datetime.datetime. \
        fromtimestamp(1505564918).timetuple()
    m_datetime.utcnow.return_value = m_utcnow
    # corrupt access_token
    access_token = access_token + 'lol'
    sso_headers = mock.Mock
    sso_headers.headers = {'Authorization': 'Bearer %s' % access_token}
    nb_users = len(admin.get('/api/v1/users').data['users'])
    with app.app_context():
        flask.g.db_conn = engine.connect()
        mech = authm.OpenIDCAuth(sso_headers)
        with pytest.raises(dci_exc.DCIException):
            mech.authenticate()
        assert mech.identity is None
        nb_users_after_sso = len(admin.get('/api/v1/users').data['users'])
        assert nb_users == nb_users_after_sso


@mock.patch('jwt.api_jwt.datetime', spec=datetime.datetime)
def test_sso_auth_get_users(m_datetime, user_sso, app, engine):
    m_utcnow = mock.MagicMock()
    m_utcnow.utctimetuple.return_value = datetime.datetime. \
        fromtimestamp(1505564918).timetuple()
    m_datetime.utcnow.return_value = m_utcnow
    with app.app_context():
        flask.g.db_conn = engine.connect()
        gusers = user_sso.get('/api/v1/users')
        assert gusers.status_code == 200


@mock.patch('jwt.api_jwt.datetime', spec=datetime.datetime)
def test_sso_auth_get_current_user(m_datetime, user_sso, app, engine):
    m_utcnow = mock.MagicMock()
    m_utcnow.utctimetuple.return_value = datetime.datetime. \
        fromtimestamp(1505564918).timetuple()
    m_datetime.utcnow.return_value = m_utcnow
    with app.app_context():
        flask.g.db_conn = engine.connect()
        request = user_sso.get('/api/v1/users/me?embed=team,role,remotecis')
        assert request.status_code == 200
