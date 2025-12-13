# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2021 CERN.
# Copyright (C) 2021 Northwestern University.
# Copyright (C) 2023 Graz University of Technology.
#
# Invenio-Drafts-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Records service component base classes."""

from invenio_records_resources.services.records.components import MetadataComponent


class DraftMetadataComponent(MetadataComponent):
    """Service component for draft metadata integration."""

    def update_draft(self, identity, data=None, record=None, **kwargs):
        """Update draft metadata."""
        record.metadata = data.get("metadata", {})

    def publish(self, identity, draft=None, record=None, **kwargs):
        """Update draft metadata."""
        record.metadata = draft.get("metadata", {})

    def edit(self, identity, draft=None, record=None, **kwargs):
        """Update draft metadata."""
        draft.metadata = record.get("metadata", {})

    def new_version(self, identity, draft=None, record=None, **kwargs):
        """Update draft metadata."""
        draft.metadata = record.get("metadata", {})
