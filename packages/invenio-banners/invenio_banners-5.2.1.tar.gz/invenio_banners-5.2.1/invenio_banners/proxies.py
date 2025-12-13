# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 CERN.
#
# Invenio-Banners is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Proxies for accessing the current Banners extension."""

from flask import current_app
from werkzeug.local import LocalProxy

current_banners = LocalProxy(lambda: current_app.extensions["invenio-banners"])
"""Proxy for the instantiated Banners extension."""

current_banners_service = LocalProxy(
    lambda: current_app.extensions["invenio-banners"].banners_service
)
"""Proxy for the currently instantiated banners service."""
