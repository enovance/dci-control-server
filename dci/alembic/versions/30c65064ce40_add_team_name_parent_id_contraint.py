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

"""add_team_name_parent_id_contraint

Revision ID: 30c65064ce40
Revises: 6f875bc66ca9
Create Date: 2017-10-16 11:50:46.842751

"""

# revision identifiers, used by Alembic.
revision = '30c65064ce40'
down_revision = '6f875bc66ca9'
branch_labels = None
depends_on = None

from alembic import op


def upgrade():
    op.drop_constraint('teams_name_key', 'teams')
    op.create_unique_constraint('teams_name_parent_id_key', 'teams',
                                ['name', 'parent_id'])


def downgrade():
    pass
