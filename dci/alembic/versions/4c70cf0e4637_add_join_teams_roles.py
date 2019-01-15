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

"""add join_teams_roles

Revision ID: 4c70cf0e4637
Revises: 732a3e25e65e
Create Date: 2018-12-07 15:27:31.181051

"""

# revision identifiers, used by Alembic.
revision = '4c70cf0e4637'
down_revision = '732a3e25e65e'
branch_labels = None
depends_on = None

from alembic import op
from dci.db import models
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql as pg


def upgrade():
    op.create_table(
        'users_teams_roles',
        sa.Column('user_id', pg.UUID(as_uuid=True),
                  sa.ForeignKey('users.id', ondelete='CASCADE'),
                  nullable=False),
        sa.Column('team_id', pg.UUID(as_uuid=True),
                  sa.ForeignKey('teams.id', ondelete='CASCADE'),
                  nullable=True),
        sa.Column('role', models.ROLES_ENUM, default='USER', nullable=False),
        sa.UniqueConstraint('user_id', 'team_id', name='users_teams_roles_key')
    )


def downgrade():
    pass
