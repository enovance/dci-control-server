# -*- coding: utf-8 -*-
#
# Copyright (C) 2017 Red Hat, Inc
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

from datetime import datetime, timedelta
import hashlib
import hmac
import random
import string
from werkzeug._compat import to_bytes


def gen_secret(length=64):
    """ Generates a secret of given length
    """
    charset = string.ascii_letters + string.digits
    return ''.join(random.SystemRandom().choice(charset)
                   for _ in range(length))


def format_for_signature(http_verb, content_type, timestamp, url,
                         query_string, payload_hash):
    """Returns the string used to generate the signature in a correctly
    formatter manner.
    """
    return b'\n'.join((
        to_bytes(http_verb, 'utf-8'),
        to_bytes(content_type, 'utf-8'),
        to_bytes(timestamp.strftime('%Y-%m-%d %H:%M:%SZ'), 'utf-8'),
        to_bytes(url, 'utf-8'),
        to_bytes(query_string, 'utf-8'),
        to_bytes(payload_hash, 'utf-8'),
    ))


def gen_signature(secret, http_verb, content_type, timestamp, url,
                  query_string, payload):
    """Generates a signature compatible with DCI for the parameters passed"""
    payload_hash = hashlib.sha256(to_bytes(payload, 'utf-8')).hexdigest()
    stringtosign = format_for_signature(
        http_verb=http_verb,
        content_type=content_type,
        timestamp=timestamp,
        url=url,
        query_string=query_string,
        payload_hash=payload_hash
    )

    return hmac.new(to_bytes(secret, 'utf-8'),
                    stringtosign,
                    hashlib.sha256).hexdigest()


def compare_digest(foo, bar):
    """ Compares two hmac digests.
    NOTE: this uses hmac.compare_digest() if possible, a simple == else.
          hmac.compare_digest is available only in python≥(2.7.7,3.3)"""
    f = getattr(hmac, 'compare_digest', lambda a, b: a == b)
    foo = to_bytes(foo)
    bar = to_bytes(bar)
    return f(foo, bar)


def is_timestamp_in_bounds(timestamp, max_drift=timedelta(minutes=5),
                           now=datetime.utcnow()):
    return abs(now - timestamp) < max_drift


def is_valid(their_signature,
             secret, http_verb, content_type, timestamp, url,
             query_string, payload):
    """Verifies the remote signature against a locally computed signature and
    ensures the timestamp lies within ±5 minutes of current time.

    Returns True if signature is valid and timestamp within defined bounds"""
    local_signature = gen_signature(secret, http_verb, content_type, timestamp,
                                    url, query_string, payload)

    return is_timestamp_in_bounds(timestamp) and \
        compare_digest(their_signature, local_signature)
