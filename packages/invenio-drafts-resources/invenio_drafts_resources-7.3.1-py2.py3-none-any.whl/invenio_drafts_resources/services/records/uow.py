# -*- coding: utf-8 -*-
#
# Copyright (C) 2023-2024 CERN.
#
# Invenio-Drafts-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Unit of work."""

from invenio_records_resources.services.uow import RecordCommitOp


class ParentRecordCommitOp(RecordCommitOp):
    """Parent record commit operation, bulk indexing records and drafts."""

    def __init__(
        self,
        parent,
        indexer_context=None,
        bulk_index=True,
    ):
        """Initialize the parent record commit operation.

        :params indexer_context: a dict containing record/draft cls and indexers,
            or service. Expected keys: `record_cls, draft_cls, indexer, draft_indexer`.
            `None` if indexing disabled.
        :params bulk_index: if ``True`` will send to bulk indexing queue. Otherwise will
            index synchronously.
        """
        super().__init__(parent, indexer=None)
        self._indexer_context = indexer_context
        if indexer_context:
            _service = indexer_context.get("service", None)
            if _service is not None:
                self._record_cls = getattr(_service, "record_cls")
                self._draft_cls = getattr(_service, "draft_cls")
                self._record_indexer = getattr(_service, "indexer")
                self._draft_indexer = getattr(_service, "draft_indexer")
            else:
                self._record_cls = indexer_context["record_cls"]
                self._draft_cls = indexer_context["draft_cls"]
                self._record_indexer = indexer_context["indexer"]
                self._draft_indexer = indexer_context["draft_indexer"]
        self._bulk_index = bulk_index

    def _get_siblings(self):
        """Get all record and draft versions by parent.

        This operation might be slow when a record has a high number of versions and drafts.
        However, given that often versions should be re-indexed as soon as possible when the parent
        is committed, the fetching operation is done synchronously.
        """
        records_ids = self._record_cls.get_records_by_parent(
            self._record, with_deleted=False, ids_only=True
        )
        drafts_ids = self._draft_cls.get_records_by_parent(
            self._record, with_deleted=False, ids_only=True
        )
        return records_ids, drafts_ids

    def on_commit(self, uow):
        """No commit operation."""
        pass

    def on_post_commit(self, uow):
        """Bulk index as last operation."""
        if self._indexer_context is not None:
            records_ids, drafts_ids = self._get_siblings()
            if records_ids:
                if self._bulk_index:
                    self._record_indexer.bulk_index(records_ids)
                else:
                    for record_id in records_ids:
                        self._record_indexer.index_by_id(record_id)
            if drafts_ids:
                if self._bulk_index:
                    self._draft_indexer.bulk_index(drafts_ids)
                else:
                    for draft_id in drafts_ids:
                        self._draft_indexer.index_by_id(draft_id)
