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

# Global parameters about the API itself
#
HOST = '127.0.0.1'
PORT = 5000
DEBUG = True

# ElasticSearch Connection parameters
#
ES_HOST = '127.0.0.1'
ES_PORT = '9200'

# Database (SQLAlchemy) related parameters
#
SQLALCHEMY_DATABASE_URI = 'postgresql://dci:password@127.0.0.1:5432/dci'

# The following two lines will output the SQL statements
# executed by SQLAlchemy. Useful while debugging and in
# development. Turned off by default
# --------
SQLALCHEMY_ECHO = False
SQLALCHEMY_RECORD_QUERIES = False

SQLALCHEMY_POOL_SIZE = 20
SQLALCHEMY_MAX_OVERFLOW = 0
SQLALCHEMY_NATIVE_UNICODE = True

# Stores configuration, to store files and components
# STORE
STORE_ENGINE = 'Swift'
STORE_USERNAME = 'dci_components'
STORE_PASSWORD = 'test'
STORE_TENANT_NAME = 'DCI-Prod'
STORE_AUTH_URL = 'http://46.231.132.68:5000/v2.0'
STORE_CONTAINER = 'dci_components'
STORE_FILES_CONTAINER = 'dci_files'
STORE_COMPONENTS_CONTAINER = 'dci_components'

# ZMQ Connection
ZMQ_CONN = "tcp://127.0.0.1:5557"

# Logging related parameters
PROD_LOG_FORMAT = '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
DEBUG_LOG_FORMAT = (
    '-' * 80 + '\n' +
    '%(levelname)s at %(asctime)s in %(name)s:\n' +
    '%(message)s\n' +
    '-' * 80
)

LOG_FILE = '/tmp/dci.log'


LAST_UPDATED = 'updated_at'
DATE_CREATED = 'created_at'
ID_FIELD = 'id'
ITEM_URL = ('regex("[\.-a-z0-9]{8}-[-a-z0-9]{4}-'
            '[-a-z0-9]{4}-[-a-z0-9]{4}-[-a-z0-9]{12}")')

ITEM_LOOKUP_FIELD = 'id'
ETAG = 'etag'
URL_PREFIX = 'api'
X_DOMAINS = '*'
X_HEADERS = 'Authorization, Content-Type, If-Match, ETag, X-Requested-With'
MAX_CONTENT_LENGTH = 20 * 1024 * 1024

FILES_UPLOAD_FOLDER = '/var/lib/dci-control-server/files'

SSO_CLIENT_ID = 'dci'
# generated by bin/dci-gen-pem-ks-key.py
SSO_PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEA64PNcZgs1adZG4wPuaTv
fM1r2K0E4Yanp4RHEhcn38yoMZy593jB10ej/i+fLv5CRchpLpUPVl6230ugObie
IU4n5BKwt1Y11Wt65UIIf6K3pDTVX5iaT0u6ISSSMHBMpLo5ndfHQHDoMhiyuIFt
DI/RzFlhayJM5GeNjA/qhDHqd2mDEftJ9RyEYCdnRmFm8juOzdsY3DOqp6FpZqQt
+72TRfEbsYG8RRYHKOzhC4yL+7DebWpJdwBjzFx+CbmQRLUmVmIbY0VtDAfVqfFN
yv0IboebFxlX5mCTijk1k3BU8Xb3+vY5CT8f2OSUM78dfrwyX/0uAMPdBl6e0yae
/JE4TV3WXqstpubVybW2SJQT5MIcLPkD9h6hmD5HV19nPYCd1YfImWr383LEHMmB
lT40f5PcBYlqQqOkZj1lUac62cfNRkNBYbONhTLSbK/hezMH3myIHmw+qctMJZtp
kf7/j0VSQf0f1BIChjXsFfkcDuEeeTXSSxh+I9xIB4uYpDbzUiuSlDk74aRaiB3S
USDOa5hKSVfeIv7bNNMgGJQEXXyBIKfajI1MZCEEAOp/SP66Gj4q4nnNJI6aSh+3
hZ3LTvCbgf1OdidRPayfIBECq/oU9hsfu1oX3sJXYdISqaxBXfyWXSbwt5Rv1HuV
4GdQgMGs8c49SX/5ZUZii3sCAwEAAQ==
-----END PUBLIC KEY-----
"""

CA_CERT = '/etc/ssl/repo/ca.crt'
CA_KEY = '/etc/ssl/repo/ca.key'
