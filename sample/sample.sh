#!/bin/bash

set -eux

#DCI_CONTROL_SERVER=http://dci-boboa.rhcloud.com
DCI_CONTROL_SERVER=http://dci-lefaiseur.rhcloud.com/api

export DCI_CONTROL_SERVER

#git push openshift master:master -f


# create a remote ci
remoteci_id=$(curl --user 'admin:admin' -H "Content-Type: application/json" -X POST -d '[{"name": "rhci"}]' ${DCI_CONTROL_SERVER}/remotecis |jq '.id'|sed 's,",,g')

echo $remoteci_id

# create a product
product_id=$(curl --user 'admin:admin' -H "Content-Type: application/json" -X POST -d '[{"name": "packstack-rdo", "data": {"ksgen_args": {"rules-file": "%%KHALEESI_SETTINGS%%/rules/packstack-rdo-aio.yml"}}}]' ${DCI_CONTROL_SERVER}/products |jq '.id'|sed 's,",,g')

echo $product_id

# create a version
version_id=$(curl --user 'admin:admin' -H "Content-Type: application/json" -X POST -d '[{"product_id": "'${product_id}'", "data": {"ksgen_args": {"product-version-build": "latest"}}, "name": "lastest"}]' ${DCI_CONTROL_SERVER}/versions |jq '.id'|sed 's,",,g')

echo $version_id

# create a test
test_id=$(curl --user 'admin:admin' -H "Content-Type: application/json" -X POST -d '[{"data": {"ksgen_args": {"provisioner-options": "execute_provision", "product-version-workaround": "centos-7.0", "provisioner": "openstack", "distro": "centos-7.0", "tester": "tempest", "installer-network-variant": "ml2-vxlan", "product-version": "kilo", "tester-setup": "rpm", "installer-network": "neutron", "tester-tests": "all", "product-version-repo": "delorean", "workarounds": "enabled"}}, "name":"tempest"}]' ${DCI_CONTROL_SERVER}/tests |jq '.id'|sed 's,",,g')

echo $test_id


# associate a test to a version
testversion_id=$(curl --user 'admin:admin' -H "Content-Type: application/json" -X POST -d '[{"test_id": "'${test_id}'", "version_id": "'${version_id}'"}]' ${DCI_CONTROL_SERVER}/testversions |jq '.id'|sed 's,",,g')

# create a job
job_id=$(curl --user 'admin:admin' -H "Content-Type: application/json" -X POST -d '[{"remoteci_id": "'${remoteci_id}'", "testversion_id": "'${testversion_id}'"}]' ${DCI_CONTROL_SERVER}/jobs |jq '.id'|sed 's,",,g')

# add a jobstate
jobstate_id=$(curl --user 'admin:admin' -H "Content-Type: application/json" -X POST -d '[{"job_id": "'${job_id}'", "status": "ongoing"}]' ${DCI_CONTROL_SERVER}/jobstates |jq '.id'|sed 's,",,g')

# add job logs
curl --user 'admin:admin' -H "Content-Type: application/json" -X POST -d '[{"name": "log_step_1", "content": "the logs for step 1", "mime": "text/plain", "jobstate_id": "'${jobstate_id}'"}]' ${DCI_CONTROL_SERVER}/files

# add a jobstate
jobstate_id=$(curl --user 'admin:admin' -H "Content-Type: application/json" -X POST -d '[{"job_id": "'${job_id}'", "status": "ongoing"}]' ${DCI_CONTROL_SERVER}/jobstates |jq '.id'|sed 's,",,g')

# add job logs
curl --user 'admin:admin' -H "Content-Type: application/json" -X POST -d '[{"name": "log_step_1", "content": "the logs for step 1", "mime": "text/plain", "jobstate_id": "'${jobstate_id}'"}]' ${DCI_CONTROL_SERVER}/files
