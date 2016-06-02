#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 Red Hat, Inc
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
from dci import auth
from dci.db import models
import dci.dci_config as config
import functools
import getopt
import hashlib
import json
import random
import sqlalchemy
import sqlalchemy_utils.functions
import sys
import time


COMPANIES = ['IBM', 'HP', 'DELL', 'Rackspace', 'Brocade', 'Redhat', 'Huawei',
             'Juniper', 'Comcast']

COMPONENT_TYPES = ['git', 'image', 'package', 'gerrit_review']

COMPONENTS = ['Khaleesi', 'RDO manager', 'OSP director', 'DCI-control-server']

TESTS = ['tempest', 'khaleesi-tempest', 'tox']

VERSIONS = ['v0.8', 'v2.1.1', 'v1.2.15', 'v0.4.2', 'v1.1', 'v2.5']

PROJECT_NAMES = ['Morbid Epsilon', 'Rocky Pluto', 'Timely Shower',
                 'Brave Drill', 'Sad Scissors']

REMOTE_CIS_ATTRS = {
    'storage': ['netapp', 'ceph', 'swift', 'AWS'],
    'network': ['Cisco', 'Juniper', 'HP', 'Brocade'],
    'hardware': ['Dell', 'Intel', 'HP', 'Huawei'],
    'virtualization': ['KVM', 'VMWare', 'Xen', 'Hyper-V']
}

NAMES = ['foobar', 'fubar', 'foo', 'bar', 'baz', 'qux', 'quux', 'norf']

JOB_STATUSES = ['new', 'pre-run', 'running', 'post-run', 'success', 'failure']

TRIPLEOSTACKDUMP = {
  "software_deployments": [],
  "stacks": {
    "overcloud-BlockStorage-l4jgvstzdqhy": {
      "description": "No description",
      "parent": "9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
      "stack_status_reason": "Stack UPDATE completed successfully",
      "stack_name": "overcloud-BlockStorage-l4jgvstzdqhy",
      "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
      "tags": '',
      "creation_time": "2016-04-12T15:10:01",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-BlockStorage-l4jgvstzdqhy/2bfadc97-89fc-42b0-920e-b0ebd7ed3a9d",
          "rel": "self"
        }
      ],
      "updated_time": "2016-04-12T15:10:02",
      "stack_owner": "admin",
      "stack_status": "UPDATE_COMPLETE",
      "id": "2bfadc97-89fc-42b0-920e-b0ebd7ed3a9d",
      "outputs": {
        "disable_rollback": 'true',
        "description": "No description",
        "parent": "9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
        "tags": '',
        "stack_name": "overcloud-BlockStorage-l4jgvstzdqhy",
        "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
        "stack_status_reason": "Stack UPDATE completed successfully",
        "creation_time": "2016-04-12T15:10:01",
        "links": [
          {
            "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-BlockStorage-l4jgvstzdqhy/2bfadc97-89fc-42b0-920e-b0ebd7ed3a9d",
            "rel": "self"
          }
        ],
        "capabilities": [],
        "notification_topics": [],
        "updated_time": "2016-04-12T15:10:02",
        "timeout_mins": 14400,
        "stack_status": "UPDATE_COMPLETE",
        "stack_owner": "admin",
        "parameters": {
          "OS::project_id": "9de7e9a9a2a242718cffa65dae677a33",
          "OS::stack_id": "2bfadc97-89fc-42b0-920e-b0ebd7ed3a9d",
          "OS::stack_name": "overcloud-BlockStorage-l4jgvstzdqhy"
        },
        "id": "2bfadc97-89fc-42b0-920e-b0ebd7ed3a9d",
        "outputs": [],
        "template_description": "No description"
      }
    },
    "overcloud-Controller-d7iywdnu5uzr-1-klhc6fwkxjt3-NodeAdminUserData-6nnbvgya5r2h": {
      "description": "Uses cloud-init to create an additional user with a known name, in addition to the distro-default user created by the cloud-init default.\n",
      "parent": "7ecb0624-6a40-449e-bb6c-e85b8bf2b733",
      "stack_status_reason": "Stack CREATE completed successfully",
      "stack_name": "overcloud-Controller-d7iywdnu5uzr-1-klhc6fwkxjt3-NodeAdminUserData-6nnbvgya5r2h",
      "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
      "tags": '',
      "creation_time": "2016-04-12T15:10:09",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Controller-d7iywdnu5uzr-1-klhc6fwkxjt3-NodeAdminUserData-6nnbvgya5r2h/62d09a4a-79ad-4f39-aeda-3c2b850c0a11",
          "rel": "self"
        }
      ],
      "updated_time": '',
      "stack_owner": "admin",
      "stack_status": "CREATE_COMPLETE",
      "id": "62d09a4a-79ad-4f39-aeda-3c2b850c0a11",
      "outputs": {
        "disable_rollback": 'true',
        "description": "Uses cloud-init to create an additional user with a known name, in addition to the distro-default user created by the cloud-init default.\n",
        "parent": "7ecb0624-6a40-449e-bb6c-e85b8bf2b733",
        "tags": '',
        "stack_name": "overcloud-Controller-d7iywdnu5uzr-1-klhc6fwkxjt3-NodeAdminUserData-6nnbvgya5r2h",
        "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
        "stack_status_reason": "Stack CREATE completed successfully",
        "creation_time": "2016-04-12T15:10:09",
        "links": [
          {
            "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Controller-d7iywdnu5uzr-1-klhc6fwkxjt3-NodeAdminUserData-6nnbvgya5r2h/62d09a4a-79ad-4f39-aeda-3c2b850c0a11",
            "rel": "self"
          }
        ],
        "capabilities": [],
        "notification_topics": [],
        "updated_time": '',
        "timeout_mins": 14400,
        "stack_status": "CREATE_COMPLETE",
        "stack_owner": "admin",
        "parameters": {
          "node_admin_username": "heat-admin",
          "OS::project_id": "9de7e9a9a2a242718cffa65dae677a33",
          "OS::stack_id": "62d09a4a-79ad-4f39-aeda-3c2b850c0a11",
          "OS::stack_name": "overcloud-Controller-d7iywdnu5uzr-1-klhc6fwkxjt3-NodeAdminUserData-6nnbvgya5r2h"
        },
        "id": "62d09a4a-79ad-4f39-aeda-3c2b850c0a11",
        "outputs": [
          {
            "output_value": "43786f44-df7a-4352-ac0f-70011fa3ce6e",
            "description": "No description given",
            "output_key": "OS::stack_id"
          }
        ],
        "template_description": "Uses cloud-init to create an additional user with a known name, in addition to the distro-default user created by the cloud-init default.\n"
      }
    },
    "overcloud-Controller-d7iywdnu5uzr-0-j7rh7d75pr77-NodeAdminUserData-g3dzmkgbyijm": {
      "description": "Uses cloud-init to create an additional user with a known name, in addition to the distro-default user created by the cloud-init default.\n",
      "parent": "04299fe4-e771-425d-9e2b-4ceca3458de1",
      "stack_status_reason": "Stack CREATE completed successfully",
      "stack_name": "overcloud-Controller-d7iywdnu5uzr-0-j7rh7d75pr77-NodeAdminUserData-g3dzmkgbyijm",
      "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
      "tags": '',
      "creation_time": "2016-04-12T15:10:11",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Controller-d7iywdnu5uzr-0-j7rh7d75pr77-NodeAdminUserData-g3dzmkgbyijm/b0d333a8-8a62-4f34-bd06-b92126165855",
          "rel": "self"
        }
      ],
      "updated_time": '',
      "stack_owner": "admin",
      "stack_status": "CREATE_COMPLETE",
      "id": "b0d333a8-8a62-4f34-bd06-b92126165855",
      "outputs": {
        "disable_rollback": 'true',
        "description": "Uses cloud-init to create an additional user with a known name, in addition to the distro-default user created by the cloud-init default.\n",
        "parent": "04299fe4-e771-425d-9e2b-4ceca3458de1",
        "tags": '',
        "stack_name": "overcloud-Controller-d7iywdnu5uzr-0-j7rh7d75pr77-NodeAdminUserData-g3dzmkgbyijm",
        "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
        "stack_status_reason": "Stack CREATE completed successfully",
        "creation_time": "2016-04-12T15:10:11",
        "links": [
          {
            "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Controller-d7iywdnu5uzr-0-j7rh7d75pr77-NodeAdminUserData-g3dzmkgbyijm/b0d333a8-8a62-4f34-bd06-b92126165855",
            "rel": "self"
          }
        ],
        "capabilities": [],
        "notification_topics": [],
        "updated_time": '',
        "timeout_mins": 14400,
        "stack_status": "CREATE_COMPLETE",
        "stack_owner": "admin",
        "parameters": {
          "node_admin_username": "heat-admin",
          "OS::project_id": "9de7e9a9a2a242718cffa65dae677a33",
          "OS::stack_id": "b0d333a8-8a62-4f34-bd06-b92126165855",
          "OS::stack_name": "overcloud-Controller-d7iywdnu5uzr-0-j7rh7d75pr77-NodeAdminUserData-g3dzmkgbyijm"
        },
        "id": "b0d333a8-8a62-4f34-bd06-b92126165855",
        "outputs": [
          {
            "output_value": "f487e529-1143-40ee-9480-f22280dbd860",
            "description": "No description given",
            "output_key": "OS::stack_id"
          }
        ],
        "template_description": "Uses cloud-init to create an additional user with a known name, in addition to the distro-default user created by the cloud-init default.\n"
      }
    },
    "overcloud-RedisVirtualIP-ndkwnexwqzw4": {
      "description": "Creates a port for a VIP on the undercloud ctlplane network. The IP address will be chosen automatically if FixedIPs is empty.\n",
      "parent": "9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
      "stack_status_reason": "Stack CREATE completed successfully",
      "stack_name": "overcloud-RedisVirtualIP-ndkwnexwqzw4",
      "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
      "tags": '',
      "creation_time": "2016-04-12T15:09:56",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-RedisVirtualIP-ndkwnexwqzw4/74727fb1-eb7b-44c7-ad75-3e1f11fd3d67",
          "rel": "self"
        }
      ],
      "updated_time": '',
      "stack_owner": "admin",
      "stack_status": "CREATE_COMPLETE",
      "id": "74727fb1-eb7b-44c7-ad75-3e1f11fd3d67",
      "outputs": {
        "disable_rollback": 'true',
        "description": "Creates a port for a VIP on the undercloud ctlplane network. The IP address will be chosen automatically if FixedIPs is empty.\n",
        "parent": "9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
        "tags": '',
        "stack_name": "overcloud-RedisVirtualIP-ndkwnexwqzw4",
        "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
        "stack_status_reason": "Stack CREATE completed successfully",
        "creation_time": "2016-04-12T15:09:56",
        "links": [
          {
            "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-RedisVirtualIP-ndkwnexwqzw4/74727fb1-eb7b-44c7-ad75-3e1f11fd3d67",
            "rel": "self"
          }
        ],
        "capabilities": [],
        "notification_topics": [],
        "updated_time": '',
        "timeout_mins": 240,
        "stack_status": "CREATE_COMPLETE",
        "stack_owner": "admin",
        "parameters": {
          "FixedIPs": "[]",
          "OS::project_id": "9de7e9a9a2a242718cffa65dae677a33",
          "ControlPlaneNetwork": "ctlplane",
          "OS::stack_id": "74727fb1-eb7b-44c7-ad75-3e1f11fd3d67",
          "OS::stack_name": "overcloud-RedisVirtualIP-ndkwnexwqzw4",
          "ControlPlaneIP": "192.0.2.51",
          "ServiceName": "redis",
          "PortName": "redis_virtual_ip",
          "NetworkName": "internal_api"
        },
        "id": "74727fb1-eb7b-44c7-ad75-3e1f11fd3d67",
        "outputs": [
          {
            "output_value": "192.0.2.52/24",
            "description": "IP/Subnet CIDR for the ctlplane network.",
            "output_key": "ip_subnet"
          },
          {
            "output_value": "192.0.2.52",
            "description": "Virtual IP network IP (for compatibility with vip_v6.yaml)",
            "output_key": "ip_address_uri"
          },
          {
            "output_value": "192.0.2.52",
            "description": "Virtual IP network IP",
            "output_key": "ip_address"
          }
        ],
        "template_description": "Creates a port for a VIP on the undercloud ctlplane network. The IP address will be chosen automatically if FixedIPs is empty.\n"
      }
    },
    "overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3-NodeAdminUserData-hjcxomgp2c4s": {
      "description": "Uses cloud-init to create an additional user with a known name, in addition to the distro-default user created by the cloud-init default.\n",
      "parent": "59a5e87f-86f8-4998-acd4-622f97adcaa1",
      "stack_status_reason": "Stack CREATE completed successfully",
      "stack_name": "overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3-NodeAdminUserData-hjcxomgp2c4s",
      "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
      "tags": '',
      "creation_time": "2016-04-12T15:10:06",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3-NodeAdminUserData-hjcxomgp2c4s/e49fdf8e-291b-45a1-8335-d77b59054681",
          "rel": "self"
        }
      ],
      "updated_time": '',
      "stack_owner": "admin",
      "stack_status": "CREATE_COMPLETE",
      "id": "e49fdf8e-291b-45a1-8335-d77b59054681",
      "outputs": {
        "disable_rollback": 'true',
        "description": "Uses cloud-init to create an additional user with a known name, in addition to the distro-default user created by the cloud-init default.\n",
        "parent": "59a5e87f-86f8-4998-acd4-622f97adcaa1",
        "tags": '',
        "stack_name": "overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3-NodeAdminUserData-hjcxomgp2c4s",
        "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
        "stack_status_reason": "Stack CREATE completed successfully",
        "creation_time": "2016-04-12T15:10:06",
        "links": [
          {
            "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3-NodeAdminUserData-hjcxomgp2c4s/e49fdf8e-291b-45a1-8335-d77b59054681",
            "rel": "self"
          }
        ],
        "capabilities": [],
        "notification_topics": [],
        "updated_time": '',
        "timeout_mins": 14400,
        "stack_status": "CREATE_COMPLETE",
        "stack_owner": "admin",
        "parameters": {
          "node_admin_username": "heat-admin",
          "OS::project_id": "9de7e9a9a2a242718cffa65dae677a33",
          "OS::stack_id": "e49fdf8e-291b-45a1-8335-d77b59054681",
          "OS::stack_name": "overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3-NodeAdminUserData-hjcxomgp2c4s"
        },
        "id": "e49fdf8e-291b-45a1-8335-d77b59054681",
        "outputs": [
          {
            "output_value": "6307ac0e-4f18-451d-837a-1d6b153a1bbc",
            "description": "No description given",
            "output_key": "OS::stack_id"
          }
        ],
        "template_description": "Uses cloud-init to create an additional user with a known name, in addition to the distro-default user created by the cloud-init default.\n"
      }
    },
    "overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3": {
      "description": "OpenStack hypervisor node configured via Puppet.\n",
      "parent": "d3c93c64-778f-4cec-a5a8-062de076c0b6",
      "stack_status_reason": "Resource CREATE failed: ResourceInError: resources.NovaCompute: Went to status ERROR due to \"Message: No valid host was found. There are not enough hosts available., Code: 500\"",
      "stack_name": "overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3",
      "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
      "tags": '',
      "creation_time": "2016-04-12T15:10:04",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3/59a5e87f-86f8-4998-acd4-622f97adcaa1",
          "rel": "self"
        }
      ],
      "updated_time": '',
      "stack_owner": "admin",
      "stack_status": "CREATE_FAILED",
      "id": "59a5e87f-86f8-4998-acd4-622f97adcaa1",
      "outputs": {
        "disable_rollback": 'true',
        "description": "OpenStack hypervisor node configured via Puppet.\n",
        "parent": "d3c93c64-778f-4cec-a5a8-062de076c0b6",
        "tags": '',
        "stack_name": "overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3",
        "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
        "stack_status_reason": "Resource CREATE failed: ResourceInError: resources.NovaCompute: Went to status ERROR due to \"Message: No valid host was found. There are not enough hosts available., Code: 500\"",
        "creation_time": "2016-04-12T15:10:04",
        "links": [
          {
            "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3/59a5e87f-86f8-4998-acd4-622f97adcaa1",
            "rel": "self"
          }
        ],
        "capabilities": [],
        "notification_topics": [],
        "updated_time": '',
        "timeout_mins": 14400,
        "stack_status": "CREATE_FAILED",
        "stack_owner": "admin",
        "parameters": {
          "OS::project_id": "9de7e9a9a2a242718cffa65dae677a33",
          "NeutronPublicInterfaceRawDevice": "",
          "NeutronNetworkVLANRanges": "[u'datacentre:1:1000']",
          "NetworkDeploymentActions": "[u'CREATE']",
          "NovaComputeDriver": "libvirt.LibvirtDriver",
          "Hostname": "overcloud-novacompute-0",
          "NeutronTenantMtu": "1400",
          "NeutronPassword": "******",
          "NeutronFlatNetworks": "[u'datacentre']",
          "EnablePackageInstall": "False",
          "NovaOVSBridge": "br-int",
          "NovaEnableRbdBackend": "False",
          "SnmpdReadonlyUserPassword": "******",
          "NeutronTunnelTypes": "[u'vxlan']",
          "CeilometerComputeAgent": "",
          "NeutronTunnelIdRanges": "[u'1:4094']",
          "CinderEnableRbdBackend": "False",
          "NeutronVniRanges": "[u'1:4094']",
          "NeutronAgentExtensions": "[u'qos']",
          "NovaComputeLibvirtVifDriver": "",
          "CloudDomain": "localdomain",
          "OS::stack_name": "overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3",
          "NovaApiHost": "192.0.2.51",
          "RabbitClientPort": "5672",
          "NovaComputeExtraConfig": "{}",
          "ServerMetadata": "{}",
          "ServiceNetMap": "{u'NovaVncProxyNetwork': u'internal_api', u'CinderApiNetwork': u'internal_api', u'NovaApiNetwork': u'internal_api', u'CeilometerApiNetwork': u'internal_api', u'CephStorageHostnameResolveNetwork': u'storage', u'SwiftMgmtNetwork': u'storage_mgmt', u'MemcachedNetwork': u'internal_api', u'RabbitMqNetwork': u'internal_api', u'KeystoneAdminApiNetwork': u'ctlplane', u'SwiftProxyNetwork': u'storage', u'NeutronTenantNetwork': u'tenant', u'CephClusterNetwork': u'storage_mgmt', u'NovaMetadataNetwork': u'internal_api', u'ControllerHostnameResolveNetwork': u'internal_api', u'NeutronApiNetwork': u'internal_api', u'GlanceApiNetwork': u'storage', u'ObjectStorageHostnameResolveNetwork': u'internal_api', u'KeystonePublicApiNetwork': u'internal_api', u'HeatApiNetwork': u'internal_api', u'GlanceRegistryNetwork': u'internal_api', u'RedisNetwork': u'internal_api', u'MysqlNetwork': u'internal_api', u'BlockStorageHostnameResolveNetwork': u'internal_api', u'ComputeHostnameResolveNetwork': u'internal_api', u'CephPublicNetwork': u'storage', u'MongoDbNetwork': u'internal_api', u'HorizonNetwork': u'internal_api', u'CinderIscsiNetwork': u'storage'}",
          "SnmpdReadonlyUserName": "ro_snmp_user",
          "KeyName": "default",
          "NovaPublicIP": "192.0.2.51",
          "CeilometerMeteringSecret": "******",
          "KeystoneAdminApiVirtualIP": "192.0.2.51",
          "NeutronNetworkType": "[u'vxlan']",
          "CeilometerPassword": "******",
          "NtpServer": "[u'north-america.pool.ntp.org']",
          "CinderEnableNfsBackend": "False",
          "NeutronTypeDrivers": "[u'vxlan', u'vlan', u'flat', u'gre']",
          "NodeIndex": "0",
          "KeystonePublicApiVirtualIP": "192.0.2.51",
          "NeutronMechanismDrivers": "[u'openvswitch']",
          "RabbitClientUseSSL": "False",
          "NeutronAllowL3AgentFailover": "False",
          "RabbitPassword": "******",
          "NeutronEnableL2Pop": "False",
          "TimeZone": "UTC",
          "ImageUpdatePolicy": "REBUILD_PRESERVE_EPHEMERAL",
          "EndpointMap": "{u'GlanceInternal': {u'uri_no_suffix': u'http://192.0.2.51:9292', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'9292', u'uri': u'http://192.0.2.51:9292'}, u'NovaEC2Public': {u'uri_no_suffix': u'http://192.0.2.51:8773', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8773', u'uri': u'http://192.0.2.51:8773/services/Cloud'}, u'HeatPublic': {u'uri_no_suffix': u'http://192.0.2.51:8004', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8004', u'uri': u'http://192.0.2.51:8004/v1/%(tenant_id)s'}, u'KeystonePublic': {u'uri_no_suffix': u'http://192.0.2.51:5000', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'5000', u'uri': u'http://192.0.2.51:5000/v2.0'}, u'HeatAdmin': {u'uri_no_suffix': u'http://192.0.2.51:8004', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8004', u'uri': u'http://192.0.2.51:8004/v1/%(tenant_id)s'}, u'NovaEC2Admin': {u'uri_no_suffix': u'http://192.0.2.51:8773', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8773', u'uri': u'http://192.0.2.51:8773/services/Admin'}, u'CeilometerAdmin': {u'uri_no_suffix': u'http://192.0.2.51:8777', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8777', u'uri': u'http://192.0.2.51:8777'}, u'GlanceAdmin': {u'uri_no_suffix': u'http://192.0.2.51:9292', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'9292', u'uri': u'http://192.0.2.51:9292'}, u'SwiftS3Internal': {u'uri_no_suffix': u'http://192.0.2.51:8080', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8080', u'uri': u'http://192.0.2.51:8080'}, u'CinderV2Internal': {u'uri_no_suffix': u'http://192.0.2.51:8776', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8776', u'uri': u'http://192.0.2.51:8776/v2/%(tenant_id)s'}, u'NovaVNCProxyAdmin': {u'uri_no_suffix': u'http://192.0.2.51:6080', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'6080', u'uri': u'http://192.0.2.51:6080'}, u'HeatInternal': {u'uri_no_suffix': u'http://192.0.2.51:8004', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8004', u'uri': u'http://192.0.2.51:8004/v1/%(tenant_id)s'}, u'NovaV3Admin': {u'uri_no_suffix': u'http://192.0.2.51:8774', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8774', u'uri': u'http://192.0.2.51:8774/v3'}, u'NeutronPublic': {u'uri_no_suffix': u'http://192.0.2.51:9696', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'9696', u'uri': u'http://192.0.2.51:9696'}, u'CinderPublic': {u'uri_no_suffix': u'http://192.0.2.51:8776', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8776', u'uri': u'http://192.0.2.51:8776/v1/%(tenant_id)s'}, u'HorizonPublic': {u'uri_no_suffix': u'http://192.0.2.51:80', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'80', u'uri': u'http://192.0.2.51:80/dashboard'}, u'KeystoneEC2': {u'uri_no_suffix': u'http://192.0.2.51:5000', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'5000', u'uri': u'http://192.0.2.51:5000/v2.0/ec2tokens'}, u'GlancePublic': {u'uri_no_suffix': u'http://192.0.2.51:9292', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'9292', u'uri': u'http://192.0.2.51:9292'}, u'CinderV2Admin': {u'uri_no_suffix': u'http://192.0.2.51:8776', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8776', u'uri': u'http://192.0.2.51:8776/v2/%(tenant_id)s'}, u'GlanceRegistryPublic': {u'uri_no_suffix': u'http://192.0.2.51:9191', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'9191', u'uri': u'http://192.0.2.51:9191'}, u'NeutronAdmin': {u'uri_no_suffix': u'http://192.0.2.51:9696', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'9696', u'uri': u'http://192.0.2.51:9696'}, u'SwiftInternal': {u'uri_no_suffix': u'http://192.0.2.51:8080', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8080', u'uri': u'http://192.0.2.51:8080/v1/AUTH_%(tenant_id)s'}, u'NovaVNCProxyPublic': {u'uri_no_suffix': u'http://192.0.2.51:6080', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'6080', u'uri': u'http://192.0.2.51:6080'}, u'CeilometerInternal': {u'uri_no_suffix': u'http://192.0.2.51:8777', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8777', u'uri': u'http://192.0.2.51:8777'}, u'NovaInternal': {u'uri_no_suffix': u'http://192.0.2.51:8774', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8774', u'uri': u'http://192.0.2.51:8774/v2.1/%(tenant_id)s'}, u'GlanceRegistryInternal': {u'uri_no_suffix': u'http://192.0.2.51:9191', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'9191', u'uri': u'http://192.0.2.51:9191'}, u'NovaV3Internal': {u'uri_no_suffix': u'http://192.0.2.51:8774', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8774', u'uri': u'http://192.0.2.51:8774/v3'}, u'NovaAdmin': {u'uri_no_suffix': u'http://192.0.2.51:8774', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8774', u'uri': u'http://192.0.2.51:8774/v2.1/%(tenant_id)s'}, u'NovaEC2Internal': {u'uri_no_suffix': u'http://192.0.2.51:8773', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8773', u'uri': u'http://192.0.2.51:8773/services/Cloud'}, u'SwiftAdmin': {u'uri_no_suffix': u'http://192.0.2.51:8080', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8080', u'uri': u'http://192.0.2.51:8080'}, u'NeutronInternal': {u'uri_no_suffix': u'http://192.0.2.51:9696', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'9696', u'uri': u'http://192.0.2.51:9696'}, u'NovaPublic': {u'uri_no_suffix': u'http://192.0.2.51:8774', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8774', u'uri': u'http://192.0.2.51:8774/v2.1/%(tenant_id)s'}, u'SwiftS3Admin': {u'uri_no_suffix': u'http://192.0.2.51:8080', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8080', u'uri': u'http://192.0.2.51:8080'}, u'CeilometerPublic': {u'uri_no_suffix': u'http://192.0.2.51:8777', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8777', u'uri': u'http://192.0.2.51:8777'}, u'CinderV2Public': {u'uri_no_suffix': u'http://192.0.2.51:8776', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8776', u'uri': u'http://192.0.2.51:8776/v2/%(tenant_id)s'}, u'KeystoneAdmin': {u'uri_no_suffix': u'http://192.0.2.51:35357', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'35357', u'uri': u'http://192.0.2.51:35357/v2.0'}, u'GlanceRegistryAdmin': {u'uri_no_suffix': u'http://192.0.2.51:9191', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'9191', u'uri': u'http://192.0.2.51:9191'}, u'CinderInternal': {u'uri_no_suffix': u'http://192.0.2.51:8776', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8776', u'uri': u'http://192.0.2.51:8776/v1/%(tenant_id)s'}, u'SwiftS3Public': {u'uri_no_suffix': u'http://192.0.2.51:8080', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8080', u'uri': u'http://192.0.2.51:8080'}, u'NovaV3Public': {u'uri_no_suffix': u'http://192.0.2.51:8774', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8774', u'uri': u'http://192.0.2.51:8774/v3'}, u'SwiftPublic': {u'uri_no_suffix': u'http://192.0.2.51:8080', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8080', u'uri': u'http://192.0.2.51:8080/v1/AUTH_%(tenant_id)s'}, u'CinderAdmin': {u'uri_no_suffix': u'http://192.0.2.51:8776', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8776', u'uri': u'http://192.0.2.51:8776/v1/%(tenant_id)s'}, u'NovaVNCProxyInternal': {u'uri_no_suffix': u'http://192.0.2.51:6080', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'6080', u'uri': u'http://192.0.2.51:6080'}, u'KeystoneInternal': {u'uri_no_suffix': u'http://192.0.2.51:5000', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'5000', u'uri': u'http://192.0.2.51:5000/v2.0'}}",
          "RabbitUserName": "guest",
          "SchedulerHints": "{}",
          "Debug": "",
          "NeutronAgentMode": "dvr",
          "NovaSecurityGroupAPI": "neutron",
          "NovaPassword": "******",
          "NovaIPv6": "False",
          "UpgradeLevelNovaCompute": "",
          "GlanceHost": "192.0.2.51",
          "SoftwareConfigTransport": "POLL_SERVER_CFN",
          "NeutronL3HA": "True",
          "NovaComputeLibvirtType": "kvm",
          "OS::stack_id": "59a5e87f-86f8-4998-acd4-622f97adcaa1",
          "AdminPassword": "******",
          "NeutronPhysicalBridge": "br-ex",
          "NeutronDVR": "False",
          "Image": "overcloud-full",
          "ExtraConfig": "{}",
          "RabbitHost": "192.0.2.51",
          "NeutronBridgeMappings": "[u'datacentre:br-ex']",
          "NeutronServicePlugins": "[u'router', u'qos']",
          "NeutronCorePlugin": "ml2",
          "NeutronPublicInterface": "nic1",
          "NeutronMetadataProxySharedSecret": "******",
          "NovaComputeIPs": "{}",
          "HostnameMap": "{}",
          "Flavor": "compute",
          "NeutronHost": "192.0.2.51",
          "NeutronEnableTunnelling": "True",
          "UpdateIdentifier": ""
        },
        "id": "59a5e87f-86f8-4998-acd4-622f97adcaa1",
        "outputs": [
          {
            "output_value": '',
            "description": "IP address of the server in the storage_mgmt network",
            "output_key": "storage_mgmt_ip_address"
          },
          {
            "output_value": '',
            "description": "Hostname of the server",
            "output_key": "hostname"
          },
          {
            "output_value": ",,,",
            "description": "identifier which changes if the node configuration may need re-applying",
            "output_key": "config_identifier"
          },
          {
            "output_value": "ac50a70d-b709-4093-b0c8-e42285264afd",
            "description": "Heat resource handle for the Nova compute server",
            "output_key": "nova_server_resource"
          },
          {
            "output_value": '',
            "description": "IP address of the server in the tenant network",
            "output_key": "tenant_ip_address"
          },
          {
            "output_value": '',
            "description": "IP address of the server in the external network",
            "output_key": "external_ip_address"
          },
          {
            "output_value": " .localdomain ",
            "description": "Server's IP address and hostname in the /etc/hosts format\n",
            "output_key": "hosts_entry"
          },
          {
            "output_value": '',
            "description": "IP address of the server in the storage network",
            "output_key": "storage_ip_address"
          },
          {
            "output_value": '',
            "description": "IP address of the server in the internal_api network",
            "output_key": "internal_api_ip_address"
          },
          {
            "output_value": '',
            "description": "IP address of the server in the ctlplane network",
            "output_key": "ip_address"
          },
          {
            "output_value": '',
            "description": "IP address of the server in the management network",
            "output_key": "management_ip_address"
          }
        ],
        "template_description": "OpenStack hypervisor node configured via Puppet.\n"
      }
    },
    "overcloud-StorageMgmtVirtualIP-gdvz4nm4owxu": {
      "description": "Returns the control plane port (provisioning network) as the ip_address.\n",
      "parent": "9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
      "stack_status_reason": "Stack CREATE completed successfully",
      "stack_name": "overcloud-StorageMgmtVirtualIP-gdvz4nm4owxu",
      "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
      "tags": '',
      "creation_time": "2016-04-12T15:09:55",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-StorageMgmtVirtualIP-gdvz4nm4owxu/52b6c1ea-4421-411b-80ad-383f71803729",
          "rel": "self"
        }
      ],
      "updated_time": '',
      "stack_owner": "admin",
      "stack_status": "CREATE_COMPLETE",
      "id": "52b6c1ea-4421-411b-80ad-383f71803729",
      "outputs": {
        "disable_rollback": 'true',
        "description": "Returns the control plane port (provisioning network) as the ip_address.\n",
        "parent": "9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
        "tags": '',
        "stack_name": "overcloud-StorageMgmtVirtualIP-gdvz4nm4owxu",
        "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
        "stack_status_reason": "Stack CREATE completed successfully",
        "creation_time": "2016-04-12T15:09:55",
        "links": [
          {
            "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-StorageMgmtVirtualIP-gdvz4nm4owxu/52b6c1ea-4421-411b-80ad-383f71803729",
            "rel": "self"
          }
        ],
        "capabilities": [],
        "notification_topics": [],
        "updated_time": '',
        "timeout_mins": 240,
        "stack_status": "CREATE_COMPLETE",
        "stack_owner": "admin",
        "parameters": {
          "FixedIPs": "[]",
          "OS::project_id": "9de7e9a9a2a242718cffa65dae677a33",
          "ControlPlaneNetwork": "ctlplane",
          "OS::stack_id": "52b6c1ea-4421-411b-80ad-383f71803729",
          "OS::stack_name": "overcloud-StorageMgmtVirtualIP-gdvz4nm4owxu",
          "NodeIndex": "0",
          "ControlPlaneIP": "192.0.2.51",
          "ControlPlaneSubnetCidr": "24",
          "ServiceName": "",
          "PortName": "storage_management_virtual_ip",
          "IPPool": "{}",
          "NetworkName": "storage_mgmt"
        },
        "id": "52b6c1ea-4421-411b-80ad-383f71803729",
        "outputs": [
          {
            "output_value": "192.0.2.51/24",
            "description": "IP/Subnet CIDR for the pass thru network IP",
            "output_key": "ip_subnet"
          },
          {
            "output_value": "192.0.2.51",
            "description": "pass thru network IP (for compatibility with vip_v6.yaml)",
            "output_key": "ip_address_uri"
          },
          {
            "output_value": "192.0.2.51",
            "description": "pass thru network IP",
            "output_key": "ip_address"
          }
        ],
        "template_description": "Returns the control plane port (provisioning network) as the ip_address.\n"
      }
    },
    "overcloud-VipMap-ipemp65ncqfi": {
      "description": "No description",
      "parent": "9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
      "stack_status_reason": "Stack CREATE completed successfully",
      "stack_name": "overcloud-VipMap-ipemp65ncqfi",
      "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
      "tags": '',
      "creation_time": "2016-04-12T15:09:58",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-VipMap-ipemp65ncqfi/65178912-9996-4493-8561-10a62343cc39",
          "rel": "self"
        }
      ],
      "updated_time": '',
      "stack_owner": "admin",
      "stack_status": "CREATE_COMPLETE",
      "id": "65178912-9996-4493-8561-10a62343cc39",
      "outputs": {
        "disable_rollback": 'true',
        "description": "No description",
        "parent": "9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
        "tags": '',
        "stack_name": "overcloud-VipMap-ipemp65ncqfi",
        "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
        "stack_status_reason": "Stack CREATE completed successfully",
        "creation_time": "2016-04-12T15:09:58",
        "links": [
          {
            "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-VipMap-ipemp65ncqfi/65178912-9996-4493-8561-10a62343cc39",
            "rel": "self"
          }
        ],
        "capabilities": [],
        "notification_topics": [],
        "updated_time": '',
        "timeout_mins": 240,
        "stack_status": "CREATE_COMPLETE",
        "stack_owner": "admin",
        "parameters": {
          "ExternalIp": "192.0.2.51",
          "OS::project_id": "9de7e9a9a2a242718cffa65dae677a33",
          "TenantIp": "",
          "OS::stack_id": "65178912-9996-4493-8561-10a62343cc39",
          "OS::stack_name": "overcloud-VipMap-ipemp65ncqfi",
          "StorageIp": "192.0.2.51",
          "ControlPlaneIp": "192.0.2.51",
          "InternalApiIp": "192.0.2.51",
          "InternalApiIpUri": "192.0.2.51",
          "ManagementIpUri": "",
          "TenantIpUri": "",
          "ManagementIp": "",
          "StorageIpUri": "192.0.2.51",
          "StorageMgmtIpUri": "192.0.2.51",
          "ExternalIpUri": "192.0.2.51",
          "StorageMgmtIp": "192.0.2.51"
        },
        "id": "65178912-9996-4493-8561-10a62343cc39",
        "outputs": [
          {
            "output_value": {
              "management": "",
              "storage": "192.0.2.51",
              "ctlplane": "192.0.2.51",
              "external": "192.0.2.51",
              "internal_api": "192.0.2.51",
              "storage_mgmt": "192.0.2.51",
              "tenant": ""
            },
            "description": "A Hash containing a mapping of network names to assigned IPs for a specific machine.\n",
            "output_key": "net_ip_map"
          },
          {
            "output_value": {
              "management": "",
              "storage": "192.0.2.51",
              "ctlplane": "192.0.2.51",
              "external": "192.0.2.51",
              "internal_api": "192.0.2.51",
              "storage_mgmt": "192.0.2.51",
              "tenant": ""
            },
            "description": "A Hash containing a mapping of netowrk names to assigned IPs for a specific machine with brackets around IPv6 addresses for use in URLs.\n",
            "output_key": "net_ip_uri_map"
          }
        ],
        "template_description": "No description"
      }
    },
    "overcloud-Controller-d7iywdnu5uzr-1-klhc6fwkxjt3-UpdateConfig-bzgakgsj5qza": {
      "description": "Software-config for performing package updates using yum\n",
      "parent": "7ecb0624-6a40-449e-bb6c-e85b8bf2b733",
      "stack_status_reason": "Stack CREATE completed successfully",
      "stack_name": "overcloud-Controller-d7iywdnu5uzr-1-klhc6fwkxjt3-UpdateConfig-bzgakgsj5qza",
      "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
      "tags": '',
      "creation_time": "2016-04-12T15:10:08",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Controller-d7iywdnu5uzr-1-klhc6fwkxjt3-UpdateConfig-bzgakgsj5qza/fedba130-0d0e-4f2f-ad08-bf5ed0e4253f",
          "rel": "self"
        }
      ],
      "updated_time": '',
      "stack_owner": "admin",
      "stack_status": "CREATE_COMPLETE",
      "id": "fedba130-0d0e-4f2f-ad08-bf5ed0e4253f",
      "outputs": {
        "disable_rollback": 'true',
        "description": "Software-config for performing package updates using yum\n",
        "parent": "7ecb0624-6a40-449e-bb6c-e85b8bf2b733",
        "tags": '',
        "stack_name": "overcloud-Controller-d7iywdnu5uzr-1-klhc6fwkxjt3-UpdateConfig-bzgakgsj5qza",
        "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
        "stack_status_reason": "Stack CREATE completed successfully",
        "creation_time": "2016-04-12T15:10:08",
        "links": [
          {
            "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Controller-d7iywdnu5uzr-1-klhc6fwkxjt3-UpdateConfig-bzgakgsj5qza/fedba130-0d0e-4f2f-ad08-bf5ed0e4253f",
            "rel": "self"
          }
        ],
        "capabilities": [],
        "notification_topics": [],
        "updated_time": '',
        "timeout_mins": 14400,
        "stack_status": "CREATE_COMPLETE",
        "stack_owner": "admin",
        "parameters": {
          "OS::project_id": "9de7e9a9a2a242718cffa65dae677a33",
          "OS::stack_id": "fedba130-0d0e-4f2f-ad08-bf5ed0e4253f",
          "OS::stack_name": "overcloud-Controller-d7iywdnu5uzr-1-klhc6fwkxjt3-UpdateConfig-bzgakgsj5qza"
        },
        "id": "fedba130-0d0e-4f2f-ad08-bf5ed0e4253f",
        "outputs": [
          {
            "output_value": "a1ef34b3-d6ec-4710-8732-02d60e603660",
            "description": "No description given",
            "output_key": "OS::stack_id"
          }
        ],
        "template_description": "Software-config for performing package updates using yum\n"
      }
    },
    "overcloud-Controller-d7iywdnu5uzr-2-evqysybsnrrt-NodeUserData-zmwd2rjmspal": {
      "description": "This is a default no-op template which provides empty user-data which can be passed to the OS::Nova::Server resources. This template can be replaced with a different implementation via the resource registry, such that deployers may customize their first-boot configuration.\n",
      "parent": "e4dc37e4-d565-4453-8d6e-a830953eb803",
      "stack_status_reason": "Stack CREATE completed successfully",
      "stack_name": "overcloud-Controller-d7iywdnu5uzr-2-evqysybsnrrt-NodeUserData-zmwd2rjmspal",
      "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
      "tags": '',
      "creation_time": "2016-04-12T15:10:13",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Controller-d7iywdnu5uzr-2-evqysybsnrrt-NodeUserData-zmwd2rjmspal/446edf9a-cbe3-4714-a996-d07f41b18ea7",
          "rel": "self"
        }
      ],
      "updated_time": '',
      "stack_owner": "admin",
      "stack_status": "CREATE_COMPLETE",
      "id": "446edf9a-cbe3-4714-a996-d07f41b18ea7",
      "outputs": {
        "disable_rollback": 'true',
        "description": "This is a default no-op template which provides empty user-data which can be passed to the OS::Nova::Server resources. This template can be replaced with a different implementation via the resource registry, such that deployers may customize their first-boot configuration.\n",
        "parent": "e4dc37e4-d565-4453-8d6e-a830953eb803",
        "tags": '',
        "stack_name": "overcloud-Controller-d7iywdnu5uzr-2-evqysybsnrrt-NodeUserData-zmwd2rjmspal",
        "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
        "stack_status_reason": "Stack CREATE completed successfully",
        "creation_time": "2016-04-12T15:10:13",
        "links": [
          {
            "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Controller-d7iywdnu5uzr-2-evqysybsnrrt-NodeUserData-zmwd2rjmspal/446edf9a-cbe3-4714-a996-d07f41b18ea7",
            "rel": "self"
          }
        ],
        "capabilities": [],
        "notification_topics": [],
        "updated_time": '',
        "timeout_mins": 14400,
        "stack_status": "CREATE_COMPLETE",
        "stack_owner": "admin",
        "parameters": {
          "OS::project_id": "9de7e9a9a2a242718cffa65dae677a33",
          "OS::stack_id": "446edf9a-cbe3-4714-a996-d07f41b18ea7",
          "OS::stack_name": "overcloud-Controller-d7iywdnu5uzr-2-evqysybsnrrt-NodeUserData-zmwd2rjmspal"
        },
        "id": "446edf9a-cbe3-4714-a996-d07f41b18ea7",
        "outputs": [
          {
            "output_value": "11e7798a-9ed7-40f0-a4bc-8a567d7143cb",
            "description": "No description given",
            "output_key": "OS::stack_id"
          }
        ],
        "template_description": "This is a default no-op template which provides empty user-data which can be passed to the OS::Nova::Server resources. This template can be replaced with a different implementation via the resource registry, such that deployers may customize their first-boot configuration.\n"
      }
    },
    "overcloud-EndpointMap-5wrgqx6vxql2": {
      "description": "A map of OpenStack endpoints. Since the endpoints are URLs, we need to have brackets around IPv6 IP addresses. The inputs to these parameters come from net_ip_uri_map, which will include these brackets in IPv6 addresses.",
      "parent": "9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
      "stack_status_reason": "Stack CREATE completed successfully",
      "stack_name": "overcloud-EndpointMap-5wrgqx6vxql2",
      "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
      "tags": '',
      "creation_time": "2016-04-12T15:10:00",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-EndpointMap-5wrgqx6vxql2/93dede47-4221-4310-8685-032d788434fe",
          "rel": "self"
        }
      ],
      "updated_time": '',
      "stack_owner": "admin",
      "stack_status": "CREATE_COMPLETE",
      "id": "93dede47-4221-4310-8685-032d788434fe",
      "outputs": {
        "disable_rollback": 'true',
        "description": "A map of OpenStack endpoints. Since the endpoints are URLs, we need to have brackets around IPv6 IP addresses. The inputs to these parameters come from net_ip_uri_map, which will include these brackets in IPv6 addresses.",
        "parent": "9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
        "tags": '',
        "stack_name": "overcloud-EndpointMap-5wrgqx6vxql2",
        "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
        "stack_status_reason": "Stack CREATE completed successfully",
        "creation_time": "2016-04-12T15:10:00",
        "links": [
          {
            "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-EndpointMap-5wrgqx6vxql2/93dede47-4221-4310-8685-032d788434fe",
            "rel": "self"
          }
        ],
        "capabilities": [],
        "notification_topics": [],
        "updated_time": '',
        "timeout_mins": 240,
        "stack_status": "CREATE_COMPLETE",
        "stack_owner": "admin",
        "parameters": {
          "OS::project_id": "9de7e9a9a2a242718cffa65dae677a33",
          "OS::stack_id": "93dede47-4221-4310-8685-032d788434fe",
          "OS::stack_name": "overcloud-EndpointMap-5wrgqx6vxql2",
          "CloudName": "overcloud",
          "NeutronApiVirtualIP": "192.0.2.51",
          "GlanceRegistryVirtualIP": "192.0.2.51",
          "KeystonePublicApiVirtualIP": "192.0.2.51",
          "SwiftProxyVirtualIP": "192.0.2.51",
          "GlanceApiVirtualIP": "192.0.2.51",
          "HeatApiVirtualIP": "192.0.2.51",
          "NovaApiVirtualIP": "192.0.2.51",
          "PublicVirtualIP": "192.0.2.51",
          "KeystoneAdminApiVirtualIP": "192.0.2.51",
          "CinderApiVirtualIP": "192.0.2.51",
          "EndpointMap": "{u'GlanceInternal': {u'host': u'IP_ADDRESS', u'protocol': u'http', u'port': u'9292'}, u'NovaEC2Public': {u'host': u'IP_ADDRESS', u'protocol': u'http', u'port': u'8773'}, u'HeatPublic': {u'host': u'IP_ADDRESS', u'protocol': u'http', u'port': u'8004'}, u'KeystonePublic': {u'host': u'IP_ADDRESS', u'protocol': u'http', u'port': u'5000'}, u'NovaInternal': {u'host': u'IP_ADDRESS', u'protocol': u'http', u'port': u'8774'}, u'CeilometerAdmin': {u'host': u'IP_ADDRESS', u'protocol': u'http', u'port': u'8777'}, u'GlanceAdmin': {u'host': u'IP_ADDRESS', u'protocol': u'http', u'port': u'9292'}, u'NovaVNCProxyAdmin': {u'host': u'IP_ADDRESS', u'protocol': u'http', u'port': u'6080'}, u'HeatInternal': {u'host': u'IP_ADDRESS', u'protocol': u'http', u'port': u'8004'}, u'NeutronPublic': {u'host': u'IP_ADDRESS', u'protocol': u'http', u'port': u'9696'}, u'CinderPublic': {u'host': u'IP_ADDRESS', u'protocol': u'http', u'port': u'8776'}, u'HorizonPublic': {u'host': u'IP_ADDRESS', u'protocol': u'http', u'port': u'80'}, u'GlancePublic': {u'host': u'IP_ADDRESS', u'protocol': u'http', u'port': u'9292'}, u'NeutronAdmin': {u'host': u'IP_ADDRESS', u'protocol': u'http', u'port': u'9696'}, u'GlanceRegistryPublic': {u'host': u'IP_ADDRESS', u'protocol': u'http', u'port': u'9191'}, u'HeatAdmin': {u'host': u'IP_ADDRESS', u'protocol': u'http', u'port': u'8004'}, u'SwiftInternal': {u'host': u'IP_ADDRESS', u'protocol': u'http', u'port': u'8080'}, u'NovaVNCProxyPublic': {u'host': u'IP_ADDRESS', u'protocol': u'http', u'port': u'6080'}, u'CeilometerInternal': {u'host': u'IP_ADDRESS', u'protocol': u'http', u'port': u'8777'}, u'GlanceRegistryInternal': {u'host': u'IP_ADDRESS', u'protocol': u'http', u'port': u'9191'}, u'CeilometerPublic': {u'host': u'IP_ADDRESS', u'protocol': u'http', u'port': u'8777'}, u'NovaAdmin': {u'host': u'IP_ADDRESS', u'protocol': u'http', u'port': u'8774'}, u'NovaEC2Internal': {u'host': u'IP_ADDRESS', u'protocol': u'http', u'port': u'8773'}, u'SwiftAdmin': {u'host': u'IP_ADDRESS', u'protocol': u'http', u'port': u'8080'}, u'NeutronInternal': {u'host': u'IP_ADDRESS', u'protocol': u'http', u'port': u'9696'}, u'NovaPublic': {u'host': u'IP_ADDRESS', u'protocol': u'http', u'port': u'8774'}, u'NovaEC2Admin': {u'host': u'IP_ADDRESS', u'protocol': u'http', u'port': u'8773'}, u'KeystoneAdmin': {u'host': u'IP_ADDRESS', u'protocol': u'http', u'port': u'35357'}, u'GlanceRegistryAdmin': {u'host': u'IP_ADDRESS', u'protocol': u'http', u'port': u'9191'}, u'CinderInternal': {u'host': u'IP_ADDRESS', u'protocol': u'http', u'port': u'8776'}, u'SwiftPublic': {u'host': u'IP_ADDRESS', u'protocol': u'http', u'port': u'8080'}, u'CinderAdmin': {u'host': u'IP_ADDRESS', u'protocol': u'http', u'port': u'8776'}, u'NovaVNCProxyInternal': {u'host': u'IP_ADDRESS', u'protocol': u'http', u'port': u'6080'}, u'KeystoneInternal': {u'host': u'IP_ADDRESS', u'protocol': u'http', u'port': u'5000'}}",
          "MysqlVirtualIP": "192.0.2.51",
          "CeilometerApiVirtualIP": "192.0.2.51"
        },
        "id": "93dede47-4221-4310-8685-032d788434fe",
        "outputs": [
          {
            "output_value": {
              "GlanceInternal": {
                "port": "9292",
                "host": "192.0.2.51",
                "protocol": "http",
                "uri": "http://192.0.2.51:9292",
                "uri_no_suffix": "http://192.0.2.51:9292"
              },
              "NovaEC2Public": {
                "port": "8773",
                "host": "192.0.2.51",
                "protocol": "http",
                "uri": "http://192.0.2.51:8773/services/Cloud",
                "uri_no_suffix": "http://192.0.2.51:8773"
              },
              "HeatPublic": {
                "port": "8004",
                "host": "192.0.2.51",
                "protocol": "http",
                "uri": "http://192.0.2.51:8004/v1/%(tenant_id)s",
                "uri_no_suffix": "http://192.0.2.51:8004"
              },
              "CeilometerPublic": {
                "port": "8777",
                "host": "192.0.2.51",
                "protocol": "http",
                "uri": "http://192.0.2.51:8777",
                "uri_no_suffix": "http://192.0.2.51:8777"
              },
              "KeystonePublic": {
                "port": "5000",
                "host": "192.0.2.51",
                "protocol": "http",
                "uri": "http://192.0.2.51:5000/v2.0",
                "uri_no_suffix": "http://192.0.2.51:5000"
              },
              "NeutronAdmin": {
                "port": "9696",
                "host": "192.0.2.51",
                "protocol": "http",
                "uri": "http://192.0.2.51:9696",
                "uri_no_suffix": "http://192.0.2.51:9696"
              },
              "CeilometerAdmin": {
                "port": "8777",
                "host": "192.0.2.51",
                "protocol": "http",
                "uri": "http://192.0.2.51:8777",
                "uri_no_suffix": "http://192.0.2.51:8777"
              },
              "GlanceAdmin": {
                "port": "9292",
                "host": "192.0.2.51",
                "protocol": "http",
                "uri": "http://192.0.2.51:9292",
                "uri_no_suffix": "http://192.0.2.51:9292"
              },
              "SwiftInternal": {
                "port": "8080",
                "host": "192.0.2.51",
                "protocol": "http",
                "uri": "http://192.0.2.51:8080/v1/AUTH_%(tenant_id)s",
                "uri_no_suffix": "http://192.0.2.51:8080"
              },
              "CinderV2Internal": {
                "port": "8776",
                "host": "192.0.2.51",
                "protocol": "http",
                "uri": "http://192.0.2.51:8776/v2/%(tenant_id)s",
                "uri_no_suffix": "http://192.0.2.51:8776"
              },
              "NovaVNCProxyAdmin": {
                "port": "6080",
                "host": "192.0.2.51",
                "protocol": "http",
                "uri": "http://192.0.2.51:6080",
                "uri_no_suffix": "http://192.0.2.51:6080"
              },
              "HeatInternal": {
                "port": "8004",
                "host": "192.0.2.51",
                "protocol": "http",
                "uri": "http://192.0.2.51:8004/v1/%(tenant_id)s",
                "uri_no_suffix": "http://192.0.2.51:8004"
              },
              "NovaV3Admin": {
                "port": "8774",
                "host": "192.0.2.51",
                "protocol": "http",
                "uri": "http://192.0.2.51:8774/v3",
                "uri_no_suffix": "http://192.0.2.51:8774"
              },
              "NeutronPublic": {
                "port": "9696",
                "host": "192.0.2.51",
                "protocol": "http",
                "uri": "http://192.0.2.51:9696",
                "uri_no_suffix": "http://192.0.2.51:9696"
              },
              "CinderPublic": {
                "port": "8776",
                "host": "192.0.2.51",
                "protocol": "http",
                "uri": "http://192.0.2.51:8776/v1/%(tenant_id)s",
                "uri_no_suffix": "http://192.0.2.51:8776"
              },
              "HorizonPublic": {
                "port": "80",
                "host": "192.0.2.51",
                "protocol": "http",
                "uri": "http://192.0.2.51:80/dashboard",
                "uri_no_suffix": "http://192.0.2.51:80"
              },
              "KeystoneEC2": {
                "port": "5000",
                "host": "192.0.2.51",
                "protocol": "http",
                "uri": "http://192.0.2.51:5000/v2.0/ec2tokens",
                "uri_no_suffix": "http://192.0.2.51:5000"
              },
              "GlancePublic": {
                "port": "9292",
                "host": "192.0.2.51",
                "protocol": "http",
                "uri": "http://192.0.2.51:9292",
                "uri_no_suffix": "http://192.0.2.51:9292"
              },
              "CinderV2Admin": {
                "port": "8776",
                "host": "192.0.2.51",
                "protocol": "http",
                "uri": "http://192.0.2.51:8776/v2/%(tenant_id)s",
                "uri_no_suffix": "http://192.0.2.51:8776"
              },
              "GlanceRegistryPublic": {
                "port": "9191",
                "host": "192.0.2.51",
                "protocol": "http",
                "uri": "http://192.0.2.51:9191",
                "uri_no_suffix": "http://192.0.2.51:9191"
              },
              "HeatAdmin": {
                "port": "8004",
                "host": "192.0.2.51",
                "protocol": "http",
                "uri": "http://192.0.2.51:8004/v1/%(tenant_id)s",
                "uri_no_suffix": "http://192.0.2.51:8004"
              },
              "SwiftS3Internal": {
                "port": "8080",
                "host": "192.0.2.51",
                "protocol": "http",
                "uri": "http://192.0.2.51:8080",
                "uri_no_suffix": "http://192.0.2.51:8080"
              },
              "NovaVNCProxyPublic": {
                "port": "6080",
                "host": "192.0.2.51",
                "protocol": "http",
                "uri": "http://192.0.2.51:6080",
                "uri_no_suffix": "http://192.0.2.51:6080"
              },
              "CeilometerInternal": {
                "port": "8777",
                "host": "192.0.2.51",
                "protocol": "http",
                "uri": "http://192.0.2.51:8777",
                "uri_no_suffix": "http://192.0.2.51:8777"
              },
              "NovaInternal": {
                "port": "8774",
                "host": "192.0.2.51",
                "protocol": "http",
                "uri": "http://192.0.2.51:8774/v2.1/%(tenant_id)s",
                "uri_no_suffix": "http://192.0.2.51:8774"
              },
              "GlanceRegistryInternal": {
                "port": "9191",
                "host": "192.0.2.51",
                "protocol": "http",
                "uri": "http://192.0.2.51:9191",
                "uri_no_suffix": "http://192.0.2.51:9191"
              },
              "NovaV3Internal": {
                "port": "8774",
                "host": "192.0.2.51",
                "protocol": "http",
                "uri": "http://192.0.2.51:8774/v3",
                "uri_no_suffix": "http://192.0.2.51:8774"
              },
              "NovaAdmin": {
                "port": "8774",
                "host": "192.0.2.51",
                "protocol": "http",
                "uri": "http://192.0.2.51:8774/v2.1/%(tenant_id)s",
                "uri_no_suffix": "http://192.0.2.51:8774"
              },
              "NovaEC2Internal": {
                "port": "8773",
                "host": "192.0.2.51",
                "protocol": "http",
                "uri": "http://192.0.2.51:8773/services/Cloud",
                "uri_no_suffix": "http://192.0.2.51:8773"
              },
              "SwiftAdmin": {
                "port": "8080",
                "host": "192.0.2.51",
                "protocol": "http",
                "uri": "http://192.0.2.51:8080",
                "uri_no_suffix": "http://192.0.2.51:8080"
              },
              "NeutronInternal": {
                "port": "9696",
                "host": "192.0.2.51",
                "protocol": "http",
                "uri": "http://192.0.2.51:9696",
                "uri_no_suffix": "http://192.0.2.51:9696"
              },
              "NovaPublic": {
                "port": "8774",
                "host": "192.0.2.51",
                "protocol": "http",
                "uri": "http://192.0.2.51:8774/v2.1/%(tenant_id)s",
                "uri_no_suffix": "http://192.0.2.51:8774"
              },
              "SwiftS3Admin": {
                "port": "8080",
                "host": "192.0.2.51",
                "protocol": "http",
                "uri": "http://192.0.2.51:8080",
                "uri_no_suffix": "http://192.0.2.51:8080"
              },
              "NovaEC2Admin": {
                "port": "8773",
                "host": "192.0.2.51",
                "protocol": "http",
                "uri": "http://192.0.2.51:8773/services/Admin",
                "uri_no_suffix": "http://192.0.2.51:8773"
              },
              "CinderV2Public": {
                "port": "8776",
                "host": "192.0.2.51",
                "protocol": "http",
                "uri": "http://192.0.2.51:8776/v2/%(tenant_id)s",
                "uri_no_suffix": "http://192.0.2.51:8776"
              },
              "KeystoneAdmin": {
                "port": "35357",
                "host": "192.0.2.51",
                "protocol": "http",
                "uri": "http://192.0.2.51:35357/v2.0",
                "uri_no_suffix": "http://192.0.2.51:35357"
              },
              "GlanceRegistryAdmin": {
                "port": "9191",
                "host": "192.0.2.51",
                "protocol": "http",
                "uri": "http://192.0.2.51:9191",
                "uri_no_suffix": "http://192.0.2.51:9191"
              },
              "CinderInternal": {
                "port": "8776",
                "host": "192.0.2.51",
                "protocol": "http",
                "uri": "http://192.0.2.51:8776/v1/%(tenant_id)s",
                "uri_no_suffix": "http://192.0.2.51:8776"
              },
              "SwiftS3Public": {
                "port": "8080",
                "host": "192.0.2.51",
                "protocol": "http",
                "uri": "http://192.0.2.51:8080",
                "uri_no_suffix": "http://192.0.2.51:8080"
              },
              "NovaV3Public": {
                "port": "8774",
                "host": "192.0.2.51",
                "protocol": "http",
                "uri": "http://192.0.2.51:8774/v3",
                "uri_no_suffix": "http://192.0.2.51:8774"
              },
              "SwiftPublic": {
                "port": "8080",
                "host": "192.0.2.51",
                "protocol": "http",
                "uri": "http://192.0.2.51:8080/v1/AUTH_%(tenant_id)s",
                "uri_no_suffix": "http://192.0.2.51:8080"
              },
              "KeystoneInternal": {
                "port": "5000",
                "host": "192.0.2.51",
                "protocol": "http",
                "uri": "http://192.0.2.51:5000/v2.0",
                "uri_no_suffix": "http://192.0.2.51:5000"
              },
              "NovaVNCProxyInternal": {
                "port": "6080",
                "host": "192.0.2.51",
                "protocol": "http",
                "uri": "http://192.0.2.51:6080",
                "uri_no_suffix": "http://192.0.2.51:6080"
              },
              "CinderAdmin": {
                "port": "8776",
                "host": "192.0.2.51",
                "protocol": "http",
                "uri": "http://192.0.2.51:8776/v1/%(tenant_id)s",
                "uri_no_suffix": "http://192.0.2.51:8776"
              }
            },
            "description": "No description given",
            "output_key": "endpoint_map"
          }
        ],
        "template_description": "A map of OpenStack endpoints. Since the endpoints are URLs, we need to have brackets around IPv6 IP addresses. The inputs to these parameters come from net_ip_uri_map, which will include these brackets in IPv6 addresses."
      }
    },
    "overcloud-Controller-d7iywdnu5uzr-1-klhc6fwkxjt3": {
      "description": "OpenStack controller node configured by Puppet.\n",
      "parent": "119696b0-92ac-44ab-85d6-614c68af3949",
      "stack_status_reason": "Resource CREATE failed: ResourceInError: resources.Controller: Went to status ERROR due to \"Message: No valid host was found. There are not enough hosts available., Code: 500\"",
      "stack_name": "overcloud-Controller-d7iywdnu5uzr-1-klhc6fwkxjt3",
      "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
      "tags": '',
      "creation_time": "2016-04-12T15:10:07",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Controller-d7iywdnu5uzr-1-klhc6fwkxjt3/7ecb0624-6a40-449e-bb6c-e85b8bf2b733",
          "rel": "self"
        }
      ],
      "updated_time": '',
      "stack_owner": "admin",
      "stack_status": "CREATE_FAILED",
      "id": "7ecb0624-6a40-449e-bb6c-e85b8bf2b733",
      "outputs": {
        "disable_rollback": 'true',
        "description": "OpenStack controller node configured by Puppet.\n",
        "parent": "119696b0-92ac-44ab-85d6-614c68af3949",
        "tags": '',
        "stack_name": "overcloud-Controller-d7iywdnu5uzr-1-klhc6fwkxjt3",
        "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
        "stack_status_reason": "Resource CREATE failed: ResourceInError: resources.Controller: Went to status ERROR due to \"Message: No valid host was found. There are not enough hosts available., Code: 500\"",
        "creation_time": "2016-04-12T15:10:07",
        "links": [
          {
            "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Controller-d7iywdnu5uzr-1-klhc6fwkxjt3/7ecb0624-6a40-449e-bb6c-e85b8bf2b733",
            "rel": "self"
          }
        ],
        "capabilities": [],
        "notification_topics": [],
        "updated_time": '',
        "timeout_mins": 14400,
        "stack_status": "CREATE_FAILED",
        "stack_owner": "admin",
        "parameters": {
          "EnableCephStorage": "False",
          "NeutronPublicInterfaceRawDevice": "",
          "GlanceWorkers": "0",
          "NetworkDeploymentActions": "[u'CREATE']",
          "NtpServer": "[u'north-america.pool.ntp.org']",
          "NeutronTenantMtu": "1400",
          "NeutronDhcpAgentsPerNetwork": "3",
          "HeatApiVirtualIPUri": "192.0.2.51",
          "NeutronFlatNetworks": "[u'datacentre']",
          "EnablePackageInstall": "False",
          "CorosyncIPv6": "False",
          "NeutronAgentMode": "dvr_snat",
          "GlancePassword": "******",
          "NeutronTunnelIdRanges": "[u'1:4094']",
          "CinderEnableRbdBackend": "False",
          "SwiftReplicas": "3",
          "NeutronPublicInterfaceTag": "",
          "FencingConfig": "{}",
          "MemcachedIPv6": "False",
          "KeystoneSigningCertificate": "-----BEGIN CERTIFICATE-----\nMIIDJDCCAgygAwIBAgIBAjANBgkqhkiG9w0BAQUFADBTMQswCQYDVQQGEwJYWDEO\nMAwGA1UECBMFVW5zZXQxDjAMBgNVBAcTBVVuc2V0MQ4wDAYDVQQKEwVVbnNldDEU\nMBIGA1UEAxMLS2V5c3RvbmUgQ0EwHhcNMTYwNDEyMTUwOTQzWhcNMjYwNDEwMTUw\nOTQzWjBYMQswCQYDVQQGEwJYWDEOMAwGA1UECBMFVW5zZXQxDjAMBgNVBAcTBVVu\nc2V0MQ4wDAYDVQQKEwVVbnNldDEZMBcGA1UEAxMQS2V5c3RvbmUgU2lnbmluZzCC\nASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBALqFj/1OTcqwfAfkXnm9XYJ0\nk85O+JGDfWuygeS8GBP99G6FMf/xPb3DeJTzEbm2xnVn3oLyBx9eNHg28Pz+B1me\n1zJJNmNTHYY22gQ9QTNuo/2fnyehzlIB7mzeWIqbuWaeabg3FI8ujfN9l2/jxw5c\nnscakOU1/NKQOcjXgIBP7jr9l9vfLQOvZ4oPeYwkAn0li9xYhpVE70fsvE57J1JC\nr/WkL6ExZCJA78+PC5Oq1WGB86fUCSdoT0H0uDuiOgsohfFBpaL0MAXO//+L2q+Y\nsZGcgVqgPaMW97vP3dedIMYkxHbQgVUwKHUGbL9GvIrkCzmPx0z4AqbeadpyMzUC\nAwEAATANBgkqhkiG9w0BAQUFAAOCAQEAj6loZnn6GlHqpJL34es9+AT6yLaKq6py\nQtnMl3uypwO1u7opMxS0Vhluw/IpWtaiRIlfboJ9IhrDcZm6rMtn/sjoB2XbLnGI\n9v3BSj+0lGyTrP8tV4FEFrKXG46SqcU3KeHlfk5mL3JB7XzOsPE4V+IcabPg/cKt\negXPAqKOzIGKc8fbGm/q7eMI+NtP4sKgIPJOxneMKYbcHcq6sY3UmiXVMYJ1PItD\n/tE2x2tVotnnYoU1SV9wPgkfGNY2xxdO31+DgzhNA45M/31PLm98LO1U7DpiAxLu\n/tEbVyspUJkUSEmQfhQ9LoHuX4BLObJU7ZoqHzA9xFmg3e0HwAfRqA==\n-----END CERTIFICATE-----\n",
          "ControllerIPs": "{}",
          "ServiceNetMap": "{u'NovaVncProxyNetwork': u'internal_api', u'CinderApiNetwork': u'internal_api', u'NovaApiNetwork': u'internal_api', u'CeilometerApiNetwork': u'internal_api', u'CephStorageHostnameResolveNetwork': u'storage', u'SwiftMgmtNetwork': u'storage_mgmt', u'MemcachedNetwork': u'internal_api', u'RabbitMqNetwork': u'internal_api', u'KeystoneAdminApiNetwork': u'ctlplane', u'SwiftProxyNetwork': u'storage', u'NeutronTenantNetwork': u'tenant', u'CephClusterNetwork': u'storage_mgmt', u'NovaMetadataNetwork': u'internal_api', u'ControllerHostnameResolveNetwork': u'internal_api', u'NeutronApiNetwork': u'internal_api', u'GlanceApiNetwork': u'storage', u'ObjectStorageHostnameResolveNetwork': u'internal_api', u'KeystonePublicApiNetwork': u'internal_api', u'HeatApiNetwork': u'internal_api', u'GlanceRegistryNetwork': u'internal_api', u'RedisNetwork': u'internal_api', u'MysqlNetwork': u'internal_api', u'BlockStorageHostnameResolveNetwork': u'internal_api', u'ComputeHostnameResolveNetwork': u'internal_api', u'CephPublicNetwork': u'storage', u'MongoDbNetwork': u'internal_api', u'HorizonNetwork': u'internal_api', u'CinderIscsiNetwork': u'storage'}",
          "SnmpdReadonlyUserName": "ro_snmp_user",
          "ManageFirewall": "False",
          "CinderISCSIHelper": "lioadm",
          "CeilometerWorkers": "0",
          "NeutronEnableMetadataAgent": "True",
          "RabbitPassword": "******",
          "NeutronApiVirtualIP": "192.0.2.51",
          "PublicVirtualInterface": "br-ex",
          "Debug": "",
          "NeutronPublicInterface": "nic1",
          "GlanceFilePcmkDevice": "",
          "EnableFencing": "False",
          "SoftwareConfigTransport": "POLL_SERVER_CFN",
          "SwiftMountCheck": "False",
          "RabbitFDLimit": "16384",
          "HorizonSecret": "******",
          "VirtualIP": "192.0.2.51",
          "SwiftPassword": "******",
          "NeutronMetadataProxySharedSecret": "******",
          "Flavor": "control",
          "CinderApiVirtualIP": "192.0.2.51",
          "KeystonePublicApiVirtualIP": "192.0.2.51",
          "HAProxySyslogAddress": "/dev/log",
          "SwiftPartPower": "10",
          "HeatApiVirtualIP": "192.0.2.51",
          "KeystoneNotificationFormat": "basic",
          "NeutronPublicInterfaceDefaultRoute": "",
          "HeatPassword": "******",
          "InstanceNameTemplate": "instance-%08x",
          "RedisVirtualIP": "192.0.2.52",
          "ControllerExtraConfig": "{}",
          "ControlVirtualInterface": "br-ex",
          "HeatStackDomainAdminPassword": "******",
          "OS::stack_name": "overcloud-Controller-d7iywdnu5uzr-1-klhc6fwkxjt3",
          "NeutronEnableOVSAgent": "True",
          "GlanceRegistryVirtualIP": "192.0.2.51",
          "PcsdPassword": "******",
          "SwiftWorkers": "0",
          "CinderEnableIscsiBackend": "True",
          "EnableLoadBalancer": "True",
          "KeystoneNotificationDriver": "[u'messaging']",
          "NeutronEnableL3Agent": "True",
          "NeutronVniRanges": "[u'1:4094']",
          "GlanceBackend": "swift",
          "RabbitClientUseSSL": "False",
          "NeutronAllowL3AgentFailover": "False",
          "NeutronEnableL2Pop": "False",
          "HeatAuthEncryptionKey": "******",
          "UpgradeLevelNovaCompute": "",
          "GlanceFilePcmkOptions": "",
          "RabbitUserName": "guest",
          "NovaApiVirtualIP": "192.0.2.51",
          "HeatWorkers": "0",
          "GlanceLogFile": "",
          "NeutronExternalNetworkBridge": "br-ex",
          "CeilometerBackend": "mongodb",
          "CeilometerApiVirtualIP": "192.0.2.51",
          "OS::stack_id": "7ecb0624-6a40-449e-bb6c-e85b8bf2b733",
          "AdminPassword": "******",
          "NeutronDVR": "False",
          "Image": "overcloud-full",
          "ExtraConfig": "{}",
          "KeystoneSigningKey": "******",
          "KeystoneEnableDBPurge": "True",
          "CinderEnableDBPurge": "True",
          "NeutronDnsmasqOptions": "dhcp-option-force=26,1400",
          "MysqlMaxConnections": "4096",
          "NeutronTunnelTypes": "[u'vxlan']",
          "ServerMetadata": "{}",
          "Hostname": "overcloud-controller-1",
          "GlanceFilePcmkManage": "False",
          "NeutronPassword": "******",
          "NeutronBridgeMappings": "[u'datacentre:br-ex']",
          "HAProxyStatsUser": "admin",
          "EndpointMap": "{u'GlanceInternal': {u'uri_no_suffix': u'http://192.0.2.51:9292', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'9292', u'uri': u'http://192.0.2.51:9292'}, u'NovaEC2Public': {u'uri_no_suffix': u'http://192.0.2.51:8773', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8773', u'uri': u'http://192.0.2.51:8773/services/Cloud'}, u'HeatPublic': {u'uri_no_suffix': u'http://192.0.2.51:8004', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8004', u'uri': u'http://192.0.2.51:8004/v1/%(tenant_id)s'}, u'KeystonePublic': {u'uri_no_suffix': u'http://192.0.2.51:5000', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'5000', u'uri': u'http://192.0.2.51:5000/v2.0'}, u'HeatAdmin': {u'uri_no_suffix': u'http://192.0.2.51:8004', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8004', u'uri': u'http://192.0.2.51:8004/v1/%(tenant_id)s'}, u'NovaEC2Admin': {u'uri_no_suffix': u'http://192.0.2.51:8773', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8773', u'uri': u'http://192.0.2.51:8773/services/Admin'}, u'CeilometerAdmin': {u'uri_no_suffix': u'http://192.0.2.51:8777', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8777', u'uri': u'http://192.0.2.51:8777'}, u'GlanceAdmin': {u'uri_no_suffix': u'http://192.0.2.51:9292', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'9292', u'uri': u'http://192.0.2.51:9292'}, u'SwiftS3Internal': {u'uri_no_suffix': u'http://192.0.2.51:8080', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8080', u'uri': u'http://192.0.2.51:8080'}, u'CinderV2Internal': {u'uri_no_suffix': u'http://192.0.2.51:8776', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8776', u'uri': u'http://192.0.2.51:8776/v2/%(tenant_id)s'}, u'NovaVNCProxyAdmin': {u'uri_no_suffix': u'http://192.0.2.51:6080', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'6080', u'uri': u'http://192.0.2.51:6080'}, u'HeatInternal': {u'uri_no_suffix': u'http://192.0.2.51:8004', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8004', u'uri': u'http://192.0.2.51:8004/v1/%(tenant_id)s'}, u'NovaV3Admin': {u'uri_no_suffix': u'http://192.0.2.51:8774', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8774', u'uri': u'http://192.0.2.51:8774/v3'}, u'NeutronPublic': {u'uri_no_suffix': u'http://192.0.2.51:9696', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'9696', u'uri': u'http://192.0.2.51:9696'}, u'CinderPublic': {u'uri_no_suffix': u'http://192.0.2.51:8776', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8776', u'uri': u'http://192.0.2.51:8776/v1/%(tenant_id)s'}, u'HorizonPublic': {u'uri_no_suffix': u'http://192.0.2.51:80', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'80', u'uri': u'http://192.0.2.51:80/dashboard'}, u'KeystoneEC2': {u'uri_no_suffix': u'http://192.0.2.51:5000', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'5000', u'uri': u'http://192.0.2.51:5000/v2.0/ec2tokens'}, u'GlancePublic': {u'uri_no_suffix': u'http://192.0.2.51:9292', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'9292', u'uri': u'http://192.0.2.51:9292'}, u'CinderV2Admin': {u'uri_no_suffix': u'http://192.0.2.51:8776', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8776', u'uri': u'http://192.0.2.51:8776/v2/%(tenant_id)s'}, u'GlanceRegistryPublic': {u'uri_no_suffix': u'http://192.0.2.51:9191', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'9191', u'uri': u'http://192.0.2.51:9191'}, u'NeutronAdmin': {u'uri_no_suffix': u'http://192.0.2.51:9696', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'9696', u'uri': u'http://192.0.2.51:9696'}, u'SwiftInternal': {u'uri_no_suffix': u'http://192.0.2.51:8080', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8080', u'uri': u'http://192.0.2.51:8080/v1/AUTH_%(tenant_id)s'}, u'NovaVNCProxyPublic': {u'uri_no_suffix': u'http://192.0.2.51:6080', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'6080', u'uri': u'http://192.0.2.51:6080'}, u'CeilometerInternal': {u'uri_no_suffix': u'http://192.0.2.51:8777', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8777', u'uri': u'http://192.0.2.51:8777'}, u'NovaInternal': {u'uri_no_suffix': u'http://192.0.2.51:8774', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8774', u'uri': u'http://192.0.2.51:8774/v2.1/%(tenant_id)s'}, u'GlanceRegistryInternal': {u'uri_no_suffix': u'http://192.0.2.51:9191', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'9191', u'uri': u'http://192.0.2.51:9191'}, u'NovaV3Internal': {u'uri_no_suffix': u'http://192.0.2.51:8774', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8774', u'uri': u'http://192.0.2.51:8774/v3'}, u'NovaAdmin': {u'uri_no_suffix': u'http://192.0.2.51:8774', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8774', u'uri': u'http://192.0.2.51:8774/v2.1/%(tenant_id)s'}, u'NovaEC2Internal': {u'uri_no_suffix': u'http://192.0.2.51:8773', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8773', u'uri': u'http://192.0.2.51:8773/services/Cloud'}, u'SwiftAdmin': {u'uri_no_suffix': u'http://192.0.2.51:8080', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8080', u'uri': u'http://192.0.2.51:8080'}, u'NeutronInternal': {u'uri_no_suffix': u'http://192.0.2.51:9696', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'9696', u'uri': u'http://192.0.2.51:9696'}, u'NovaPublic': {u'uri_no_suffix': u'http://192.0.2.51:8774', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8774', u'uri': u'http://192.0.2.51:8774/v2.1/%(tenant_id)s'}, u'SwiftS3Admin': {u'uri_no_suffix': u'http://192.0.2.51:8080', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8080', u'uri': u'http://192.0.2.51:8080'}, u'CeilometerPublic': {u'uri_no_suffix': u'http://192.0.2.51:8777', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8777', u'uri': u'http://192.0.2.51:8777'}, u'CinderV2Public': {u'uri_no_suffix': u'http://192.0.2.51:8776', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8776', u'uri': u'http://192.0.2.51:8776/v2/%(tenant_id)s'}, u'KeystoneAdmin': {u'uri_no_suffix': u'http://192.0.2.51:35357', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'35357', u'uri': u'http://192.0.2.51:35357/v2.0'}, u'GlanceRegistryAdmin': {u'uri_no_suffix': u'http://192.0.2.51:9191', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'9191', u'uri': u'http://192.0.2.51:9191'}, u'CinderInternal': {u'uri_no_suffix': u'http://192.0.2.51:8776', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8776', u'uri': u'http://192.0.2.51:8776/v1/%(tenant_id)s'}, u'SwiftS3Public': {u'uri_no_suffix': u'http://192.0.2.51:8080', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8080', u'uri': u'http://192.0.2.51:8080'}, u'NovaV3Public': {u'uri_no_suffix': u'http://192.0.2.51:8774', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8774', u'uri': u'http://192.0.2.51:8774/v3'}, u'SwiftPublic': {u'uri_no_suffix': u'http://192.0.2.51:8080', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8080', u'uri': u'http://192.0.2.51:8080/v1/AUTH_%(tenant_id)s'}, u'CinderAdmin': {u'uri_no_suffix': u'http://192.0.2.51:8776', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8776', u'uri': u'http://192.0.2.51:8776/v1/%(tenant_id)s'}, u'NovaVNCProxyInternal': {u'uri_no_suffix': u'http://192.0.2.51:6080', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'6080', u'uri': u'http://192.0.2.51:6080'}, u'KeystoneInternal': {u'uri_no_suffix': u'http://192.0.2.51:5000', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'5000', u'uri': u'http://192.0.2.51:5000/v2.0'}}",
          "NeutronEnableIsolatedMetadata": "False",
          "PurgeFirewallRules": "False",
          "NeutronEnableTunnelling": "True",
          "GlanceFilePcmkFstype": "nfs",
          "RabbitCookie": "******",
          "KeyName": "default",
          "MysqlRootPassword": "******",
          "MysqlClusterUniquePart": "24V843Vtte",
          "CinderPassword": "******",
          "NeutronTypeDrivers": "[u'vxlan', u'vlan', u'flat', u'gre']",
          "NodeIndex": "1",
          "CinderLVMLoopDeviceSize": "10280",
          "SwiftRingBuild": "True",
          "SchedulerHints": "{}",
          "CinderNfsServers": "[]",
          "ImageUpdatePolicy": "REBUILD_PRESERVE_EPHEMERAL",
          "MysqlInnodbBufferPoolSize": "0",
          "NeutronPluginExtensions": "[u'qos', u'port_security']",
          "RedisVirtualIPUri": "192.0.2.52",
          "AdminToken": "******",
          "SwiftHashSuffix": "******",
          "SwiftMinPartHours": "1",
          "KeystoneSSLCertificate": "",
          "NeutronL3HA": "True",
          "EnableGalera": "True",
          "MongoDbNoJournal": "False",
          "NeutronCorePlugin": "ml2",
          "CinderWorkers": "0",
          "CeilometerMeteringSecret": "******",
          "CinderEnableNfsBackend": "False",
          "HostnameMap": "{}",
          "MongoDbIPv6": "False",
          "OS::project_id": "9de7e9a9a2a242718cffa65dae677a33",
          "EnableSwiftStorage": "True",
          "PublicVirtualIP": "192.0.2.51",
          "NeutronEnableDHCPAgent": "True",
          "SnmpdReadonlyUserPassword": "******",
          "TimeZone": "UTC",
          "HorizonAllowedHosts": "[u'*']",
          "MysqlVirtualIP": "192.0.2.51",
          "NovaEnableDBPurge": "True",
          "RabbitClientPort": "5672",
          "SwiftProxyVirtualIP": "192.0.2.51",
          "KeystoneSSLCertificateKey": "******",
          "GlanceApiVirtualIP": "192.0.2.51",
          "KeystoneAdminApiVirtualIP": "192.0.2.51",
          "NeutronNetworkType": "[u'vxlan']",
          "CeilometerPassword": "******",
          "CinderBackendConfig": "{}",
          "NeutronMechanismDrivers": "[u'openvswitch']",
          "CeilometerStoreEvents": "False",
          "GlanceNotifierStrategy": "noop",
          "NeutronWorkers": "0",
          "MysqlVirtualIPUri": "192.0.2.51",
          "KeystoneCACertificate": "-----BEGIN CERTIFICATE-----\nMIIDNzCCAh+gAwIBAgIBATANBgkqhkiG9w0BAQUFADBTMQswCQYDVQQGEwJYWDEO\nMAwGA1UECBMFVW5zZXQxDjAMBgNVBAcTBVVuc2V0MQ4wDAYDVQQKEwVVbnNldDEU\nMBIGA1UEAxMLS2V5c3RvbmUgQ0EwHhcNMTYwNDEyMTUwOTQzWhcNMjYwNDEwMTUw\nOTQzWjBTMQswCQYDVQQGEwJYWDEOMAwGA1UECBMFVW5zZXQxDjAMBgNVBAcTBVVu\nc2V0MQ4wDAYDVQQKEwVVbnNldDEUMBIGA1UEAxMLS2V5c3RvbmUgQ0EwggEiMA0G\nCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQC1qd7Dvdrp0vw00HWxjqtCfqLS+/Oa\nr3ODws1I6TeaaBDGfrsvhQsGIEV2HXHw5XvZa5l6JgbbH+zcCiescMdIz6BkxrrG\n0bssq9eP7M9JPW1Ezo6LkMwPJiBpGWtw2EZ9pfIBH7AMR/cmweWmDi09sWy4O9q+\npB28luSmeSshqJZ6S1L6pqWdPQcvNFwpRFgZr3rRbyvVKS76GABMS30CGbT0h8Fj\nWwzGN1nCeSvTOHGvnOC714E81XApOViPz/ysrAc591mK5JORsFOXkH27OTMiWC9t\nb9lJQ7LZAU9EIywokLmPaW8wG+DCwgQs9KbHFOG2S7LfMhE/+Sh5L8n3AgMBAAGj\nFjAUMBIGA1UdEwEB/wQIMAYBAf8CAQAwDQYJKoZIhvcNAQEFBQADggEBAInsYCil\newgy2kwq4ArR3bHC7b5jYo/9SKylrsDrgUb38/iQZei3wooa2V+l1SbkznahwpI5\nqAqywzT8o9d8/LUji1631H3fuyCTb4UHX3SE/iw2UVmFVyWw0AMkj3gDJ9iVw8rR\nUvSwbdNySGZNl8BwETObLR4gyIpIY5Kq2ztitaxIg1xMlkDAe66trzCunt8Kt2Os\n8m3ObKr8TXbQMA6v01FigaipNjxXDyHPGv1S14PvQiguX6CiD02L5eXPjoJfLlOC\n/MjeK2f2YxvPf/BKUWbvekQApcCGayPpuiPM0z5oam1KDVsNMAAEE6a7UyAZs2NT\niEqras+fEAFIy3I=\n-----END CERTIFICATE-----\n",
          "NovaWorkers": "0",
          "NovaPassword": "******",
          "CloudDomain": "localdomain",
          "CinderNfsMountOptions": "",
          "RedisPassword": "******",
          "NeutronPublicInterfaceIP": "",
          "NovaIPv6": "False",
          "KeystoneWorkers": "0",
          "HAProxyStatsPassword": "zRe2ynBbCdjwYFPjyj6m2wUWQ",
          "NeutronServicePlugins": "[u'router', u'qos']",
          "NeutronAgentExtensions": "[u'qos']",
          "UpdateIdentifier": "",
          "HeatEnableDBPurge": "True",
          "RabbitIPv6": "False",
          "NeutronNetworkVLANRanges": "[u'datacentre:1:1000']"
        },
        "id": "7ecb0624-6a40-449e-bb6c-e85b8bf2b733",
        "outputs": [
          {
            "output_value": '',
            "description": "IP address of the server in the storage_mgmt network",
            "output_key": "storage_mgmt_ip_address"
          },
          {
            "output_value": '',
            "description": "MD5 checksum of the TLS Certificate Modulus",
            "output_key": "tls_cert_modulus_md5"
          },
          {
            "output_value": '',
            "description": "IP address of the server in the storage network",
            "output_key": "storage_ip_address"
          },
          {
            "output_value": '',
            "description": "MD5 checksum of the TLS Key Modulus",
            "output_key": "tls_key_modulus_md5"
          },
          {
            "output_value": ",,,,",
            "description": "identifier which changes if the controller configuration may need re-applying",
            "output_key": "config_identifier"
          },
          {
            "output_value": '',
            "description": "Hostname of the server",
            "output_key": "hostname"
          },
          {
            "output_value": '',
            "description": "IP address of the server in the tenant network",
            "output_key": "tenant_ip_address"
          },
          {
            "output_value": '',
            "description": "IP address of the server in the external network",
            "output_key": "external_ip_address"
          },
          {
            "output_value": "r1z1-:%PORT%/d1",
            "description": "Swift device formatted for swift-ring-builder",
            "output_key": "swift_device"
          },
          {
            "output_value": {
              "ip": '',
              "name": ''
            },
            "description": "Node object in the format {ip: ..., name: ...} format that the corosync element expects\n",
            "output_key": "corosync_node"
          },
          {
            "output_value": " .localdomain ",
            "description": "Server's IP address and hostname in the /etc/hosts format\n",
            "output_key": "hosts_entry"
          },
          {
            "output_value": ":11211",
            "description": "Swift proxy-memcache value",
            "output_key": "swift_proxy_memcache"
          },
          {
            "output_value": "f94ae27a-f3eb-445a-bcdb-8fcaf15c145e",
            "description": "Heat resource handle for the Nova compute server",
            "output_key": "nova_server_resource"
          },
          {
            "output_value": '',
            "description": "IP address of the server in the internal_api network",
            "output_key": "internal_api_ip_address"
          },
          {
            "output_value": '',
            "description": "IP address of the server in the ctlplane network",
            "output_key": "ip_address"
          },
          {
            "output_value": '',
            "description": "IP address of the server in the management network",
            "output_key": "management_ip_address"
          }
        ],
        "template_description": "OpenStack controller node configured by Puppet.\n"
      }
    },
    "overcloud-Networks-zyubznagvv6c-InternalNetwork-cafng6vxx6bp": {
      "description": "A stack which creates no network(s).",
      "parent": "bfb0f40b-3c67-4e65-8517-6cff9dfab7ff",
      "stack_status_reason": "Stack CREATE completed successfully",
      "stack_name": "overcloud-Networks-zyubznagvv6c-InternalNetwork-cafng6vxx6bp",
      "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
      "tags": '',
      "creation_time": "2016-04-12T15:09:49",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Networks-zyubznagvv6c-InternalNetwork-cafng6vxx6bp/c207d1a9-b433-4fee-966d-14488e4d6016",
          "rel": "self"
        }
      ],
      "updated_time": '',
      "stack_owner": "admin",
      "stack_status": "CREATE_COMPLETE",
      "id": "c207d1a9-b433-4fee-966d-14488e4d6016",
      "outputs": {
        "disable_rollback": 'true',
        "description": "A stack which creates no network(s).",
        "parent": "bfb0f40b-3c67-4e65-8517-6cff9dfab7ff",
        "tags": '',
        "stack_name": "overcloud-Networks-zyubznagvv6c-InternalNetwork-cafng6vxx6bp",
        "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
        "stack_status_reason": "Stack CREATE completed successfully",
        "creation_time": "2016-04-12T15:09:49",
        "links": [
          {
            "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Networks-zyubznagvv6c-InternalNetwork-cafng6vxx6bp/c207d1a9-b433-4fee-966d-14488e4d6016",
            "rel": "self"
          }
        ],
        "capabilities": [],
        "notification_topics": [],
        "updated_time": '',
        "timeout_mins": 240,
        "stack_status": "CREATE_COMPLETE",
        "stack_owner": "admin",
        "parameters": {
          "OS::project_id": "9de7e9a9a2a242718cffa65dae677a33",
          "OS::stack_id": "c207d1a9-b433-4fee-966d-14488e4d6016",
          "OS::stack_name": "overcloud-Networks-zyubznagvv6c-InternalNetwork-cafng6vxx6bp"
        },
        "id": "c207d1a9-b433-4fee-966d-14488e4d6016",
        "outputs": [],
        "template_description": "A stack which creates no network(s)."
      }
    },
    "overcloud-Controller-d7iywdnu5uzr-0-j7rh7d75pr77-UpdateConfig-ziuftbxwxiqx": {
      "description": "Software-config for performing package updates using yum\n",
      "parent": "04299fe4-e771-425d-9e2b-4ceca3458de1",
      "stack_status_reason": "Stack CREATE completed successfully",
      "stack_name": "overcloud-Controller-d7iywdnu5uzr-0-j7rh7d75pr77-UpdateConfig-ziuftbxwxiqx",
      "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
      "tags": '',
      "creation_time": "2016-04-12T15:10:10",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Controller-d7iywdnu5uzr-0-j7rh7d75pr77-UpdateConfig-ziuftbxwxiqx/c8244467-ef13-47f9-8282-79e92de5c9ee",
          "rel": "self"
        }
      ],
      "updated_time": '',
      "stack_owner": "admin",
      "stack_status": "CREATE_COMPLETE",
      "id": "c8244467-ef13-47f9-8282-79e92de5c9ee",
      "outputs": {
        "disable_rollback": 'true',
        "description": "Software-config for performing package updates using yum\n",
        "parent": "04299fe4-e771-425d-9e2b-4ceca3458de1",
        "tags": '',
        "stack_name": "overcloud-Controller-d7iywdnu5uzr-0-j7rh7d75pr77-UpdateConfig-ziuftbxwxiqx",
        "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
        "stack_status_reason": "Stack CREATE completed successfully",
        "creation_time": "2016-04-12T15:10:10",
        "links": [
          {
            "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Controller-d7iywdnu5uzr-0-j7rh7d75pr77-UpdateConfig-ziuftbxwxiqx/c8244467-ef13-47f9-8282-79e92de5c9ee",
            "rel": "self"
          }
        ],
        "capabilities": [],
        "notification_topics": [],
        "updated_time": '',
        "timeout_mins": 14400,
        "stack_status": "CREATE_COMPLETE",
        "stack_owner": "admin",
        "parameters": {
          "OS::project_id": "9de7e9a9a2a242718cffa65dae677a33",
          "OS::stack_id": "c8244467-ef13-47f9-8282-79e92de5c9ee",
          "OS::stack_name": "overcloud-Controller-d7iywdnu5uzr-0-j7rh7d75pr77-UpdateConfig-ziuftbxwxiqx"
        },
        "id": "c8244467-ef13-47f9-8282-79e92de5c9ee",
        "outputs": [
          {
            "output_value": "e26b133d-d6f5-4b4e-9570-850068e2d2e0",
            "description": "No description given",
            "output_key": "OS::stack_id"
          }
        ],
        "template_description": "Software-config for performing package updates using yum\n"
      }
    },
    "overcloud-Networks-zyubznagvv6c-ExternalNetwork-vmp3e66swxg6": {
      "description": "A stack which creates no network(s).",
      "parent": "bfb0f40b-3c67-4e65-8517-6cff9dfab7ff",
      "stack_status_reason": "Stack CREATE completed successfully",
      "stack_name": "overcloud-Networks-zyubznagvv6c-ExternalNetwork-vmp3e66swxg6",
      "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
      "tags": '',
      "creation_time": "2016-04-12T15:09:49",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Networks-zyubznagvv6c-ExternalNetwork-vmp3e66swxg6/62c70746-8f9d-418a-9b42-bbab15556d64",
          "rel": "self"
        }
      ],
      "updated_time": '',
      "stack_owner": "admin",
      "stack_status": "CREATE_COMPLETE",
      "id": "62c70746-8f9d-418a-9b42-bbab15556d64",
      "outputs": {
        "disable_rollback": 'true',
        "description": "A stack which creates no network(s).",
        "parent": "bfb0f40b-3c67-4e65-8517-6cff9dfab7ff",
        "tags": '',
        "stack_name": "overcloud-Networks-zyubznagvv6c-ExternalNetwork-vmp3e66swxg6",
        "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
        "stack_status_reason": "Stack CREATE completed successfully",
        "creation_time": "2016-04-12T15:09:49",
        "links": [
          {
            "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Networks-zyubznagvv6c-ExternalNetwork-vmp3e66swxg6/62c70746-8f9d-418a-9b42-bbab15556d64",
            "rel": "self"
          }
        ],
        "capabilities": [],
        "notification_topics": [],
        "updated_time": '',
        "timeout_mins": 240,
        "stack_status": "CREATE_COMPLETE",
        "stack_owner": "admin",
        "parameters": {
          "OS::project_id": "9de7e9a9a2a242718cffa65dae677a33",
          "OS::stack_id": "62c70746-8f9d-418a-9b42-bbab15556d64",
          "OS::stack_name": "overcloud-Networks-zyubznagvv6c-ExternalNetwork-vmp3e66swxg6"
        },
        "id": "62c70746-8f9d-418a-9b42-bbab15556d64",
        "outputs": [],
        "template_description": "A stack which creates no network(s)."
      }
    },
    "overcloud-CephStorage-sejj7dhcfhtd": {
      "description": "No description",
      "parent": "9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
      "stack_status_reason": "Stack UPDATE completed successfully",
      "stack_name": "overcloud-CephStorage-sejj7dhcfhtd",
      "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
      "tags": '',
      "creation_time": "2016-04-12T15:09:52",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-CephStorage-sejj7dhcfhtd/0404dbec-c920-4351-9c35-79977300b74a",
          "rel": "self"
        }
      ],
      "updated_time": "2016-04-12T15:09:53",
      "stack_owner": "admin",
      "stack_status": "UPDATE_COMPLETE",
      "id": "0404dbec-c920-4351-9c35-79977300b74a",
      "outputs": {
        "disable_rollback": 'true',
        "description": "No description",
        "parent": "9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
        "tags": '',
        "stack_name": "overcloud-CephStorage-sejj7dhcfhtd",
        "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
        "stack_status_reason": "Stack UPDATE completed successfully",
        "creation_time": "2016-04-12T15:09:52",
        "links": [
          {
            "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-CephStorage-sejj7dhcfhtd/0404dbec-c920-4351-9c35-79977300b74a",
            "rel": "self"
          }
        ],
        "capabilities": [],
        "notification_topics": [],
        "updated_time": "2016-04-12T15:09:53",
        "timeout_mins": 14400,
        "stack_status": "UPDATE_COMPLETE",
        "stack_owner": "admin",
        "parameters": {
          "OS::project_id": "9de7e9a9a2a242718cffa65dae677a33",
          "OS::stack_id": "0404dbec-c920-4351-9c35-79977300b74a",
          "OS::stack_name": "overcloud-CephStorage-sejj7dhcfhtd"
        },
        "id": "0404dbec-c920-4351-9c35-79977300b74a",
        "outputs": [],
        "template_description": "No description"
      }
    },
    "overcloud-Networks-zyubznagvv6c-TenantNetwork-e3myke3plkcn": {
      "description": "A stack which creates no network(s).",
      "parent": "bfb0f40b-3c67-4e65-8517-6cff9dfab7ff",
      "stack_status_reason": "Stack CREATE completed successfully",
      "stack_name": "overcloud-Networks-zyubznagvv6c-TenantNetwork-e3myke3plkcn",
      "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
      "tags": '',
      "creation_time": "2016-04-12T15:09:49",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Networks-zyubznagvv6c-TenantNetwork-e3myke3plkcn/43b4cf3a-90c5-448c-8d21-0beb32e4d309",
          "rel": "self"
        }
      ],
      "updated_time": '',
      "stack_owner": "admin",
      "stack_status": "CREATE_COMPLETE",
      "id": "43b4cf3a-90c5-448c-8d21-0beb32e4d309",
      "outputs": {
        "disable_rollback": 'true',
        "description": "A stack which creates no network(s).",
        "parent": "bfb0f40b-3c67-4e65-8517-6cff9dfab7ff",
        "tags": '',
        "stack_name": "overcloud-Networks-zyubznagvv6c-TenantNetwork-e3myke3plkcn",
        "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
        "stack_status_reason": "Stack CREATE completed successfully",
        "creation_time": "2016-04-12T15:09:49",
        "links": [
          {
            "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Networks-zyubznagvv6c-TenantNetwork-e3myke3plkcn/43b4cf3a-90c5-448c-8d21-0beb32e4d309",
            "rel": "self"
          }
        ],
        "capabilities": [],
        "notification_topics": [],
        "updated_time": '',
        "timeout_mins": 240,
        "stack_status": "CREATE_COMPLETE",
        "stack_owner": "admin",
        "parameters": {
          "OS::project_id": "9de7e9a9a2a242718cffa65dae677a33",
          "OS::stack_id": "43b4cf3a-90c5-448c-8d21-0beb32e4d309",
          "OS::stack_name": "overcloud-Networks-zyubznagvv6c-TenantNetwork-e3myke3plkcn"
        },
        "id": "43b4cf3a-90c5-448c-8d21-0beb32e4d309",
        "outputs": [],
        "template_description": "A stack which creates no network(s)."
      }
    },
    "overcloud": {
      "description": "Deploy an OpenStack environment, consisting of several node types (roles), Controller, Compute, BlockStorage, SwiftStorage and CephStorage.  The Storage roles enable independent scaling of the storage components, but the minimal deployment is one Controller and one Compute node.\n",
      "parent": '',
      "stack_status_reason": "Resource CREATE failed: resources.Compute: ResourceInError: resources[0].resources.NovaCompute: Went to status ERROR due to \"Message: No valid host was found. There are not enough hosts available., Code: 500\"",
      "stack_name": "overcloud",
      "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
      "tags": '',
      "creation_time": "2016-04-12T15:09:47",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "self"
        }
      ],
      "updated_time": '',
      "stack_owner": "admin",
      "stack_status": "CREATE_FAILED",
      "id": "9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
      "outputs": {
        "disable_rollback": 'true',
        "description": "Deploy an OpenStack environment, consisting of several node types (roles), Controller, Compute, BlockStorage, SwiftStorage and CephStorage.  The Storage roles enable independent scaling of the storage components, but the minimal deployment is one Controller and one Compute node.\n",
        "parent": '',
        "tags": '',
        "stack_name": "overcloud",
        "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
        "stack_status_reason": "Resource CREATE failed: resources.Compute: ResourceInError: resources[0].resources.NovaCompute: Went to status ERROR due to \"Message: No valid host was found. There are not enough hosts available., Code: 500\"",
        "creation_time": "2016-04-12T15:09:47",
        "links": [
          {
            "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
            "rel": "self"
          }
        ],
        "capabilities": [],
        "notification_topics": [],
        "updated_time": '',
        "timeout_mins": 240,
        "stack_status": "CREATE_FAILED",
        "stack_owner": "admin",
        "parameters": {
          "NeutronPublicInterfaceRawDevice": "",
          "KeystoneSigningKey": "******",
          "NtpServer": "[u'north-america.pool.ntp.org']",
          "NeutronTenantMtu": "1400",
          "NeutronDhcpAgentsPerNetwork": "3",
          "Debug": "",
          "NeutronFlatNetworks": "[u'datacentre']",
          "CorosyncIPv6": "False",
          "NovaEnableRbdBackend": "False",
          "controllerImage": "overcloud-full",
          "GlancePassword": "******",
          "NeutronTunnelIdRanges": "[u'1:4094']",
          "CinderEnableRbdBackend": "False",
          "CephStorageSchedulerHints": "{}",
          "SwiftReplicas": "3",
          "NeutronPublicInterfaceTag": "",
          "FencingConfig": "{}",
          "ControllerHostnameFormat": "%stackname%-controller-%index%",
          "NovaComputeLibvirtVifDriver": "",
          "CloudDomain": "localdomain",
          "CephStorageCount": "0",
          "ServiceNetMap": "{u'NovaVncProxyNetwork': u'internal_api', u'CinderApiNetwork': u'internal_api', u'NovaApiNetwork': u'internal_api', u'CeilometerApiNetwork': u'internal_api', u'CephStorageHostnameResolveNetwork': u'storage', u'SwiftMgmtNetwork': u'storage_mgmt', u'MemcachedNetwork': u'internal_api', u'RabbitMqNetwork': u'internal_api', u'KeystoneAdminApiNetwork': u'ctlplane', u'SwiftProxyNetwork': u'storage', u'NeutronTenantNetwork': u'tenant', u'CephClusterNetwork': u'storage_mgmt', u'NovaMetadataNetwork': u'internal_api', u'ControllerHostnameResolveNetwork': u'internal_api', u'NeutronApiNetwork': u'internal_api', u'GlanceApiNetwork': u'storage', u'ObjectStorageHostnameResolveNetwork': u'internal_api', u'KeystonePublicApiNetwork': u'internal_api', u'HeatApiNetwork': u'internal_api', u'GlanceRegistryNetwork': u'internal_api', u'RedisNetwork': u'internal_api', u'MysqlNetwork': u'internal_api', u'BlockStorageHostnameResolveNetwork': u'internal_api', u'ComputeHostnameResolveNetwork': u'internal_api', u'CephPublicNetwork': u'storage', u'MongoDbNetwork': u'internal_api', u'HorizonNetwork': u'internal_api', u'CinderIscsiNetwork': u'storage'}",
          "SnmpdReadonlyUserName": "ro_snmp_user",
          "KeyName": "default",
          "CinderISCSIHelper": "lioadm",
          "BlockStorageImage": "overcloud-full",
          "OvercloudControlFlavor": "control",
          "CloudName": "overcloud",
          "RabbitPassword": "******",
          "OS::stack_id": "9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "PublicVirtualInterface": "br-ex",
          "DeployIdentifier": "1460473783",
          "NeutronPublicInterface": "nic1",
          "MemcachedIPv6": "False",
          "EnableFencing": "False",
          "StorageVirtualFixedIPs": "[]",
          "ObjectStorageSchedulerHints": "{}",
          "RabbitFDLimit": "16384",
          "NovaComputeSchedulerHints": "{}",
          "OvercloudSwiftStorageFlavor": "baremetal",
          "SwiftPassword": "******",
          "NeutronMetadataProxySharedSecret": "******",
          "CephStorageRemovalPolicies": "[]",
          "BlockStorageSchedulerHints": "{}",
          "InternalApiVirtualFixedIPs": "[]",
          "SwiftPartPower": "10",
          "KeystoneNotificationFormat": "basic",
          "NeutronPublicInterfaceDefaultRoute": "",
          "SnmpdReadonlyUserPassword": "******",
          "InstanceNameTemplate": "instance-%08x",
          "SwiftMountCheck": "False",
          "ControlVirtualInterface": "br-ex",
          "HeatStackDomainAdminPassword": "******",
          "OS::stack_name": "overcloud",
          "OvercloudComputeFlavor": "compute",
          "CephAdminKey": "******",
          "CinderEnableIscsiBackend": "True",
          "BlockStorageExtraConfig": "{}",
          "GlanceBackend": "swift",
          "ObjectStorageExtraConfig": "{}",
          "ComputeHostnameFormat": "%stackname%-novacompute-%index%",
          "controllerExtraConfig": "{}",
          "PurgeFirewallRules": "False",
          "ControllerEnableCephStorage": "False",
          "ControllerRemovalPolicies": "[]",
          "RabbitIPv6": "False",
          "RabbitClientUseSSL": "False",
          "NeutronAllowL3AgentFailover": "False",
          "NeutronEnableL2Pop": "False",
          "RabbitUserName": "guest",
          "KeystoneSigningCertificate": "-----BEGIN CERTIFICATE-----\nMIIDJDCCAgygAwIBAgIBAjANBgkqhkiG9w0BAQUFADBTMQswCQYDVQQGEwJYWDEO\nMAwGA1UECBMFVW5zZXQxDjAMBgNVBAcTBVVuc2V0MQ4wDAYDVQQKEwVVbnNldDEU\nMBIGA1UEAxMLS2V5c3RvbmUgQ0EwHhcNMTYwNDEyMTUwOTQzWhcNMjYwNDEwMTUw\nOTQzWjBYMQswCQYDVQQGEwJYWDEOMAwGA1UECBMFVW5zZXQxDjAMBgNVBAcTBVVu\nc2V0MQ4wDAYDVQQKEwVVbnNldDEZMBcGA1UEAxMQS2V5c3RvbmUgU2lnbmluZzCC\nASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBALqFj/1OTcqwfAfkXnm9XYJ0\nk85O+JGDfWuygeS8GBP99G6FMf/xPb3DeJTzEbm2xnVn3oLyBx9eNHg28Pz+B1me\n1zJJNmNTHYY22gQ9QTNuo/2fnyehzlIB7mzeWIqbuWaeabg3FI8ujfN9l2/jxw5c\nnscakOU1/NKQOcjXgIBP7jr9l9vfLQOvZ4oPeYwkAn0li9xYhpVE70fsvE57J1JC\nr/WkL6ExZCJA78+PC5Oq1WGB86fUCSdoT0H0uDuiOgsohfFBpaL0MAXO//+L2q+Y\nsZGcgVqgPaMW97vP3dedIMYkxHbQgVUwKHUGbL9GvIrkCzmPx0z4AqbeadpyMzUC\nAwEAATANBgkqhkiG9w0BAQUFAAOCAQEAj6loZnn6GlHqpJL34es9+AT6yLaKq6py\nQtnMl3uypwO1u7opMxS0Vhluw/IpWtaiRIlfboJ9IhrDcZm6rMtn/sjoB2XbLnGI\n9v3BSj+0lGyTrP8tV4FEFrKXG46SqcU3KeHlfk5mL3JB7XzOsPE4V+IcabPg/cKt\negXPAqKOzIGKc8fbGm/q7eMI+NtP4sKgIPJOxneMKYbcHcq6sY3UmiXVMYJ1PItD\n/tE2x2tVotnnYoU1SV9wPgkfGNY2xxdO31+DgzhNA45M/31PLm98LO1U7DpiAxLu\n/tEbVyspUJkUSEmQfhQ9LoHuX4BLObJU7ZoqHzA9xFmg3e0HwAfRqA==\n-----END CERTIFICATE-----\n",
          "KeystoneNotificationDriver": "[u'messaging']",
          "GlanceLogFile": "",
          "NeutronExternalNetworkBridge": "br-ex",
          "CeilometerBackend": "mongodb",
          "SwiftHashSuffix": "******",
          "RabbitCookieSalt": "unset",
          "AdminPassword": "******",
          "NeutronDVR": "False",
          "MongoDbIPv6": "False",
          "CephClusterFSID": "",
          "CephStorageHostnameFormat": "%stackname%-cephstorage-%index%",
          "CephStorageImage": "overcloud-full",
          "NeutronDnsmasqOptions": "dhcp-option-force=26,%MTU%",
          "MysqlMaxConnections": "4096",
          "ControllerCount": "3",
          "NeutronTunnelTypes": "[u'vxlan']",
          "OS::project_id": "9de7e9a9a2a242718cffa65dae677a33",
          "PublicVirtualFixedIPs": "[]",
          "StorageMgmtVirtualFixedIPs": "[]",
          "NeutronPassword": "******",
          "NeutronBridgeMappings": "[u'datacentre:br-ex']",
          "NeutronEnableIsolatedMetadata": "False",
          "NeutronVniRanges": "[u'1:4094']",
          "NeutronAgentMode": "dvr_snat",
          "NovaImage": "overcloud-full",
          "NeutronEnableTunnelling": "True",
          "ServerMetadata": "{}",
          "ManageFirewall": "False",
          "CephExternalMonHost": "",
          "OvercloudCephStorageFlavor": "baremetal",
          "CinderPassword": "******",
          "NeutronTypeDrivers": "[u'vxlan', u'vlan', u'flat', u'gre']",
          "ObjectStorageCount": "0",
          "CinderLVMLoopDeviceSize": "10280",
          "BlockStorageHostnameFormat": "%stackname%-blockstorage-%index%",
          "CinderNfsServers": "[]",
          "CephClientKey": "******",
          "ImageUpdatePolicy": "REBUILD_PRESERVE_EPHEMERAL",
          "MysqlInnodbBufferPoolSize": "0",
          "NeutronPluginExtensions": "[u'qos', u'port_security']",
          "BlockStorageCount": "0",
          "NovaSecurityGroupAPI": "neutron",
          "ControlFixedIPs": "[]",
          "AdminToken": "******",
          "ObjectStorageHostnameFormat": "%stackname%-objectstorage-%index%",
          "SwiftMinPartHours": "1",
          "HAProxySyslogAddress": "/dev/log",
          "SwiftStorageImage": "overcloud-full",
          "NeutronL3HA": "True",
          "NovaComputeLibvirtType": "kvm",
          "EnableGalera": "True",
          "MongoDbNoJournal": "False",
          "CephMonKey": "******",
          "ComputeRemovalPolicies": "[]",
          "NeutronCorePlugin": "ml2",
          "HypervisorNeutronPhysicalBridge": "br-ex",
          "CeilometerMeteringSecret": "******",
          "CinderEnableNfsBackend": "False",
          "ControllerSchedulerHints": "{}",
          "HypervisorNeutronPublicInterface": "nic1",
          "NovaComputeDriver": "libvirt.LibvirtDriver",
          "ExtraConfig": "{}",
          "NovaOVSBridge": "br-int",
          "HeatPassword": "******",
          "TimeZone": "UTC",
          "HorizonAllowedHosts": "[u'*']",
          "OvercloudBlockStorageFlavor": "baremetal",
          "BlockStorageRemovalPolicies": "[]",
          "RabbitClientPort": "5672",
          "NeutronComputeAgentMode": "dvr",
          "ComputeCount": "1",
          "KeystoneSSLCertificateKey": "******",
          "NeutronControlPlaneID": "ctlplane",
          "NeutronNetworkType": "[u'vxlan']",
          "CeilometerPassword": "******",
          "ObjectStorageRemovalPolicies": "[]",
          "NeutronMechanismDrivers": "[u'openvswitch']",
          "ControllerEnableSwiftStorage": "True",
          "GlanceNotifierStrategy": "noop",
          "KeystoneSSLCertificate": "",
          "KeystoneCACertificate": "-----BEGIN CERTIFICATE-----\nMIIDNzCCAh+gAwIBAgIBATANBgkqhkiG9w0BAQUFADBTMQswCQYDVQQGEwJYWDEO\nMAwGA1UECBMFVW5zZXQxDjAMBgNVBAcTBVVuc2V0MQ4wDAYDVQQKEwVVbnNldDEU\nMBIGA1UEAxMLS2V5c3RvbmUgQ0EwHhcNMTYwNDEyMTUwOTQzWhcNMjYwNDEwMTUw\nOTQzWjBTMQswCQYDVQQGEwJYWDEOMAwGA1UECBMFVW5zZXQxDjAMBgNVBAcTBVVu\nc2V0MQ4wDAYDVQQKEwVVbnNldDEUMBIGA1UEAxMLS2V5c3RvbmUgQ0EwggEiMA0G\nCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQC1qd7Dvdrp0vw00HWxjqtCfqLS+/Oa\nr3ODws1I6TeaaBDGfrsvhQsGIEV2HXHw5XvZa5l6JgbbH+zcCiescMdIz6BkxrrG\n0bssq9eP7M9JPW1Ezo6LkMwPJiBpGWtw2EZ9pfIBH7AMR/cmweWmDi09sWy4O9q+\npB28luSmeSshqJZ6S1L6pqWdPQcvNFwpRFgZr3rRbyvVKS76GABMS30CGbT0h8Fj\nWwzGN1nCeSvTOHGvnOC714E81XApOViPz/ysrAc591mK5JORsFOXkH27OTMiWC9t\nb9lJQ7LZAU9EIywokLmPaW8wG+DCwgQs9KbHFOG2S7LfMhE/+Sh5L8n3AgMBAAGj\nFjAUMBIGA1UdEwEB/wQIMAYBAf8CAQAwDQYJKoZIhvcNAQEFBQADggEBAInsYCil\newgy2kwq4ArR3bHC7b5jYo/9SKylrsDrgUb38/iQZei3wooa2V+l1SbkznahwpI5\nqAqywzT8o9d8/LUji1631H3fuyCTb4UHX3SE/iw2UVmFVyWw0AMkj3gDJ9iVw8rR\nUvSwbdNySGZNl8BwETObLR4gyIpIY5Kq2ztitaxIg1xMlkDAe66trzCunt8Kt2Os\n8m3ObKr8TXbQMA6v01FigaipNjxXDyHPGv1S14PvQiguX6CiD02L5eXPjoJfLlOC\n/MjeK2f2YxvPf/BKUWbvekQApcCGayPpuiPM0z5oam1KDVsNMAAEE6a7UyAZs2NT\niEqras+fEAFIy3I=\n-----END CERTIFICATE-----\n",
          "NovaPassword": "******",
          "CephStorageExtraConfig": "{}",
          "CinderNfsMountOptions": "",
          "RedisPassword": "******",
          "NeutronPublicInterfaceIP": "",
          "NovaIPv6": "False",
          "CeilometerComputeAgent": "",
          "NeutronServicePlugins": "[u'router', u'qos']",
          "NeutronAgentExtensions": "[u'qos']",
          "UpdateIdentifier": "",
          "NovaComputeExtraConfig": "{}",
          "NeutronNetworkVLANRanges": "[u'datacentre:1:1000']"
        },
        "id": "9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
        "outputs": [
          {
            "output_value": "192.0.2.51",
            "description": "VIP for Heat API internal endpoint",
            "output_key": "HeatInternalVip"
          },
          {
            "output_value": "192.0.2.51",
            "description": "VIP for Ceilometer API internal endpoint",
            "output_key": "CeilometerInternalVip"
          },
          {
            "output_value": "192.0.2.51",
            "description": "VIP for Glance API internal endpoint",
            "output_key": "GlanceInternalVip"
          },
          {
            "output_value": "192.0.2.51",
            "description": "VIP for Keystone API internal endpoint",
            "output_key": "KeystoneInternalVip"
          },
          {
            "output_value": "192.0.2.51",
            "description": "Controller VIP for public API endpoints",
            "output_key": "PublicVip"
          },
          {
            "output_value": "http://192.0.2.51:5000/v2.0",
            "description": "URL for the Overcloud Keystone service",
            "output_key": "KeystoneURL"
          },
          {
            "output_value": "192.0.2.51",
            "description": "VIP for Neutron API internal endpoint",
            "output_key": "NeutronInternalVip"
          },
          {
            "output_value": "192.0.2.51",
            "description": "VIP for Swift Proxy internal endpoint",
            "output_key": "SwiftInternalVip"
          },
          {
            "output_value": "192.0.2.51",
            "description": "VIP for Cinder API internal endpoint",
            "output_key": "CinderInternalVip"
          },
          {
            "output_value": "192.0.2.51",
            "description": "Keystone Admin VIP endpoint",
            "output_key": "KeystoneAdminVip"
          },
          {
            "output_value": "192.0.2.51",
            "description": "VIP for Nova API internal endpoint",
            "output_key": "NovaInternalVip"
          }
        ],
        "template_description": "Deploy an OpenStack environment, consisting of several node types (roles), Controller, Compute, BlockStorage, SwiftStorage and CephStorage.  The Storage roles enable independent scaling of the storage components, but the minimal deployment is one Controller and one Compute node.\n"
      }
    },
    "overcloud-StorageVirtualIP-kgolkxflflvk": {
      "description": "Returns the control plane port (provisioning network) as the ip_address.\n",
      "parent": "9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
      "stack_status_reason": "Stack CREATE completed successfully",
      "stack_name": "overcloud-StorageVirtualIP-kgolkxflflvk",
      "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
      "tags": '',
      "creation_time": "2016-04-12T15:09:57",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-StorageVirtualIP-kgolkxflflvk/00e3d273-7ad2-434d-b700-86f112b6b2fd",
          "rel": "self"
        }
      ],
      "updated_time": '',
      "stack_owner": "admin",
      "stack_status": "CREATE_COMPLETE",
      "id": "00e3d273-7ad2-434d-b700-86f112b6b2fd",
      "outputs": {
        "disable_rollback": 'true',
        "description": "Returns the control plane port (provisioning network) as the ip_address.\n",
        "parent": "9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
        "tags": '',
        "stack_name": "overcloud-StorageVirtualIP-kgolkxflflvk",
        "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
        "stack_status_reason": "Stack CREATE completed successfully",
        "creation_time": "2016-04-12T15:09:57",
        "links": [
          {
            "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-StorageVirtualIP-kgolkxflflvk/00e3d273-7ad2-434d-b700-86f112b6b2fd",
            "rel": "self"
          }
        ],
        "capabilities": [],
        "notification_topics": [],
        "updated_time": '',
        "timeout_mins": 240,
        "stack_status": "CREATE_COMPLETE",
        "stack_owner": "admin",
        "parameters": {
          "FixedIPs": "[]",
          "OS::project_id": "9de7e9a9a2a242718cffa65dae677a33",
          "ControlPlaneNetwork": "ctlplane",
          "OS::stack_id": "00e3d273-7ad2-434d-b700-86f112b6b2fd",
          "OS::stack_name": "overcloud-StorageVirtualIP-kgolkxflflvk",
          "NodeIndex": "0",
          "ControlPlaneIP": "192.0.2.51",
          "ControlPlaneSubnetCidr": "24",
          "ServiceName": "",
          "PortName": "storage_virtual_ip",
          "IPPool": "{}",
          "NetworkName": "storage"
        },
        "id": "00e3d273-7ad2-434d-b700-86f112b6b2fd",
        "outputs": [
          {
            "output_value": "192.0.2.51/24",
            "description": "IP/Subnet CIDR for the pass thru network IP",
            "output_key": "ip_subnet"
          },
          {
            "output_value": "192.0.2.51",
            "description": "pass thru network IP (for compatibility with vip_v6.yaml)",
            "output_key": "ip_address_uri"
          },
          {
            "output_value": "192.0.2.51",
            "description": "pass thru network IP",
            "output_key": "ip_address"
          }
        ],
        "template_description": "Returns the control plane port (provisioning network) as the ip_address.\n"
      }
    },
    "overcloud-VipConfig-ratodrtp6nte": {
      "description": "Configure hieradata for service -> virtual IP mappings.\n",
      "parent": "9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
      "stack_status_reason": "Stack CREATE completed successfully",
      "stack_name": "overcloud-VipConfig-ratodrtp6nte",
      "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
      "tags": '',
      "creation_time": "2016-04-12T15:09:48",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-VipConfig-ratodrtp6nte/e74802ee-8e2c-4c11-a8d4-4e1d81527ad9",
          "rel": "self"
        }
      ],
      "updated_time": '',
      "stack_owner": "admin",
      "stack_status": "CREATE_COMPLETE",
      "id": "e74802ee-8e2c-4c11-a8d4-4e1d81527ad9",
      "outputs": {
        "disable_rollback": 'true',
        "description": "Configure hieradata for service -> virtual IP mappings.\n",
        "parent": "9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
        "tags": '',
        "stack_name": "overcloud-VipConfig-ratodrtp6nte",
        "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
        "stack_status_reason": "Stack CREATE completed successfully",
        "creation_time": "2016-04-12T15:09:48",
        "links": [
          {
            "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-VipConfig-ratodrtp6nte/e74802ee-8e2c-4c11-a8d4-4e1d81527ad9",
            "rel": "self"
          }
        ],
        "capabilities": [],
        "notification_topics": [],
        "updated_time": '',
        "timeout_mins": 240,
        "stack_status": "CREATE_COMPLETE",
        "stack_owner": "admin",
        "parameters": {
          "OS::project_id": "9de7e9a9a2a242718cffa65dae677a33",
          "OS::stack_id": "e74802ee-8e2c-4c11-a8d4-4e1d81527ad9",
          "OS::stack_name": "overcloud-VipConfig-ratodrtp6nte"
        },
        "id": "e74802ee-8e2c-4c11-a8d4-4e1d81527ad9",
        "outputs": [
          {
            "output_value": "7efb061b-ffc3-42ac-a95f-c9bd70177e84",
            "description": "The VipConfigImpl resource.",
            "output_key": "OS::stack_id"
          }
        ],
        "template_description": "Configure hieradata for service -> virtual IP mappings.\n"
      }
    },
    "overcloud-PublicVirtualIP-wd3dmh5doc3v": {
      "description": "Returns the control plane port (provisioning network) as the ip_address.\n",
      "parent": "9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
      "stack_status_reason": "Stack CREATE completed successfully",
      "stack_name": "overcloud-PublicVirtualIP-wd3dmh5doc3v",
      "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
      "tags": '',
      "creation_time": "2016-04-12T15:09:56",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-PublicVirtualIP-wd3dmh5doc3v/736e0867-a120-4a38-8b7e-ea7113bdadc0",
          "rel": "self"
        }
      ],
      "updated_time": '',
      "stack_owner": "admin",
      "stack_status": "CREATE_COMPLETE",
      "id": "736e0867-a120-4a38-8b7e-ea7113bdadc0",
      "outputs": {
        "disable_rollback": 'true',
        "description": "Returns the control plane port (provisioning network) as the ip_address.\n",
        "parent": "9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
        "tags": '',
        "stack_name": "overcloud-PublicVirtualIP-wd3dmh5doc3v",
        "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
        "stack_status_reason": "Stack CREATE completed successfully",
        "creation_time": "2016-04-12T15:09:56",
        "links": [
          {
            "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-PublicVirtualIP-wd3dmh5doc3v/736e0867-a120-4a38-8b7e-ea7113bdadc0",
            "rel": "self"
          }
        ],
        "capabilities": [],
        "notification_topics": [],
        "updated_time": '',
        "timeout_mins": 240,
        "stack_status": "CREATE_COMPLETE",
        "stack_owner": "admin",
        "parameters": {
          "FixedIPs": "[]",
          "OS::project_id": "9de7e9a9a2a242718cffa65dae677a33",
          "ControlPlaneNetwork": "ctlplane",
          "OS::stack_id": "736e0867-a120-4a38-8b7e-ea7113bdadc0",
          "OS::stack_name": "overcloud-PublicVirtualIP-wd3dmh5doc3v",
          "NodeIndex": "0",
          "ControlPlaneIP": "192.0.2.51",
          "ControlPlaneSubnetCidr": "24",
          "ServiceName": "",
          "PortName": "public_virtual_ip",
          "IPPool": "{}",
          "NetworkName": "external"
        },
        "id": "736e0867-a120-4a38-8b7e-ea7113bdadc0",
        "outputs": [
          {
            "output_value": "192.0.2.51/24",
            "description": "IP/Subnet CIDR for the pass thru network IP",
            "output_key": "ip_subnet"
          },
          {
            "output_value": "192.0.2.51",
            "description": "pass thru network IP (for compatibility with vip_v6.yaml)",
            "output_key": "ip_address_uri"
          },
          {
            "output_value": "192.0.2.51",
            "description": "pass thru network IP",
            "output_key": "ip_address"
          }
        ],
        "template_description": "Returns the control plane port (provisioning network) as the ip_address.\n"
      }
    },
    "overcloud-Controller-d7iywdnu5uzr-2-evqysybsnrrt-UpdateConfig-56e74twlex5q": {
      "description": "Software-config for performing package updates using yum\n",
      "parent": "e4dc37e4-d565-4453-8d6e-a830953eb803",
      "stack_status_reason": "Stack CREATE completed successfully",
      "stack_name": "overcloud-Controller-d7iywdnu5uzr-2-evqysybsnrrt-UpdateConfig-56e74twlex5q",
      "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
      "tags": '',
      "creation_time": "2016-04-12T15:10:13",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Controller-d7iywdnu5uzr-2-evqysybsnrrt-UpdateConfig-56e74twlex5q/4553c7da-9b10-4097-81b1-74ba1b71fc4e",
          "rel": "self"
        }
      ],
      "updated_time": '',
      "stack_owner": "admin",
      "stack_status": "CREATE_COMPLETE",
      "id": "4553c7da-9b10-4097-81b1-74ba1b71fc4e",
      "outputs": {
        "disable_rollback": 'true',
        "description": "Software-config for performing package updates using yum\n",
        "parent": "e4dc37e4-d565-4453-8d6e-a830953eb803",
        "tags": '',
        "stack_name": "overcloud-Controller-d7iywdnu5uzr-2-evqysybsnrrt-UpdateConfig-56e74twlex5q",
        "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
        "stack_status_reason": "Stack CREATE completed successfully",
        "creation_time": "2016-04-12T15:10:13",
        "links": [
          {
            "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Controller-d7iywdnu5uzr-2-evqysybsnrrt-UpdateConfig-56e74twlex5q/4553c7da-9b10-4097-81b1-74ba1b71fc4e",
            "rel": "self"
          }
        ],
        "capabilities": [],
        "notification_topics": [],
        "updated_time": '',
        "timeout_mins": 14400,
        "stack_status": "CREATE_COMPLETE",
        "stack_owner": "admin",
        "parameters": {
          "OS::project_id": "9de7e9a9a2a242718cffa65dae677a33",
          "OS::stack_id": "4553c7da-9b10-4097-81b1-74ba1b71fc4e",
          "OS::stack_name": "overcloud-Controller-d7iywdnu5uzr-2-evqysybsnrrt-UpdateConfig-56e74twlex5q"
        },
        "id": "4553c7da-9b10-4097-81b1-74ba1b71fc4e",
        "outputs": [
          {
            "output_value": "a383753f-790e-4a38-aa64-65088d273c1a",
            "description": "No description given",
            "output_key": "OS::stack_id"
          }
        ],
        "template_description": "Software-config for performing package updates using yum\n"
      }
    },
    "overcloud-Networks-zyubznagvv6c-StorageNetwork-e2elgonsbsvu": {
      "description": "A stack which creates no network(s).",
      "parent": "bfb0f40b-3c67-4e65-8517-6cff9dfab7ff",
      "stack_status_reason": "Stack CREATE completed successfully",
      "stack_name": "overcloud-Networks-zyubznagvv6c-StorageNetwork-e2elgonsbsvu",
      "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
      "tags": '',
      "creation_time": "2016-04-12T15:09:49",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Networks-zyubznagvv6c-StorageNetwork-e2elgonsbsvu/be8920e1-6db8-4199-baf0-4362c776bfb4",
          "rel": "self"
        }
      ],
      "updated_time": '',
      "stack_owner": "admin",
      "stack_status": "CREATE_COMPLETE",
      "id": "be8920e1-6db8-4199-baf0-4362c776bfb4",
      "outputs": {
        "disable_rollback": 'true',
        "description": "A stack which creates no network(s).",
        "parent": "bfb0f40b-3c67-4e65-8517-6cff9dfab7ff",
        "tags": '',
        "stack_name": "overcloud-Networks-zyubznagvv6c-StorageNetwork-e2elgonsbsvu",
        "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
        "stack_status_reason": "Stack CREATE completed successfully",
        "creation_time": "2016-04-12T15:09:49",
        "links": [
          {
            "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Networks-zyubznagvv6c-StorageNetwork-e2elgonsbsvu/be8920e1-6db8-4199-baf0-4362c776bfb4",
            "rel": "self"
          }
        ],
        "capabilities": [],
        "notification_topics": [],
        "updated_time": '',
        "timeout_mins": 240,
        "stack_status": "CREATE_COMPLETE",
        "stack_owner": "admin",
        "parameters": {
          "OS::project_id": "9de7e9a9a2a242718cffa65dae677a33",
          "OS::stack_id": "be8920e1-6db8-4199-baf0-4362c776bfb4",
          "OS::stack_name": "overcloud-Networks-zyubznagvv6c-StorageNetwork-e2elgonsbsvu"
        },
        "id": "be8920e1-6db8-4199-baf0-4362c776bfb4",
        "outputs": [],
        "template_description": "A stack which creates no network(s)."
      }
    },
    "overcloud-Controller-d7iywdnu5uzr-0-j7rh7d75pr77": {
      "description": "OpenStack controller node configured by Puppet.\n",
      "parent": "119696b0-92ac-44ab-85d6-614c68af3949",
      "stack_status_reason": "Resource CREATE failed: ResourceInError: resources.Controller: Went to status ERROR due to \"Message: No valid host was found. There are not enough hosts available., Code: 500\"",
      "stack_name": "overcloud-Controller-d7iywdnu5uzr-0-j7rh7d75pr77",
      "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
      "tags": '',
      "creation_time": "2016-04-12T15:10:09",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Controller-d7iywdnu5uzr-0-j7rh7d75pr77/04299fe4-e771-425d-9e2b-4ceca3458de1",
          "rel": "self"
        }
      ],
      "updated_time": '',
      "stack_owner": "admin",
      "stack_status": "CREATE_FAILED",
      "id": "04299fe4-e771-425d-9e2b-4ceca3458de1",
      "outputs": {
        "disable_rollback": 'true',
        "description": "OpenStack controller node configured by Puppet.\n",
        "parent": "119696b0-92ac-44ab-85d6-614c68af3949",
        "tags": '',
        "stack_name": "overcloud-Controller-d7iywdnu5uzr-0-j7rh7d75pr77",
        "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
        "stack_status_reason": "Resource CREATE failed: ResourceInError: resources.Controller: Went to status ERROR due to \"Message: No valid host was found. There are not enough hosts available., Code: 500\"",
        "creation_time": "2016-04-12T15:10:09",
        "links": [
          {
            "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Controller-d7iywdnu5uzr-0-j7rh7d75pr77/04299fe4-e771-425d-9e2b-4ceca3458de1",
            "rel": "self"
          }
        ],
        "capabilities": [],
        "notification_topics": [],
        "updated_time": '',
        "timeout_mins": 14400,
        "stack_status": "CREATE_FAILED",
        "stack_owner": "admin",
        "parameters": {
          "EnableCephStorage": "False",
          "NeutronPublicInterfaceRawDevice": "",
          "GlanceWorkers": "0",
          "NetworkDeploymentActions": "[u'CREATE']",
          "NtpServer": "[u'north-america.pool.ntp.org']",
          "NeutronTenantMtu": "1400",
          "NeutronDhcpAgentsPerNetwork": "3",
          "HeatApiVirtualIPUri": "192.0.2.51",
          "NeutronFlatNetworks": "[u'datacentre']",
          "EnablePackageInstall": "False",
          "CorosyncIPv6": "False",
          "NeutronAgentMode": "dvr_snat",
          "GlancePassword": "******",
          "NeutronTunnelIdRanges": "[u'1:4094']",
          "CinderEnableRbdBackend": "False",
          "SwiftReplicas": "3",
          "NeutronPublicInterfaceTag": "",
          "FencingConfig": "{}",
          "MemcachedIPv6": "False",
          "KeystoneSigningCertificate": "-----BEGIN CERTIFICATE-----\nMIIDJDCCAgygAwIBAgIBAjANBgkqhkiG9w0BAQUFADBTMQswCQYDVQQGEwJYWDEO\nMAwGA1UECBMFVW5zZXQxDjAMBgNVBAcTBVVuc2V0MQ4wDAYDVQQKEwVVbnNldDEU\nMBIGA1UEAxMLS2V5c3RvbmUgQ0EwHhcNMTYwNDEyMTUwOTQzWhcNMjYwNDEwMTUw\nOTQzWjBYMQswCQYDVQQGEwJYWDEOMAwGA1UECBMFVW5zZXQxDjAMBgNVBAcTBVVu\nc2V0MQ4wDAYDVQQKEwVVbnNldDEZMBcGA1UEAxMQS2V5c3RvbmUgU2lnbmluZzCC\nASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBALqFj/1OTcqwfAfkXnm9XYJ0\nk85O+JGDfWuygeS8GBP99G6FMf/xPb3DeJTzEbm2xnVn3oLyBx9eNHg28Pz+B1me\n1zJJNmNTHYY22gQ9QTNuo/2fnyehzlIB7mzeWIqbuWaeabg3FI8ujfN9l2/jxw5c\nnscakOU1/NKQOcjXgIBP7jr9l9vfLQOvZ4oPeYwkAn0li9xYhpVE70fsvE57J1JC\nr/WkL6ExZCJA78+PC5Oq1WGB86fUCSdoT0H0uDuiOgsohfFBpaL0MAXO//+L2q+Y\nsZGcgVqgPaMW97vP3dedIMYkxHbQgVUwKHUGbL9GvIrkCzmPx0z4AqbeadpyMzUC\nAwEAATANBgkqhkiG9w0BAQUFAAOCAQEAj6loZnn6GlHqpJL34es9+AT6yLaKq6py\nQtnMl3uypwO1u7opMxS0Vhluw/IpWtaiRIlfboJ9IhrDcZm6rMtn/sjoB2XbLnGI\n9v3BSj+0lGyTrP8tV4FEFrKXG46SqcU3KeHlfk5mL3JB7XzOsPE4V+IcabPg/cKt\negXPAqKOzIGKc8fbGm/q7eMI+NtP4sKgIPJOxneMKYbcHcq6sY3UmiXVMYJ1PItD\n/tE2x2tVotnnYoU1SV9wPgkfGNY2xxdO31+DgzhNA45M/31PLm98LO1U7DpiAxLu\n/tEbVyspUJkUSEmQfhQ9LoHuX4BLObJU7ZoqHzA9xFmg3e0HwAfRqA==\n-----END CERTIFICATE-----\n",
          "ControllerIPs": "{}",
          "ServiceNetMap": "{u'NovaVncProxyNetwork': u'internal_api', u'CinderApiNetwork': u'internal_api', u'NovaApiNetwork': u'internal_api', u'CeilometerApiNetwork': u'internal_api', u'CephStorageHostnameResolveNetwork': u'storage', u'SwiftMgmtNetwork': u'storage_mgmt', u'MemcachedNetwork': u'internal_api', u'RabbitMqNetwork': u'internal_api', u'KeystoneAdminApiNetwork': u'ctlplane', u'SwiftProxyNetwork': u'storage', u'NeutronTenantNetwork': u'tenant', u'CephClusterNetwork': u'storage_mgmt', u'NovaMetadataNetwork': u'internal_api', u'ControllerHostnameResolveNetwork': u'internal_api', u'NeutronApiNetwork': u'internal_api', u'GlanceApiNetwork': u'storage', u'ObjectStorageHostnameResolveNetwork': u'internal_api', u'KeystonePublicApiNetwork': u'internal_api', u'HeatApiNetwork': u'internal_api', u'GlanceRegistryNetwork': u'internal_api', u'RedisNetwork': u'internal_api', u'MysqlNetwork': u'internal_api', u'BlockStorageHostnameResolveNetwork': u'internal_api', u'ComputeHostnameResolveNetwork': u'internal_api', u'CephPublicNetwork': u'storage', u'MongoDbNetwork': u'internal_api', u'HorizonNetwork': u'internal_api', u'CinderIscsiNetwork': u'storage'}",
          "SnmpdReadonlyUserName": "ro_snmp_user",
          "ManageFirewall": "False",
          "CinderISCSIHelper": "lioadm",
          "CeilometerWorkers": "0",
          "NeutronEnableMetadataAgent": "True",
          "RabbitPassword": "******",
          "NeutronApiVirtualIP": "192.0.2.51",
          "PublicVirtualInterface": "br-ex",
          "Debug": "",
          "NeutronPublicInterface": "nic1",
          "GlanceFilePcmkDevice": "",
          "EnableFencing": "False",
          "SoftwareConfigTransport": "POLL_SERVER_CFN",
          "SwiftMountCheck": "False",
          "RabbitFDLimit": "16384",
          "HorizonSecret": "******",
          "VirtualIP": "192.0.2.51",
          "SwiftPassword": "******",
          "NeutronMetadataProxySharedSecret": "******",
          "Flavor": "control",
          "CinderApiVirtualIP": "192.0.2.51",
          "KeystonePublicApiVirtualIP": "192.0.2.51",
          "HAProxySyslogAddress": "/dev/log",
          "SwiftPartPower": "10",
          "HeatApiVirtualIP": "192.0.2.51",
          "KeystoneNotificationFormat": "basic",
          "NeutronPublicInterfaceDefaultRoute": "",
          "HeatPassword": "******",
          "InstanceNameTemplate": "instance-%08x",
          "RedisVirtualIP": "192.0.2.52",
          "ControllerExtraConfig": "{}",
          "ControlVirtualInterface": "br-ex",
          "HeatStackDomainAdminPassword": "******",
          "OS::stack_name": "overcloud-Controller-d7iywdnu5uzr-0-j7rh7d75pr77",
          "NeutronEnableOVSAgent": "True",
          "GlanceRegistryVirtualIP": "192.0.2.51",
          "PcsdPassword": "******",
          "SwiftWorkers": "0",
          "CinderEnableIscsiBackend": "True",
          "EnableLoadBalancer": "True",
          "KeystoneNotificationDriver": "[u'messaging']",
          "NeutronEnableL3Agent": "True",
          "NeutronVniRanges": "[u'1:4094']",
          "GlanceBackend": "swift",
          "RabbitClientUseSSL": "False",
          "NeutronAllowL3AgentFailover": "False",
          "NeutronEnableL2Pop": "False",
          "HeatAuthEncryptionKey": "******",
          "UpgradeLevelNovaCompute": "",
          "GlanceFilePcmkOptions": "",
          "RabbitUserName": "guest",
          "NovaApiVirtualIP": "192.0.2.51",
          "HeatWorkers": "0",
          "GlanceLogFile": "",
          "NeutronExternalNetworkBridge": "br-ex",
          "CeilometerBackend": "mongodb",
          "CeilometerApiVirtualIP": "192.0.2.51",
          "OS::stack_id": "04299fe4-e771-425d-9e2b-4ceca3458de1",
          "AdminPassword": "******",
          "NeutronDVR": "False",
          "Image": "overcloud-full",
          "ExtraConfig": "{}",
          "KeystoneSigningKey": "******",
          "KeystoneEnableDBPurge": "True",
          "CinderEnableDBPurge": "True",
          "NeutronDnsmasqOptions": "dhcp-option-force=26,1400",
          "MysqlMaxConnections": "4096",
          "NeutronTunnelTypes": "[u'vxlan']",
          "ServerMetadata": "{}",
          "Hostname": "overcloud-controller-0",
          "GlanceFilePcmkManage": "False",
          "NeutronPassword": "******",
          "NeutronBridgeMappings": "[u'datacentre:br-ex']",
          "HAProxyStatsUser": "admin",
          "EndpointMap": "{u'GlanceInternal': {u'uri_no_suffix': u'http://192.0.2.51:9292', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'9292', u'uri': u'http://192.0.2.51:9292'}, u'NovaEC2Public': {u'uri_no_suffix': u'http://192.0.2.51:8773', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8773', u'uri': u'http://192.0.2.51:8773/services/Cloud'}, u'HeatPublic': {u'uri_no_suffix': u'http://192.0.2.51:8004', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8004', u'uri': u'http://192.0.2.51:8004/v1/%(tenant_id)s'}, u'KeystonePublic': {u'uri_no_suffix': u'http://192.0.2.51:5000', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'5000', u'uri': u'http://192.0.2.51:5000/v2.0'}, u'HeatAdmin': {u'uri_no_suffix': u'http://192.0.2.51:8004', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8004', u'uri': u'http://192.0.2.51:8004/v1/%(tenant_id)s'}, u'NovaEC2Admin': {u'uri_no_suffix': u'http://192.0.2.51:8773', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8773', u'uri': u'http://192.0.2.51:8773/services/Admin'}, u'CeilometerAdmin': {u'uri_no_suffix': u'http://192.0.2.51:8777', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8777', u'uri': u'http://192.0.2.51:8777'}, u'GlanceAdmin': {u'uri_no_suffix': u'http://192.0.2.51:9292', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'9292', u'uri': u'http://192.0.2.51:9292'}, u'SwiftS3Internal': {u'uri_no_suffix': u'http://192.0.2.51:8080', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8080', u'uri': u'http://192.0.2.51:8080'}, u'CinderV2Internal': {u'uri_no_suffix': u'http://192.0.2.51:8776', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8776', u'uri': u'http://192.0.2.51:8776/v2/%(tenant_id)s'}, u'NovaVNCProxyAdmin': {u'uri_no_suffix': u'http://192.0.2.51:6080', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'6080', u'uri': u'http://192.0.2.51:6080'}, u'HeatInternal': {u'uri_no_suffix': u'http://192.0.2.51:8004', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8004', u'uri': u'http://192.0.2.51:8004/v1/%(tenant_id)s'}, u'NovaV3Admin': {u'uri_no_suffix': u'http://192.0.2.51:8774', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8774', u'uri': u'http://192.0.2.51:8774/v3'}, u'NeutronPublic': {u'uri_no_suffix': u'http://192.0.2.51:9696', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'9696', u'uri': u'http://192.0.2.51:9696'}, u'CinderPublic': {u'uri_no_suffix': u'http://192.0.2.51:8776', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8776', u'uri': u'http://192.0.2.51:8776/v1/%(tenant_id)s'}, u'HorizonPublic': {u'uri_no_suffix': u'http://192.0.2.51:80', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'80', u'uri': u'http://192.0.2.51:80/dashboard'}, u'KeystoneEC2': {u'uri_no_suffix': u'http://192.0.2.51:5000', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'5000', u'uri': u'http://192.0.2.51:5000/v2.0/ec2tokens'}, u'GlancePublic': {u'uri_no_suffix': u'http://192.0.2.51:9292', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'9292', u'uri': u'http://192.0.2.51:9292'}, u'CinderV2Admin': {u'uri_no_suffix': u'http://192.0.2.51:8776', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8776', u'uri': u'http://192.0.2.51:8776/v2/%(tenant_id)s'}, u'GlanceRegistryPublic': {u'uri_no_suffix': u'http://192.0.2.51:9191', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'9191', u'uri': u'http://192.0.2.51:9191'}, u'NeutronAdmin': {u'uri_no_suffix': u'http://192.0.2.51:9696', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'9696', u'uri': u'http://192.0.2.51:9696'}, u'SwiftInternal': {u'uri_no_suffix': u'http://192.0.2.51:8080', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8080', u'uri': u'http://192.0.2.51:8080/v1/AUTH_%(tenant_id)s'}, u'NovaVNCProxyPublic': {u'uri_no_suffix': u'http://192.0.2.51:6080', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'6080', u'uri': u'http://192.0.2.51:6080'}, u'CeilometerInternal': {u'uri_no_suffix': u'http://192.0.2.51:8777', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8777', u'uri': u'http://192.0.2.51:8777'}, u'NovaInternal': {u'uri_no_suffix': u'http://192.0.2.51:8774', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8774', u'uri': u'http://192.0.2.51:8774/v2.1/%(tenant_id)s'}, u'GlanceRegistryInternal': {u'uri_no_suffix': u'http://192.0.2.51:9191', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'9191', u'uri': u'http://192.0.2.51:9191'}, u'NovaV3Internal': {u'uri_no_suffix': u'http://192.0.2.51:8774', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8774', u'uri': u'http://192.0.2.51:8774/v3'}, u'NovaAdmin': {u'uri_no_suffix': u'http://192.0.2.51:8774', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8774', u'uri': u'http://192.0.2.51:8774/v2.1/%(tenant_id)s'}, u'NovaEC2Internal': {u'uri_no_suffix': u'http://192.0.2.51:8773', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8773', u'uri': u'http://192.0.2.51:8773/services/Cloud'}, u'SwiftAdmin': {u'uri_no_suffix': u'http://192.0.2.51:8080', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8080', u'uri': u'http://192.0.2.51:8080'}, u'NeutronInternal': {u'uri_no_suffix': u'http://192.0.2.51:9696', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'9696', u'uri': u'http://192.0.2.51:9696'}, u'NovaPublic': {u'uri_no_suffix': u'http://192.0.2.51:8774', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8774', u'uri': u'http://192.0.2.51:8774/v2.1/%(tenant_id)s'}, u'SwiftS3Admin': {u'uri_no_suffix': u'http://192.0.2.51:8080', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8080', u'uri': u'http://192.0.2.51:8080'}, u'CeilometerPublic': {u'uri_no_suffix': u'http://192.0.2.51:8777', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8777', u'uri': u'http://192.0.2.51:8777'}, u'CinderV2Public': {u'uri_no_suffix': u'http://192.0.2.51:8776', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8776', u'uri': u'http://192.0.2.51:8776/v2/%(tenant_id)s'}, u'KeystoneAdmin': {u'uri_no_suffix': u'http://192.0.2.51:35357', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'35357', u'uri': u'http://192.0.2.51:35357/v2.0'}, u'GlanceRegistryAdmin': {u'uri_no_suffix': u'http://192.0.2.51:9191', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'9191', u'uri': u'http://192.0.2.51:9191'}, u'CinderInternal': {u'uri_no_suffix': u'http://192.0.2.51:8776', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8776', u'uri': u'http://192.0.2.51:8776/v1/%(tenant_id)s'}, u'SwiftS3Public': {u'uri_no_suffix': u'http://192.0.2.51:8080', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8080', u'uri': u'http://192.0.2.51:8080'}, u'NovaV3Public': {u'uri_no_suffix': u'http://192.0.2.51:8774', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8774', u'uri': u'http://192.0.2.51:8774/v3'}, u'SwiftPublic': {u'uri_no_suffix': u'http://192.0.2.51:8080', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8080', u'uri': u'http://192.0.2.51:8080/v1/AUTH_%(tenant_id)s'}, u'CinderAdmin': {u'uri_no_suffix': u'http://192.0.2.51:8776', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8776', u'uri': u'http://192.0.2.51:8776/v1/%(tenant_id)s'}, u'NovaVNCProxyInternal': {u'uri_no_suffix': u'http://192.0.2.51:6080', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'6080', u'uri': u'http://192.0.2.51:6080'}, u'KeystoneInternal': {u'uri_no_suffix': u'http://192.0.2.51:5000', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'5000', u'uri': u'http://192.0.2.51:5000/v2.0'}}",
          "NeutronEnableIsolatedMetadata": "False",
          "PurgeFirewallRules": "False",
          "NeutronEnableTunnelling": "True",
          "GlanceFilePcmkFstype": "nfs",
          "RabbitCookie": "******",
          "KeyName": "default",
          "MysqlRootPassword": "******",
          "MysqlClusterUniquePart": "24V843Vtte",
          "CinderPassword": "******",
          "NeutronTypeDrivers": "[u'vxlan', u'vlan', u'flat', u'gre']",
          "NodeIndex": "0",
          "CinderLVMLoopDeviceSize": "10280",
          "SwiftRingBuild": "True",
          "SchedulerHints": "{}",
          "CinderNfsServers": "[]",
          "ImageUpdatePolicy": "REBUILD_PRESERVE_EPHEMERAL",
          "MysqlInnodbBufferPoolSize": "0",
          "NeutronPluginExtensions": "[u'qos', u'port_security']",
          "RedisVirtualIPUri": "192.0.2.52",
          "AdminToken": "******",
          "SwiftHashSuffix": "******",
          "SwiftMinPartHours": "1",
          "KeystoneSSLCertificate": "",
          "NeutronL3HA": "True",
          "EnableGalera": "True",
          "MongoDbNoJournal": "False",
          "NeutronCorePlugin": "ml2",
          "CinderWorkers": "0",
          "CeilometerMeteringSecret": "******",
          "CinderEnableNfsBackend": "False",
          "HostnameMap": "{}",
          "MongoDbIPv6": "False",
          "OS::project_id": "9de7e9a9a2a242718cffa65dae677a33",
          "EnableSwiftStorage": "True",
          "PublicVirtualIP": "192.0.2.51",
          "NeutronEnableDHCPAgent": "True",
          "SnmpdReadonlyUserPassword": "******",
          "TimeZone": "UTC",
          "HorizonAllowedHosts": "[u'*']",
          "MysqlVirtualIP": "192.0.2.51",
          "NovaEnableDBPurge": "True",
          "RabbitClientPort": "5672",
          "SwiftProxyVirtualIP": "192.0.2.51",
          "KeystoneSSLCertificateKey": "******",
          "GlanceApiVirtualIP": "192.0.2.51",
          "KeystoneAdminApiVirtualIP": "192.0.2.51",
          "NeutronNetworkType": "[u'vxlan']",
          "CeilometerPassword": "******",
          "CinderBackendConfig": "{}",
          "NeutronMechanismDrivers": "[u'openvswitch']",
          "CeilometerStoreEvents": "False",
          "GlanceNotifierStrategy": "noop",
          "NeutronWorkers": "0",
          "MysqlVirtualIPUri": "192.0.2.51",
          "KeystoneCACertificate": "-----BEGIN CERTIFICATE-----\nMIIDNzCCAh+gAwIBAgIBATANBgkqhkiG9w0BAQUFADBTMQswCQYDVQQGEwJYWDEO\nMAwGA1UECBMFVW5zZXQxDjAMBgNVBAcTBVVuc2V0MQ4wDAYDVQQKEwVVbnNldDEU\nMBIGA1UEAxMLS2V5c3RvbmUgQ0EwHhcNMTYwNDEyMTUwOTQzWhcNMjYwNDEwMTUw\nOTQzWjBTMQswCQYDVQQGEwJYWDEOMAwGA1UECBMFVW5zZXQxDjAMBgNVBAcTBVVu\nc2V0MQ4wDAYDVQQKEwVVbnNldDEUMBIGA1UEAxMLS2V5c3RvbmUgQ0EwggEiMA0G\nCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQC1qd7Dvdrp0vw00HWxjqtCfqLS+/Oa\nr3ODws1I6TeaaBDGfrsvhQsGIEV2HXHw5XvZa5l6JgbbH+zcCiescMdIz6BkxrrG\n0bssq9eP7M9JPW1Ezo6LkMwPJiBpGWtw2EZ9pfIBH7AMR/cmweWmDi09sWy4O9q+\npB28luSmeSshqJZ6S1L6pqWdPQcvNFwpRFgZr3rRbyvVKS76GABMS30CGbT0h8Fj\nWwzGN1nCeSvTOHGvnOC714E81XApOViPz/ysrAc591mK5JORsFOXkH27OTMiWC9t\nb9lJQ7LZAU9EIywokLmPaW8wG+DCwgQs9KbHFOG2S7LfMhE/+Sh5L8n3AgMBAAGj\nFjAUMBIGA1UdEwEB/wQIMAYBAf8CAQAwDQYJKoZIhvcNAQEFBQADggEBAInsYCil\newgy2kwq4ArR3bHC7b5jYo/9SKylrsDrgUb38/iQZei3wooa2V+l1SbkznahwpI5\nqAqywzT8o9d8/LUji1631H3fuyCTb4UHX3SE/iw2UVmFVyWw0AMkj3gDJ9iVw8rR\nUvSwbdNySGZNl8BwETObLR4gyIpIY5Kq2ztitaxIg1xMlkDAe66trzCunt8Kt2Os\n8m3ObKr8TXbQMA6v01FigaipNjxXDyHPGv1S14PvQiguX6CiD02L5eXPjoJfLlOC\n/MjeK2f2YxvPf/BKUWbvekQApcCGayPpuiPM0z5oam1KDVsNMAAEE6a7UyAZs2NT\niEqras+fEAFIy3I=\n-----END CERTIFICATE-----\n",
          "NovaWorkers": "0",
          "NovaPassword": "******",
          "CloudDomain": "localdomain",
          "CinderNfsMountOptions": "",
          "RedisPassword": "******",
          "NeutronPublicInterfaceIP": "",
          "NovaIPv6": "False",
          "KeystoneWorkers": "0",
          "HAProxyStatsPassword": "zRe2ynBbCdjwYFPjyj6m2wUWQ",
          "NeutronServicePlugins": "[u'router', u'qos']",
          "NeutronAgentExtensions": "[u'qos']",
          "UpdateIdentifier": "",
          "HeatEnableDBPurge": "True",
          "RabbitIPv6": "False",
          "NeutronNetworkVLANRanges": "[u'datacentre:1:1000']"
        },
        "id": "04299fe4-e771-425d-9e2b-4ceca3458de1",
        "outputs": [
          {
            "output_value": '',
            "description": "IP address of the server in the storage_mgmt network",
            "output_key": "storage_mgmt_ip_address"
          },
          {
            "output_value": '',
            "description": "MD5 checksum of the TLS Certificate Modulus",
            "output_key": "tls_cert_modulus_md5"
          },
          {
            "output_value": '',
            "description": "IP address of the server in the storage network",
            "output_key": "storage_ip_address"
          },
          {
            "output_value": '',
            "description": "MD5 checksum of the TLS Key Modulus",
            "output_key": "tls_key_modulus_md5"
          },
          {
            "output_value": ",,,,",
            "description": "identifier which changes if the controller configuration may need re-applying",
            "output_key": "config_identifier"
          },
          {
            "output_value": '',
            "description": "Hostname of the server",
            "output_key": "hostname"
          },
          {
            "output_value": '',
            "description": "IP address of the server in the tenant network",
            "output_key": "tenant_ip_address"
          },
          {
            "output_value": '',
            "description": "IP address of the server in the external network",
            "output_key": "external_ip_address"
          },
          {
            "output_value": "r1z1-:%PORT%/d1",
            "description": "Swift device formatted for swift-ring-builder",
            "output_key": "swift_device"
          },
          {
            "output_value": {
              "ip": '',
              "name": ''
            },
            "description": "Node object in the format {ip: ..., name: ...} format that the corosync element expects\n",
            "output_key": "corosync_node"
          },
          {
            "output_value": " .localdomain ",
            "description": "Server's IP address and hostname in the /etc/hosts format\n",
            "output_key": "hosts_entry"
          },
          {
            "output_value": ":11211",
            "description": "Swift proxy-memcache value",
            "output_key": "swift_proxy_memcache"
          },
          {
            "output_value": "b041492b-36af-4a84-8480-2313e4885337",
            "description": "Heat resource handle for the Nova compute server",
            "output_key": "nova_server_resource"
          },
          {
            "output_value": '',
            "description": "IP address of the server in the internal_api network",
            "output_key": "internal_api_ip_address"
          },
          {
            "output_value": '',
            "description": "IP address of the server in the ctlplane network",
            "output_key": "ip_address"
          },
          {
            "output_value": '',
            "description": "IP address of the server in the management network",
            "output_key": "management_ip_address"
          }
        ],
        "template_description": "OpenStack controller node configured by Puppet.\n"
      }
    },
    "overcloud-Controller-d7iywdnu5uzr": {
      "description": "No description",
      "parent": "9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
      "stack_status_reason": "ResourceInError: resources[2].resources.Controller: Went to status ERROR due to \"Message: No valid host was found. There are not enough hosts available., Code: 500\"",
      "stack_name": "overcloud-Controller-d7iywdnu5uzr",
      "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
      "tags": '',
      "creation_time": "2016-04-12T15:10:04",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Controller-d7iywdnu5uzr/119696b0-92ac-44ab-85d6-614c68af3949",
          "rel": "self"
        }
      ],
      "updated_time": "2016-04-12T15:10:06",
      "stack_owner": "admin",
      "stack_status": "UPDATE_FAILED",
      "id": "119696b0-92ac-44ab-85d6-614c68af3949",
      "outputs": {
        "disable_rollback": 'true',
        "description": "No description",
        "parent": "9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
        "tags": '',
        "stack_name": "overcloud-Controller-d7iywdnu5uzr",
        "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
        "stack_status_reason": "ResourceInError: resources[2].resources.Controller: Went to status ERROR due to \"Message: No valid host was found. There are not enough hosts available., Code: 500\"",
        "creation_time": "2016-04-12T15:10:04",
        "links": [
          {
            "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Controller-d7iywdnu5uzr/119696b0-92ac-44ab-85d6-614c68af3949",
            "rel": "self"
          }
        ],
        "capabilities": [],
        "notification_topics": [],
        "updated_time": "2016-04-12T15:10:06",
        "timeout_mins": 14400,
        "stack_status": "UPDATE_FAILED",
        "stack_owner": "admin",
        "parameters": {
          "OS::project_id": "9de7e9a9a2a242718cffa65dae677a33",
          "OS::stack_id": "119696b0-92ac-44ab-85d6-614c68af3949",
          "OS::stack_name": "overcloud-Controller-d7iywdnu5uzr"
        },
        "id": "119696b0-92ac-44ab-85d6-614c68af3949",
        "outputs": [],
        "template_description": "No description"
      }
    },
    "overcloud-Controller-d7iywdnu5uzr-1-klhc6fwkxjt3-NodeUserData-5lya23guqvpw": {
      "description": "This is a default no-op template which provides empty user-data which can be passed to the OS::Nova::Server resources. This template can be replaced with a different implementation via the resource registry, such that deployers may customize their first-boot configuration.\n",
      "parent": "7ecb0624-6a40-449e-bb6c-e85b8bf2b733",
      "stack_status_reason": "Stack CREATE completed successfully",
      "stack_name": "overcloud-Controller-d7iywdnu5uzr-1-klhc6fwkxjt3-NodeUserData-5lya23guqvpw",
      "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
      "tags": '',
      "creation_time": "2016-04-12T15:10:09",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Controller-d7iywdnu5uzr-1-klhc6fwkxjt3-NodeUserData-5lya23guqvpw/5a489755-7326-4f1c-ade4-96a9b162ac44",
          "rel": "self"
        }
      ],
      "updated_time": '',
      "stack_owner": "admin",
      "stack_status": "CREATE_COMPLETE",
      "id": "5a489755-7326-4f1c-ade4-96a9b162ac44",
      "outputs": {
        "disable_rollback": 'true',
        "description": "This is a default no-op template which provides empty user-data which can be passed to the OS::Nova::Server resources. This template can be replaced with a different implementation via the resource registry, such that deployers may customize their first-boot configuration.\n",
        "parent": "7ecb0624-6a40-449e-bb6c-e85b8bf2b733",
        "tags": '',
        "stack_name": "overcloud-Controller-d7iywdnu5uzr-1-klhc6fwkxjt3-NodeUserData-5lya23guqvpw",
        "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
        "stack_status_reason": "Stack CREATE completed successfully",
        "creation_time": "2016-04-12T15:10:09",
        "links": [
          {
            "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Controller-d7iywdnu5uzr-1-klhc6fwkxjt3-NodeUserData-5lya23guqvpw/5a489755-7326-4f1c-ade4-96a9b162ac44",
            "rel": "self"
          }
        ],
        "capabilities": [],
        "notification_topics": [],
        "updated_time": '',
        "timeout_mins": 14400,
        "stack_status": "CREATE_COMPLETE",
        "stack_owner": "admin",
        "parameters": {
          "OS::project_id": "9de7e9a9a2a242718cffa65dae677a33",
          "OS::stack_id": "5a489755-7326-4f1c-ade4-96a9b162ac44",
          "OS::stack_name": "overcloud-Controller-d7iywdnu5uzr-1-klhc6fwkxjt3-NodeUserData-5lya23guqvpw"
        },
        "id": "5a489755-7326-4f1c-ade4-96a9b162ac44",
        "outputs": [
          {
            "output_value": "c13ea1dc-5798-406a-9295-ad64f9ecfe2e",
            "description": "No description given",
            "output_key": "OS::stack_id"
          }
        ],
        "template_description": "This is a default no-op template which provides empty user-data which can be passed to the OS::Nova::Server resources. This template can be replaced with a different implementation via the resource registry, such that deployers may customize their first-boot configuration.\n"
      }
    },
    "overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3-UpdateConfig-gfypsblpw6ci": {
      "description": "Software-config for performing package updates using yum\n",
      "parent": "59a5e87f-86f8-4998-acd4-622f97adcaa1",
      "stack_status_reason": "Stack CREATE completed successfully",
      "stack_name": "overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3-UpdateConfig-gfypsblpw6ci",
      "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
      "tags": '',
      "creation_time": "2016-04-12T15:10:06",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3-UpdateConfig-gfypsblpw6ci/a6fa0cac-66bd-4efb-b5a6-a37a8fc13f36",
          "rel": "self"
        }
      ],
      "updated_time": '',
      "stack_owner": "admin",
      "stack_status": "CREATE_COMPLETE",
      "id": "a6fa0cac-66bd-4efb-b5a6-a37a8fc13f36",
      "outputs": {
        "disable_rollback": 'true',
        "description": "Software-config for performing package updates using yum\n",
        "parent": "59a5e87f-86f8-4998-acd4-622f97adcaa1",
        "tags": '',
        "stack_name": "overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3-UpdateConfig-gfypsblpw6ci",
        "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
        "stack_status_reason": "Stack CREATE completed successfully",
        "creation_time": "2016-04-12T15:10:06",
        "links": [
          {
            "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3-UpdateConfig-gfypsblpw6ci/a6fa0cac-66bd-4efb-b5a6-a37a8fc13f36",
            "rel": "self"
          }
        ],
        "capabilities": [],
        "notification_topics": [],
        "updated_time": '',
        "timeout_mins": 14400,
        "stack_status": "CREATE_COMPLETE",
        "stack_owner": "admin",
        "parameters": {
          "OS::project_id": "9de7e9a9a2a242718cffa65dae677a33",
          "OS::stack_id": "a6fa0cac-66bd-4efb-b5a6-a37a8fc13f36",
          "OS::stack_name": "overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3-UpdateConfig-gfypsblpw6ci"
        },
        "id": "a6fa0cac-66bd-4efb-b5a6-a37a8fc13f36",
        "outputs": [
          {
            "output_value": "913aca44-764c-4550-bf7a-37ac24c53228",
            "description": "No description given",
            "output_key": "OS::stack_id"
          }
        ],
        "template_description": "Software-config for performing package updates using yum\n"
      }
    },
    "overcloud-Networks-zyubznagvv6c": {
      "description": "Create networks to split out Overcloud traffic",
      "parent": "9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
      "stack_status_reason": "Stack CREATE completed successfully",
      "stack_name": "overcloud-Networks-zyubznagvv6c",
      "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
      "tags": '',
      "creation_time": "2016-04-12T15:09:48",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Networks-zyubznagvv6c/bfb0f40b-3c67-4e65-8517-6cff9dfab7ff",
          "rel": "self"
        }
      ],
      "updated_time": '',
      "stack_owner": "admin",
      "stack_status": "CREATE_COMPLETE",
      "id": "bfb0f40b-3c67-4e65-8517-6cff9dfab7ff",
      "outputs": {
        "disable_rollback": 'true',
        "description": "Create networks to split out Overcloud traffic",
        "parent": "9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
        "tags": '',
        "stack_name": "overcloud-Networks-zyubznagvv6c",
        "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
        "stack_status_reason": "Stack CREATE completed successfully",
        "creation_time": "2016-04-12T15:09:48",
        "links": [
          {
            "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Networks-zyubznagvv6c/bfb0f40b-3c67-4e65-8517-6cff9dfab7ff",
            "rel": "self"
          }
        ],
        "capabilities": [],
        "notification_topics": [],
        "updated_time": '',
        "timeout_mins": 240,
        "stack_status": "CREATE_COMPLETE",
        "stack_owner": "admin",
        "parameters": {
          "OS::project_id": "9de7e9a9a2a242718cffa65dae677a33",
          "OS::stack_id": "bfb0f40b-3c67-4e65-8517-6cff9dfab7ff",
          "OS::stack_name": "overcloud-Networks-zyubznagvv6c"
        },
        "id": "bfb0f40b-3c67-4e65-8517-6cff9dfab7ff",
        "outputs": [],
        "template_description": "Create networks to split out Overcloud traffic"
      }
    },
    "overcloud-Networks-zyubznagvv6c-StorageMgmtNetwork-2bir7wn3igpz": {
      "description": "A stack which creates no network(s).",
      "parent": "bfb0f40b-3c67-4e65-8517-6cff9dfab7ff",
      "stack_status_reason": "Stack CREATE completed successfully",
      "stack_name": "overcloud-Networks-zyubznagvv6c-StorageMgmtNetwork-2bir7wn3igpz",
      "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
      "tags": '',
      "creation_time": "2016-04-12T15:09:50",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Networks-zyubznagvv6c-StorageMgmtNetwork-2bir7wn3igpz/c1df71aa-60c0-4302-8227-2584aa2b7cab",
          "rel": "self"
        }
      ],
      "updated_time": '',
      "stack_owner": "admin",
      "stack_status": "CREATE_COMPLETE",
      "id": "c1df71aa-60c0-4302-8227-2584aa2b7cab",
      "outputs": {
        "disable_rollback": 'true',
        "description": "A stack which creates no network(s).",
        "parent": "bfb0f40b-3c67-4e65-8517-6cff9dfab7ff",
        "tags": '',
        "stack_name": "overcloud-Networks-zyubznagvv6c-StorageMgmtNetwork-2bir7wn3igpz",
        "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
        "stack_status_reason": "Stack CREATE completed successfully",
        "creation_time": "2016-04-12T15:09:50",
        "links": [
          {
            "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Networks-zyubznagvv6c-StorageMgmtNetwork-2bir7wn3igpz/c1df71aa-60c0-4302-8227-2584aa2b7cab",
            "rel": "self"
          }
        ],
        "capabilities": [],
        "notification_topics": [],
        "updated_time": '',
        "timeout_mins": 240,
        "stack_status": "CREATE_COMPLETE",
        "stack_owner": "admin",
        "parameters": {
          "OS::project_id": "9de7e9a9a2a242718cffa65dae677a33",
          "OS::stack_id": "c1df71aa-60c0-4302-8227-2584aa2b7cab",
          "OS::stack_name": "overcloud-Networks-zyubznagvv6c-StorageMgmtNetwork-2bir7wn3igpz"
        },
        "id": "c1df71aa-60c0-4302-8227-2584aa2b7cab",
        "outputs": [],
        "template_description": "A stack which creates no network(s)."
      }
    },
    "overcloud-ObjectStorage-vmfquqg5aqwz": {
      "description": "No description",
      "parent": "9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
      "stack_status_reason": "Stack UPDATE completed successfully",
      "stack_name": "overcloud-ObjectStorage-vmfquqg5aqwz",
      "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
      "tags": '',
      "creation_time": "2016-04-12T15:09:53",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-ObjectStorage-vmfquqg5aqwz/578ad72f-1c10-4d6d-bbb5-f1e3faf3ca4f",
          "rel": "self"
        }
      ],
      "updated_time": "2016-04-12T15:09:53",
      "stack_owner": "admin",
      "stack_status": "UPDATE_COMPLETE",
      "id": "578ad72f-1c10-4d6d-bbb5-f1e3faf3ca4f",
      "outputs": {
        "disable_rollback": 'true',
        "description": "No description",
        "parent": "9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
        "tags": '',
        "stack_name": "overcloud-ObjectStorage-vmfquqg5aqwz",
        "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
        "stack_status_reason": "Stack UPDATE completed successfully",
        "creation_time": "2016-04-12T15:09:53",
        "links": [
          {
            "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-ObjectStorage-vmfquqg5aqwz/578ad72f-1c10-4d6d-bbb5-f1e3faf3ca4f",
            "rel": "self"
          }
        ],
        "capabilities": [],
        "notification_topics": [],
        "updated_time": "2016-04-12T15:09:53",
        "timeout_mins": 14400,
        "stack_status": "UPDATE_COMPLETE",
        "stack_owner": "admin",
        "parameters": {
          "OS::project_id": "9de7e9a9a2a242718cffa65dae677a33",
          "OS::stack_id": "578ad72f-1c10-4d6d-bbb5-f1e3faf3ca4f",
          "OS::stack_name": "overcloud-ObjectStorage-vmfquqg5aqwz"
        },
        "id": "578ad72f-1c10-4d6d-bbb5-f1e3faf3ca4f",
        "outputs": [],
        "template_description": "No description"
      }
    },
    "overcloud-Controller-d7iywdnu5uzr-0-j7rh7d75pr77-NodeUserData-hjxzuycgntle": {
      "description": "This is a default no-op template which provides empty user-data which can be passed to the OS::Nova::Server resources. This template can be replaced with a different implementation via the resource registry, such that deployers may customize their first-boot configuration.\n",
      "parent": "04299fe4-e771-425d-9e2b-4ceca3458de1",
      "stack_status_reason": "Stack CREATE completed successfully",
      "stack_name": "overcloud-Controller-d7iywdnu5uzr-0-j7rh7d75pr77-NodeUserData-hjxzuycgntle",
      "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
      "tags": '',
      "creation_time": "2016-04-12T15:10:11",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Controller-d7iywdnu5uzr-0-j7rh7d75pr77-NodeUserData-hjxzuycgntle/58fd623b-289f-4b71-ba5e-a9103c15d052",
          "rel": "self"
        }
      ],
      "updated_time": '',
      "stack_owner": "admin",
      "stack_status": "CREATE_COMPLETE",
      "id": "58fd623b-289f-4b71-ba5e-a9103c15d052",
      "outputs": {
        "disable_rollback": 'true',
        "description": "This is a default no-op template which provides empty user-data which can be passed to the OS::Nova::Server resources. This template can be replaced with a different implementation via the resource registry, such that deployers may customize their first-boot configuration.\n",
        "parent": "04299fe4-e771-425d-9e2b-4ceca3458de1",
        "tags": '',
        "stack_name": "overcloud-Controller-d7iywdnu5uzr-0-j7rh7d75pr77-NodeUserData-hjxzuycgntle",
        "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
        "stack_status_reason": "Stack CREATE completed successfully",
        "creation_time": "2016-04-12T15:10:11",
        "links": [
          {
            "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Controller-d7iywdnu5uzr-0-j7rh7d75pr77-NodeUserData-hjxzuycgntle/58fd623b-289f-4b71-ba5e-a9103c15d052",
            "rel": "self"
          }
        ],
        "capabilities": [],
        "notification_topics": [],
        "updated_time": '',
        "timeout_mins": 14400,
        "stack_status": "CREATE_COMPLETE",
        "stack_owner": "admin",
        "parameters": {
          "OS::project_id": "9de7e9a9a2a242718cffa65dae677a33",
          "OS::stack_id": "58fd623b-289f-4b71-ba5e-a9103c15d052",
          "OS::stack_name": "overcloud-Controller-d7iywdnu5uzr-0-j7rh7d75pr77-NodeUserData-hjxzuycgntle"
        },
        "id": "58fd623b-289f-4b71-ba5e-a9103c15d052",
        "outputs": [
          {
            "output_value": "465cc2bf-8738-41c3-959a-aefe4aaa2f2f",
            "description": "No description given",
            "output_key": "OS::stack_id"
          }
        ],
        "template_description": "This is a default no-op template which provides empty user-data which can be passed to the OS::Nova::Server resources. This template can be replaced with a different implementation via the resource registry, such that deployers may customize their first-boot configuration.\n"
      }
    },
    "overcloud-Controller-d7iywdnu5uzr-2-evqysybsnrrt-NodeAdminUserData-najecjhb77tx": {
      "description": "Uses cloud-init to create an additional user with a known name, in addition to the distro-default user created by the cloud-init default.\n",
      "parent": "e4dc37e4-d565-4453-8d6e-a830953eb803",
      "stack_status_reason": "Stack CREATE completed successfully",
      "stack_name": "overcloud-Controller-d7iywdnu5uzr-2-evqysybsnrrt-NodeAdminUserData-najecjhb77tx",
      "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
      "tags": '',
      "creation_time": "2016-04-12T15:10:14",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Controller-d7iywdnu5uzr-2-evqysybsnrrt-NodeAdminUserData-najecjhb77tx/0a831aaa-b8c3-46af-897f-5045407ca1bc",
          "rel": "self"
        }
      ],
      "updated_time": '',
      "stack_owner": "admin",
      "stack_status": "CREATE_COMPLETE",
      "id": "0a831aaa-b8c3-46af-897f-5045407ca1bc",
      "outputs": {
        "disable_rollback": 'true',
        "description": "Uses cloud-init to create an additional user with a known name, in addition to the distro-default user created by the cloud-init default.\n",
        "parent": "e4dc37e4-d565-4453-8d6e-a830953eb803",
        "tags": '',
        "stack_name": "overcloud-Controller-d7iywdnu5uzr-2-evqysybsnrrt-NodeAdminUserData-najecjhb77tx",
        "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
        "stack_status_reason": "Stack CREATE completed successfully",
        "creation_time": "2016-04-12T15:10:14",
        "links": [
          {
            "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Controller-d7iywdnu5uzr-2-evqysybsnrrt-NodeAdminUserData-najecjhb77tx/0a831aaa-b8c3-46af-897f-5045407ca1bc",
            "rel": "self"
          }
        ],
        "capabilities": [],
        "notification_topics": [],
        "updated_time": '',
        "timeout_mins": 14400,
        "stack_status": "CREATE_COMPLETE",
        "stack_owner": "admin",
        "parameters": {
          "node_admin_username": "heat-admin",
          "OS::project_id": "9de7e9a9a2a242718cffa65dae677a33",
          "OS::stack_id": "0a831aaa-b8c3-46af-897f-5045407ca1bc",
          "OS::stack_name": "overcloud-Controller-d7iywdnu5uzr-2-evqysybsnrrt-NodeAdminUserData-najecjhb77tx"
        },
        "id": "0a831aaa-b8c3-46af-897f-5045407ca1bc",
        "outputs": [
          {
            "output_value": "16640818-88eb-4603-9f26-b570a4f747e0",
            "description": "No description given",
            "output_key": "OS::stack_id"
          }
        ],
        "template_description": "Uses cloud-init to create an additional user with a known name, in addition to the distro-default user created by the cloud-init default.\n"
      }
    },
    "overcloud-Compute-56idrrd2a77s": {
      "description": "No description",
      "parent": "9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
      "stack_status_reason": "ResourceInError: resources[0].resources.NovaCompute: Went to status ERROR due to \"Message: No valid host was found. There are not enough hosts available., Code: 500\"",
      "stack_name": "overcloud-Compute-56idrrd2a77s",
      "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
      "tags": '',
      "creation_time": "2016-04-12T15:10:02",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s/d3c93c64-778f-4cec-a5a8-062de076c0b6",
          "rel": "self"
        }
      ],
      "updated_time": "2016-04-12T15:10:03",
      "stack_owner": "admin",
      "stack_status": "UPDATE_FAILED",
      "id": "d3c93c64-778f-4cec-a5a8-062de076c0b6",
      "outputs": {
        "disable_rollback": 'true',
        "description": "No description",
        "parent": "9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
        "tags": '',
        "stack_name": "overcloud-Compute-56idrrd2a77s",
        "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
        "stack_status_reason": "ResourceInError: resources[0].resources.NovaCompute: Went to status ERROR due to \"Message: No valid host was found. There are not enough hosts available., Code: 500\"",
        "creation_time": "2016-04-12T15:10:02",
        "links": [
          {
            "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s/d3c93c64-778f-4cec-a5a8-062de076c0b6",
            "rel": "self"
          }
        ],
        "capabilities": [],
        "notification_topics": [],
        "updated_time": "2016-04-12T15:10:03",
        "timeout_mins": 14400,
        "stack_status": "UPDATE_FAILED",
        "stack_owner": "admin",
        "parameters": {
          "OS::project_id": "9de7e9a9a2a242718cffa65dae677a33",
          "OS::stack_id": "d3c93c64-778f-4cec-a5a8-062de076c0b6",
          "OS::stack_name": "overcloud-Compute-56idrrd2a77s"
        },
        "id": "d3c93c64-778f-4cec-a5a8-062de076c0b6",
        "outputs": [],
        "template_description": "No description"
      }
    },
    "overcloud-InternalApiVirtualIP-ln4exmem57yc": {
      "description": "Returns the control plane port (provisioning network) as the ip_address.\n",
      "parent": "9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
      "stack_status_reason": "Stack CREATE completed successfully",
      "stack_name": "overcloud-InternalApiVirtualIP-ln4exmem57yc",
      "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
      "tags": '',
      "creation_time": "2016-04-12T15:09:56",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-InternalApiVirtualIP-ln4exmem57yc/c8e8f2d2-d3f3-4cf2-9d31-a1cf5c00b93d",
          "rel": "self"
        }
      ],
      "updated_time": '',
      "stack_owner": "admin",
      "stack_status": "CREATE_COMPLETE",
      "id": "c8e8f2d2-d3f3-4cf2-9d31-a1cf5c00b93d",
      "outputs": {
        "disable_rollback": 'true',
        "description": "Returns the control plane port (provisioning network) as the ip_address.\n",
        "parent": "9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
        "tags": '',
        "stack_name": "overcloud-InternalApiVirtualIP-ln4exmem57yc",
        "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
        "stack_status_reason": "Stack CREATE completed successfully",
        "creation_time": "2016-04-12T15:09:56",
        "links": [
          {
            "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-InternalApiVirtualIP-ln4exmem57yc/c8e8f2d2-d3f3-4cf2-9d31-a1cf5c00b93d",
            "rel": "self"
          }
        ],
        "capabilities": [],
        "notification_topics": [],
        "updated_time": '',
        "timeout_mins": 240,
        "stack_status": "CREATE_COMPLETE",
        "stack_owner": "admin",
        "parameters": {
          "FixedIPs": "[]",
          "OS::project_id": "9de7e9a9a2a242718cffa65dae677a33",
          "ControlPlaneNetwork": "ctlplane",
          "OS::stack_id": "c8e8f2d2-d3f3-4cf2-9d31-a1cf5c00b93d",
          "OS::stack_name": "overcloud-InternalApiVirtualIP-ln4exmem57yc",
          "NodeIndex": "0",
          "ControlPlaneIP": "192.0.2.51",
          "ControlPlaneSubnetCidr": "24",
          "ServiceName": "",
          "PortName": "internal_api_virtual_ip",
          "IPPool": "{}",
          "NetworkName": "internal_api"
        },
        "id": "c8e8f2d2-d3f3-4cf2-9d31-a1cf5c00b93d",
        "outputs": [
          {
            "output_value": "192.0.2.51/24",
            "description": "IP/Subnet CIDR for the pass thru network IP",
            "output_key": "ip_subnet"
          },
          {
            "output_value": "192.0.2.51",
            "description": "pass thru network IP (for compatibility with vip_v6.yaml)",
            "output_key": "ip_address_uri"
          },
          {
            "output_value": "192.0.2.51",
            "description": "pass thru network IP",
            "output_key": "ip_address"
          }
        ],
        "template_description": "Returns the control plane port (provisioning network) as the ip_address.\n"
      }
    },
    "overcloud-Controller-d7iywdnu5uzr-2-evqysybsnrrt": {
      "description": "OpenStack controller node configured by Puppet.\n",
      "parent": "119696b0-92ac-44ab-85d6-614c68af3949",
      "stack_status_reason": "Resource CREATE failed: ResourceInError: resources.Controller: Went to status ERROR due to \"Message: No valid host was found. There are not enough hosts available., Code: 500\"",
      "stack_name": "overcloud-Controller-d7iywdnu5uzr-2-evqysybsnrrt",
      "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
      "tags": '',
      "creation_time": "2016-04-12T15:10:10",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Controller-d7iywdnu5uzr-2-evqysybsnrrt/e4dc37e4-d565-4453-8d6e-a830953eb803",
          "rel": "self"
        }
      ],
      "updated_time": '',
      "stack_owner": "admin",
      "stack_status": "CREATE_FAILED",
      "id": "e4dc37e4-d565-4453-8d6e-a830953eb803",
      "outputs": {
        "disable_rollback": 'true',
        "description": "OpenStack controller node configured by Puppet.\n",
        "parent": "119696b0-92ac-44ab-85d6-614c68af3949",
        "tags": '',
        "stack_name": "overcloud-Controller-d7iywdnu5uzr-2-evqysybsnrrt",
        "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
        "stack_status_reason": "Resource CREATE failed: ResourceInError: resources.Controller: Went to status ERROR due to \"Message: No valid host was found. There are not enough hosts available., Code: 500\"",
        "creation_time": "2016-04-12T15:10:10",
        "links": [
          {
            "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Controller-d7iywdnu5uzr-2-evqysybsnrrt/e4dc37e4-d565-4453-8d6e-a830953eb803",
            "rel": "self"
          }
        ],
        "capabilities": [],
        "notification_topics": [],
        "updated_time": '',
        "timeout_mins": 14400,
        "stack_status": "CREATE_FAILED",
        "stack_owner": "admin",
        "parameters": {
          "EnableCephStorage": "False",
          "NeutronPublicInterfaceRawDevice": "",
          "GlanceWorkers": "0",
          "NetworkDeploymentActions": "[u'CREATE']",
          "NtpServer": "[u'north-america.pool.ntp.org']",
          "NeutronTenantMtu": "1400",
          "NeutronDhcpAgentsPerNetwork": "3",
          "HeatApiVirtualIPUri": "192.0.2.51",
          "NeutronFlatNetworks": "[u'datacentre']",
          "EnablePackageInstall": "False",
          "CorosyncIPv6": "False",
          "NeutronAgentMode": "dvr_snat",
          "GlancePassword": "******",
          "NeutronTunnelIdRanges": "[u'1:4094']",
          "CinderEnableRbdBackend": "False",
          "SwiftReplicas": "3",
          "NeutronPublicInterfaceTag": "",
          "FencingConfig": "{}",
          "MemcachedIPv6": "False",
          "KeystoneSigningCertificate": "-----BEGIN CERTIFICATE-----\nMIIDJDCCAgygAwIBAgIBAjANBgkqhkiG9w0BAQUFADBTMQswCQYDVQQGEwJYWDEO\nMAwGA1UECBMFVW5zZXQxDjAMBgNVBAcTBVVuc2V0MQ4wDAYDVQQKEwVVbnNldDEU\nMBIGA1UEAxMLS2V5c3RvbmUgQ0EwHhcNMTYwNDEyMTUwOTQzWhcNMjYwNDEwMTUw\nOTQzWjBYMQswCQYDVQQGEwJYWDEOMAwGA1UECBMFVW5zZXQxDjAMBgNVBAcTBVVu\nc2V0MQ4wDAYDVQQKEwVVbnNldDEZMBcGA1UEAxMQS2V5c3RvbmUgU2lnbmluZzCC\nASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBALqFj/1OTcqwfAfkXnm9XYJ0\nk85O+JGDfWuygeS8GBP99G6FMf/xPb3DeJTzEbm2xnVn3oLyBx9eNHg28Pz+B1me\n1zJJNmNTHYY22gQ9QTNuo/2fnyehzlIB7mzeWIqbuWaeabg3FI8ujfN9l2/jxw5c\nnscakOU1/NKQOcjXgIBP7jr9l9vfLQOvZ4oPeYwkAn0li9xYhpVE70fsvE57J1JC\nr/WkL6ExZCJA78+PC5Oq1WGB86fUCSdoT0H0uDuiOgsohfFBpaL0MAXO//+L2q+Y\nsZGcgVqgPaMW97vP3dedIMYkxHbQgVUwKHUGbL9GvIrkCzmPx0z4AqbeadpyMzUC\nAwEAATANBgkqhkiG9w0BAQUFAAOCAQEAj6loZnn6GlHqpJL34es9+AT6yLaKq6py\nQtnMl3uypwO1u7opMxS0Vhluw/IpWtaiRIlfboJ9IhrDcZm6rMtn/sjoB2XbLnGI\n9v3BSj+0lGyTrP8tV4FEFrKXG46SqcU3KeHlfk5mL3JB7XzOsPE4V+IcabPg/cKt\negXPAqKOzIGKc8fbGm/q7eMI+NtP4sKgIPJOxneMKYbcHcq6sY3UmiXVMYJ1PItD\n/tE2x2tVotnnYoU1SV9wPgkfGNY2xxdO31+DgzhNA45M/31PLm98LO1U7DpiAxLu\n/tEbVyspUJkUSEmQfhQ9LoHuX4BLObJU7ZoqHzA9xFmg3e0HwAfRqA==\n-----END CERTIFICATE-----\n",
          "ControllerIPs": "{}",
          "ServiceNetMap": "{u'NovaVncProxyNetwork': u'internal_api', u'CinderApiNetwork': u'internal_api', u'NovaApiNetwork': u'internal_api', u'CeilometerApiNetwork': u'internal_api', u'CephStorageHostnameResolveNetwork': u'storage', u'SwiftMgmtNetwork': u'storage_mgmt', u'MemcachedNetwork': u'internal_api', u'RabbitMqNetwork': u'internal_api', u'KeystoneAdminApiNetwork': u'ctlplane', u'SwiftProxyNetwork': u'storage', u'NeutronTenantNetwork': u'tenant', u'CephClusterNetwork': u'storage_mgmt', u'NovaMetadataNetwork': u'internal_api', u'ControllerHostnameResolveNetwork': u'internal_api', u'NeutronApiNetwork': u'internal_api', u'GlanceApiNetwork': u'storage', u'ObjectStorageHostnameResolveNetwork': u'internal_api', u'KeystonePublicApiNetwork': u'internal_api', u'HeatApiNetwork': u'internal_api', u'GlanceRegistryNetwork': u'internal_api', u'RedisNetwork': u'internal_api', u'MysqlNetwork': u'internal_api', u'BlockStorageHostnameResolveNetwork': u'internal_api', u'ComputeHostnameResolveNetwork': u'internal_api', u'CephPublicNetwork': u'storage', u'MongoDbNetwork': u'internal_api', u'HorizonNetwork': u'internal_api', u'CinderIscsiNetwork': u'storage'}",
          "SnmpdReadonlyUserName": "ro_snmp_user",
          "ManageFirewall": "False",
          "CinderISCSIHelper": "lioadm",
          "CeilometerWorkers": "0",
          "NeutronEnableMetadataAgent": "True",
          "RabbitPassword": "******",
          "NeutronApiVirtualIP": "192.0.2.51",
          "PublicVirtualInterface": "br-ex",
          "Debug": "",
          "NeutronPublicInterface": "nic1",
          "GlanceFilePcmkDevice": "",
          "EnableFencing": "False",
          "SoftwareConfigTransport": "POLL_SERVER_CFN",
          "SwiftMountCheck": "False",
          "RabbitFDLimit": "16384",
          "HorizonSecret": "******",
          "VirtualIP": "192.0.2.51",
          "SwiftPassword": "******",
          "NeutronMetadataProxySharedSecret": "******",
          "Flavor": "control",
          "CinderApiVirtualIP": "192.0.2.51",
          "KeystonePublicApiVirtualIP": "192.0.2.51",
          "HAProxySyslogAddress": "/dev/log",
          "SwiftPartPower": "10",
          "HeatApiVirtualIP": "192.0.2.51",
          "KeystoneNotificationFormat": "basic",
          "NeutronPublicInterfaceDefaultRoute": "",
          "HeatPassword": "******",
          "InstanceNameTemplate": "instance-%08x",
          "RedisVirtualIP": "192.0.2.52",
          "ControllerExtraConfig": "{}",
          "ControlVirtualInterface": "br-ex",
          "HeatStackDomainAdminPassword": "******",
          "OS::stack_name": "overcloud-Controller-d7iywdnu5uzr-2-evqysybsnrrt",
          "NeutronEnableOVSAgent": "True",
          "GlanceRegistryVirtualIP": "192.0.2.51",
          "PcsdPassword": "******",
          "SwiftWorkers": "0",
          "CinderEnableIscsiBackend": "True",
          "EnableLoadBalancer": "True",
          "KeystoneNotificationDriver": "[u'messaging']",
          "NeutronEnableL3Agent": "True",
          "NeutronVniRanges": "[u'1:4094']",
          "GlanceBackend": "swift",
          "RabbitClientUseSSL": "False",
          "NeutronAllowL3AgentFailover": "False",
          "NeutronEnableL2Pop": "False",
          "HeatAuthEncryptionKey": "******",
          "UpgradeLevelNovaCompute": "",
          "GlanceFilePcmkOptions": "",
          "RabbitUserName": "guest",
          "NovaApiVirtualIP": "192.0.2.51",
          "HeatWorkers": "0",
          "GlanceLogFile": "",
          "NeutronExternalNetworkBridge": "br-ex",
          "CeilometerBackend": "mongodb",
          "CeilometerApiVirtualIP": "192.0.2.51",
          "OS::stack_id": "e4dc37e4-d565-4453-8d6e-a830953eb803",
          "AdminPassword": "******",
          "NeutronDVR": "False",
          "Image": "overcloud-full",
          "ExtraConfig": "{}",
          "KeystoneSigningKey": "******",
          "KeystoneEnableDBPurge": "True",
          "CinderEnableDBPurge": "True",
          "NeutronDnsmasqOptions": "dhcp-option-force=26,1400",
          "MysqlMaxConnections": "4096",
          "NeutronTunnelTypes": "[u'vxlan']",
          "ServerMetadata": "{}",
          "Hostname": "overcloud-controller-2",
          "GlanceFilePcmkManage": "False",
          "NeutronPassword": "******",
          "NeutronBridgeMappings": "[u'datacentre:br-ex']",
          "HAProxyStatsUser": "admin",
          "EndpointMap": "{u'GlanceInternal': {u'uri_no_suffix': u'http://192.0.2.51:9292', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'9292', u'uri': u'http://192.0.2.51:9292'}, u'NovaEC2Public': {u'uri_no_suffix': u'http://192.0.2.51:8773', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8773', u'uri': u'http://192.0.2.51:8773/services/Cloud'}, u'HeatPublic': {u'uri_no_suffix': u'http://192.0.2.51:8004', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8004', u'uri': u'http://192.0.2.51:8004/v1/%(tenant_id)s'}, u'KeystonePublic': {u'uri_no_suffix': u'http://192.0.2.51:5000', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'5000', u'uri': u'http://192.0.2.51:5000/v2.0'}, u'HeatAdmin': {u'uri_no_suffix': u'http://192.0.2.51:8004', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8004', u'uri': u'http://192.0.2.51:8004/v1/%(tenant_id)s'}, u'NovaEC2Admin': {u'uri_no_suffix': u'http://192.0.2.51:8773', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8773', u'uri': u'http://192.0.2.51:8773/services/Admin'}, u'CeilometerAdmin': {u'uri_no_suffix': u'http://192.0.2.51:8777', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8777', u'uri': u'http://192.0.2.51:8777'}, u'GlanceAdmin': {u'uri_no_suffix': u'http://192.0.2.51:9292', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'9292', u'uri': u'http://192.0.2.51:9292'}, u'SwiftS3Internal': {u'uri_no_suffix': u'http://192.0.2.51:8080', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8080', u'uri': u'http://192.0.2.51:8080'}, u'CinderV2Internal': {u'uri_no_suffix': u'http://192.0.2.51:8776', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8776', u'uri': u'http://192.0.2.51:8776/v2/%(tenant_id)s'}, u'NovaVNCProxyAdmin': {u'uri_no_suffix': u'http://192.0.2.51:6080', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'6080', u'uri': u'http://192.0.2.51:6080'}, u'HeatInternal': {u'uri_no_suffix': u'http://192.0.2.51:8004', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8004', u'uri': u'http://192.0.2.51:8004/v1/%(tenant_id)s'}, u'NovaV3Admin': {u'uri_no_suffix': u'http://192.0.2.51:8774', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8774', u'uri': u'http://192.0.2.51:8774/v3'}, u'NeutronPublic': {u'uri_no_suffix': u'http://192.0.2.51:9696', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'9696', u'uri': u'http://192.0.2.51:9696'}, u'CinderPublic': {u'uri_no_suffix': u'http://192.0.2.51:8776', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8776', u'uri': u'http://192.0.2.51:8776/v1/%(tenant_id)s'}, u'HorizonPublic': {u'uri_no_suffix': u'http://192.0.2.51:80', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'80', u'uri': u'http://192.0.2.51:80/dashboard'}, u'KeystoneEC2': {u'uri_no_suffix': u'http://192.0.2.51:5000', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'5000', u'uri': u'http://192.0.2.51:5000/v2.0/ec2tokens'}, u'GlancePublic': {u'uri_no_suffix': u'http://192.0.2.51:9292', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'9292', u'uri': u'http://192.0.2.51:9292'}, u'CinderV2Admin': {u'uri_no_suffix': u'http://192.0.2.51:8776', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8776', u'uri': u'http://192.0.2.51:8776/v2/%(tenant_id)s'}, u'GlanceRegistryPublic': {u'uri_no_suffix': u'http://192.0.2.51:9191', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'9191', u'uri': u'http://192.0.2.51:9191'}, u'NeutronAdmin': {u'uri_no_suffix': u'http://192.0.2.51:9696', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'9696', u'uri': u'http://192.0.2.51:9696'}, u'SwiftInternal': {u'uri_no_suffix': u'http://192.0.2.51:8080', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8080', u'uri': u'http://192.0.2.51:8080/v1/AUTH_%(tenant_id)s'}, u'NovaVNCProxyPublic': {u'uri_no_suffix': u'http://192.0.2.51:6080', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'6080', u'uri': u'http://192.0.2.51:6080'}, u'CeilometerInternal': {u'uri_no_suffix': u'http://192.0.2.51:8777', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8777', u'uri': u'http://192.0.2.51:8777'}, u'NovaInternal': {u'uri_no_suffix': u'http://192.0.2.51:8774', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8774', u'uri': u'http://192.0.2.51:8774/v2.1/%(tenant_id)s'}, u'GlanceRegistryInternal': {u'uri_no_suffix': u'http://192.0.2.51:9191', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'9191', u'uri': u'http://192.0.2.51:9191'}, u'NovaV3Internal': {u'uri_no_suffix': u'http://192.0.2.51:8774', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8774', u'uri': u'http://192.0.2.51:8774/v3'}, u'NovaAdmin': {u'uri_no_suffix': u'http://192.0.2.51:8774', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8774', u'uri': u'http://192.0.2.51:8774/v2.1/%(tenant_id)s'}, u'NovaEC2Internal': {u'uri_no_suffix': u'http://192.0.2.51:8773', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8773', u'uri': u'http://192.0.2.51:8773/services/Cloud'}, u'SwiftAdmin': {u'uri_no_suffix': u'http://192.0.2.51:8080', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8080', u'uri': u'http://192.0.2.51:8080'}, u'NeutronInternal': {u'uri_no_suffix': u'http://192.0.2.51:9696', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'9696', u'uri': u'http://192.0.2.51:9696'}, u'NovaPublic': {u'uri_no_suffix': u'http://192.0.2.51:8774', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8774', u'uri': u'http://192.0.2.51:8774/v2.1/%(tenant_id)s'}, u'SwiftS3Admin': {u'uri_no_suffix': u'http://192.0.2.51:8080', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8080', u'uri': u'http://192.0.2.51:8080'}, u'CeilometerPublic': {u'uri_no_suffix': u'http://192.0.2.51:8777', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8777', u'uri': u'http://192.0.2.51:8777'}, u'CinderV2Public': {u'uri_no_suffix': u'http://192.0.2.51:8776', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8776', u'uri': u'http://192.0.2.51:8776/v2/%(tenant_id)s'}, u'KeystoneAdmin': {u'uri_no_suffix': u'http://192.0.2.51:35357', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'35357', u'uri': u'http://192.0.2.51:35357/v2.0'}, u'GlanceRegistryAdmin': {u'uri_no_suffix': u'http://192.0.2.51:9191', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'9191', u'uri': u'http://192.0.2.51:9191'}, u'CinderInternal': {u'uri_no_suffix': u'http://192.0.2.51:8776', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8776', u'uri': u'http://192.0.2.51:8776/v1/%(tenant_id)s'}, u'SwiftS3Public': {u'uri_no_suffix': u'http://192.0.2.51:8080', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8080', u'uri': u'http://192.0.2.51:8080'}, u'NovaV3Public': {u'uri_no_suffix': u'http://192.0.2.51:8774', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8774', u'uri': u'http://192.0.2.51:8774/v3'}, u'SwiftPublic': {u'uri_no_suffix': u'http://192.0.2.51:8080', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8080', u'uri': u'http://192.0.2.51:8080/v1/AUTH_%(tenant_id)s'}, u'CinderAdmin': {u'uri_no_suffix': u'http://192.0.2.51:8776', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'8776', u'uri': u'http://192.0.2.51:8776/v1/%(tenant_id)s'}, u'NovaVNCProxyInternal': {u'uri_no_suffix': u'http://192.0.2.51:6080', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'6080', u'uri': u'http://192.0.2.51:6080'}, u'KeystoneInternal': {u'uri_no_suffix': u'http://192.0.2.51:5000', u'host': u'192.0.2.51', u'protocol': u'http', u'port': u'5000', u'uri': u'http://192.0.2.51:5000/v2.0'}}",
          "NeutronEnableIsolatedMetadata": "False",
          "PurgeFirewallRules": "False",
          "NeutronEnableTunnelling": "True",
          "GlanceFilePcmkFstype": "nfs",
          "RabbitCookie": "******",
          "KeyName": "default",
          "MysqlRootPassword": "******",
          "MysqlClusterUniquePart": "24V843Vtte",
          "CinderPassword": "******",
          "NeutronTypeDrivers": "[u'vxlan', u'vlan', u'flat', u'gre']",
          "NodeIndex": "2",
          "CinderLVMLoopDeviceSize": "10280",
          "SwiftRingBuild": "True",
          "SchedulerHints": "{}",
          "CinderNfsServers": "[]",
          "ImageUpdatePolicy": "REBUILD_PRESERVE_EPHEMERAL",
          "MysqlInnodbBufferPoolSize": "0",
          "NeutronPluginExtensions": "[u'qos', u'port_security']",
          "RedisVirtualIPUri": "192.0.2.52",
          "AdminToken": "******",
          "SwiftHashSuffix": "******",
          "SwiftMinPartHours": "1",
          "KeystoneSSLCertificate": "",
          "NeutronL3HA": "True",
          "EnableGalera": "True",
          "MongoDbNoJournal": "False",
          "NeutronCorePlugin": "ml2",
          "CinderWorkers": "0",
          "CeilometerMeteringSecret": "******",
          "CinderEnableNfsBackend": "False",
          "HostnameMap": "{}",
          "MongoDbIPv6": "False",
          "OS::project_id": "9de7e9a9a2a242718cffa65dae677a33",
          "EnableSwiftStorage": "True",
          "PublicVirtualIP": "192.0.2.51",
          "NeutronEnableDHCPAgent": "True",
          "SnmpdReadonlyUserPassword": "******",
          "TimeZone": "UTC",
          "HorizonAllowedHosts": "[u'*']",
          "MysqlVirtualIP": "192.0.2.51",
          "NovaEnableDBPurge": "True",
          "RabbitClientPort": "5672",
          "SwiftProxyVirtualIP": "192.0.2.51",
          "KeystoneSSLCertificateKey": "******",
          "GlanceApiVirtualIP": "192.0.2.51",
          "KeystoneAdminApiVirtualIP": "192.0.2.51",
          "NeutronNetworkType": "[u'vxlan']",
          "CeilometerPassword": "******",
          "CinderBackendConfig": "{}",
          "NeutronMechanismDrivers": "[u'openvswitch']",
          "CeilometerStoreEvents": "False",
          "GlanceNotifierStrategy": "noop",
          "NeutronWorkers": "0",
          "MysqlVirtualIPUri": "192.0.2.51",
          "KeystoneCACertificate": "-----BEGIN CERTIFICATE-----\nMIIDNzCCAh+gAwIBAgIBATANBgkqhkiG9w0BAQUFADBTMQswCQYDVQQGEwJYWDEO\nMAwGA1UECBMFVW5zZXQxDjAMBgNVBAcTBVVuc2V0MQ4wDAYDVQQKEwVVbnNldDEU\nMBIGA1UEAxMLS2V5c3RvbmUgQ0EwHhcNMTYwNDEyMTUwOTQzWhcNMjYwNDEwMTUw\nOTQzWjBTMQswCQYDVQQGEwJYWDEOMAwGA1UECBMFVW5zZXQxDjAMBgNVBAcTBVVu\nc2V0MQ4wDAYDVQQKEwVVbnNldDEUMBIGA1UEAxMLS2V5c3RvbmUgQ0EwggEiMA0G\nCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQC1qd7Dvdrp0vw00HWxjqtCfqLS+/Oa\nr3ODws1I6TeaaBDGfrsvhQsGIEV2HXHw5XvZa5l6JgbbH+zcCiescMdIz6BkxrrG\n0bssq9eP7M9JPW1Ezo6LkMwPJiBpGWtw2EZ9pfIBH7AMR/cmweWmDi09sWy4O9q+\npB28luSmeSshqJZ6S1L6pqWdPQcvNFwpRFgZr3rRbyvVKS76GABMS30CGbT0h8Fj\nWwzGN1nCeSvTOHGvnOC714E81XApOViPz/ysrAc591mK5JORsFOXkH27OTMiWC9t\nb9lJQ7LZAU9EIywokLmPaW8wG+DCwgQs9KbHFOG2S7LfMhE/+Sh5L8n3AgMBAAGj\nFjAUMBIGA1UdEwEB/wQIMAYBAf8CAQAwDQYJKoZIhvcNAQEFBQADggEBAInsYCil\newgy2kwq4ArR3bHC7b5jYo/9SKylrsDrgUb38/iQZei3wooa2V+l1SbkznahwpI5\nqAqywzT8o9d8/LUji1631H3fuyCTb4UHX3SE/iw2UVmFVyWw0AMkj3gDJ9iVw8rR\nUvSwbdNySGZNl8BwETObLR4gyIpIY5Kq2ztitaxIg1xMlkDAe66trzCunt8Kt2Os\n8m3ObKr8TXbQMA6v01FigaipNjxXDyHPGv1S14PvQiguX6CiD02L5eXPjoJfLlOC\n/MjeK2f2YxvPf/BKUWbvekQApcCGayPpuiPM0z5oam1KDVsNMAAEE6a7UyAZs2NT\niEqras+fEAFIy3I=\n-----END CERTIFICATE-----\n",
          "NovaWorkers": "0",
          "NovaPassword": "******",
          "CloudDomain": "localdomain",
          "CinderNfsMountOptions": "",
          "RedisPassword": "******",
          "NeutronPublicInterfaceIP": "",
          "NovaIPv6": "False",
          "KeystoneWorkers": "0",
          "HAProxyStatsPassword": "zRe2ynBbCdjwYFPjyj6m2wUWQ",
          "NeutronServicePlugins": "[u'router', u'qos']",
          "NeutronAgentExtensions": "[u'qos']",
          "UpdateIdentifier": "",
          "HeatEnableDBPurge": "True",
          "RabbitIPv6": "False",
          "NeutronNetworkVLANRanges": "[u'datacentre:1:1000']"
        },
        "id": "e4dc37e4-d565-4453-8d6e-a830953eb803",
        "outputs": [
          {
            "output_value": '',
            "description": "IP address of the server in the storage_mgmt network",
            "output_key": "storage_mgmt_ip_address"
          },
          {
            "output_value": '',
            "description": "MD5 checksum of the TLS Certificate Modulus",
            "output_key": "tls_cert_modulus_md5"
          },
          {
            "output_value": '',
            "description": "IP address of the server in the storage network",
            "output_key": "storage_ip_address"
          },
          {
            "output_value": '',
            "description": "MD5 checksum of the TLS Key Modulus",
            "output_key": "tls_key_modulus_md5"
          },
          {
            "output_value": ",,,,",
            "description": "identifier which changes if the controller configuration may need re-applying",
            "output_key": "config_identifier"
          },
          {
            "output_value": '',
            "description": "Hostname of the server",
            "output_key": "hostname"
          },
          {
            "output_value": '',
            "description": "IP address of the server in the tenant network",
            "output_key": "tenant_ip_address"
          },
          {
            "output_value": '',
            "description": "IP address of the server in the external network",
            "output_key": "external_ip_address"
          },
          {
            "output_value": "r1z1-:%PORT%/d1",
            "description": "Swift device formatted for swift-ring-builder",
            "output_key": "swift_device"
          },
          {
            "output_value": {
              "ip": '',
              "name": ''
            },
            "description": "Node object in the format {ip: ..., name: ...} format that the corosync element expects\n",
            "output_key": "corosync_node"
          },
          {
            "output_value": " .localdomain ",
            "description": "Server's IP address and hostname in the /etc/hosts format\n",
            "output_key": "hosts_entry"
          },
          {
            "output_value": ":11211",
            "description": "Swift proxy-memcache value",
            "output_key": "swift_proxy_memcache"
          },
          {
            "output_value": "7a6d9cb4-679e-46dd-ab85-1dded96737b3",
            "description": "Heat resource handle for the Nova compute server",
            "output_key": "nova_server_resource"
          },
          {
            "output_value": '',
            "description": "IP address of the server in the internal_api network",
            "output_key": "internal_api_ip_address"
          },
          {
            "output_value": '',
            "description": "IP address of the server in the ctlplane network",
            "output_key": "ip_address"
          },
          {
            "output_value": '',
            "description": "IP address of the server in the management network",
            "output_key": "management_ip_address"
          }
        ],
        "template_description": "OpenStack controller node configured by Puppet.\n"
      }
    },
    "overcloud-Networks-zyubznagvv6c-ManagementNetwork-tip34zbqkbzx": {
      "description": "A stack which creates no network(s).",
      "parent": "bfb0f40b-3c67-4e65-8517-6cff9dfab7ff",
      "stack_status_reason": "Stack CREATE completed successfully",
      "stack_name": "overcloud-Networks-zyubznagvv6c-ManagementNetwork-tip34zbqkbzx",
      "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
      "tags": '',
      "creation_time": "2016-04-12T15:09:50",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Networks-zyubznagvv6c-ManagementNetwork-tip34zbqkbzx/3589cd45-fbff-4209-8dfe-93ae426d2579",
          "rel": "self"
        }
      ],
      "updated_time": '',
      "stack_owner": "admin",
      "stack_status": "CREATE_COMPLETE",
      "id": "3589cd45-fbff-4209-8dfe-93ae426d2579",
      "outputs": {
        "disable_rollback": 'true',
        "description": "A stack which creates no network(s).",
        "parent": "bfb0f40b-3c67-4e65-8517-6cff9dfab7ff",
        "tags": '',
        "stack_name": "overcloud-Networks-zyubznagvv6c-ManagementNetwork-tip34zbqkbzx",
        "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
        "stack_status_reason": "Stack CREATE completed successfully",
        "creation_time": "2016-04-12T15:09:50",
        "links": [
          {
            "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Networks-zyubznagvv6c-ManagementNetwork-tip34zbqkbzx/3589cd45-fbff-4209-8dfe-93ae426d2579",
            "rel": "self"
          }
        ],
        "capabilities": [],
        "notification_topics": [],
        "updated_time": '',
        "timeout_mins": 240,
        "stack_status": "CREATE_COMPLETE",
        "stack_owner": "admin",
        "parameters": {
          "OS::project_id": "9de7e9a9a2a242718cffa65dae677a33",
          "OS::stack_id": "3589cd45-fbff-4209-8dfe-93ae426d2579",
          "OS::stack_name": "overcloud-Networks-zyubznagvv6c-ManagementNetwork-tip34zbqkbzx"
        },
        "id": "3589cd45-fbff-4209-8dfe-93ae426d2579",
        "outputs": [],
        "template_description": "A stack which creates no network(s)."
      }
    },
    "overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3-NodeUserData-ohqnzhts3v3d": {
      "description": "This is a default no-op template which provides empty user-data which can be passed to the OS::Nova::Server resources. This template can be replaced with a different implementation via the resource registry, such that deployers may customize their first-boot configuration.\n",
      "parent": "59a5e87f-86f8-4998-acd4-622f97adcaa1",
      "stack_status_reason": "Stack CREATE completed successfully",
      "stack_name": "overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3-NodeUserData-ohqnzhts3v3d",
      "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
      "tags": '',
      "creation_time": "2016-04-12T15:10:05",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3-NodeUserData-ohqnzhts3v3d/390a5c23-7616-4784-9ffd-edbc18810605",
          "rel": "self"
        }
      ],
      "updated_time": '',
      "stack_owner": "admin",
      "stack_status": "CREATE_COMPLETE",
      "id": "390a5c23-7616-4784-9ffd-edbc18810605",
      "outputs": {
        "disable_rollback": 'true',
        "description": "This is a default no-op template which provides empty user-data which can be passed to the OS::Nova::Server resources. This template can be replaced with a different implementation via the resource registry, such that deployers may customize their first-boot configuration.\n",
        "parent": "59a5e87f-86f8-4998-acd4-622f97adcaa1",
        "tags": '',
        "stack_name": "overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3-NodeUserData-ohqnzhts3v3d",
        "stack_user_project_id": "d1c530e0805b4b96af7da94696175f95",
        "stack_status_reason": "Stack CREATE completed successfully",
        "creation_time": "2016-04-12T15:10:05",
        "links": [
          {
            "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3-NodeUserData-ohqnzhts3v3d/390a5c23-7616-4784-9ffd-edbc18810605",
            "rel": "self"
          }
        ],
        "capabilities": [],
        "notification_topics": [],
        "updated_time": '',
        "timeout_mins": 14400,
        "stack_status": "CREATE_COMPLETE",
        "stack_owner": "admin",
        "parameters": {
          "OS::project_id": "9de7e9a9a2a242718cffa65dae677a33",
          "OS::stack_id": "390a5c23-7616-4784-9ffd-edbc18810605",
          "OS::stack_name": "overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3-NodeUserData-ohqnzhts3v3d"
        },
        "id": "390a5c23-7616-4784-9ffd-edbc18810605",
        "outputs": [
          {
            "output_value": "15d39c15-efc4-472b-9a64-2d1d0e06d218",
            "description": "No description given",
            "output_key": "OS::stack_id"
          }
        ],
        "template_description": "This is a default no-op template which provides empty user-data which can be passed to the OS::Nova::Server resources. This template can be replaced with a different implementation via the resource registry, such that deployers may customize their first-boot configuration.\n"
      }
    }
  },
  "resources": {
    "PcsdPassword": {
      "resource_name": "PcsdPassword",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/PcsdPassword",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "PcsdPassword",
      "creation_time": "2016-04-12T15:09:47",
      "resource_status": "CREATE_COMPLETE",
      "updated_time": "2016-04-12T15:09:47",
      "required_by": [
        "Controller"
      ],
      "resource_status_reason": "state changed",
      "physical_resource_id": "overcloud-PcsdPassword-p7phuhwjkc52",
      "resource_type": "OS::Heat::RandomString",
      "metadata": {}
    },
    "BlockStorageNodesPostDeployment": {
      "resource_name": "BlockStorageNodesPostDeployment",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/BlockStorageNodesPostDeployment",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "BlockStorageNodesPostDeployment",
      "creation_time": "2016-04-12T15:09:47",
      "resource_status": "INIT_COMPLETE",
      "updated_time": "2016-04-12T15:09:47",
      "required_by": [],
      "resource_status_reason": "",
      "physical_resource_id": "",
      "resource_type": "OS::TripleO::BlockStoragePostDeployment",
      "metadata": {}
    },
    "VipConfig": {
      "resource_name": "VipConfig",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/VipConfig",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-VipConfig-ratodrtp6nte/e74802ee-8e2c-4c11-a8d4-4e1d81527ad9",
          "rel": "nested"
        }
      ],
      "logical_resource_id": "VipConfig",
      "creation_time": "2016-04-12T15:09:47",
      "resource_status_reason": "state changed",
      "updated_time": "2016-04-12T15:09:47",
      "required_by": [
        "VipDeployment"
      ],
      "resource_status": "CREATE_COMPLETE",
      "physical_resource_id": "e74802ee-8e2c-4c11-a8d4-4e1d81527ad9",
      "resource_type": "OS::TripleO::VipConfig",
      "metadata": {}
    },
    "CephStorageCephDeployment": {
      "resource_name": "CephStorageCephDeployment",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/CephStorageCephDeployment",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "CephStorageCephDeployment",
      "creation_time": "2016-04-12T15:09:47",
      "resource_status": "INIT_COMPLETE",
      "updated_time": "2016-04-12T15:09:47",
      "required_by": [
        "CephStorageNodesPostDeployment"
      ],
      "resource_status_reason": "",
      "physical_resource_id": "",
      "resource_type": "OS::Heat::StructuredDeployments",
      "metadata": {}
    },
    "user_config": {
      "parent_resource": "NodeAdminUserData",
      "resource_name": "user_config",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3-NodeAdminUserData-hjcxomgp2c4s/e49fdf8e-291b-45a1-8335-d77b59054681/resources/user_config",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3-NodeAdminUserData-hjcxomgp2c4s/e49fdf8e-291b-45a1-8335-d77b59054681",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "user_config",
      "creation_time": "2016-04-12T15:10:06",
      "resource_status": "CREATE_COMPLETE",
      "updated_time": "2016-04-12T15:10:06",
      "required_by": [
        "userdata"
      ],
      "resource_status_reason": "state changed",
      "physical_resource_id": "6ff86ac7-eb35-4329-884d-a395792b878d",
      "resource_type": "OS::Heat::CloudConfig",
      "metadata": {}
    },
    "InternalApiVirtualIP": {
      "resource_name": "InternalApiVirtualIP",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/InternalApiVirtualIP",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-InternalApiVirtualIP-ln4exmem57yc/c8e8f2d2-d3f3-4cf2-9d31-a1cf5c00b93d",
          "rel": "nested"
        }
      ],
      "logical_resource_id": "InternalApiVirtualIP",
      "creation_time": "2016-04-12T15:09:47",
      "resource_status_reason": "state changed",
      "updated_time": "2016-04-12T15:09:47",
      "required_by": [
        "VipMap"
      ],
      "resource_status": "CREATE_COMPLETE",
      "physical_resource_id": "c8e8f2d2-d3f3-4cf2-9d31-a1cf5c00b93d",
      "resource_type": "OS::TripleO::Network::Ports::InternalApiVipPort",
      "metadata": {}
    },
    "ControllerAllNodesValidationDeployment": {
      "resource_name": "ControllerAllNodesValidationDeployment",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/ControllerAllNodesValidationDeployment",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "ControllerAllNodesValidationDeployment",
      "creation_time": "2016-04-12T15:09:47",
      "resource_status": "INIT_COMPLETE",
      "updated_time": "2016-04-12T15:09:47",
      "required_by": [
        "AllNodesExtraConfig"
      ],
      "resource_status_reason": "",
      "physical_resource_id": "",
      "resource_type": "OS::Heat::StructuredDeployments",
      "metadata": {}
    },
    "ControlVirtualIP": {
      "resource_name": "ControlVirtualIP",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/ControlVirtualIP",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "ControlVirtualIP",
      "creation_time": "2016-04-12T15:09:47",
      "resource_status": "CREATE_COMPLETE",
      "updated_time": "2016-04-12T15:09:47",
      "required_by": [
        "InternalApiVirtualIP",
        "VipMap",
        "StorageVirtualIP",
        "PublicVirtualIP",
        "RedisVirtualIP",
        "StorageMgmtVirtualIP"
      ],
      "resource_status_reason": "state changed",
      "physical_resource_id": "c1714192-d6d4-4f16-aa96-98dd14868a6b",
      "resource_type": "OS::Neutron::Port",
      "metadata": {}
    },
    "0": {
      "parent_resource": "Compute",
      "resource_name": "0",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s/d3c93c64-778f-4cec-a5a8-062de076c0b6/resources/0",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s/d3c93c64-778f-4cec-a5a8-062de076c0b6",
          "rel": "stack"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3/59a5e87f-86f8-4998-acd4-622f97adcaa1",
          "rel": "nested"
        }
      ],
      "logical_resource_id": "0",
      "creation_time": "2016-04-12T15:10:03",
      "resource_status_reason": "ResourceInError: resources[0].resources.NovaCompute: Went to status ERROR due to \"Message: No valid host was found. There are not enough hosts available., Code: 500\"",
      "updated_time": "2016-04-12T15:10:03",
      "required_by": [],
      "resource_status": "CREATE_FAILED",
      "physical_resource_id": "59a5e87f-86f8-4998-acd4-622f97adcaa1",
      "resource_type": "OS::TripleO::Compute",
      "metadata": {}
    },
    "ObjectStorageNodesPostDeployment": {
      "resource_name": "ObjectStorageNodesPostDeployment",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/ObjectStorageNodesPostDeployment",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "ObjectStorageNodesPostDeployment",
      "creation_time": "2016-04-12T15:09:47",
      "resource_status": "INIT_COMPLETE",
      "updated_time": "2016-04-12T15:09:47",
      "required_by": [],
      "resource_status_reason": "",
      "physical_resource_id": "",
      "resource_type": "OS::TripleO::ObjectStoragePostDeployment",
      "metadata": {}
    },
    "VipDeployment": {
      "resource_name": "VipDeployment",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/VipDeployment",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "VipDeployment",
      "creation_time": "2016-04-12T15:09:47",
      "resource_status": "INIT_COMPLETE",
      "updated_time": "2016-04-12T15:09:47",
      "required_by": [],
      "resource_status_reason": "",
      "physical_resource_id": "",
      "resource_type": "OS::Heat::StructuredDeployments",
      "metadata": {}
    },
    "ExternalNetwork": {
      "parent_resource": "Networks",
      "resource_name": "ExternalNetwork",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Networks-zyubznagvv6c/bfb0f40b-3c67-4e65-8517-6cff9dfab7ff/resources/ExternalNetwork",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Networks-zyubznagvv6c/bfb0f40b-3c67-4e65-8517-6cff9dfab7ff",
          "rel": "stack"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Networks-zyubznagvv6c-ExternalNetwork-vmp3e66swxg6/62c70746-8f9d-418a-9b42-bbab15556d64",
          "rel": "nested"
        }
      ],
      "logical_resource_id": "ExternalNetwork",
      "creation_time": "2016-04-12T15:09:48",
      "resource_status_reason": "state changed",
      "updated_time": "2016-04-12T15:09:48",
      "required_by": [],
      "resource_status": "CREATE_COMPLETE",
      "physical_resource_id": "62c70746-8f9d-418a-9b42-bbab15556d64",
      "resource_type": "OS::TripleO::Network::External",
      "metadata": {}
    },
    "NetIpMap": {
      "parent_resource": "0",
      "resource_name": "NetIpMap",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3/59a5e87f-86f8-4998-acd4-622f97adcaa1/resources/NetIpMap",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3/59a5e87f-86f8-4998-acd4-622f97adcaa1",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "NetIpMap",
      "creation_time": "2016-04-12T15:10:05",
      "resource_status": "INIT_COMPLETE",
      "updated_time": "2016-04-12T15:10:05",
      "required_by": [
        "NovaComputeDeployment"
      ],
      "resource_status_reason": "",
      "physical_resource_id": "",
      "resource_type": "OS::TripleO::Network::Ports::NetIpMap",
      "metadata": {}
    },
    "userdata": {
      "parent_resource": "NodeAdminUserData",
      "resource_name": "userdata",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3-NodeAdminUserData-hjcxomgp2c4s/e49fdf8e-291b-45a1-8335-d77b59054681/resources/userdata",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3-NodeAdminUserData-hjcxomgp2c4s/e49fdf8e-291b-45a1-8335-d77b59054681",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "userdata",
      "creation_time": "2016-04-12T15:10:06",
      "resource_status": "CREATE_COMPLETE",
      "updated_time": "2016-04-12T15:10:06",
      "required_by": [],
      "resource_status_reason": "state changed",
      "physical_resource_id": "6307ac0e-4f18-451d-837a-1d6b153a1bbc",
      "resource_type": "OS::Heat::MultipartMime",
      "metadata": {}
    },
    "TenantPort": {
      "parent_resource": "0",
      "resource_name": "TenantPort",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3/59a5e87f-86f8-4998-acd4-622f97adcaa1/resources/TenantPort",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3/59a5e87f-86f8-4998-acd4-622f97adcaa1",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "TenantPort",
      "creation_time": "2016-04-12T15:10:05",
      "resource_status": "INIT_COMPLETE",
      "updated_time": "2016-04-12T15:10:05",
      "required_by": [
        "NetworkConfig",
        "NetIpMap"
      ],
      "resource_status_reason": "",
      "physical_resource_id": "",
      "resource_type": "OS::TripleO::Compute::Ports::TenantPort",
      "metadata": {}
    },
    "NetworkConfig": {
      "parent_resource": "0",
      "resource_name": "NetworkConfig",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3/59a5e87f-86f8-4998-acd4-622f97adcaa1/resources/NetworkConfig",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3/59a5e87f-86f8-4998-acd4-622f97adcaa1",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "NetworkConfig",
      "creation_time": "2016-04-12T15:10:05",
      "resource_status": "INIT_COMPLETE",
      "updated_time": "2016-04-12T15:10:05",
      "required_by": [
        "NetworkDeployment"
      ],
      "resource_status_reason": "",
      "physical_resource_id": "",
      "resource_type": "OS::TripleO::Compute::Net::SoftwareConfig",
      "metadata": {}
    },
    "ControllerBootstrapNodeConfig": {
      "resource_name": "ControllerBootstrapNodeConfig",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/ControllerBootstrapNodeConfig",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "ControllerBootstrapNodeConfig",
      "creation_time": "2016-04-12T15:09:47",
      "resource_status": "INIT_COMPLETE",
      "updated_time": "2016-04-12T15:09:47",
      "required_by": [
        "ControllerBootstrapNodeDeployment"
      ],
      "resource_status_reason": "",
      "physical_resource_id": "",
      "resource_type": "OS::TripleO::BootstrapNode::SoftwareConfig",
      "metadata": {}
    },
    "ComputeCephDeployment": {
      "resource_name": "ComputeCephDeployment",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/ComputeCephDeployment",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "ComputeCephDeployment",
      "creation_time": "2016-04-12T15:09:47",
      "resource_status": "INIT_COMPLETE",
      "updated_time": "2016-04-12T15:09:47",
      "required_by": [
        "ComputeNodesPostDeployment"
      ],
      "resource_status_reason": "",
      "physical_resource_id": "",
      "resource_type": "OS::Heat::StructuredDeployments",
      "metadata": {}
    },
    "BlockStorageAllNodesValidationDeployment": {
      "resource_name": "BlockStorageAllNodesValidationDeployment",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/BlockStorageAllNodesValidationDeployment",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "BlockStorageAllNodesValidationDeployment",
      "creation_time": "2016-04-12T15:09:47",
      "resource_status": "INIT_COMPLETE",
      "updated_time": "2016-04-12T15:09:47",
      "required_by": [
        "AllNodesExtraConfig"
      ],
      "resource_status_reason": "",
      "physical_resource_id": "",
      "resource_type": "OS::Heat::StructuredDeployments",
      "metadata": {}
    },
    "HorizonSecret": {
      "resource_name": "HorizonSecret",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/HorizonSecret",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "HorizonSecret",
      "creation_time": "2016-04-12T15:09:47",
      "resource_status": "CREATE_COMPLETE",
      "updated_time": "2016-04-12T15:09:47",
      "required_by": [
        "Controller"
      ],
      "resource_status_reason": "state changed",
      "physical_resource_id": "overcloud-HorizonSecret-wz7nw7pi23wf",
      "resource_type": "OS::Heat::RandomString",
      "metadata": {}
    },
    "VipConfigImpl": {
      "parent_resource": "VipConfig",
      "resource_name": "VipConfigImpl",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-VipConfig-ratodrtp6nte/e74802ee-8e2c-4c11-a8d4-4e1d81527ad9/resources/VipConfigImpl",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-VipConfig-ratodrtp6nte/e74802ee-8e2c-4c11-a8d4-4e1d81527ad9",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "VipConfigImpl",
      "creation_time": "2016-04-12T15:09:48",
      "resource_status": "CREATE_COMPLETE",
      "updated_time": "2016-04-12T15:09:48",
      "required_by": [],
      "resource_status_reason": "state changed",
      "physical_resource_id": "7efb061b-ffc3-42ac-a95f-c9bd70177e84",
      "resource_type": "OS::Heat::StructuredConfig",
      "metadata": {}
    },
    "StorageMgmtVirtualIP": {
      "resource_name": "StorageMgmtVirtualIP",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/StorageMgmtVirtualIP",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-StorageMgmtVirtualIP-gdvz4nm4owxu/52b6c1ea-4421-411b-80ad-383f71803729",
          "rel": "nested"
        }
      ],
      "logical_resource_id": "StorageMgmtVirtualIP",
      "creation_time": "2016-04-12T15:09:47",
      "resource_status_reason": "state changed",
      "updated_time": "2016-04-12T15:09:47",
      "required_by": [
        "VipMap"
      ],
      "resource_status": "CREATE_COMPLETE",
      "physical_resource_id": "52b6c1ea-4421-411b-80ad-383f71803729",
      "resource_type": "OS::TripleO::Network::Ports::StorageMgmtVipPort",
      "metadata": {}
    },
    "SwiftDevicesAndProxyConfig": {
      "resource_name": "SwiftDevicesAndProxyConfig",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/SwiftDevicesAndProxyConfig",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "SwiftDevicesAndProxyConfig",
      "creation_time": "2016-04-12T15:09:47",
      "resource_status": "INIT_COMPLETE",
      "updated_time": "2016-04-12T15:09:47",
      "required_by": [
        "ObjectStorageSwiftDeployment",
        "ControllerSwiftDeployment"
      ],
      "resource_status_reason": "",
      "physical_resource_id": "",
      "resource_type": "OS::TripleO::SwiftDevicesAndProxy::SoftwareConfig",
      "metadata": {}
    },
    "CephStorageAllNodesDeployment": {
      "resource_name": "CephStorageAllNodesDeployment",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/CephStorageAllNodesDeployment",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "CephStorageAllNodesDeployment",
      "creation_time": "2016-04-12T15:09:47",
      "resource_status": "INIT_COMPLETE",
      "updated_time": "2016-04-12T15:09:47",
      "required_by": [
        "CephStorageNodesPostDeployment",
        "CephStorageAllNodesValidationDeployment"
      ],
      "resource_status_reason": "",
      "physical_resource_id": "",
      "resource_type": "OS::Heat::StructuredDeployments",
      "metadata": {}
    },
    "ObjectStorageSwiftDeployment": {
      "resource_name": "ObjectStorageSwiftDeployment",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/ObjectStorageSwiftDeployment",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "ObjectStorageSwiftDeployment",
      "creation_time": "2016-04-12T15:09:47",
      "resource_status": "INIT_COMPLETE",
      "updated_time": "2016-04-12T15:09:47",
      "required_by": [
        "ObjectStorageNodesPostDeployment"
      ],
      "resource_status_reason": "",
      "physical_resource_id": "",
      "resource_type": "OS::Heat::StructuredDeployments",
      "metadata": {}
    },
    "StorageMgmtPort": {
      "parent_resource": "0",
      "resource_name": "StorageMgmtPort",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3/59a5e87f-86f8-4998-acd4-622f97adcaa1/resources/StorageMgmtPort",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3/59a5e87f-86f8-4998-acd4-622f97adcaa1",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "StorageMgmtPort",
      "creation_time": "2016-04-12T15:10:05",
      "resource_status": "INIT_COMPLETE",
      "updated_time": "2016-04-12T15:10:05",
      "required_by": [
        "NetworkConfig",
        "NetIpMap"
      ],
      "resource_status_reason": "",
      "physical_resource_id": "",
      "resource_type": "OS::TripleO::Compute::Ports::StorageMgmtPort",
      "metadata": {}
    },
    "NovaComputeDeployment": {
      "parent_resource": "0",
      "resource_name": "NovaComputeDeployment",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3/59a5e87f-86f8-4998-acd4-622f97adcaa1/resources/NovaComputeDeployment",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3/59a5e87f-86f8-4998-acd4-622f97adcaa1",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "NovaComputeDeployment",
      "creation_time": "2016-04-12T15:10:05",
      "resource_status": "INIT_COMPLETE",
      "updated_time": "2016-04-12T15:10:05",
      "required_by": [
        "NodeTLSCAData",
        "ComputeExtraConfigPre"
      ],
      "resource_status_reason": "",
      "physical_resource_id": "",
      "resource_type": "OS::TripleO::SoftwareDeployment",
      "metadata": {}
    },
    "InternalApiPort": {
      "parent_resource": "0",
      "resource_name": "InternalApiPort",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3/59a5e87f-86f8-4998-acd4-622f97adcaa1/resources/InternalApiPort",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3/59a5e87f-86f8-4998-acd4-622f97adcaa1",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "InternalApiPort",
      "creation_time": "2016-04-12T15:10:05",
      "resource_status": "INIT_COMPLETE",
      "updated_time": "2016-04-12T15:10:05",
      "required_by": [
        "NetworkConfig",
        "NetIpMap"
      ],
      "resource_status_reason": "",
      "physical_resource_id": "",
      "resource_type": "OS::TripleO::Compute::Ports::InternalApiPort",
      "metadata": {}
    },
    "allNodesConfig": {
      "resource_name": "allNodesConfig",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/allNodesConfig",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "allNodesConfig",
      "creation_time": "2016-04-12T15:09:47",
      "resource_status": "INIT_COMPLETE",
      "updated_time": "2016-04-12T15:09:47",
      "required_by": [
        "CephStorageAllNodesDeployment",
        "ComputeAllNodesDeployment",
        "BlockStorageAllNodesDeployment",
        "ObjectStorageAllNodesDeployment",
        "ControllerAllNodesDeployment"
      ],
      "resource_status_reason": "",
      "physical_resource_id": "",
      "resource_type": "OS::TripleO::AllNodes::SoftwareConfig",
      "metadata": {}
    },
    "TenantNetwork": {
      "parent_resource": "Networks",
      "resource_name": "TenantNetwork",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Networks-zyubznagvv6c/bfb0f40b-3c67-4e65-8517-6cff9dfab7ff/resources/TenantNetwork",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Networks-zyubznagvv6c/bfb0f40b-3c67-4e65-8517-6cff9dfab7ff",
          "rel": "stack"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Networks-zyubznagvv6c-TenantNetwork-e3myke3plkcn/43b4cf3a-90c5-448c-8d21-0beb32e4d309",
          "rel": "nested"
        }
      ],
      "logical_resource_id": "TenantNetwork",
      "creation_time": "2016-04-12T15:09:48",
      "resource_status_reason": "state changed",
      "updated_time": "2016-04-12T15:09:48",
      "required_by": [],
      "resource_status": "CREATE_COMPLETE",
      "physical_resource_id": "43b4cf3a-90c5-448c-8d21-0beb32e4d309",
      "resource_type": "OS::TripleO::Network::Tenant",
      "metadata": {}
    },
    "StorageVirtualIP": {
      "resource_name": "StorageVirtualIP",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/StorageVirtualIP",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-StorageVirtualIP-kgolkxflflvk/00e3d273-7ad2-434d-b700-86f112b6b2fd",
          "rel": "nested"
        }
      ],
      "logical_resource_id": "StorageVirtualIP",
      "creation_time": "2016-04-12T15:09:47",
      "resource_status_reason": "state changed",
      "updated_time": "2016-04-12T15:09:47",
      "required_by": [
        "VipMap"
      ],
      "resource_status": "CREATE_COMPLETE",
      "physical_resource_id": "00e3d273-7ad2-434d-b700-86f112b6b2fd",
      "resource_type": "OS::TripleO::Network::Ports::StorageVipPort",
      "metadata": {}
    },
    "ControllerSwiftDeployment": {
      "resource_name": "ControllerSwiftDeployment",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/ControllerSwiftDeployment",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "ControllerSwiftDeployment",
      "creation_time": "2016-04-12T15:09:47",
      "resource_status": "INIT_COMPLETE",
      "updated_time": "2016-04-12T15:09:47",
      "required_by": [
        "ControllerNodesPostDeployment"
      ],
      "resource_status_reason": "",
      "physical_resource_id": "",
      "resource_type": "OS::Heat::StructuredDeployments",
      "metadata": {}
    },
    "Controller": {
      "parent_resource": "2",
      "resource_name": "Controller",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Controller-d7iywdnu5uzr-2-evqysybsnrrt/e4dc37e4-d565-4453-8d6e-a830953eb803/resources/Controller",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Controller-d7iywdnu5uzr-2-evqysybsnrrt/e4dc37e4-d565-4453-8d6e-a830953eb803",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "Controller",
      "creation_time": "2016-04-12T15:10:12",
      "resource_status": "CREATE_FAILED",
      "updated_time": "2016-04-12T15:10:12",
      "required_by": [
        "NodeTLSData",
        "NodeTLSCAData",
        "StoragePort",
        "NetIpMap",
        "ControllerDeployment",
        "NetworkConfig",
        "ManagementPort",
        "ControllerExtraConfigPre",
        "NetIpSubnetMap",
        "UpdateDeployment",
        "InternalApiPort",
        "NetworkDeployment",
        "NodeExtraConfig",
        "StorageMgmtPort",
        "TenantPort",
        "ExternalPort"
      ],
      "resource_status_reason": "ResourceInError: resources.Controller: Went to status ERROR due to \"Message: No valid host was found. There are not enough hosts available., Code: 500\"",
      "physical_resource_id": "7a6d9cb4-679e-46dd-ab85-1dded96737b3",
      "resource_type": "OS::Nova::Server",
      "metadata": {
        "deployments": [],
        "os-collect-config": {
          "cfn": {
            "stack_name": "overcloud-Controller-d7iywdnu5uzr-2-evqysybsnrrt",
            "metadata_url": "http://192.0.2.240:8000/v1/",
            "path": "Controller.Metadata",
            "secret_access_key": "79bb62ffbad5464d96ec7bef8442fb4c",
            "access_key_id": "04c81a5e748340cca6d3530fdbe39f12"
          }
        }
      }
    },
    "VipPort": {
      "parent_resource": "RedisVirtualIP",
      "resource_name": "VipPort",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-RedisVirtualIP-ndkwnexwqzw4/74727fb1-eb7b-44c7-ad75-3e1f11fd3d67/resources/VipPort",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-RedisVirtualIP-ndkwnexwqzw4/74727fb1-eb7b-44c7-ad75-3e1f11fd3d67",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "VipPort",
      "creation_time": "2016-04-12T15:09:56",
      "resource_status": "CREATE_COMPLETE",
      "updated_time": "2016-04-12T15:09:56",
      "required_by": [],
      "resource_status_reason": "state changed",
      "physical_resource_id": "43c395bb-7dd3-4f73-ba76-73efef205b47",
      "resource_type": "OS::Neutron::Port",
      "metadata": {}
    },
    "ObjectStorageAllNodesValidationDeployment": {
      "resource_name": "ObjectStorageAllNodesValidationDeployment",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/ObjectStorageAllNodesValidationDeployment",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "ObjectStorageAllNodesValidationDeployment",
      "creation_time": "2016-04-12T15:09:47",
      "resource_status": "INIT_COMPLETE",
      "updated_time": "2016-04-12T15:09:47",
      "required_by": [
        "AllNodesExtraConfig"
      ],
      "resource_status_reason": "",
      "physical_resource_id": "",
      "resource_type": "OS::Heat::StructuredDeployments",
      "metadata": {}
    },
    "VipMap": {
      "resource_name": "VipMap",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/VipMap",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-VipMap-ipemp65ncqfi/65178912-9996-4493-8561-10a62343cc39",
          "rel": "nested"
        }
      ],
      "logical_resource_id": "VipMap",
      "creation_time": "2016-04-12T15:09:47",
      "resource_status_reason": "state changed",
      "updated_time": "2016-04-12T15:09:47",
      "required_by": [
        "BlockStorage",
        "Controller",
        "EndpointMap",
        "Compute",
        "VipDeployment"
      ],
      "resource_status": "CREATE_COMPLETE",
      "physical_resource_id": "65178912-9996-4493-8561-10a62343cc39",
      "resource_type": "OS::TripleO::Network::Ports::NetVipMap",
      "metadata": {}
    },
    "ObjectStorage": {
      "resource_name": "ObjectStorage",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/ObjectStorage",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-ObjectStorage-vmfquqg5aqwz/578ad72f-1c10-4d6d-bbb5-f1e3faf3ca4f",
          "rel": "nested"
        }
      ],
      "logical_resource_id": "ObjectStorage",
      "creation_time": "2016-04-12T15:09:47",
      "resource_status_reason": "state changed",
      "updated_time": "2016-04-12T15:09:47",
      "required_by": [
        "SwiftDevicesAndProxyConfig",
        "ObjectStorageSwiftDeployment",
        "ObjectStorageNodesPostDeployment",
        "UpdateWorkflow",
        "ObjectStorageAllNodesDeployment",
        "ObjectStorageAllNodesValidationDeployment",
        "AllNodesExtraConfig",
        "allNodesConfig"
      ],
      "resource_status": "CREATE_COMPLETE",
      "physical_resource_id": "578ad72f-1c10-4d6d-bbb5-f1e3faf3ca4f",
      "resource_type": "OS::Heat::ResourceGroup",
      "metadata": {}
    },
    "HeatAuthEncryptionKey": {
      "resource_name": "HeatAuthEncryptionKey",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/HeatAuthEncryptionKey",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "HeatAuthEncryptionKey",
      "creation_time": "2016-04-12T15:09:47",
      "resource_status": "CREATE_COMPLETE",
      "updated_time": "2016-04-12T15:09:47",
      "required_by": [
        "Controller"
      ],
      "resource_status_reason": "state changed",
      "physical_resource_id": "overcloud-HeatAuthEncryptionKey-j6aaydfkqpqj",
      "resource_type": "OS::Heat::RandomString",
      "metadata": {}
    },
    "UpdateConfig": {
      "parent_resource": "0",
      "resource_name": "UpdateConfig",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3/59a5e87f-86f8-4998-acd4-622f97adcaa1/resources/UpdateConfig",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3/59a5e87f-86f8-4998-acd4-622f97adcaa1",
          "rel": "stack"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3-UpdateConfig-gfypsblpw6ci/a6fa0cac-66bd-4efb-b5a6-a37a8fc13f36",
          "rel": "nested"
        }
      ],
      "logical_resource_id": "UpdateConfig",
      "creation_time": "2016-04-12T15:10:05",
      "resource_status_reason": "state changed",
      "updated_time": "2016-04-12T15:10:05",
      "required_by": [
        "UpdateDeployment"
      ],
      "resource_status": "CREATE_COMPLETE",
      "physical_resource_id": "a6fa0cac-66bd-4efb-b5a6-a37a8fc13f36",
      "resource_type": "OS::TripleO::Tasks::PackageUpdate",
      "metadata": {}
    },
    "NetIpSubnetMap": {
      "parent_resource": "2",
      "resource_name": "NetIpSubnetMap",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Controller-d7iywdnu5uzr-2-evqysybsnrrt/e4dc37e4-d565-4453-8d6e-a830953eb803/resources/NetIpSubnetMap",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Controller-d7iywdnu5uzr-2-evqysybsnrrt/e4dc37e4-d565-4453-8d6e-a830953eb803",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "NetIpSubnetMap",
      "creation_time": "2016-04-12T15:10:11",
      "resource_status": "INIT_COMPLETE",
      "updated_time": "2016-04-12T15:10:11",
      "required_by": [
        "ControllerDeployment"
      ],
      "resource_status_reason": "",
      "physical_resource_id": "",
      "resource_type": "OS::TripleO::Network::Ports::NetIpSubnetMap",
      "metadata": {}
    },
    "ComputeNodesPostDeployment": {
      "resource_name": "ComputeNodesPostDeployment",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/ComputeNodesPostDeployment",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "ComputeNodesPostDeployment",
      "creation_time": "2016-04-12T15:09:47",
      "resource_status": "INIT_COMPLETE",
      "updated_time": "2016-04-12T15:09:47",
      "required_by": [],
      "resource_status_reason": "",
      "physical_resource_id": "",
      "resource_type": "OS::TripleO::ComputePostDeployment",
      "metadata": {}
    },
    "UpdateDeployment": {
      "parent_resource": "0",
      "resource_name": "UpdateDeployment",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3/59a5e87f-86f8-4998-acd4-622f97adcaa1/resources/UpdateDeployment",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3/59a5e87f-86f8-4998-acd4-622f97adcaa1",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "UpdateDeployment",
      "creation_time": "2016-04-12T15:10:05",
      "resource_status": "INIT_COMPLETE",
      "updated_time": "2016-04-12T15:10:05",
      "required_by": [
        "NovaComputeDeployment"
      ],
      "resource_status_reason": "",
      "physical_resource_id": "",
      "resource_type": "OS::Heat::SoftwareDeployment",
      "metadata": {}
    },
    "NovaCompute": {
      "parent_resource": "0",
      "resource_name": "NovaCompute",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3/59a5e87f-86f8-4998-acd4-622f97adcaa1/resources/NovaCompute",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3/59a5e87f-86f8-4998-acd4-622f97adcaa1",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "NovaCompute",
      "creation_time": "2016-04-12T15:10:05",
      "resource_status": "CREATE_FAILED",
      "updated_time": "2016-04-12T15:10:05",
      "required_by": [
        "ManagementPort",
        "NodeTLSCAData",
        "StorageMgmtPort",
        "NetworkConfig",
        "TenantPort",
        "UpdateDeployment",
        "NetworkDeployment",
        "NodeExtraConfig",
        "NovaComputeDeployment",
        "StoragePort",
        "ComputeExtraConfigPre",
        "NetIpMap",
        "InternalApiPort",
        "ExternalPort"
      ],
      "resource_status_reason": "ResourceInError: resources.NovaCompute: Went to status ERROR due to \"Message: No valid host was found. There are not enough hosts available., Code: 500\"",
      "physical_resource_id": "ac50a70d-b709-4093-b0c8-e42285264afd",
      "resource_type": "OS::Nova::Server",
      "metadata": {
        "deployments": [],
        "os-collect-config": {
          "cfn": {
            "stack_name": "overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3",
            "metadata_url": "http://192.0.2.240:8000/v1/",
            "path": "NovaCompute.Metadata",
            "secret_access_key": "7be11f7606884f30bdd9fe6c3db4ce5b",
            "access_key_id": "a59587aeb2614a86aa3b0d88bdba3a5a"
          }
        }
      }
    },
    "Networks": {
      "resource_name": "Networks",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/Networks",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Networks-zyubznagvv6c/bfb0f40b-3c67-4e65-8517-6cff9dfab7ff",
          "rel": "nested"
        }
      ],
      "logical_resource_id": "Networks",
      "creation_time": "2016-04-12T15:09:47",
      "resource_status_reason": "state changed",
      "updated_time": "2016-04-12T15:09:47",
      "required_by": [
        "InternalApiVirtualIP",
        "BlockStorage",
        "ObjectStorage",
        "CephStorage",
        "RedisVirtualIP",
        "StorageVirtualIP",
        "PublicVirtualIP",
        "Controller",
        "StorageMgmtVirtualIP",
        "ControlVirtualIP",
        "Compute"
      ],
      "resource_status": "CREATE_COMPLETE",
      "physical_resource_id": "bfb0f40b-3c67-4e65-8517-6cff9dfab7ff",
      "resource_type": "OS::TripleO::Network",
      "metadata": {}
    },
    "ManagementPort": {
      "parent_resource": "0",
      "resource_name": "ManagementPort",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3/59a5e87f-86f8-4998-acd4-622f97adcaa1/resources/ManagementPort",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3/59a5e87f-86f8-4998-acd4-622f97adcaa1",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "ManagementPort",
      "creation_time": "2016-04-12T15:10:05",
      "resource_status": "INIT_COMPLETE",
      "updated_time": "2016-04-12T15:10:05",
      "required_by": [
        "NetworkConfig",
        "NetIpMap"
      ],
      "resource_status_reason": "",
      "physical_resource_id": "",
      "resource_type": "OS::TripleO::Compute::Ports::ManagementPort",
      "metadata": {}
    },
    "ControllerAllNodesDeployment": {
      "resource_name": "ControllerAllNodesDeployment",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/ControllerAllNodesDeployment",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "ControllerAllNodesDeployment",
      "creation_time": "2016-04-12T15:09:47",
      "resource_status": "INIT_COMPLETE",
      "updated_time": "2016-04-12T15:09:47",
      "required_by": [
        "ControllerAllNodesValidationDeployment",
        "ControllerNodesPostDeployment"
      ],
      "resource_status_reason": "",
      "physical_resource_id": "",
      "resource_type": "OS::Heat::StructuredDeployments",
      "metadata": {}
    },
    "UpdateWorkflow": {
      "resource_name": "UpdateWorkflow",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/UpdateWorkflow",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "UpdateWorkflow",
      "creation_time": "2016-04-12T15:09:47",
      "resource_status": "INIT_COMPLETE",
      "updated_time": "2016-04-12T15:09:47",
      "required_by": [
        "AllNodesExtraConfig"
      ],
      "resource_status_reason": "",
      "physical_resource_id": "",
      "resource_type": "OS::TripleO::Tasks::UpdateWorkflow",
      "metadata": {}
    },
    "StoragePort": {
      "parent_resource": "0",
      "resource_name": "StoragePort",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3/59a5e87f-86f8-4998-acd4-622f97adcaa1/resources/StoragePort",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3/59a5e87f-86f8-4998-acd4-622f97adcaa1",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "StoragePort",
      "creation_time": "2016-04-12T15:10:05",
      "resource_status": "INIT_COMPLETE",
      "updated_time": "2016-04-12T15:10:05",
      "required_by": [
        "NetworkConfig",
        "NetIpMap"
      ],
      "resource_status_reason": "",
      "physical_resource_id": "",
      "resource_type": "OS::TripleO::Compute::Ports::StoragePort",
      "metadata": {}
    },
    "RabbitCookie": {
      "resource_name": "RabbitCookie",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/RabbitCookie",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "RabbitCookie",
      "creation_time": "2016-04-12T15:09:47",
      "resource_status": "CREATE_COMPLETE",
      "updated_time": "2016-04-12T15:09:47",
      "required_by": [
        "Controller"
      ],
      "resource_status_reason": "state changed",
      "physical_resource_id": "overcloud-RabbitCookie-txibprcr2xlz",
      "resource_type": "OS::Heat::RandomString",
      "metadata": {}
    },
    "2": {
      "parent_resource": "Controller",
      "resource_name": "2",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Controller-d7iywdnu5uzr/119696b0-92ac-44ab-85d6-614c68af3949/resources/2",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Controller-d7iywdnu5uzr/119696b0-92ac-44ab-85d6-614c68af3949",
          "rel": "stack"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Controller-d7iywdnu5uzr-2-evqysybsnrrt/e4dc37e4-d565-4453-8d6e-a830953eb803",
          "rel": "nested"
        }
      ],
      "logical_resource_id": "2",
      "creation_time": "2016-04-12T15:10:09",
      "resource_status_reason": "ResourceInError: resources[2].resources.Controller: Went to status ERROR due to \"Message: No valid host was found. There are not enough hosts available., Code: 500\"",
      "updated_time": "2016-04-12T15:10:09",
      "required_by": [],
      "resource_status": "CREATE_FAILED",
      "physical_resource_id": "e4dc37e4-d565-4453-8d6e-a830953eb803",
      "resource_type": "OS::TripleO::Controller",
      "metadata": {}
    },
    "MysqlRootPassword": {
      "resource_name": "MysqlRootPassword",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/MysqlRootPassword",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "MysqlRootPassword",
      "creation_time": "2016-04-12T15:09:47",
      "resource_status": "CREATE_COMPLETE",
      "updated_time": "2016-04-12T15:09:47",
      "required_by": [
        "Controller"
      ],
      "resource_status_reason": "state changed",
      "physical_resource_id": "overcloud-MysqlRootPassword-vm3ychm6egrs",
      "resource_type": "OS::Heat::RandomString",
      "metadata": {}
    },
    "StorageNetwork": {
      "parent_resource": "Networks",
      "resource_name": "StorageNetwork",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Networks-zyubznagvv6c/bfb0f40b-3c67-4e65-8517-6cff9dfab7ff/resources/StorageNetwork",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Networks-zyubznagvv6c/bfb0f40b-3c67-4e65-8517-6cff9dfab7ff",
          "rel": "stack"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Networks-zyubznagvv6c-StorageNetwork-e2elgonsbsvu/be8920e1-6db8-4199-baf0-4362c776bfb4",
          "rel": "nested"
        }
      ],
      "logical_resource_id": "StorageNetwork",
      "creation_time": "2016-04-12T15:09:48",
      "resource_status_reason": "state changed",
      "updated_time": "2016-04-12T15:09:48",
      "required_by": [],
      "resource_status": "CREATE_COMPLETE",
      "physical_resource_id": "be8920e1-6db8-4199-baf0-4362c776bfb4",
      "resource_type": "OS::TripleO::Network::Storage",
      "metadata": {}
    },
    "MysqlClusterUniquePart": {
      "resource_name": "MysqlClusterUniquePart",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/MysqlClusterUniquePart",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "MysqlClusterUniquePart",
      "creation_time": "2016-04-12T15:09:47",
      "resource_status": "CREATE_COMPLETE",
      "updated_time": "2016-04-12T15:09:47",
      "required_by": [
        "Controller"
      ],
      "resource_status_reason": "state changed",
      "physical_resource_id": "overcloud-MysqlClusterUniquePart-vnlg7volil7x",
      "resource_type": "OS::Heat::RandomString",
      "metadata": {}
    },
    "NodeAdminUserData": {
      "parent_resource": "0",
      "resource_name": "NodeAdminUserData",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3/59a5e87f-86f8-4998-acd4-622f97adcaa1/resources/NodeAdminUserData",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3/59a5e87f-86f8-4998-acd4-622f97adcaa1",
          "rel": "stack"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3-NodeAdminUserData-hjcxomgp2c4s/e49fdf8e-291b-45a1-8335-d77b59054681",
          "rel": "nested"
        }
      ],
      "logical_resource_id": "NodeAdminUserData",
      "creation_time": "2016-04-12T15:10:05",
      "resource_status_reason": "state changed",
      "updated_time": "2016-04-12T15:10:05",
      "required_by": [
        "UserData"
      ],
      "resource_status": "CREATE_COMPLETE",
      "physical_resource_id": "e49fdf8e-291b-45a1-8335-d77b59054681",
      "resource_type": "OS::TripleO::NodeAdminUserData",
      "metadata": {}
    },
    "ControllerNodesPostDeployment": {
      "resource_name": "ControllerNodesPostDeployment",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/ControllerNodesPostDeployment",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "ControllerNodesPostDeployment",
      "creation_time": "2016-04-12T15:09:47",
      "resource_status": "INIT_COMPLETE",
      "updated_time": "2016-04-12T15:09:47",
      "required_by": [
        "BlockStorageNodesPostDeployment",
        "CephStorageNodesPostDeployment"
      ],
      "resource_status_reason": "",
      "physical_resource_id": "",
      "resource_type": "OS::TripleO::ControllerPostDeployment",
      "metadata": {}
    },
    "ControllerCephDeployment": {
      "resource_name": "ControllerCephDeployment",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/ControllerCephDeployment",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "ControllerCephDeployment",
      "creation_time": "2016-04-12T15:09:47",
      "resource_status": "INIT_COMPLETE",
      "updated_time": "2016-04-12T15:09:47",
      "required_by": [
        "ControllerNodesPostDeployment"
      ],
      "resource_status_reason": "",
      "physical_resource_id": "",
      "resource_type": "OS::Heat::StructuredDeployments",
      "metadata": {}
    },
    "NodeExtraConfig": {
      "parent_resource": "0",
      "resource_name": "NodeExtraConfig",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3/59a5e87f-86f8-4998-acd4-622f97adcaa1/resources/NodeExtraConfig",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3/59a5e87f-86f8-4998-acd4-622f97adcaa1",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "NodeExtraConfig",
      "creation_time": "2016-04-12T15:10:04",
      "resource_status": "INIT_COMPLETE",
      "updated_time": "2016-04-12T15:10:04",
      "required_by": [],
      "resource_status_reason": "",
      "physical_resource_id": "",
      "resource_type": "OS::TripleO::NodeExtraConfig",
      "metadata": {}
    },
    "Compute": {
      "resource_name": "Compute",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/Compute",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s/d3c93c64-778f-4cec-a5a8-062de076c0b6",
          "rel": "nested"
        }
      ],
      "logical_resource_id": "Compute",
      "creation_time": "2016-04-12T15:09:47",
      "resource_status_reason": "resources.Compute: ResourceInError: resources[0].resources.NovaCompute: Went to status ERROR due to \"Message: No valid host was found. There are not enough hosts available., Code: 500\"",
      "updated_time": "2016-04-12T15:09:47",
      "required_by": [
        "ComputeAllNodesDeployment",
        "allNodesConfig",
        "ComputeAllNodesValidationDeployment",
        "UpdateWorkflow",
        "ComputeNodesPostDeployment",
        "AllNodesExtraConfig",
        "ComputeCephDeployment"
      ],
      "resource_status": "CREATE_FAILED",
      "physical_resource_id": "d3c93c64-778f-4cec-a5a8-062de076c0b6",
      "resource_type": "OS::Heat::ResourceGroup",
      "metadata": {}
    },
    "ControllerDeployment": {
      "parent_resource": "2",
      "resource_name": "ControllerDeployment",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Controller-d7iywdnu5uzr-2-evqysybsnrrt/e4dc37e4-d565-4453-8d6e-a830953eb803/resources/ControllerDeployment",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Controller-d7iywdnu5uzr-2-evqysybsnrrt/e4dc37e4-d565-4453-8d6e-a830953eb803",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "ControllerDeployment",
      "creation_time": "2016-04-12T15:10:11",
      "resource_status": "INIT_COMPLETE",
      "updated_time": "2016-04-12T15:10:11",
      "required_by": [
        "ControllerExtraConfigPre"
      ],
      "resource_status_reason": "",
      "physical_resource_id": "",
      "resource_type": "OS::TripleO::SoftwareDeployment",
      "metadata": {}
    },
    "ControllerConfig": {
      "parent_resource": "2",
      "resource_name": "ControllerConfig",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Controller-d7iywdnu5uzr-2-evqysybsnrrt/e4dc37e4-d565-4453-8d6e-a830953eb803/resources/ControllerConfig",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Controller-d7iywdnu5uzr-2-evqysybsnrrt/e4dc37e4-d565-4453-8d6e-a830953eb803",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "ControllerConfig",
      "creation_time": "2016-04-12T15:10:11",
      "resource_status": "INIT_COMPLETE",
      "updated_time": "2016-04-12T15:10:11",
      "required_by": [
        "ControllerDeployment"
      ],
      "resource_status_reason": "",
      "physical_resource_id": "",
      "resource_type": "OS::Heat::StructuredConfig",
      "metadata": {}
    },
    "BlockStorageAllNodesDeployment": {
      "resource_name": "BlockStorageAllNodesDeployment",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/BlockStorageAllNodesDeployment",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "BlockStorageAllNodesDeployment",
      "creation_time": "2016-04-12T15:09:47",
      "resource_status": "INIT_COMPLETE",
      "updated_time": "2016-04-12T15:09:47",
      "required_by": [
        "BlockStorageNodesPostDeployment",
        "BlockStorageAllNodesValidationDeployment"
      ],
      "resource_status_reason": "",
      "physical_resource_id": "",
      "resource_type": "OS::Heat::StructuredDeployments",
      "metadata": {}
    },
    "ControllerClusterConfig": {
      "resource_name": "ControllerClusterConfig",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/ControllerClusterConfig",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "ControllerClusterConfig",
      "creation_time": "2016-04-12T15:09:47",
      "resource_status": "INIT_COMPLETE",
      "updated_time": "2016-04-12T15:09:47",
      "required_by": [
        "ControllerClusterDeployment"
      ],
      "resource_status_reason": "",
      "physical_resource_id": "",
      "resource_type": "OS::Heat::StructuredConfig",
      "metadata": {}
    },
    "NetworkDeployment": {
      "parent_resource": "0",
      "resource_name": "NetworkDeployment",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3/59a5e87f-86f8-4998-acd4-622f97adcaa1/resources/NetworkDeployment",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3/59a5e87f-86f8-4998-acd4-622f97adcaa1",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "NetworkDeployment",
      "creation_time": "2016-04-12T15:10:05",
      "resource_status": "INIT_COMPLETE",
      "updated_time": "2016-04-12T15:10:05",
      "required_by": [
        "NovaComputeDeployment"
      ],
      "resource_status_reason": "",
      "physical_resource_id": "",
      "resource_type": "OS::TripleO::SoftwareDeployment",
      "metadata": {}
    },
    "AllNodesExtraConfig": {
      "resource_name": "AllNodesExtraConfig",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/AllNodesExtraConfig",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "AllNodesExtraConfig",
      "creation_time": "2016-04-12T15:09:47",
      "resource_status": "INIT_COMPLETE",
      "updated_time": "2016-04-12T15:09:47",
      "required_by": [
        "BlockStorageNodesPostDeployment",
        "ComputeNodesPostDeployment",
        "ObjectStorageNodesPostDeployment",
        "CephStorageNodesPostDeployment",
        "ControllerNodesPostDeployment"
      ],
      "resource_status_reason": "",
      "physical_resource_id": "",
      "resource_type": "OS::TripleO::AllNodesExtraConfig",
      "metadata": {}
    },
    "NodeTLSData": {
      "parent_resource": "2",
      "resource_name": "NodeTLSData",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Controller-d7iywdnu5uzr-2-evqysybsnrrt/e4dc37e4-d565-4453-8d6e-a830953eb803/resources/NodeTLSData",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Controller-d7iywdnu5uzr-2-evqysybsnrrt/e4dc37e4-d565-4453-8d6e-a830953eb803",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "NodeTLSData",
      "creation_time": "2016-04-12T15:10:11",
      "resource_status": "INIT_COMPLETE",
      "updated_time": "2016-04-12T15:10:11",
      "required_by": [
        "NodeExtraConfig",
        "ControllerConfig"
      ],
      "resource_status_reason": "",
      "physical_resource_id": "",
      "resource_type": "OS::TripleO::NodeTLSData",
      "metadata": {}
    },
    "ControllerBootstrapNodeDeployment": {
      "resource_name": "ControllerBootstrapNodeDeployment",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/ControllerBootstrapNodeDeployment",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "ControllerBootstrapNodeDeployment",
      "creation_time": "2016-04-12T15:09:47",
      "resource_status": "INIT_COMPLETE",
      "updated_time": "2016-04-12T15:09:47",
      "required_by": [
        "ControllerNodesPostDeployment"
      ],
      "resource_status_reason": "",
      "physical_resource_id": "",
      "resource_type": "OS::Heat::StructuredDeployments",
      "metadata": {}
    },
    "ObjectStorageAllNodesDeployment": {
      "resource_name": "ObjectStorageAllNodesDeployment",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/ObjectStorageAllNodesDeployment",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "ObjectStorageAllNodesDeployment",
      "creation_time": "2016-04-12T15:09:47",
      "resource_status": "INIT_COMPLETE",
      "updated_time": "2016-04-12T15:09:47",
      "required_by": [
        "ObjectStorageAllNodesValidationDeployment",
        "ObjectStorageNodesPostDeployment"
      ],
      "resource_status_reason": "",
      "physical_resource_id": "",
      "resource_type": "OS::Heat::StructuredDeployments",
      "metadata": {}
    },
    "NodeUserData": {
      "parent_resource": "0",
      "resource_name": "NodeUserData",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3/59a5e87f-86f8-4998-acd4-622f97adcaa1/resources/NodeUserData",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3/59a5e87f-86f8-4998-acd4-622f97adcaa1",
          "rel": "stack"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3-NodeUserData-ohqnzhts3v3d/390a5c23-7616-4784-9ffd-edbc18810605",
          "rel": "nested"
        }
      ],
      "logical_resource_id": "NodeUserData",
      "creation_time": "2016-04-12T15:10:05",
      "resource_status_reason": "state changed",
      "updated_time": "2016-04-12T15:10:05",
      "required_by": [
        "UserData"
      ],
      "resource_status": "CREATE_COMPLETE",
      "physical_resource_id": "390a5c23-7616-4784-9ffd-edbc18810605",
      "resource_type": "OS::TripleO::NodeUserData",
      "metadata": {}
    },
    "ControllerExtraConfigPre": {
      "parent_resource": "2",
      "resource_name": "ControllerExtraConfigPre",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Controller-d7iywdnu5uzr-2-evqysybsnrrt/e4dc37e4-d565-4453-8d6e-a830953eb803/resources/ControllerExtraConfigPre",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Controller-d7iywdnu5uzr-2-evqysybsnrrt/e4dc37e4-d565-4453-8d6e-a830953eb803",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "ControllerExtraConfigPre",
      "creation_time": "2016-04-12T15:10:11",
      "resource_status": "INIT_COMPLETE",
      "updated_time": "2016-04-12T15:10:11",
      "required_by": [
        "NodeExtraConfig"
      ],
      "resource_status_reason": "",
      "physical_resource_id": "",
      "resource_type": "OS::TripleO::ControllerExtraConfigPre",
      "metadata": {}
    },
    "NodeTLSCAData": {
      "parent_resource": "0",
      "resource_name": "NodeTLSCAData",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3/59a5e87f-86f8-4998-acd4-622f97adcaa1/resources/NodeTLSCAData",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3/59a5e87f-86f8-4998-acd4-622f97adcaa1",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "NodeTLSCAData",
      "creation_time": "2016-04-12T15:10:04",
      "resource_status": "INIT_COMPLETE",
      "updated_time": "2016-04-12T15:10:04",
      "required_by": [
        "NodeExtraConfig"
      ],
      "resource_status_reason": "",
      "physical_resource_id": "",
      "resource_type": "OS::TripleO::NodeTLSCAData",
      "metadata": {}
    },
    "ExternalPort": {
      "parent_resource": "0",
      "resource_name": "ExternalPort",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3/59a5e87f-86f8-4998-acd4-622f97adcaa1/resources/ExternalPort",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3/59a5e87f-86f8-4998-acd4-622f97adcaa1",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "ExternalPort",
      "creation_time": "2016-04-12T15:10:05",
      "resource_status": "INIT_COMPLETE",
      "updated_time": "2016-04-12T15:10:05",
      "required_by": [
        "NetworkConfig",
        "NetIpMap"
      ],
      "resource_status_reason": "",
      "physical_resource_id": "",
      "resource_type": "OS::TripleO::Compute::Ports::ExternalPort",
      "metadata": {}
    },
    "AllNodesValidationConfig": {
      "resource_name": "AllNodesValidationConfig",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/AllNodesValidationConfig",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "AllNodesValidationConfig",
      "creation_time": "2016-04-12T15:09:47",
      "resource_status": "INIT_COMPLETE",
      "updated_time": "2016-04-12T15:09:47",
      "required_by": [
        "ControllerAllNodesValidationDeployment",
        "ObjectStorageAllNodesValidationDeployment",
        "BlockStorageAllNodesValidationDeployment",
        "ComputeAllNodesValidationDeployment",
        "CephStorageAllNodesValidationDeployment"
      ],
      "resource_status_reason": "",
      "physical_resource_id": "",
      "resource_type": "OS::TripleO::AllNodes::Validation",
      "metadata": {}
    },
    "PublicVirtualIP": {
      "resource_name": "PublicVirtualIP",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/PublicVirtualIP",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-PublicVirtualIP-wd3dmh5doc3v/736e0867-a120-4a38-8b7e-ea7113bdadc0",
          "rel": "nested"
        }
      ],
      "logical_resource_id": "PublicVirtualIP",
      "creation_time": "2016-04-12T15:09:47",
      "resource_status_reason": "state changed",
      "updated_time": "2016-04-12T15:09:47",
      "required_by": [
        "VipMap"
      ],
      "resource_status": "CREATE_COMPLETE",
      "physical_resource_id": "736e0867-a120-4a38-8b7e-ea7113bdadc0",
      "resource_type": "OS::TripleO::Network::Ports::ExternalVipPort",
      "metadata": {}
    },
    "ComputeExtraConfigPre": {
      "parent_resource": "0",
      "resource_name": "ComputeExtraConfigPre",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3/59a5e87f-86f8-4998-acd4-622f97adcaa1/resources/ComputeExtraConfigPre",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3/59a5e87f-86f8-4998-acd4-622f97adcaa1",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "ComputeExtraConfigPre",
      "creation_time": "2016-04-12T15:10:04",
      "resource_status": "INIT_COMPLETE",
      "updated_time": "2016-04-12T15:10:04",
      "required_by": [
        "NodeExtraConfig"
      ],
      "resource_status_reason": "",
      "physical_resource_id": "",
      "resource_type": "OS::TripleO::ComputeExtraConfigPre",
      "metadata": {}
    },
    "ControllerIpListMap": {
      "resource_name": "ControllerIpListMap",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/ControllerIpListMap",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "ControllerIpListMap",
      "creation_time": "2016-04-12T15:09:47",
      "resource_status": "INIT_COMPLETE",
      "updated_time": "2016-04-12T15:09:47",
      "required_by": [
        "allNodesConfig",
        "CephClusterConfig"
      ],
      "resource_status_reason": "",
      "physical_resource_id": "",
      "resource_type": "OS::TripleO::Network::Ports::NetIpListMap",
      "metadata": {}
    },
    "InternalNetwork": {
      "parent_resource": "Networks",
      "resource_name": "InternalNetwork",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Networks-zyubznagvv6c/bfb0f40b-3c67-4e65-8517-6cff9dfab7ff/resources/InternalNetwork",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Networks-zyubznagvv6c/bfb0f40b-3c67-4e65-8517-6cff9dfab7ff",
          "rel": "stack"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Networks-zyubznagvv6c-InternalNetwork-cafng6vxx6bp/c207d1a9-b433-4fee-966d-14488e4d6016",
          "rel": "nested"
        }
      ],
      "logical_resource_id": "InternalNetwork",
      "creation_time": "2016-04-12T15:09:48",
      "resource_status_reason": "state changed",
      "updated_time": "2016-04-12T15:09:48",
      "required_by": [],
      "resource_status": "CREATE_COMPLETE",
      "physical_resource_id": "c207d1a9-b433-4fee-966d-14488e4d6016",
      "resource_type": "OS::TripleO::Network::InternalApi",
      "metadata": {}
    },
    "NovaComputeConfig": {
      "parent_resource": "0",
      "resource_name": "NovaComputeConfig",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3/59a5e87f-86f8-4998-acd4-622f97adcaa1/resources/NovaComputeConfig",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3/59a5e87f-86f8-4998-acd4-622f97adcaa1",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "NovaComputeConfig",
      "creation_time": "2016-04-12T15:10:05",
      "resource_status": "CREATE_COMPLETE",
      "updated_time": "2016-04-12T15:10:05",
      "required_by": [
        "NovaComputeDeployment"
      ],
      "resource_status_reason": "state changed",
      "physical_resource_id": "5a77f97b-500a-4cb8-a943-27c54e77a1bd",
      "resource_type": "OS::Heat::StructuredConfig",
      "metadata": {}
    },
    "ManagementNetwork": {
      "parent_resource": "Networks",
      "resource_name": "ManagementNetwork",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Networks-zyubznagvv6c/bfb0f40b-3c67-4e65-8517-6cff9dfab7ff/resources/ManagementNetwork",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Networks-zyubznagvv6c/bfb0f40b-3c67-4e65-8517-6cff9dfab7ff",
          "rel": "stack"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Networks-zyubznagvv6c-ManagementNetwork-tip34zbqkbzx/3589cd45-fbff-4209-8dfe-93ae426d2579",
          "rel": "nested"
        }
      ],
      "logical_resource_id": "ManagementNetwork",
      "creation_time": "2016-04-12T15:09:48",
      "resource_status_reason": "state changed",
      "updated_time": "2016-04-12T15:09:48",
      "required_by": [],
      "resource_status": "CREATE_COMPLETE",
      "physical_resource_id": "3589cd45-fbff-4209-8dfe-93ae426d2579",
      "resource_type": "OS::TripleO::Network::Management",
      "metadata": {}
    },
    "CephClusterConfig": {
      "resource_name": "CephClusterConfig",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/CephClusterConfig",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "CephClusterConfig",
      "creation_time": "2016-04-12T15:09:47",
      "resource_status": "INIT_COMPLETE",
      "updated_time": "2016-04-12T15:09:47",
      "required_by": [
        "ControllerCephDeployment",
        "CephStorageCephDeployment",
        "ComputeCephDeployment"
      ],
      "resource_status_reason": "",
      "physical_resource_id": "",
      "resource_type": "OS::TripleO::CephClusterConfig::SoftwareConfig",
      "metadata": {}
    },
    "BlockStorage": {
      "resource_name": "BlockStorage",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/BlockStorage",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-BlockStorage-l4jgvstzdqhy/2bfadc97-89fc-42b0-920e-b0ebd7ed3a9d",
          "rel": "nested"
        }
      ],
      "logical_resource_id": "BlockStorage",
      "creation_time": "2016-04-12T15:09:47",
      "resource_status_reason": "state changed",
      "updated_time": "2016-04-12T15:09:47",
      "required_by": [
        "BlockStorageAllNodesDeployment",
        "BlockStorageNodesPostDeployment",
        "BlockStorageAllNodesValidationDeployment",
        "AllNodesExtraConfig",
        "UpdateWorkflow",
        "allNodesConfig"
      ],
      "resource_status": "CREATE_COMPLETE",
      "physical_resource_id": "2bfadc97-89fc-42b0-920e-b0ebd7ed3a9d",
      "resource_type": "OS::Heat::ResourceGroup",
      "metadata": {}
    },
    "RedisVirtualIP": {
      "resource_name": "RedisVirtualIP",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/RedisVirtualIP",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-RedisVirtualIP-ndkwnexwqzw4/74727fb1-eb7b-44c7-ad75-3e1f11fd3d67",
          "rel": "nested"
        }
      ],
      "logical_resource_id": "RedisVirtualIP",
      "creation_time": "2016-04-12T15:09:47",
      "resource_status_reason": "state changed",
      "updated_time": "2016-04-12T15:09:47",
      "required_by": [
        "Controller",
        "VipDeployment"
      ],
      "resource_status": "CREATE_COMPLETE",
      "physical_resource_id": "74727fb1-eb7b-44c7-ad75-3e1f11fd3d67",
      "resource_type": "OS::TripleO::Network::Ports::RedisVipPort",
      "metadata": {}
    },
    "1": {
      "parent_resource": "Controller",
      "resource_name": "1",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Controller-d7iywdnu5uzr/119696b0-92ac-44ab-85d6-614c68af3949/resources/1",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Controller-d7iywdnu5uzr/119696b0-92ac-44ab-85d6-614c68af3949",
          "rel": "stack"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Controller-d7iywdnu5uzr-1-klhc6fwkxjt3/7ecb0624-6a40-449e-bb6c-e85b8bf2b733",
          "rel": "nested"
        }
      ],
      "logical_resource_id": "1",
      "creation_time": "2016-04-12T15:10:06",
      "resource_status_reason": "ResourceInError: resources[1].resources.Controller: Went to status ERROR due to \"Message: No valid host was found. There are not enough hosts available., Code: 500\"",
      "updated_time": "2016-04-12T15:10:06",
      "required_by": [],
      "resource_status": "CREATE_FAILED",
      "physical_resource_id": "7ecb0624-6a40-449e-bb6c-e85b8bf2b733",
      "resource_type": "OS::TripleO::Controller",
      "metadata": {}
    },
    "config": {
      "parent_resource": "UpdateConfig",
      "resource_name": "config",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3-UpdateConfig-gfypsblpw6ci/a6fa0cac-66bd-4efb-b5a6-a37a8fc13f36/resources/config",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3-UpdateConfig-gfypsblpw6ci/a6fa0cac-66bd-4efb-b5a6-a37a8fc13f36",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "config",
      "creation_time": "2016-04-12T15:10:06",
      "resource_status": "CREATE_COMPLETE",
      "updated_time": "2016-04-12T15:10:06",
      "required_by": [],
      "resource_status_reason": "state changed",
      "physical_resource_id": "913aca44-764c-4550-bf7a-37ac24c53228",
      "resource_type": "OS::Heat::SoftwareConfig",
      "metadata": {}
    },
    "StorageMgmtNetwork": {
      "parent_resource": "Networks",
      "resource_name": "StorageMgmtNetwork",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Networks-zyubznagvv6c/bfb0f40b-3c67-4e65-8517-6cff9dfab7ff/resources/StorageMgmtNetwork",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Networks-zyubznagvv6c/bfb0f40b-3c67-4e65-8517-6cff9dfab7ff",
          "rel": "stack"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Networks-zyubznagvv6c-StorageMgmtNetwork-2bir7wn3igpz/c1df71aa-60c0-4302-8227-2584aa2b7cab",
          "rel": "nested"
        }
      ],
      "logical_resource_id": "StorageMgmtNetwork",
      "creation_time": "2016-04-12T15:09:48",
      "resource_status_reason": "state changed",
      "updated_time": "2016-04-12T15:09:48",
      "required_by": [],
      "resource_status": "CREATE_COMPLETE",
      "physical_resource_id": "c1df71aa-60c0-4302-8227-2584aa2b7cab",
      "resource_type": "OS::TripleO::Network::StorageMgmt",
      "metadata": {}
    },
    "CephStorageNodesPostDeployment": {
      "resource_name": "CephStorageNodesPostDeployment",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/CephStorageNodesPostDeployment",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "CephStorageNodesPostDeployment",
      "creation_time": "2016-04-12T15:09:47",
      "resource_status": "INIT_COMPLETE",
      "updated_time": "2016-04-12T15:09:47",
      "required_by": [],
      "resource_status_reason": "",
      "physical_resource_id": "",
      "resource_type": "OS::TripleO::CephStoragePostDeployment",
      "metadata": {}
    },
    "ControllerClusterDeployment": {
      "resource_name": "ControllerClusterDeployment",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/ControllerClusterDeployment",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "ControllerClusterDeployment",
      "creation_time": "2016-04-12T15:09:47",
      "resource_status": "INIT_COMPLETE",
      "updated_time": "2016-04-12T15:09:47",
      "required_by": [],
      "resource_status_reason": "",
      "physical_resource_id": "",
      "resource_type": "OS::Heat::StructuredDeployments",
      "metadata": {}
    },
    "EndpointMap": {
      "resource_name": "EndpointMap",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/EndpointMap",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-EndpointMap-5wrgqx6vxql2/93dede47-4221-4310-8685-032d788434fe",
          "rel": "nested"
        }
      ],
      "logical_resource_id": "EndpointMap",
      "creation_time": "2016-04-12T15:09:47",
      "resource_status_reason": "state changed",
      "updated_time": "2016-04-12T15:09:47",
      "required_by": [
        "BlockStorage",
        "Controller",
        "Compute"
      ],
      "resource_status": "CREATE_COMPLETE",
      "physical_resource_id": "93dede47-4221-4310-8685-032d788434fe",
      "resource_type": "OS::TripleO::EndpointMap",
      "metadata": {}
    },
    "ComputeAllNodesDeployment": {
      "resource_name": "ComputeAllNodesDeployment",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/ComputeAllNodesDeployment",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "ComputeAllNodesDeployment",
      "creation_time": "2016-04-12T15:09:47",
      "resource_status": "INIT_COMPLETE",
      "updated_time": "2016-04-12T15:09:47",
      "required_by": [
        "ComputeNodesPostDeployment",
        "ComputeAllNodesValidationDeployment"
      ],
      "resource_status_reason": "",
      "physical_resource_id": "",
      "resource_type": "OS::Heat::StructuredDeployments",
      "metadata": {}
    },
    "CephStorageAllNodesValidationDeployment": {
      "resource_name": "CephStorageAllNodesValidationDeployment",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/CephStorageAllNodesValidationDeployment",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "CephStorageAllNodesValidationDeployment",
      "creation_time": "2016-04-12T15:09:47",
      "resource_status": "INIT_COMPLETE",
      "updated_time": "2016-04-12T15:09:47",
      "required_by": [
        "AllNodesExtraConfig"
      ],
      "resource_status_reason": "",
      "physical_resource_id": "",
      "resource_type": "OS::Heat::StructuredDeployments",
      "metadata": {}
    },
    "UserData": {
      "parent_resource": "0",
      "resource_name": "UserData",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3/59a5e87f-86f8-4998-acd4-622f97adcaa1/resources/UserData",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-Compute-56idrrd2a77s-0-djt27nywnrg3/59a5e87f-86f8-4998-acd4-622f97adcaa1",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "UserData",
      "creation_time": "2016-04-12T15:10:05",
      "resource_status": "CREATE_COMPLETE",
      "updated_time": "2016-04-12T15:10:05",
      "required_by": [
        "NovaCompute"
      ],
      "resource_status_reason": "state changed",
      "physical_resource_id": "3f330bb9-f545-4ec1-8fb2-a7f329e42fc6",
      "resource_type": "OS::Heat::MultipartMime",
      "metadata": {}
    },
    "CephStorage": {
      "resource_name": "CephStorage",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/CephStorage",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud-CephStorage-sejj7dhcfhtd/0404dbec-c920-4351-9c35-79977300b74a",
          "rel": "nested"
        }
      ],
      "logical_resource_id": "CephStorage",
      "creation_time": "2016-04-12T15:09:47",
      "resource_status_reason": "state changed",
      "updated_time": "2016-04-12T15:09:47",
      "required_by": [
        "CephStorageAllNodesDeployment",
        "CephStorageNodesPostDeployment",
        "CephStorageAllNodesValidationDeployment",
        "CephStorageCephDeployment",
        "UpdateWorkflow",
        "AllNodesExtraConfig",
        "allNodesConfig"
      ],
      "resource_status": "CREATE_COMPLETE",
      "physical_resource_id": "0404dbec-c920-4351-9c35-79977300b74a",
      "resource_type": "OS::Heat::ResourceGroup",
      "metadata": {}
    },
    "ComputeAllNodesValidationDeployment": {
      "resource_name": "ComputeAllNodesValidationDeployment",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/ComputeAllNodesValidationDeployment",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "ComputeAllNodesValidationDeployment",
      "creation_time": "2016-04-12T15:09:47",
      "resource_status": "INIT_COMPLETE",
      "updated_time": "2016-04-12T15:09:47",
      "required_by": [
        "AllNodesExtraConfig"
      ],
      "resource_status_reason": "",
      "physical_resource_id": "",
      "resource_type": "OS::Heat::StructuredDeployments",
      "metadata": {}
    }
  },
  "events": {
    "CephStorage": {
      "resource_name": "CephStorage",
      "event_time": "2016-04-12T15:09:52",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/CephStorage/events/908508ae-b2d1-48ab-b6bf-433827c17cde",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/CephStorage",
          "rel": "resource"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "CephStorage",
      "resource_status": "CREATE_IN_PROGRESS",
      "resource_status_reason": "state changed",
      "physical_resource_id": '',
      "id": "908508ae-b2d1-48ab-b6bf-433827c17cde"
    },
    "VipConfig": {
      "resource_name": "VipConfig",
      "event_time": "2016-04-12T15:09:48",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/VipConfig/events/674c34c7-a1b9-4e18-af39-afb6b58c318a",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/VipConfig",
          "rel": "resource"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "VipConfig",
      "resource_status": "CREATE_IN_PROGRESS",
      "resource_status_reason": "state changed",
      "physical_resource_id": '',
      "id": "674c34c7-a1b9-4e18-af39-afb6b58c318a"
    },
    "PublicVirtualIP": {
      "resource_name": "PublicVirtualIP",
      "event_time": "2016-04-12T15:09:55",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/PublicVirtualIP/events/a481349c-d525-4a4e-aa91-211395f279c9",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/PublicVirtualIP",
          "rel": "resource"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "PublicVirtualIP",
      "resource_status": "CREATE_IN_PROGRESS",
      "resource_status_reason": "state changed",
      "physical_resource_id": '',
      "id": "a481349c-d525-4a4e-aa91-211395f279c9"
    },
    "StorageVirtualIP": {
      "resource_name": "StorageVirtualIP",
      "event_time": "2016-04-12T15:09:56",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/StorageVirtualIP/events/3201a5ff-b8d4-4e75-9053-dcecb84c0185",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/StorageVirtualIP",
          "rel": "resource"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "StorageVirtualIP",
      "resource_status": "CREATE_IN_PROGRESS",
      "resource_status_reason": "state changed",
      "physical_resource_id": '',
      "id": "3201a5ff-b8d4-4e75-9053-dcecb84c0185"
    },
    "InternalApiVirtualIP": {
      "resource_name": "InternalApiVirtualIP",
      "event_time": "2016-04-12T15:09:56",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/InternalApiVirtualIP/events/a4afac05-00df-4775-933c-129d89300b11",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/InternalApiVirtualIP",
          "rel": "resource"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "InternalApiVirtualIP",
      "resource_status": "CREATE_IN_PROGRESS",
      "resource_status_reason": "state changed",
      "physical_resource_id": '',
      "id": "a4afac05-00df-4775-933c-129d89300b11"
    },
    "BlockStorage": {
      "resource_name": "BlockStorage",
      "event_time": "2016-04-12T15:10:01",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/BlockStorage/events/5d099a2b-0ac8-4b27-a832-189f3f66e117",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/BlockStorage",
          "rel": "resource"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "BlockStorage",
      "resource_status": "CREATE_IN_PROGRESS",
      "resource_status_reason": "state changed",
      "physical_resource_id": '',
      "id": "5d099a2b-0ac8-4b27-a832-189f3f66e117"
    },
    "RedisVirtualIP": {
      "resource_name": "RedisVirtualIP",
      "event_time": "2016-04-12T15:09:56",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/RedisVirtualIP/events/73ddce4b-a5e8-40a4-bdb9-156df6c8bf83",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/RedisVirtualIP",
          "rel": "resource"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "RedisVirtualIP",
      "resource_status": "CREATE_IN_PROGRESS",
      "resource_status_reason": "state changed",
      "physical_resource_id": '',
      "id": "73ddce4b-a5e8-40a4-bdb9-156df6c8bf83"
    },
    "overcloud": {
      "resource_name": "overcloud",
      "event_time": "2016-04-12T15:09:48",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/overcloud/events/c9514253-6eb6-43f1-95ce-1d33b857697f",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/overcloud",
          "rel": "resource"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "overcloud",
      "resource_status": "CREATE_IN_PROGRESS",
      "resource_status_reason": "Stack CREATE started",
      "physical_resource_id": "9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
      "id": "c9514253-6eb6-43f1-95ce-1d33b857697f"
    },
    "PcsdPassword": {
      "resource_name": "PcsdPassword",
      "event_time": "2016-04-12T15:09:48",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/PcsdPassword/events/8fe2e8da-bcba-46d7-b12f-127a66059953",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/PcsdPassword",
          "rel": "resource"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "PcsdPassword",
      "resource_status": "CREATE_IN_PROGRESS",
      "resource_status_reason": "state changed",
      "physical_resource_id": '',
      "id": "8fe2e8da-bcba-46d7-b12f-127a66059953"
    },
    "RabbitCookie": {
      "resource_name": "RabbitCookie",
      "event_time": "2016-04-12T15:09:48",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/RabbitCookie/events/b07830b3-596c-45f8-aa48-9abc8f40f2ad",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/RabbitCookie",
          "rel": "resource"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "RabbitCookie",
      "resource_status": "CREATE_IN_PROGRESS",
      "resource_status_reason": "state changed",
      "physical_resource_id": '',
      "id": "b07830b3-596c-45f8-aa48-9abc8f40f2ad"
    },
    "ControlVirtualIP": {
      "resource_name": "ControlVirtualIP",
      "event_time": "2016-04-12T15:09:53",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/ControlVirtualIP/events/e7ecad48-cfa4-43f7-9296-9ca47cd474e5",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/ControlVirtualIP",
          "rel": "resource"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "ControlVirtualIP",
      "resource_status": "CREATE_IN_PROGRESS",
      "resource_status_reason": "state changed",
      "physical_resource_id": '',
      "id": "e7ecad48-cfa4-43f7-9296-9ca47cd474e5"
    },
    "Controller": {
      "resource_name": "Controller",
      "event_time": "2016-04-12T15:10:04",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/Controller/events/8cb584e5-6aba-4175-a9d8-6edbcc3f9e0e",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/Controller",
          "rel": "resource"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "Controller",
      "resource_status": "CREATE_IN_PROGRESS",
      "resource_status_reason": "state changed",
      "physical_resource_id": '',
      "id": "8cb584e5-6aba-4175-a9d8-6edbcc3f9e0e"
    },
    "MysqlRootPassword": {
      "resource_name": "MysqlRootPassword",
      "event_time": "2016-04-12T15:09:48",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/MysqlRootPassword/events/79e9cf3b-c9c8-435d-894b-0af97b1a501c",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/MysqlRootPassword",
          "rel": "resource"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "MysqlRootPassword",
      "resource_status": "CREATE_IN_PROGRESS",
      "resource_status_reason": "state changed",
      "physical_resource_id": '',
      "id": "79e9cf3b-c9c8-435d-894b-0af97b1a501c"
    },
    "MysqlClusterUniquePart": {
      "resource_name": "MysqlClusterUniquePart",
      "event_time": "2016-04-12T15:09:48",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/MysqlClusterUniquePart/events/498d79a2-959c-49d2-8a91-6cdb96e8e95f",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/MysqlClusterUniquePart",
          "rel": "resource"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "MysqlClusterUniquePart",
      "resource_status": "CREATE_IN_PROGRESS",
      "resource_status_reason": "state changed",
      "physical_resource_id": '',
      "id": "498d79a2-959c-49d2-8a91-6cdb96e8e95f"
    },
    "Compute": {
      "resource_name": "Compute",
      "event_time": "2016-04-12T15:10:02",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/Compute/events/fd224291-2403-46c9-be43-a0fe68d10c7a",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/Compute",
          "rel": "resource"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "Compute",
      "resource_status": "CREATE_IN_PROGRESS",
      "resource_status_reason": "state changed",
      "physical_resource_id": '',
      "id": "fd224291-2403-46c9-be43-a0fe68d10c7a"
    },
    "VipMap": {
      "resource_name": "VipMap",
      "event_time": "2016-04-12T15:09:58",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/VipMap/events/07fbc803-d12f-450e-a01c-e80603f9a445",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/VipMap",
          "rel": "resource"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "VipMap",
      "resource_status": "CREATE_IN_PROGRESS",
      "resource_status_reason": "state changed",
      "physical_resource_id": '',
      "id": "07fbc803-d12f-450e-a01c-e80603f9a445"
    },
    "ObjectStorage": {
      "resource_name": "ObjectStorage",
      "event_time": "2016-04-12T15:09:53",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/ObjectStorage/events/7f5f0ee2-b104-4fde-b703-cafa0e4c255d",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/ObjectStorage",
          "rel": "resource"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "ObjectStorage",
      "resource_status": "CREATE_IN_PROGRESS",
      "resource_status_reason": "state changed",
      "physical_resource_id": '',
      "id": "7f5f0ee2-b104-4fde-b703-cafa0e4c255d"
    },
    "HeatAuthEncryptionKey": {
      "resource_name": "HeatAuthEncryptionKey",
      "event_time": "2016-04-12T15:09:48",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/HeatAuthEncryptionKey/events/74c16f0a-fcd4-4e8f-bed4-bdfed71ad576",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/HeatAuthEncryptionKey",
          "rel": "resource"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "HeatAuthEncryptionKey",
      "resource_status": "CREATE_IN_PROGRESS",
      "resource_status_reason": "state changed",
      "physical_resource_id": '',
      "id": "74c16f0a-fcd4-4e8f-bed4-bdfed71ad576"
    },
    "EndpointMap": {
      "resource_name": "EndpointMap",
      "event_time": "2016-04-12T15:10:00",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/EndpointMap/events/2138e0d9-c7bd-475e-a0ba-81cc24f59962",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/EndpointMap",
          "rel": "resource"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "EndpointMap",
      "resource_status": "CREATE_IN_PROGRESS",
      "resource_status_reason": "state changed",
      "physical_resource_id": '',
      "id": "2138e0d9-c7bd-475e-a0ba-81cc24f59962"
    },
    "StorageMgmtVirtualIP": {
      "resource_name": "StorageMgmtVirtualIP",
      "event_time": "2016-04-12T15:09:55",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/StorageMgmtVirtualIP/events/721ab1e1-2b91-4fa7-9555-61c769714331",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/StorageMgmtVirtualIP",
          "rel": "resource"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "StorageMgmtVirtualIP",
      "resource_status": "CREATE_IN_PROGRESS",
      "resource_status_reason": "state changed",
      "physical_resource_id": '',
      "id": "721ab1e1-2b91-4fa7-9555-61c769714331"
    },
    "HorizonSecret": {
      "resource_name": "HorizonSecret",
      "event_time": "2016-04-12T15:09:48",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/HorizonSecret/events/34ab0d12-570e-4780-bb48-106328e4f0a2",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/HorizonSecret",
          "rel": "resource"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "HorizonSecret",
      "resource_status": "CREATE_IN_PROGRESS",
      "resource_status_reason": "state changed",
      "physical_resource_id": '',
      "id": "34ab0d12-570e-4780-bb48-106328e4f0a2"
    },
    "Networks": {
      "resource_name": "Networks",
      "event_time": "2016-04-12T15:09:48",
      "links": [
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/Networks/events/f5d22d22-8d1e-4234-ae18-346ff8b1352b",
          "rel": "self"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee/resources/Networks",
          "rel": "resource"
        },
        {
          "href": "http://192.0.2.240:8004/v1/9de7e9a9a2a242718cffa65dae677a33/stacks/overcloud/9d47fbf2-1f57-4ae4-9d65-6a799ea284ee",
          "rel": "stack"
        }
      ],
      "logical_resource_id": "Networks",
      "resource_status": "CREATE_IN_PROGRESS",
      "resource_status_reason": "state changed",
      "physical_resource_id": '',
      "id": "f5d22d22-8d1e-4234-ae18-346ff8b1352b"
    }
  }
}

LOREM_IPSUM = [
    'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
    'Donec a diam lectus. Sed sit amet ipsum mauris.',
    'Maecenas congue ligula ac quam viverra nec consectetur ante hendrerit.',
    'Donec et mollis dolor.',
    'Praesent et diam eget libero egestas mattis sit amet vitae augue.',
    'Nam tincidunt congue enim, ut porta lorem lacinia consectetur.',
    'Donec ut libero sed arcu vehicula ultricies a non tortor.',
    'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
    'Aenean ut gravida lorem. Ut turpis felis, pulvinar a semper sed, '
    'adipiscing id dolor.',
    'Pellentesque auctor nisi id magna consequat sagittis.',
    'Curabitur dapibus enim sit amet elit pharetra tincidunt feugiat '
    'nisl imperdiet.',
    'Ut convallis libero in urna ultrices accumsan.',
    'Donec sed odio eros.',
    'Donec viverra mi quis quam pulvinar at malesuada arcu rhoncus.',
    'Cum sociis natoque penatibus et magnis dis parturient montes, '
    'nascetur ridiculus mus.',
    'In rutrum accumsan ultricies.',
    'Mauris vitae nisi at sem facilisis semper ac in est.'
]

JUNIT = """
<testsuite errors="0" failures="0" name="pytest" skips="1"
           tests="3" time="46.050">
<properties>
  <property name="x" value="y" />
  <property name="a" value="b" />
</properties>
<testcase classname="" file="test-requirements.txt"
          name="test-requirements.txt" time="0.0109479427338">
    <skipped message="all tests skipped by +SKIP option"
             type="pytest.skip">Skipped for whatever reasons</skipped>
</testcase>
<testcase classname="tests.test_app" file="tests/test_app.py" line="26"
          name="test_cors_preflight" time="2.91562318802"/>
<testcase classname="tests.test_app" file="tests/test_app.py" line="42"
          name="test_cors_headers" time="0.574683904648"/>
</testsuite>"""

DATA = {
    "ksgen_args": {
        "installer-network-variant": "ml2-vxlan",
        "installer-env": "virthost",
        "installer-tempest": "minimal",
        "installer-network": "neutron",
        "installer-topology": "minimal",
        "distro": "centos-7.0",
        "product": "rdo",
        "extra-vars": {
            "installer": {
                "nodes": {
                    "node_cpu": 24
                }
            },
            "provisioner": {
                "type": "manual"
            }
        },
        "installer-images": "build",
        "installer-deploy": "templates",
        "installer-network-isolation": "single_nic_vlans",
        "product-version-build": "last_known_good_mgt",
        "product-version": "liberty",
        "installer": "rdo_manager",
        "product-version-repo": "delorean_mgt",
        "workarounds": "enabled",
        "installer-post_action": "none",
        "provisioner": "manual"
    }
}


def create_remote_cis(db_conn, company, tests, topic_id):
    # create 3 remote CIS per company (one for each test)
    remote_cis = {}

    def generate_jd_names(test_name, job_definition_names):
        name = '%s %s %s' % (company['name'], test_name,
                             random.choice(VERSIONS))
        if len(job_definition_names) == 3:
            return job_definition_names
        if name not in job_definition_names:
            job_definition_names.append(name)

        return generate_jd_names(test_name, job_definition_names)

    def generate_data_field():
        data = {}
        for _ in range(0, random.randint(0, 10)):
            data_type = random.choice(list(REMOTE_CIS_ATTRS.keys()))
            data[data_type] = random.choice(REMOTE_CIS_ATTRS[data_type])
        return data

    for i, test_name in enumerate(tests):
        remote_ci = {
            'data': DATA,
            'team_id': company['id'],
            'name': '%s - %d' % (company['name'], i)
        }
        remote_ci = db_insert(db_conn, models.REMOTECIS, **remote_ci)
        job_definitions = []

        # create 3 job definitions for each test
        for job_definition_name in generate_jd_names(test_name, []):
            job_definition = {
                'name': job_definition_name,
                'priority': random.randint(0, 10) * 100,
                'topic_id': topic_id,
                'type': "type_%s" % (random.randint(0, 10) * 100)
            }
            job_definition['id'] = db_insert(db_conn, models.JOBDEFINITIONS,
                                             **job_definition)
            job_definitions.append(job_definition)

        remote_cis[remote_ci] = job_definitions

    return remote_cis


def create_jobs(db_conn, company_id, remote_cis):
    jobs = []
    for remote_ci, job_definitions in remote_cis.items():
        for job_definition in job_definitions:
            delta = datetime.timedelta(hours=random.randint(0, 10))
            since = datetime.timedelta(days=random.randint(0, 3),
                                       hours=random.randint(0, 10))
            job = {
                'remoteci_id': remote_ci,
                'jobdefinition_id': job_definition['id'],
                'created_at': datetime.datetime.now() - since - delta,
                'updated_at': datetime.datetime.now() - since,
                'status': random.choice(JOB_STATUSES),
                'configuration': json.dumps(TRIPLEOSTACKDUMP),
                'team_id': company_id
            }

            if not bool(random.randint(0, 4)):
                c = lorem(1, bool(random.randint(0, 3)))
                job['comment'] = c

            job['id'] = db_insert(db_conn, models.JOBS, **job)
            jobs.append(job)

    return jobs


def create_jobdefinition_components(db_conn, components, job_definitions):
    for job_definition in job_definitions:

        # add between 1 and 5 components on the jobdefinition
        nb_components = random.randint(1, 5)
        for i in range(0, nb_components):
            db_insert(db_conn, models.JOIN_JOBDEFINITIONS_COMPONENTS,
                      jobdefinition_id=job_definition['id'],
                      component_id=components[i])


def create_files(db_conn, jobstate, company_id):
    def filename_generator():
        words = []
        for _ in range(0, random.randint(1, 4)):
            words.append(random.choice(NAMES))
        return '_'.join(words)

    for _ in range(0, random.randint(1, 4)):

        name = '%s.txt' % filename_generator()
        args = {
            'name': name,
            'mime': 'text/plain',
            'md5': hashlib.md5(name.encode('utf8')).hexdigest(),
            'jobstate_id': jobstate,
            'team_id': company_id
        }

        db_insert(db_conn, models.FILES, **args)


def attach_files_to_jobs(db_conn, job, company_id):
    job, job_def = job
    id = job['id']

    def filename_generator():
        words = []
        for _ in range(0, random.randint(1, 4)):
            words.append(random.choice(NAMES))
        return '_'.join(words)

    name = '%s.txt' % filename_generator()
    args = {
        'name': name,
        'mime': 'text/plain',
        'md5': hashlib.md5(name.encode('utf8')).hexdigest(),
        'job_id': id,
        'team_id': company_id
    }

    db_insert(db_conn, models.FILES, **args)

    # Insert a Junit file
    name = '%s.xml' % filename_generator()
    args = {
        'name': name,
        'content': JUNIT,
        'mime': 'application/junit',
        'md5': hashlib.md5(name.encode('utf8')).hexdigest(),
        'job_id': id,
        'team_id': company_id
    }
    db_insert(db_conn, models.FILES, **args)


def create_jobstates_and_files(db_conn, job, company_id):
    job, job_def = job

    name = job_def['name']
    step = job['status']
    id = job['id']

    # create "new" jobstate do not create files
    db_insert(db_conn, models.JOBSTATES, status='new',
              comment='Job "%s" created' % name,
              job_id=id, team_id=company_id,
              created_at=job['created_at'])

    if step == 'new':
        return

    start, end = job['created_at'], job['updated_at']
    start = time.mktime(start.timetuple())
    end = time.mktime(end.timetuple())

    step_number = JOB_STATUSES.index(step)

    # calculate timedelta for job running
    job_start = int(start + random.random() * (end - start))
    job_duration = end - job_start

    def compute_creation(current_step):
        step_index = JOB_STATUSES.index(current_step)
        creation = job_start + (job_duration * step_index / step_number)
        return datetime.datetime.fromtimestamp(creation)

    # create "pre-run" jobstate and new files associated
    created_at = compute_creation('pre-run')
    jobstate = db_insert(db_conn, models.JOBSTATES, status='pre-run',
                         comment='initializing %s' % name,
                         job_id=id, team_id=company_id, created_at=created_at)
    create_files(db_conn, jobstate, company_id)

    if step == 'pre-run':
        return

    # create "running" jobstate
    created_at = compute_creation('running')
    jobstate = db_insert(db_conn, models.JOBSTATES, status='running',
                         comment='running %s...' % name,
                         job_id=id, team_id=company_id, created_at=created_at)
    create_files(db_conn, jobstate, company_id)

    if step == 'running':
        return

    # create "post-run" jobstate sometimes
    created_at = compute_creation('post-run')
    if random.random() > 0.7 and step != 'post-run':
        jobstate = db_insert(db_conn, models.JOBSTATES, status='post-run',
                             comment='finalizing %s...' % name,
                             job_id=id, team_id=company_id,
                             created_at=created_at)

        create_files(db_conn, jobstate, company_id)

    if step == 'post-run':
        return

    # choose between "success", "failure" jobstate
    created_at = compute_creation('success')
    jobstate = db_insert(db_conn, models.JOBSTATES, status=job['status'],
                         comment='%s %s' % (name, step),
                         job_id=id, team_id=company_id,
                         created_at=created_at)
    # no file creation on last state


def db_insert(db_conn, model_item, **kwargs):
    query = model_item.insert().values(**kwargs)
    return db_conn.execute(query).inserted_primary_key[0]


def lorem(size=len(LOREM_IPSUM), l=True):
    nb = random.randint(1, len(LOREM_IPSUM))

    line = ' '.join(LOREM_IPSUM[0:7]) if l else ''

    return line + '\n'.join(LOREM_IPSUM[0:nb])


def init_db(db_conn):
    db_ins = functools.partial(db_insert, db_conn)

    topic_id = db_ins(models.TOPICS, name="the_topic")

    components = []
    for component in COMPONENTS:
        component_type = random.choice(COMPONENT_TYPES)

        for i in range(0, 5):
            project = random.choice(PROJECT_NAMES)
            project_slug = '-'.join(project.lower().split())
            commit = (hashlib.sha1(str(random.random()).encode('utf8'))
                      .hexdigest())

            url = 'https://github.com/%s/commit/%s'
            attrs = {
                'name': component + '-%s' % i,
                'type': component_type,
                'canonical_project_name': '%s - %s' % (component, project),
                # This entry is basically a copy of the other fields,
                # this will may be removed in the future
                'data': DATA,
                'sha': commit,
                'title': project,
                'message': lorem(),
                'url': url % (project_slug, commit),
                'ref': '',
                'topic_id': topic_id
            }
            components.append(db_ins(models.COMPONENTS, **attrs))

    tests = {}
    for test in TESTS:
        tests[test] = db_ins(models.TESTS, name=test, data=DATA,
                             topic_id=topic_id)

    # Create the super admin user
    admin_team = db_ins(models.TEAMS, name='admin')

    db_ins(models.USERS, name='admin',
           role='admin',
           password=auth.hash_password('admin'),
           team_id=admin_team)

    # Attach the team admin to one topic
    db_ins(models.JOINS_TOPICS_TEAMS, topic_id=topic_id,
           team_id=admin_team)

    # For each constructor create an admin and a user, cis and jobs
    for company in COMPANIES:
        c = {}
        c['name'] = company
        c['id'] = db_ins(models.TEAMS, name=company)

        # create a topic for the team
        topic_id = db_ins(models.TOPICS, name=company)
        # Attach topic to team
        db_ins(models.JOINS_TOPICS_TEAMS, topic_id=topic_id, team_id=c['id'])

        user = {'name': '%s_user' % (company.lower(),),
                'password': auth.hash_password(company), 'team_id': c['id']}
        admin = {'name': '%s_admin' % (company.lower(),),
                 'password': auth.hash_password(company), 'team_id': c['id']}

        c['user'] = db_ins(models.USERS, **user)
        c['admin'] = db_ins(models.USERS, **admin)

        remote_cis = create_remote_cis(db_conn, c, tests, topic_id)
        jobs = create_jobs(db_conn, c['id'], remote_cis)
        # flatten job_definitions
        job_definitions = [jd for jds in remote_cis.values() for jd in jds]
        create_jobdefinition_components(db_conn, components, job_definitions)
        for job in zip(jobs, job_definitions):
            create_jobstates_and_files(db_conn, job, c['id'])
            attach_files_to_jobs(db_conn, job, c['id'])


if __name__ == '__main__':
    conf = config.generate_conf()
    db_uri = conf['SQLALCHEMY_DATABASE_URI']

    try:
        opts, args = getopt.getopt(sys.argv[1:], "y")
    except getopt.GetoptError:
        print('you can force the deletion by adding -y as a parameter')

    if sqlalchemy_utils.functions.database_exists(db_uri):
        flag = opts and '-y' in opts[0]
        while not flag:
            print('Be carefull this script will override your database:')
            print(db_uri)
            print('')
            i = raw_input('Continue ? [y/N] ').lower()
            if not i or i == 'n':
                sys.exit(0)
            if i == 'y':
                break

        sqlalchemy_utils.functions.drop_database(db_uri)

    sqlalchemy_utils.functions.create_database(db_uri)

    engine = sqlalchemy.create_engine(db_uri)
    models.metadata.create_all(engine)
    with engine.begin() as conn:
        init_db(conn)
