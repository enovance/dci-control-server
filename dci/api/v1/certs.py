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
import flask
import logging
import os.path

from sqlalchemy import orm
from OpenSSL import crypto

from dci import decorators
from dci.api.v1 import api
from dci.api.v1 import base
from dci.api.v1 import export_control
from dci.common import exceptions as dci_exc
from dci.db import models2

logger = logging.getLogger()


def splitpath(path):
    path = os.path.normpath(path)
    paths = path.split("/")
    return [p for p in paths if p]


@api.route("/certs/verify", methods=["GET"])
def verify_repo_access():
    headers = flask.request.headers
    verify = headers.get("SSLVerify")
    fp = headers.get("SSLFingerprint")
    url = headers.get("X-Original-URI")

    if verify != "SUCCESS":
        raise dci_exc.DCIException(
            message="wrong SSLVerify header: %s" % verify, status_code=403
        )

    if len(splitpath(url)) < 3:
        raise dci_exc.DCIException(
            message="requested url is invalid: %s" % url, status_code=403
        )

    product_id, topic_id, component_id = splitpath(url)[:3]

    q_remoteci = flask.g.session.query(models2.Remoteci).filter(
        models2.Remoteci.cert_fp == fp
    )
    try:
        remoteci = q_remoteci.one()
    except orm.exc.NoResultFound:
        raise dci_exc.DCIException(
            message="remoteci fingerprint not found: %s" % fp, status_code=404
        )

    product = base.get_resource_orm(models2.Product, product_id)
    if product.state != "active":
        raise dci_exc.DCIException(
            message="product %s/%s is not active" % (product.name, product.id),
            status_code=403,
        )

    topic = base.get_resource_orm(models2.Topic, topic_id)
    if topic.state != "active":
        raise dci_exc.DCIException(
            message="topic %s/%s is not active" % (topic.name, topic.id),
            status_code=403,
        )

    if str(topic.product_id) != str(product_id):
        raise dci_exc.DCIException(
            message="topic %s/%s does not belongs to product %s/%s"
            % (topic.name, topic.id, product.name, product.id),
            status_code=403,
        )

    component = base.get_resource_orm(models2.Component, component_id)
    if component.state != "active":
        raise dci_exc.DCIException(
            message="component %s/%s is not active" % (component.name, component.id),
            status_code=403,
        )

    if str(component.topic_id) != str(topic_id):
        raise dci_exc.DCIException(
            message="component %s/%s does not belongs to topic %s/%s"
            % (component.name, component.id, topic.name, topic.id),
            status_code=403,
        )

    team_id = remoteci.team_id
    team = base.get_resource_orm(models2.Team, team_id)
    if team.state != "active":
        raise dci_exc.DCIException(
            message="team %s/%s is not active" % (team.name, team.id), status_code=403
        )

    team_ids = [team_id]
    if not export_control.is_teams_associated_to_product(team_ids, product_id):
        raise dci_exc.DCIException(
            message="team %s is not associated to the product %s"
            % (team.name, product.name),
            status_code=403,
        )

    if topic.export_control is True:
        return flask.Response(None, 200)

    if not export_control.is_teams_associated_to_topic(team_ids, topic_id):
        raise dci_exc.DCIException(
            message="team %s is not associated to the topic %s"
            % (team.name, topic.name),
            status_code=403,
        )

    return flask.Response(None, 200)


@api.route("/certs/check", methods=["POST"])
@decorators.login_required
def verify_remoteci_cert(identity):
    if identity.is_not_remoteci():
        raise dci_exc.DCIException("Only remoteci can verify certificate")

    remoteci = base.get_resource_orm(models2.Remoteci, identity.id)
    cert = flask.request.json["cert"]
    c = crypto.load_certificate(crypto.FILETYPE_PEM, cert)

    if c.has_expired():
        raise dci_exc.DCIException("Certificate is expired")

    cert_fp = c.digest("sha1").decode("utf-8").replace(":", "").lower()
    if cert_fp == remoteci.cert_fp:
        return flask.Response("", 204, content_type="application/json")
    raise dci_exc.Forbidden()
