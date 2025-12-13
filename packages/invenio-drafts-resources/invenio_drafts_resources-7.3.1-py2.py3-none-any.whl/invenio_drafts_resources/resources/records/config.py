# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Invenio-Drafts-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Draft aware Record Resource Config override."""

from invenio_records_resources.resources import (
    RecordResourceConfig as RecordResourceConfigBase,
)

from .args import SearchRequestArgsSchema


class RecordResourceConfig(RecordResourceConfigBase):
    """Draft aware Record resource config."""

    url_prefix = ""

    routes = {
        "user-prefix": "/user",
        "list": "",
        "item": "/<pid_value>",
        "item-versions": "/<pid_value>/versions",
        "item-latest": "/<pid_value>/versions/latest",
        "item-draft": "/<pid_value>/draft",
        "item-publish": "/<pid_value>/draft/actions/publish",
        "item-files-import": "/<pid_value>/draft/actions/files-import",
    }

    request_search_args = SearchRequestArgsSchema
