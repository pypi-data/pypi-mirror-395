# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 CERN.
#
# Invenio-Banners is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio Resources module to create REST APIs."""

from .config import BannerResourceConfig
from .resource import BannerResource

__all__ = (
    "BannerResource",
    "BannerResourceConfig",
)
