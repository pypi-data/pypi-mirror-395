# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2023 CERN.
#
# Invenio-Banners is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio module providing management APIs for banners."""


def create_banners_api_bp(app):
    """Create the banners resource api blueprint."""
    ext = app.extensions["invenio-banners"]
    return ext.banners_resource.as_blueprint()
