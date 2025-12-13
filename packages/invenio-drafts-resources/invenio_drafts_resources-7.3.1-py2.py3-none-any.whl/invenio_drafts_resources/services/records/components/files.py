# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 CERN.
#
# Invenio-Drafts-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Records service component base classes."""
from invenio_records_resources.services.base.config import _make_cls
from invenio_records_resources.services.records.components.files import FilesAttrConfig

from .base import BaseRecordFilesComponent

# Configure file attributes for files component
DraftFilesComponent = _make_cls(BaseRecordFilesComponent, {**FilesAttrConfig})
