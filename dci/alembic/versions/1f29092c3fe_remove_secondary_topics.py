#
# Copyright (C) 2020 Red Hat, Inc
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

"""remove secondary topics

Revision ID: 1f29092c3fe
Revises: 1726221a976
Create Date: 2020-06-07 22:44:36.686576

"""

# revision identifiers, used by Alembic.
revision = '1f29092c3fe'
down_revision = '1726221a976'
branch_labels = None
depends_on = None

from alembic import op


def upgrade():
    op.drop_column('jobs', 'topic_id_secondary')


def downgrade():
    pass
