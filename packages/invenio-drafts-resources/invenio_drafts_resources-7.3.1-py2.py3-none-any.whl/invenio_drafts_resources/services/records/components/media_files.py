# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2024 CERN.
# Copyright (C) 2021 Northwestern University.
# Copyright (C) 2023 Graz University of Technology.
#
# Invenio-Drafts-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Records service component base classes."""
from invenio_i18n import gettext as _
from invenio_records_resources.services.base.config import _make_cls
from marshmallow import ValidationError

from .base import BaseRecordFilesComponent


class _DraftMediaFilesComponent(BaseRecordFilesComponent):
    """Draft media files component."""

    def create(self, identity, data=None, record=None, errors=None):
        """Assigns files.enabled.

        NOTE: `record` actually refers to the draft
              (this interface is used in records-resources and rdm-records)
        """
        draft = record
        files = self.get_record_files(draft)

        # disable the media files by default
        enabled = data.get(self.files_data_key, {}).get(
            "enabled", self.service.config.default_media_files_enabled
        )

        files.enabled = enabled

    def update_draft(self, identity, data=None, record=None, errors=None):
        """Assigns files.enabled and warns if files are missing.

        NOTE: `record` actually refers to the draft
              (this interface is used in records-resources and rdm-records)
        """
        draft = record
        draft_files = self.get_record_files(draft)
        record_files = self.get_record_files(record)
        enabled = data.get(self.files_data_key, {}).get("enabled", record_files.enabled)
        default_preview = data.get(self.files_data_key, {}).get("default_preview")

        try:
            self.assign_files_enabled(draft, enabled)
        except ValidationError as e:
            errors.append(
                {"field": f"{self.files_data_key}.enabled", "messages": e.messages}
            )
            return  # exit early

        if draft_files.enabled and not draft_files.items():
            errors.append(
                {
                    "field": f"{self.files_data_key}.enabled",
                    "messages": [
                        _(
                            "Missing uploaded files. To disable files for "
                            "this record please mark it as metadata-only."
                        )
                    ],
                }
            )

        try:
            self.assign_files_default_preview(
                draft,
                default_preview,
            )
        except ValidationError as e:
            errors.append(
                {
                    "field": f"{self.files_data_key}.default_preview",
                    "messages": e.messages,
                }
            )

    def _publish_new(self, identity, draft, record):
        """Action when publishing a new draft."""
        # For unpublished drafts (new and new version), we move the draft
        # bucket from the draft to the record (instead of creating a new, and
        # deleting one). For consistency, we keep a bucket for all records
        # independently of if they have files enabled or not.
        draft_files = self.get_record_files(draft)
        draft_bucket = self.get_record_bucket(draft)

        if draft_bucket is None:
            # legacy compatibility safety check - create bucket if missing
            draft_files.create_bucket()
            draft_bucket = self.get_record_bucket(draft)

        super()._publish_new(identity, draft, record)

    def edit(self, identity, draft=None, record=None):
        """Edit callback."""
        draft_files = self.get_record_files(draft)
        record_files = self.get_record_files(record)
        draft_bucket = self.get_record_bucket(draft)
        if draft_bucket is None:
            # Happens, when a soft-deleted draft is un-deleted.
            draft[self.files_data_key] = {"enabled": record_files.enabled}
            # re-fetch the files attribute - above data getter sets the attribute
            draft_files = self.get_record_files(draft)
            draft_files.create_bucket()
        # we copy always file objects and tear them down when publish
        draft_files.copy(record_files)
        # in the media files we don't lock the bucket
        # - they can be simply edited from draft

    def _publish_edit(self, identity, draft, record):
        """Action when publishing an edit to an existing record."""
        record_files = self.get_record_files(record)
        draft_files = self.get_record_files(draft)

        record_files.unlock()
        # As the files can be enabled after the first publish, and thus the record will
        # have an outdated value, we make sure that record files are enabled
        # according to draft
        record_files.enabled = draft_files.enabled
        record_files.sync(draft_files, delete_extras=True)
        record_files.lock()
        # Teardown the bucket and files created in edit().
        self._purge_bucket_and_ovs(draft_files)

    def new_version(self, identity, draft=None, record=None):
        """New version callback."""
        # We don't copy files from the previous version, but instead allow
        # users to import the files.
        draft_files = self.get_record_files(draft)
        # Set media files to the default config
        draft_files.enabled = self.service.config.default_media_files_enabled

    def import_files(self, identity, draft=None, record=None):
        """Import files callback."""
        # We don't need the import for media files
        return


MediaFilesAttrConfig = {
    "_files_attr_key": "media_files",
    "_files_data_key": "media_files",
    "_files_bucket_attr_key": "media_bucket",
    "_files_bucket_id_attr_key": "media_bucket_id",
}

### Configure file attributes for media files component
DraftMediaFilesComponent = _make_cls(
    _DraftMediaFilesComponent, {**MediaFilesAttrConfig}
)
