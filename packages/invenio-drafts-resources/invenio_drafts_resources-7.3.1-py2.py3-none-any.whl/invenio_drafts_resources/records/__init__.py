# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2021 CERN.
# Copyright (C) 2021 Northwestern University.
#
# Invenio-Drafts-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Data layer API.

The 'records' folder name stands for the generic records-resource's data layer.
It applies to both api.py's Draft and Record.
"""

from .api import Draft, ParentRecord, Record
from .models import DraftMetadataBase, ParentRecordMixin, ParentRecordStateMixin

__all__ = (
    "Draft",
    "DraftMetadataBase",
    "ParentRecord",
    "ParentRecordMixin",
    "ParentRecordStateMixin",
    "Record",
)
