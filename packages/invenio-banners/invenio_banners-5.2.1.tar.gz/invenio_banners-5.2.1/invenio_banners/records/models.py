# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2023 CERN.
# Copyright (C) 2024-2025 Graz University of Technology.
#
# Invenio-Banners is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Models."""

from datetime import datetime, timezone

import sqlalchemy as sa
from flask import current_app
from invenio_db import db
from sqlalchemy import or_
from sqlalchemy.sql import text
from sqlalchemy_utils.models import Timestamp

from ..resources.errors import BannerNotExistsError


class BannerModel(db.Model, Timestamp):
    """Defines a message to show to users."""

    __tablename__ = "banners"

    id = db.Column(db.Integer, primary_key=True)

    message = db.Column(db.Text, nullable=False)
    """The message content."""

    url_path = db.Column(db.String(255), nullable=True)
    """Define in which URL /path the message will be visible."""

    category = db.Column(db.String(20), nullable=False)
    """Category of the message, for styling messages per category."""

    start_datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    """Start date and time (UTC), can be immediate or delayed."""

    end_datetime = db.Column(db.DateTime, nullable=True)
    """End date and time (UTC), must be after `start` or forever if null."""

    active = db.Column(db.Boolean(name="active"), nullable=False, default=True)
    """Defines if the message is active, only one at the same time."""

    @classmethod
    def create(cls, data):
        """Create a new banner."""
        _categories = [t[0] for t in current_app.config["BANNERS_CATEGORIES"]]
        assert data.get("category") in _categories

        with db.session.begin_nested():
            obj = cls(
                message=data.get("message"),
                category=data.get("category"),
                url_path=data.get("url_path"),
                start_datetime=data.get("start_datetime"),
                end_datetime=data.get("end_datetime"),
                active=data.get("active"),
            )
            db.session.add(obj)

        return obj

    @classmethod
    def update(cls, data, id):
        """Update an existing banner."""
        with db.session.begin_nested():
            # NOTE:
            # with db.session.get(cls, id) the model itself would be
            # returned and this classmethod would be called
            db.session.query(cls).filter_by(id=id).update(data)

    @classmethod
    def get(cls, id):
        """Get banner by its id."""
        if banner := db.session.get(cls, id):
            return banner

        raise BannerNotExistsError(id)

    @classmethod
    def delete(cls, banner):
        """Delete banner by its id."""
        with db.session.begin_nested():
            db.session.delete(banner)

    @classmethod
    def get_active(cls, url_path):
        """Return active banners."""
        now = datetime.now(timezone.utc).replace(tzinfo=None)

        query = (
            db.session.query(cls)
            .filter(cls.active.is_(True))
            .filter(cls.start_datetime <= now)
            .filter((cls.end_datetime.is_(None)) | (now <= cls.end_datetime))
        )

        # filter by url_path
        active_banners = query.filter(
            sa.or_(
                cls.url_path.is_(None),
                sa.literal(url_path).startswith(cls.url_path),
            )
        )

        return active_banners.all()

    @classmethod
    def search(cls, search_params, filters=None):
        """Filter banners accordingly to query params."""
        if filters:
            filtered = db.session.query(BannerModel).filter(or_(*filters))
        else:
            filtered = db.session.query(BannerModel).filter()

        banners = filtered.order_by(
            search_params["sort_direction"](text(",".join(search_params["sort"])))
        ).paginate(
            page=search_params["page"],
            per_page=search_params["size"],
            error_out=False,
        )

        return banners

    @classmethod
    def disable_expired(cls):
        """Disable any old still active messages to keep everything clean."""
        now = datetime.now(timezone.utc).replace(tzinfo=None)

        query = (
            db.session.query(cls)
            .filter(cls.active.is_(True))
            .filter(cls.end_datetime.isnot(None))
            .filter(cls.end_datetime < now)
        )

        for old in query.all():
            old.active = False
