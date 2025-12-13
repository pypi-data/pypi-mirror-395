# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Drafts-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Record schema."""

from invenio_records_resources.services.records.schema import BaseRecordSchema
from marshmallow import Schema, fields
from marshmallow_utils.fields import NestedAttribute


class VersionsSchema(Schema):
    """Versions schema."""

    is_latest = fields.Boolean()
    is_latest_draft = fields.Boolean()
    index = fields.Integer()


class ParentSchema(Schema):
    """Parent record schema."""

    id = fields.Str()


class RecordSchema(BaseRecordSchema):
    """Schema for records in JSON."""

    parent = NestedAttribute(ParentSchema, dump_only=True)
    versions = NestedAttribute(VersionsSchema, dump_only=True)
    is_published = fields.Boolean(dump_only=True)
    is_draft = fields.Boolean(dump_only=True)
    expires_at = fields.Str(dump_only=True)
