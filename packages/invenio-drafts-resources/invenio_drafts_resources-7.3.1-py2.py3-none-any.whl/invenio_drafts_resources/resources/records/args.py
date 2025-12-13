# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CERN.
# Copyright (C) 2021 Northwestern University.
#
# Invenio-Drafts-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Schemas for parameter parsing."""


from invenio_records_resources.resources.records.args import (
    SearchRequestArgsSchema as SearchRequestArgsSchemaBase,
)
from marshmallow import fields


class SearchRequestArgsSchema(SearchRequestArgsSchemaBase):
    """Extend schema with all versions field."""

    allversions = fields.Boolean()
    include_deleted = fields.Boolean()
