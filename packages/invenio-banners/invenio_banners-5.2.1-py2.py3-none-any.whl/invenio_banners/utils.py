# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2023 CERN.
# Copyright (C) 2025 Graz University of Technology.
#
# Invenio-Banners is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Utils."""

from flask import request

from .records.models import BannerModel


def get_active_banners_for_request():
    """Get active banner for the current URL path request."""
    url_path = request.path
    return BannerModel.get_active(url_path)


def style_category(category):
    """Return predefined Semantic-UI classes for each banner category."""
    style_class = "{}"
    if category == "warning":
        style_class = style_class.format("warning")
    elif category == "other":
        style_class = style_class.format("grey")
    else:
        style_class = style_class.format("info")
    return style_class


def strtobool(value):
    """String to bool.

    since python3.12 removed distutils.util and the function is simple it has
    been reimplemented

    Convert a string representation of truth to true (1) or false (0).

    True values are y, yes, t, true, on and 1; false values are n, no, f, false,
    off and 0. Raises ValueError if val is anything else.
    """
    v = str(value)
    if v.lower() in ["y", "yes", "t", "true", "on", "1"]:
        return True
    elif v.lower() in ["n", "no", "f", "false", "off", "0"]:
        return False
    else:
        msg = f"value: {value} is not of y, yes, t, true, on, 1 or n, no, f, false, off, 0"
        raise ValueError(msg)
