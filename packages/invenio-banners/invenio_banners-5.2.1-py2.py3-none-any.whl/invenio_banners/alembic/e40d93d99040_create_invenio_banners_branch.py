#
# This file is part of Invenio.
# Copyright (C) 2016-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Create invenio-banners branch."""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "e40d93d99040"
down_revision = None
branch_labels = ("invenio_banners",)
depends_on = "dbdbc1b19cf2"


def upgrade():
    """Upgrade database."""
    pass


def downgrade():
    """Downgrade database."""
    pass
