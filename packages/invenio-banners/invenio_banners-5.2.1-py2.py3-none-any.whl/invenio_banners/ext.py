# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2023 CERN.
#
# Invenio-Banners is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio extension app."""

from flask import Blueprint

from . import config
from .resources import BannerResource, BannerResourceConfig
from .services import BannerService, BannerServiceConfig
from .utils import get_active_banners_for_request

blueprint = Blueprint(
    "invenio_banners",
    __name__,
    template_folder="templates",
    static_folder="static",
)


class InvenioBanners(object):
    """Invenio-Banners extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)
        self.init_services(app)
        self.init_resources(app)
        app.extensions["invenio-banners"] = self
        app.register_blueprint(blueprint)
        app.jinja_env.globals["get_active_banners"] = get_active_banners_for_request
        app.jinja_env.filters["style_banner_category"] = app.config[
            "BANNERS_CATEGORIES_TO_STYLE"
        ]

    def init_config(self, app):
        """Initialize configuration."""
        for k in dir(config):
            if k.startswith("BANNERS_"):
                app.config.setdefault(k, getattr(config, k))

    def init_services(self, app):
        """Initialize the services for banners."""
        self.banners_service = BannerService(config=BannerServiceConfig)

    def init_resources(self, app):
        """Initialize the resources for banners."""
        self.banners_resource = BannerResource(
            service=self.banners_service,
            config=BannerResourceConfig,
        )
