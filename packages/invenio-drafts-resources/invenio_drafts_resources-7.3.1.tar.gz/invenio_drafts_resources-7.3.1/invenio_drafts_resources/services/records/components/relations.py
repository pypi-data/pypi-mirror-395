# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2025 CERN.
#
# Invenio-RDM-Records is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Records service relations component."""

from invenio_records_resources.services.records.components import (
    RelationsComponent as RelationsComponentBase,
)


class RelationsComponent(RelationsComponentBase):
    """Relations service component."""

    def read_draft(self, identity, draft=None, errors=None):
        """Read draft handler."""
        draft.relations.dereference()
