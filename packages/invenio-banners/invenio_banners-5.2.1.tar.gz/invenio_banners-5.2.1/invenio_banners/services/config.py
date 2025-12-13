# -*- coding: utf-8 -*-
#
# Copyright (C) 2022-2023 CERN.
#
# Invenio-Banners is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Banners Service configuration."""

from invenio_i18n import gettext as _
from invenio_records_resources.services import Link, RecordServiceConfig
from invenio_records_resources.services.records.links import pagination_links
from sqlalchemy import asc, desc

from ..records.models import BannerModel
from .permissions import BannersPermissionPolicy
from .results import BannerItem, BannerList
from .schemas import BannerSchema


class BannersLink(Link):
    """Link variables setter for Banner links."""

    @staticmethod
    def vars(banner, vars):
        """Variables for the URI template."""
        vars.update({"id": banner.id})


class SearchOptions:
    """Search options."""

    sort_direction_default = "asc"
    sort_direction_options = {
        "asc": dict(
            title=_("Ascending"),
            fn=asc,
        ),
        "desc": dict(
            title=_("Descending"),
            fn=desc,
        ),
    }

    sort_default = "start_datetime"
    sort_options = {
        "url_path": dict(
            title=_("Url path"),
            fields=["url_path"],
        ),
        "start_datetime": dict(
            title=_("Start time"),
            fields=["start_datetime"],
        ),
        "end_datetime": dict(
            title=_("End time"),
            fields=["end_datetime"],
        ),
        "active": dict(
            title=_("Active"),
            fields=["active"],
        ),
    }
    pagination_options = {
        "default_results_per_page": 25,
    }


class BannerServiceConfig(RecordServiceConfig):
    """Service factory configuration."""

    result_item_cls = BannerItem
    result_list_cls = BannerList
    permission_policy_cls = BannersPermissionPolicy
    schema = BannerSchema

    # Search configuration
    search = SearchOptions

    # links configuration
    links_item = {
        "self": BannersLink("{+api}/banners/{id}"),
    }
    links_search = pagination_links("{+api}/banners{?args*}")
    record_cls = BannerModel
