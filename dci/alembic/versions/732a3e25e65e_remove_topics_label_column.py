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

"""remove topics.label column

Revision ID: 732a3e25e65e
Revises: 379d2d558f54
Create Date: 2018-12-13 10:55:36.509774

"""

# revision identifiers, used by Alembic.
revision = "732a3e25e65e"
down_revision = "379d2d558f54"
branch_labels = None
depends_on = None

from alembic import op


def upgrade():
    op.drop_column("topics", "label")


def downgrade():
    pass
