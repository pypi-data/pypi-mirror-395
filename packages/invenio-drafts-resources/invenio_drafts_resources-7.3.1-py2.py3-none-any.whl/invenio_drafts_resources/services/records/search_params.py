# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CERN.
# Copyright (C) 2021 Northwestern University.
#
# Invenio-Records-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Sort parameter interpreter API."""

from functools import partial

from invenio_records_resources.services.records.params.base import ParamInterpreter


class AllVersionsParam(ParamInterpreter):
    """Evaluates the 'allversions' parameter."""

    def __init__(self, field_name, config):
        """Construct."""
        self.field_name = field_name
        super().__init__(config)

    @classmethod
    def factory(cls, field):
        """Create a new filter parameter."""
        return partial(cls, field)

    def apply(self, identity, search, params):
        """Evaluate the allversions parameter on the search."""
        if not params.get("allversions"):
            search = search.filter("term", **{self.field_name: True})
        return search
