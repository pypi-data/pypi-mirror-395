# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2025 CERN.
# Copyright (C) 2020 Northwestern University.
# Copyright (C) 2024 KTH Royal Institute of Technology.
#
# Invenio-Drafts-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Primary service for working with records and drafts."""

from flask import current_app
from invenio_audit_logs.services import AuditLogOp
from invenio_db import db
from invenio_i18n import gettext as _
from invenio_pidstore.errors import PIDDoesNotExistError
from invenio_records_resources.services import LinksTemplate
from invenio_records_resources.services import RecordService as RecordServiceBase
from invenio_records_resources.services import ServiceSchemaWrapper
from invenio_records_resources.services.uow import (
    RecordBulkIndexOp,
    RecordCommitOp,
    RecordDeleteOp,
    RecordIndexOp,
    unit_of_work,
)
from invenio_search.engine import dsl
from kombu import Queue
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.local import LocalProxy

from invenio_drafts_resources.auditlog.actions import (
    DraftCreateAuditLog,
    DraftDeleteAuditLog,
    DraftEditAuditLog,
    DraftNewVersionAuditLog,
    RecordPublishAuditLog,
)

from ...resources.records.errors import DraftNotCreatedError
from .uow import ParentRecordCommitOp


class RecordService(RecordServiceBase):
    """Record and draft service interface.

    This service provides an interface to business logic for published and
    draft records.
    """

    def __init__(self, config, files_service=None, draft_files_service=None):
        """Constructor for RecordService."""
        super().__init__(config)
        self._files = files_service
        self._draft_files = draft_files_service

    #
    # Subservices
    #
    @property
    def files(self):
        """Record files service."""
        return self._files

    @property
    def draft_files(self):
        """Draft files service."""
        return self._draft_files

    #
    # Properties
    #
    @property
    def schema_parent(self):
        """Schema for parent records."""
        return ServiceSchemaWrapper(self, schema=self.config.schema_parent)

    @property
    def draft_cls(self):
        """Factory for creating a record class."""
        return self.config.draft_cls

    @property
    def draft_indexer(self):
        """Factory for creating an indexer instance."""
        return self.config.draft_indexer_cls(
            # the routing key is mandatory in the indexer constructor since
            # it is afterwards passed explicitly to the created consumers
            # and producers. this means that it is not strictly necessary to
            # pass it to the queue constructor. however, it is passed for
            # consistency (in case the queue is used by itself) and to help
            # entity declaration on publish.
            queue=LocalProxy(
                lambda: Queue(
                    self.config.draft_indexer_queue_name,
                    exchange=current_app.config["INDEXER_MQ_EXCHANGE"],
                    routing_key=self.config.draft_indexer_queue_name,
                )
            ),
            routing_key=self.config.draft_indexer_queue_name,
            record_cls=self.config.draft_cls,
            record_to_index=self.record_to_index,
            record_dumper=self.config.index_dumper,
        )

    # High-level API
    # Inherits record search, read, create, delete and update

    def update(self, *args, **kwargs):
        """Do not use."""
        raise NotImplementedError(_("Records should be updated via their draft."))

    def search_drafts(
        self,
        identity,
        params=None,
        search_preference=None,
        expand=False,
        extra_filter=None,
        **kwargs,
    ):
        """Search for drafts records matching the querystring."""
        self.require_permission(identity, "search_drafts")
        # Prepare and execute the search
        params = params or {}

        # `has_draft` systemfield is not defined here. This is not ideal
        # but it helps avoid overriding the method. See how is used in
        # https://github.com/inveniosoftware/invenio-rdm-records
        search_draft_filter = dsl.Q("term", has_draft=False)

        if extra_filter:
            search_draft_filter &= extra_filter

        search_result = self._search(
            "search_drafts",
            identity,
            params,
            search_preference,
            record_cls=self.draft_cls,
            search_opts=self.config.search_drafts,
            extra_filter=search_draft_filter,
            permission_action="read_draft",
            **kwargs,
        ).execute()

        return self.result_list(
            self,
            identity,
            search_result,
            params,
            links_tpl=LinksTemplate(
                self.config.links_search_drafts, context={"args": params}
            ),
            links_item_tpl=self.links_item_tpl,
            expandable_fields=self.expandable_fields,
            expand=expand,
        )

    def search_versions(
        self,
        identity,
        id_,
        params=None,
        search_preference=None,
        expand=False,
        permission_action="read",
        **kwargs,
    ):
        """Search for record's versions."""
        try:
            record = self.record_cls.pid.resolve(id_, registered_only=False)
        except NoResultFound:
            record = self.draft_cls.pid.resolve(id_, registered_only=False)

        self.require_permission(identity, "read", record=record)
        extra_filter = dsl.Q("term", **{"parent.id": str(record.parent.pid.pid_value)})
        if filter_ := kwargs.pop("extra_filter", None):
            extra_filter = filter_ & extra_filter

        # Prepare and execute the search
        params = params or {}

        search_result = self._search(
            "search_versions",
            identity,
            params,
            search_preference,
            record_cls=self.record_cls,
            search_opts=self.config.search_versions,
            extra_filter=extra_filter,
            permission_action=permission_action,
            **kwargs,
        ).execute()

        return self.result_list(
            self,
            identity,
            search_result,
            params,
            links_tpl=LinksTemplate(
                self.config.links_search_versions,
                context={"pid_value": id_, "args": params},
            ),
            links_item_tpl=self.links_item_tpl,
            expandable_fields=self.expandable_fields,
            expand=expand,
        )

    def read_draft(self, identity, id_, expand=False):
        """Retrieve a draft."""
        # Resolve and require permission
        try:
            draft = self.draft_cls.pid.resolve(id_, registered_only=False)
        except NoResultFound:
            # Happens when record is published and not being edited (i.e. PID
            # with object id exists for the published record, but object
            # getter fails to get the draft object because only the record
            # object exists).
            raise DraftNotCreatedError(self.draft_cls.pid.field._pid_type, id_)

        self.require_permission(identity, "read_draft", record=draft)

        # NOTE: We can't re-run the schema vadliation here, because the draft since the
        # draft data that we have stored, is not necessarily valid input data for the
        # service schema. We should make this possible in the future, but for now we
        # just allow components to add their own errors to the draft result.
        errors = []

        # Run components
        for component in self.components:
            if hasattr(component, "read_draft"):
                component.read_draft(identity, draft=draft, errors=errors)

        return self.result_item(
            self,
            identity,
            draft,
            errors=errors,
            links_tpl=self.links_item_tpl,
            expandable_fields=self.expandable_fields,
            expand=expand,
        )

    def read_latest(self, identity, id_, expand=False):
        """Retrieve latest record.

        If provided with the ID of a parent record it will resolve it and return the latest version of the record.
        """
        # Resolve and require permission

        try:
            record = self.record_cls.pid.resolve(id_)
            # Retrieve latest if record is not
            if not record.versions.is_latest:
                record = self.record_cls.get_record(record.versions.latest_id)
        except NoResultFound:
            parent_pid = self.record_cls.parent_record_cls.pid.resolve(id_)
            version_state = self.record_cls.versions.resolve(
                parent_id=parent_pid.pid.object_uuid
            )
            if version_state and version_state.latest_id:
                record = self.record_cls.get_record(version_state.latest_id)
            else:
                raise NoResultFound(_("Failed to fetch the record versions."))

        self.require_permission(identity, "read", record=record)

        return self.result_item(
            self,
            identity,
            record,
            links_tpl=self.links_item_tpl,
            expandable_fields=self.expandable_fields,
            expand=expand,
        )

    @unit_of_work()
    def update_draft(
        self, identity, id_, data, revision_id=None, uow=None, expand=False
    ):
        """Replace a draft."""
        draft = self.draft_cls.pid.resolve(id_, registered_only=False)

        self.check_revision_id(draft, revision_id)

        # Permissions
        self.require_permission(identity, "update_draft", record=draft)

        # Load data with service schema
        data, errors = self.schema.load(
            data,
            context=dict(
                identity=identity,
                pid=draft.pid,
                record=draft,
            ),
            # Saving a draft only saves valid metadata and reports
            # (doesn't raise) errors
            raise_errors=False,
        )

        # Run components
        self.run_components(
            "update_draft", identity, record=draft, data=data, errors=errors, uow=uow
        )

        # Commit and index
        uow.register(RecordCommitOp(draft, indexer=self.indexer))

        uow.register(AuditLogOp(DraftEditAuditLog.build(identity, id_)))

        return self.result_item(
            self,
            identity,
            draft,
            links_tpl=self.links_item_tpl,
            errors=errors,
            expandable_fields=self.expandable_fields,
            expand=expand,
        )

    @unit_of_work()
    def create(self, identity, data, uow=None, expand=False):
        """Create a draft for a new record.

        It does NOT eagerly create the associated record.
        """
        res = self._create(
            self.draft_cls,
            identity,
            data,
            raise_errors=False,
            uow=uow,
            expand=expand,
        )

        uow.register(ParentRecordCommitOp(res._record.parent))

        uow.register(AuditLogOp(DraftCreateAuditLog.build(identity, str(res.id))))

        return res

    @unit_of_work()
    def edit(self, identity, id_, uow=None, expand=False):
        """Create a new revision or a draft for an existing record.

        :param id_: record PID value.
        """
        # Draft exists - return it
        try:
            draft = self.draft_cls.pid.resolve(id_, registered_only=False)
            self.require_permission(identity, "edit", record=draft)

            return self.result_item(
                self, identity, draft, links_tpl=self.links_item_tpl
            )
        except (NoResultFound, PIDDoesNotExistError):
            # We catch PIDDoesNotExistError because a published record with
            # a soft-deleted draft will raise this error. The lines below
            # will catch the case that a id does not exists and raise a
            # PIDDoesNotExistError that can be handled as 404 in the resource
            # layer.
            pass

        # Draft does not exist - so get the main record we want to edit and
        # create a draft from it
        record = self.record_cls.pid.resolve(id_)
        self.require_permission(identity, "edit", record=record)
        draft = self.draft_cls.edit(record)

        # Run components
        self.run_components("edit", identity, draft=draft, record=record, uow=uow)

        uow.register(RecordCommitOp(draft, indexer=self.indexer))

        # Reindex the record to trigger update of computed values in the
        # available dumpers of the record.
        uow.register(RecordIndexOp(record, indexer=self.indexer))

        uow.register(AuditLogOp(DraftCreateAuditLog.build(identity, id_)))

        return self.result_item(
            self,
            identity,
            draft,
            links_tpl=self.links_item_tpl,
            expandable_fields=self.expandable_fields,
            expand=expand,
        )

    @unit_of_work()
    def publish(self, identity, id_, uow=None, expand=False):
        """Publish a draft.

        Idea:
            - Get the draft from the data layer (draft is not passed in)
            - Validate it more strictly than when it was originally saved
              (drafts can be incomplete but only complete drafts can be turned
              into records)
            - Create or update associated (published) record with data
        """
        # Get the draft
        draft = self.draft_cls.pid.resolve(id_, registered_only=False)
        self.require_permission(identity, "publish", record=draft)

        # Validate the draft strictly - since a draft can be saved with errors
        # we do a strict validation here to make sure only valid drafts can be
        # published.
        self._validate_draft(identity, draft)

        # Create the record from the draft
        latest_id = draft.versions.latest_id
        record = self.record_cls.publish(draft)

        # Run components
        self.run_components("publish", identity, draft=draft, record=record, uow=uow)

        # Commit and index
        uow.register(RecordCommitOp(record, indexer=self.indexer))
        uow.register(RecordDeleteOp(draft, force=False, indexer=self.indexer))

        if latest_id:
            self._reindex_latest(latest_id, uow=uow)

        uow.register(
            AuditLogOp(RecordPublishAuditLog.build(identity, id_, record=record))
        )

        return self.result_item(
            self,
            identity,
            record,
            links_tpl=self.links_item_tpl,
            expandable_fields=self.expandable_fields,
            expand=expand,
        )

    @unit_of_work()
    def new_version(self, identity, id_, uow=None, expand=False):
        """Create a new version of a record."""
        # Get the record - i.e. you can only create a new version in case
        # at least one published record already exists.
        record = self.record_cls.pid.resolve(id_)

        # Check permissions
        self.require_permission(identity, "new_version", record=record)

        # Draft for new version already exists? if so return it
        if record.versions.next_draft_id:
            next_draft = self.draft_cls.get_record(record.versions.next_draft_id)
            return self.result_item(
                self, identity, next_draft, links_tpl=self.links_item_tpl
            )

        # Draft for new version does not exist, so create it
        next_draft = self.draft_cls.new_version(record)

        # Get the latest published record if it's not the current one.
        if not record.versions.is_latest:
            record = self.record_cls.get_record(record.versions.latest_id)

        # Run components
        self.run_components(
            "new_version", identity, draft=next_draft, record=record, uow=uow
        )

        # Commit and index
        uow.register(RecordCommitOp(next_draft, indexer=self.indexer))

        self._reindex_latest(next_draft.versions.latest_id, record=record, uow=uow)

        uow.register(
            AuditLogOp(
                DraftNewVersionAuditLog.build(identity, next_draft.pid.pid_value),
            )
        )

        return self.result_item(
            self,
            identity,
            next_draft,
            links_tpl=self.links_item_tpl,
            expandable_fields=self.expandable_fields,
            expand=expand,
        )

    @unit_of_work()
    def delete_draft(self, identity, id_, revision_id=None, uow=None):
        """Delete a record from database and search indexes."""
        draft = self.draft_cls.pid.resolve(id_, registered_only=False)
        latest_id = draft.versions.latest_id

        self.check_revision_id(draft, revision_id)

        # Permissions
        self.require_permission(identity, "delete_draft", record=draft)

        # Get published record if exists
        try:
            record = self.record_cls.get_record(draft.id)
        except NoResultFound:
            record = None

        # We soft-delete a draft when a published record exists, in order to
        # keep the version_id counter around for optimistic concurrency
        # control (both for search indexing and for REST API clients)
        force = False if record else True

        # Run components
        self.run_components(
            "delete_draft", identity, draft=draft, record=record, force=force, uow=uow
        )

        # Note, the parent record deletion logic is implemented in the
        # ParentField and will automatically take care of deleting the parent
        # record in case this is the only draft that exists for the parent.
        # We refresh the index because users are usually redirected to a
        # search result immediately after, and we don't want the users to see
        # their just deleted draft.
        uow.register(
            RecordDeleteOp(draft, indexer=self.indexer, force=force, index_refresh=True)
        )

        if force:
            # Case 1: We deleted a new draft (without a published record) or a
            # new version draft (without a published).
            # In this case, we reindex the latest published record/draft
            self._reindex_latest(latest_id, refresh=True, uow=uow)
        else:
            # Case 2: We deleted a draft for a published record.
            # In this case we reindex just the published record to trigger and
            # update of computed values.
            uow.register(
                RecordIndexOp(record, indexer=self.indexer, index_refresh=True)
            )

        uow.register(AuditLogOp(DraftDeleteAuditLog.build(identity, id_)))

        return True

    @unit_of_work()
    def import_files(self, identity, id_, uow=None):
        """Import files from previous record version."""
        if self.draft_files is None:
            raise RuntimeError(_("Files support is not enabled."))

        # Read draft
        draft = self.draft_cls.pid.resolve(id_, registered_only=False)
        self.require_permission(identity, "update_draft", record=draft)

        # Retrieve latest record
        record = self.record_cls.get_record(draft.versions.latest_id)
        self.require_permission(identity, "read_files", record=record)

        # Run components
        self.run_components(
            "import_files", identity, draft=draft, record=record, uow=uow
        )

        # Commit and index
        uow.register(RecordCommitOp(draft, indexer=self.indexer))

        return self.draft_files.file_result_list(
            self.draft_files,
            identity,
            results=draft.files.values(),
            record=draft,
            links_tpl=self.draft_files.file_links_list_tpl(id_),
            links_item_tpl=self.draft_files.file_links_item_tpl(id_),
        )

    def rebuild_index(self, identity):
        """Reindex all records and drafts.

        Note: Skips (soft) deleted records and drafts.
        """
        ret_val = super().rebuild_index(identity)

        model_cls = self.draft_cls.model_cls
        drafts = (
            db.session.query(model_cls.id)
            .filter(model_cls.is_deleted == False)
            .yield_per(1000)
        )

        self.draft_indexer.bulk_index((draft.id for draft in drafts))

        return ret_val

    def validate_draft(self, identity, id_, ignore_field_permissions=False):
        """Validate a draft."""
        draft = self.draft_cls.pid.resolve(id_, registered_only=False)
        self._validate_draft(identity, draft, ignore_field_permissions)

    def _validate_draft(self, identity, draft, ignore_field_permissions=False):
        """Validate a draft.

        This method is internal because it works with a data access layer
        draft, and thus should not be called from outside the service.
        """
        # Convert to draft into service layer draft result item (a record
        # projection for the given identity). This way we can load and validate
        # the data with the service schema.
        draft_item = self.result_item(self, identity, draft)
        validation_context = {
            "identity": identity,
            "pid": draft.pid,
            "record": draft,
        }

        if ignore_field_permissions:
            # optionally, we override the field-level permission checks with an
            # "allow all" because sometimes we only care about the structural and
            # semantic validation of drafts, but not the permissions that have been
            # checked elsewhere already

            def always_allow(*args, **kwargs):
                """Liberal override for permission_policy.allows(...)."""
                return True

            validation_context["field_permission_check"] = always_allow

        # Validate the data - will raise ValidationError if not valid.
        # note: schema.dump() will not raise ValidationErrors since marshmallow 3.0.0rc9
        self.schema.load(
            data=draft_item.data,
            context=validation_context,
            raise_errors=True,  # this is the default, but might as well be explicit
        )

    @unit_of_work()
    def _reindex_latest(
        self, latest_id, record=None, draft=None, refresh=False, uow=None
    ):
        """Reindex the latest published record and draft.

        This triggers and update of computed values in the index, such as
        "is_latest".

        This method is internal because it works with a data access layer
        record/draft, and thus should not be called from outside the service.
        """
        # We only have a draft, no latest to index
        if not latest_id:
            return

        # Note, the record may not be the latest published record, and we only
        # want to index the latest published.
        if record is None or latest_id != record.id:
            record = self.record_cls.get_record(latest_id)
        uow.register(RecordIndexOp(record, indexer=self.indexer, index_refresh=refresh))

        # Note, a draft may or may not exist for a published record (depending
        # on if it's being edited).
        try:
            draft = self.draft_cls.get_record(latest_id)
            uow.register(
                RecordIndexOp(draft, indexer=self.indexer, index_refresh=refresh)
            )
        except NoResultFound:
            pass

    def _get_record_and_parent_by_id(self, id_):
        """Resolve the record and its parent, by the given ID.

        If the ID belongs to a parent record, no child record will be
        resolved.
        """
        record = self.record_cls.pid.resolve(id_, registered_only=False)
        parent = record.parent

        return record, parent

    def _get_draft_and_parent_by_id(self, id_):
        """Resolve the draft and its parent, by the given ID."""
        draft = self.draft_cls.pid.resolve(id_, registered_only=False)
        parent = draft.parent

        return draft, parent

    @unit_of_work()
    def cleanup_drafts(self, timedelta, uow=None, search_gc_deletes=60):
        """Hard delete of soft deleted drafts.

        :param int timedelta: timedelta that should pass since
            the last update of the draft in order to be hard deleted.
        :param int search_gc_deletes: time in seconds, corresponding to the search cluster
            setting `index.gc_deletes` (see https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-delete.html#delete-versioning),
            default to 60 seconds. Search cluster caches deleted documents for `index.gc_deletes` seconds.
        """
        self.draft_cls.cleanup_drafts(timedelta, search_gc_deletes)

    @unit_of_work()
    def reindex_latest_first(
        self, identity, search_preference=None, extra_filter=None, uow=None
    ):
        """Reindexes records matching the query filter, prioritizing latest versions.

        Records will be retrieved from search engine and current versions re-indexed first.
        The latest version of a record is reindexed twice, but we trade that off for the guarantee that it also gets re-indexed first.

        .. warning::

            this service call should only be used during asynchronous calls (e.g. not inside a HTTP request context), since ``search.sync()`` might take some time.
        """
        self.require_permission(identity, "manage")

        # Create a search instance with the given filters. We avoid the overhead of executing params interpreters (e.g. aggregations)
        search = self.create_search(
            identity,
            self.record_cls,
            self.config.search,
            permission_action="read",
            extra_filter=extra_filter,
            preference=search_preference,
        )

        # Search only latest versions and register them for indexing
        latest_versions = search.filter("term", **{"versions.is_latest": True}).scan()
        for res in latest_versions:
            try:
                record = self.record_cls.pid.resolve(res.id)
                uow.register(RecordIndexOp(record, indexer=self.indexer))
            # Safe check, only re-index records that are resolvable
            except:
                continue

        # Search all versions and register them for bulk indexing
        # source(False): don't return any field, just the metadata
        all_versions = search.source(False).scan()
        all_iterable_ids = (res.meta.id for res in all_versions)
        uow.register(RecordBulkIndexOp(all_iterable_ids, indexer=self.indexer))

        return True
