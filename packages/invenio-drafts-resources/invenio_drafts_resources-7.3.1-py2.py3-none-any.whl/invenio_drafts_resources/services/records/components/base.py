# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2025 CERN.
#
# Invenio-Drafts-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.
#

"""Base class for service components."""
from invenio_i18n import gettext as _
from invenio_records_resources.proxies import current_transfer_registry
from invenio_records_resources.services.files.transfer.base import TransferStatus
from invenio_records_resources.services.records.components import (
    BaseRecordFilesComponent as _BaseRecordFilesComponent,
)
from invenio_records_resources.services.records.components import (
    ServiceComponent as BaseServiceComponent,
)
from marshmallow import ValidationError


class ServiceComponent(BaseServiceComponent):
    """Base service component."""

    def read_draft(self, identity, draft=None, errors=None):
        """Update draft handler."""
        pass

    def update_draft(self, identity, data=None, record=None, errors=None):
        """Update draft handler."""
        pass

    def delete_draft(self, identity, draft=None, record=None, force=False):
        """Delete draft handler."""
        pass

    def edit(self, identity, draft=None, record=None):
        """Edit a record handler."""
        pass

    def new_version(self, identity, draft=None, record=None):
        """New version handler."""
        pass

    def publish(self, identity, draft=None, record=None):
        """Publish handler."""
        pass

    def import_files(self, identity, draft=None, record=None):
        """Import files handler."""
        pass

    def post_publish(self, identity, record=None, is_published=False):
        """Post publish handler."""
        pass


class BaseRecordFilesComponent(ServiceComponent, _BaseRecordFilesComponent):
    """Base record/draft files component.

    Attention: needs file attribute configuration!
    """

    #
    # API
    #
    def create(self, identity, data=None, record=None, errors=None):
        """Assigns files.enabled.

        NOTE: `record` actually refers to the draft
              (this interface is used in records-resources and rdm-records)
        """
        draft = record
        files = self.get_record_files(draft)
        enabled = data.get(self.files_data_key, {}).get(
            "enabled", self.service.config.default_files_enabled
        )

        if files.enabled != enabled:
            if not self.service.check_permission(
                identity, "manage_files", record=draft
            ):
                errors.append(
                    {
                        "field": f"{self.files_data_key}.enabled",
                        "messages": [
                            _("You don't have permissions to manage files options.")
                        ],
                    }
                )
                return  # exit early

        files.enabled = enabled

    def update_draft(self, identity, data=None, record=None, errors=None):
        """Assigns files.enabled and warns if files are missing.

        NOTE: `record` actually refers to the draft
              (this interface is used in records-resources and rdm-records)
        """
        draft = record
        draft_files = self.get_record_files(draft)
        default_preview = data.get(self.files_data_key, {}).get("default_preview")
        can_toggle_files = self.service.check_permission(
            identity, "manage_files", record=draft
        )

        enabled = data.get(self.files_data_key, {}).get(
            "enabled", self.service.config.default_files_enabled
        )

        if draft_files.enabled != enabled:
            if not can_toggle_files:
                errors.append(
                    {
                        "field": f"{self.files_data_key}.enabled",
                        "messages": [
                            _("You don't have permissions to manage files options.")
                        ],
                    }
                )
                return  # exit early

        try:
            self.assign_files_enabled(draft, enabled)
        except ValidationError as e:
            errors.append(
                {"field": f"{self.files_data_key}.enabled", "messages": e.messages}
            )
            return  # exit early

        if draft_files.enabled and not draft_files.items():
            if can_toggle_files:
                my_message = _(
                    "Missing uploaded files. To disable files for this record please mark it as metadata-only."
                )
            else:
                my_message = _("Missing uploaded files.")
            errors.append(
                {
                    "field": f"{self.files_data_key}.enabled",
                    "messages": [my_message],
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

    def edit(self, identity, draft=None, record=None):
        """Edit callback."""
        draft_files = self.get_record_files(draft)
        record_files = self.get_record_files(record)
        draft_bucket = self.get_record_bucket(draft)
        lock_files = self.service.config.lock_edit_published_files(
            self.service, identity, record=record, draft=draft
        )

        if draft_bucket is None:
            # Happens, when a soft-deleted draft is un-deleted.
            draft[self.files_data_key] = {"enabled": True}
            # re-fetch the files attribute - above data getter sets the attribute
            draft_files = self.get_record_files(draft)
            draft_files.create_bucket()

        # we copy always file objects and tear them down when publish
        draft_files.copy(record_files)
        if lock_files:
            # force going through the new version
            draft_files.lock()

    def new_version(self, identity, draft=None, record=None):
        """New version callback."""
        # We don't copy files from the previous version, but instead allow
        # users to import the files.
        draft_files = self.get_record_files(draft)
        record_files = self.get_record_files(record)
        draft_files.enabled = record_files.enabled

    def _purge_bucket_and_ovs(self, files):
        """Purge associated bucket and object versions."""
        if files.bucket:
            if files.bucket.locked:
                files.unlock()
            files.teardown(full=True)

    def _publish_new(self, identity, draft, record):
        """Action when publishing a new draft."""
        # For unpublished drafts (new and new version), we move the draft
        # bucket from the draft to the record (instead of creating a new, and
        # deleting one). For consistency, we keep a bucket for all records
        # independently of if they have files enabled or not.
        record_files = self.get_record_files(record)
        draft_files = self.get_record_files(draft)
        draft_bucket = self.get_record_bucket(draft)

        record_files.set_bucket(draft_bucket)
        record_files.copy(draft_files, copy_obj=False)
        # Lock the bucket
        record_files.lock()

        # Cleanup
        if draft_files.enabled:
            # Hard delete all draft file records but keep the object versions
            draft_files.teardown(full=False)
        draft_files.unset_bucket()

    def _publish_edit(self, identity, draft, record):
        """Action when publishing an edit to an existing record."""
        record_files = self.get_record_files(record)
        draft_files = self.get_record_files(draft)

        # sync draft files with record
        record_files.unlock()
        # As the files can be enabled after the first publish, and thus the record will
        # have an outdated value, we make sure that record files are enabled
        # according to draft
        record_files.enabled = draft_files.enabled
        record_files.sync(draft_files, delete_extras=True)
        record_files.lock()

        # Teardown the bucket and files created in edit().
        self._purge_bucket_and_ovs(draft_files)

    def _check_file_completed(self, file_record):
        """Check if file upload has completed."""
        transfer = current_transfer_registry.get_transfer(
            record=file_record.record,
            file_record=file_record,
            file_service=self.service.draft_files,
        )
        if transfer.status == TransferStatus.COMPLETED:
            return True

    def publish(self, identity, draft=None, record=None):
        """Copy bucket and files to record."""
        draft_files = self.get_record_files(draft)
        record_bucket_id = self.get_record_bucket_id(record)

        if draft_files.enabled and draft_files.bucket:
            if not draft_files.items():
                raise ValidationError(
                    _(
                        "Missing uploaded files. To disable files for "
                        "this record please mark it as metadata-only."
                    ),
                    field_name=f"{self.files_data_key}.enabled",
                )
        if draft_files.enabled:
            for file_record in draft_files.values():
                if not self._check_file_completed(file_record):
                    raise ValidationError(
                        _(
                            "One or more files have not completed their transfer, please wait."
                        ),
                        field_name=self.files_data_key,
                    )
        if record_bucket_id:
            self._publish_edit(identity, draft, record)
        else:
            self._publish_new(identity, draft, record)

    def delete_draft(self, identity, draft=None, record=None, force=False):
        """Delete files associated with a draft.

        :param force: If force is True, it means that the draft is being force
            deleted instead of soft deleted (i.e. an unpublished draft).
        """
        draft_files = self.get_record_files(draft)

        # Teardown the bucket and files if any.
        self._purge_bucket_and_ovs(draft_files)

    def import_files(self, identity, draft=None, record=None):
        """Import files handler."""
        record_files = self.get_record_files(record)
        draft_files = self.get_record_files(draft)
        if not draft_files.enabled:
            raise ValidationError(
                _("Files support must be enabled."),
                field_name=f"{self.files_data_key}.enabled",
            )

        if draft_files.items():
            raise ValidationError(
                _("Please remove all files first."),
                field_name=f"{self.files_data_key}.enabled",
            )

        if not record_files.enabled and not record_files.bucket:
            raise ValidationError(
                _("The record has no files."),
                field_name=f"{self.files_data_key}.enabled",
            )

        # Copy over the files
        draft_files.copy(record_files)
