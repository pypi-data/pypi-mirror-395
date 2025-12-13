# -*- coding: utf-8 -*-
#
# Copyright (C) 2022-2023 CERN.
# Copyright (C) 2024 Graz University of Technology.
#
# Invenio-Banners is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Service results."""

from invenio_records_resources.services.records.results import RecordItem, RecordList

try:
    # flask_sqlalchemy<3.0.0
    from flask_sqlalchemy import Pagination
except ImportError:
    # flask_sqlalchemy>=3.0.0
    from flask_sqlalchemy.pagination import Pagination


class BannerItem(RecordItem):
    """Single banner result."""

    def __init__(
        self,
        service,
        identity,
        banner,
        links_tpl=None,
        errors=None,
        schema=None,
    ):
        """Constructor."""
        super().__init__(service, identity, banner, errors, links_tpl, schema)

    @property
    def data(self):
        """Property to get the banner."""
        if self._data:
            return self._data

        self._data = self._schema.dump(
            self._obj,
            context={
                "identity": self._identity,
                "record": self._record,
            },
        )

        if self._links_tpl:
            self._data["links"] = self.links

        return self._data


class BannerList(RecordList):
    """List of banner results."""

    def __init__(
        self,
        service,
        identity,
        banners,
        params=None,
        links_tpl=None,
        links_item_tpl=None,
        schema=None,
    ):
        """Constructor."""
        super().__init__(
            service, identity, banners, params, links_tpl, links_item_tpl, schema
        )

    @property
    def hits(self):
        """Iterator over the hits."""
        for record in self.banners_result():
            # Project the record
            projection = self._schema.dump(
                record,
                context=dict(
                    identity=self._identity,
                    record=record,
                ),
            )

            if self._links_item_tpl:
                projection["links"] = self._links_item_tpl.expand(
                    self._identity, record
                )

            yield projection

    def to_dict(self):
        """Return result as a dictionary."""
        res = {
            "hits": {
                "hits": list(self.hits),
                "total": self.total,
            }
        }

        if self._params:
            if self._links_tpl:
                res["links"] = self._links_tpl.expand(self._identity, self.pagination)

        return res

    @property
    def total(self):
        """Get total number of banners."""
        return (
            self._results.total
            if isinstance(self._results, Pagination)
            else len(self._results)
        )

    def banners_result(self):
        """Get iterable banners list."""
        return (
            self._results.items
            if isinstance(self._results, Pagination)
            else self._results
        )
