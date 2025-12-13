# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2021 CERN.
# Copyright (C) 2021 Northwestern University.
#
# Invenio-Drafts-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Record service component for drafts."""

from .base import ServiceComponent
from .files import DraftFilesComponent
from .media_files import DraftMediaFilesComponent
from .metadata import DraftMetadataComponent
from .pid import PIDComponent
from .relations import RelationsComponent

__all__ = (
    "ServiceComponent",
    "DraftFilesComponent",
    "DraftMetadataComponent",
    "PIDComponent",
    "RelationsComponent",
    "DraftMediaFilesComponent",
)
