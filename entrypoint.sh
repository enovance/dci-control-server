#!/bin/sh

python bin/dci-wait-for-db
python bin/dci-dbinit
python bin/keycloak-provision.py

pubkey=$(python bin/dci-get-pem-ks-key.py http://keycloak:8080 dci-test)

export SSO_PUBLIC_KEY="$pubkey"

exec "$@"
