# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2023 CERN.
# Copyright (C) 2024 KTH Royal Institute of Technology.
#
# Invenio-Banners is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Configuration variables."""

from invenio_i18n import lazy_gettext as _

from invenio_banners.utils import style_category

BANNERS_CATEGORIES = [
    ("info", _("Info")),
    ("warning", _("Warning")),
    ("other", _("Other")),
]
"""Categories to define different types of messages. List of (id, label)."""

BANNERS_CATEGORIES_TO_STYLE = style_category
"""Function to transform the banner category to a specific Semantic-UI class."""

BANNERS_SEARCH = {
    "facets": [],
    "sort": [
        "url_path",
        "start_datetime",
        "end_datetime",
        "active",
    ],
}
"""Banner search configuration (i.e list of banners)"""

BANNERS_SORT_OPTIONS = {
    "url_path": dict(
        title=_("URL path"),
        fields=["url_path"],
    ),
    "start_datetime": dict(
        title=_("Start DateTime"),
        fields=["start_datetime"],
    ),
    "end_datetime": dict(
        title=_("End DateTime"),
        fields=["end_datetime"],
    ),
    "active": dict(
        title=_("Active"),
        fields=["active"],
    ),
}
"""Definitions of available Banners sort options. """
