#
# Copyright (C) 2018 Red Hat, Inc
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

"""add state to issues

Revision ID: 6a224b67052
Revises: 358cdb161d55
Create Date: 2018-11-13 20:53:55.247713

"""

# revision identifiers, used by Alembic.
revision = '6a224b67052'
down_revision = '358cdb161d55'
branch_labels = None
depends_on = None

from dci.common import utils
from alembic import op
import sqlalchemy as sa


RESOURCE_STATES = ['active', 'inactive', 'archived']
STATES = sa.Enum(*RESOURCE_STATES, name='states')


def upgrade():
    op.add_column('issues', sa.Column('state', STATES, default='active'))
    op.add_column('issues', sa.Column('etag', sa.String(40), nullable=False,
                                      default=utils.gen_etag,
                                      onupdate=utils.gen_etag))


def downgrade():
    pass
