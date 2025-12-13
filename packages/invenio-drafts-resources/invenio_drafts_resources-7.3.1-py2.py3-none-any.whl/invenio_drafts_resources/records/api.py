# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2023 CERN.
# Copyright (C) 2021 Northwestern University.
#
# Invenio-Drafts-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Record, Draft and Parent Record API classes.

These classes belongs to the  data access layer and MUST ONLY be accessed from
within the service layer. It's wrong to use these classes in the presentation
layer.

A record and a draft share a single parent record. The parent record is used
to store properties common to all versions of a record (e.g. access control).

The draft and record share the same UUID, and thus both also share a single
persistent identifier. The parent record has its own UUID and own persistent
identifier.
"""

import uuid
from datetime import datetime, timedelta

from invenio_db import db
from invenio_pidstore.models import PIDStatus
from invenio_pidstore.providers.recordid_v2 import RecordIdProviderV2
from invenio_records.systemfields import ModelField
from invenio_records_resources.records import Record as RecordBase
from invenio_records_resources.records.systemfields import PIDField, PIDStatusCheckField
from sqlalchemy.orm.exc import NoResultFound

from .systemfields import ParentField, VersionsField


#
# Persistent identifier providers
#
class DraftRecordIdProviderV2(RecordIdProviderV2):
    """Draft PID provider."""

    default_status_with_obj = PIDStatus.NEW


#
# Record API classes
#
class ParentRecord(RecordBase):
    """Parent record API."""

    # Configuration
    model_cls = None

    pid = PIDField("id", provider=DraftRecordIdProviderV2, delete=True)


class Record(RecordBase):
    """Record API."""

    #: Class attribute to make it easy to check if record is a draft or not.
    is_draft = False

    #
    # Configuration to be set by a subclass
    #

    #: The record's SQLAlchemy model class. Must be set by the subclass.
    model_cls = None
    #: The parent state's SQLAlchemy model class. Must be set by the subclass.
    versions_model_cls = None
    #: The parent record's API class. Must be set by the subclass.
    parent_record_cls = None

    #
    # System fields
    #
    #: The internal persistent identifier. Records and drafts share UUID.
    pid = PIDField("id", provider=DraftRecordIdProviderV2, delete=True)

    #: System field to check if a record has been published.
    is_published = PIDStatusCheckField(status=PIDStatus.REGISTERED)

    #: The parent record - the draft is responsible for creating the parent.
    parent = ParentField(
        ParentRecord, create=False, soft_delete=False, hard_delete=False
    )

    #: Version relationship
    versions = VersionsField(create=True, set_latest=True)

    @classmethod
    def get_records_by_parent(cls, parent, with_deleted=True, ids_only=False):
        """Get all sibling records for the specified parent record."""
        with db.session.no_autoflush:
            rec_models = cls.model_cls.query.filter_by(parent_id=parent.id)
            if not with_deleted:
                rec_models = rec_models.filter_by(is_deleted=False)

            if ids_only:
                return (rec_model.id for rec_model in rec_models)
            else:
                return (
                    cls(rec_model.data, model=rec_model, parent=parent)
                    for rec_model in rec_models
                )

    @classmethod
    def get_latest_by_parent(cls, parent, id_only=False):
        """Get the latest record for the specified parent record.

        It might return None if there is no latest published version yet.
        """
        with db.session.no_autoflush:
            version = cls.versions_model_cls.query.filter_by(
                parent_id=parent.id
            ).one_or_none()
            has_latest = version and version.latest_id
            if not has_latest:
                return None

            rec_model = cls.model_cls.query.filter_by(id=version.latest_id).one()
            if id_only:
                return rec_model.id
            else:
                return cls(rec_model.data, model=rec_model, parent=parent)

    @classmethod
    def publish(cls, draft):
        """Publish a draft as a new record.

        If a record already exists, we simply get the record. If a draft has
        not yet been published, we create the record.

        The caller is responsible for registering the internal persistent
        identifiers (see ``register()``).
        """
        if draft.is_published:
            record = cls.get_record(draft.id)
        else:
            record = cls.create(
                {},
                # A draft and record share UUID, so we reuse the draft's id/pid
                id_=draft.id,
                pid=draft.pid,
                # Link the record with the parent record and set the versioning
                # relationship.
                parent=draft.parent,
                versions=draft.versions,
            )
            # Merge the PIDs into the current db session if not already in the
            # session.
            cls.pid.session_merge(record)
            cls.parent_record_cls.pid.session_merge(record.parent)
        return record

    def register(self):
        """Register the internal persistent identifiers."""
        if not self.parent.pid.is_registered():
            self.parent.pid.register()
            self.parent.commit()
        self.pid.register()


class Draft(Record):
    """Draft base API for metadata creation and manipulation."""

    #: Class attribute to make it easy to check if record is a draft or not.
    is_draft = True

    #
    # Configuration to be set by a subclass
    #

    #: The record's SQLAlchemy model class. Must be set by the subclass.
    model_cls = None
    #: The parent state's SQLAlchemy model class. Must be set by the subclass.
    versions_model_cls = None
    #: The parent record's API class. Must be set by the subclass.
    parent_record_cls = None

    #
    # System fields
    #

    #: The internal persistent identifier. Records and drafts share UUID.
    pid = PIDField("id", provider=DraftRecordIdProviderV2, delete=False)

    #: The parent record - the draft is responsible for creating the parent.
    parent = ParentField(ParentRecord, create=True, soft_delete=False, hard_delete=True)

    #: Version relationship
    versions = VersionsField(create=True, set_next=True)

    #: The expiry date of the draft.
    expires_at = ModelField()

    #: Revision id of record from which this draft was created.
    fork_version_id = ModelField()

    @classmethod
    def new_version(cls, record):
        """Create a draft for a new version of a record.

        The caller is responsible for:
        1) checking if a draft for a new version already exists
        2) moving the record data into the draft data.
        """
        return cls.create(
            {},
            # We create a new id, because this is for a new version.
            id=uuid.uuid4(),
            # Links the draft with the same parent (i.e. a new version).
            parent=record.parent,
            versions=record.versions,
            # New drafts without a record (i.e. unpublished drafts) must set
            # the fork version id to None.
            fork_version_id=None,
        )

    @classmethod
    def edit(cls, record):
        """Create a draft for editing an existing version of a record."""
        try:
            # We soft-delete a draft once it has been published, in order to
            # keep the version_id counter around for optimistic concurrency
            # control (both for search indexing and for REST API clients)
            draft = cls.get_record(record.id, with_deleted=True)
            if draft.is_deleted:
                draft.undelete()
                # Below line is needed to dump PID back into the draft.
                draft.pid = record.pid
                # Ensure record is link with the parent
                draft.parent = record.parent
                draft.versions = record.versions
                # Ensure we record the revision id we forked from
                draft.fork_version_id = record.revision_id
                # Note, other values like bucket_id values was kept in the
                # soft-deleted record, so we are not setting them again here.
        except NoResultFound:
            # If a draft was ever force deleted, then we re-create it.
            # A classic scenario for this case is editing a published record
            # after enough time has passed for its original draft to have
            # been cleaned up. It then needs to be recreated.
            draft = cls.create(
                {},
                # A draft to edit a record must share the id and uuid.
                id_=record.id,
                pid=record.pid,
                # Link it with the same parent record
                parent=record.parent,
                versions=record.versions,
                # Record which record version we forked from.
                fork_version_id=record.revision_id,
            )
        return draft

    @classmethod
    def cleanup_drafts(cls, td, search_gc_deletes=60):
        """Clean up (hard delete) all the soft deleted drafts.

        The soft-deleted drafts in the last timedelta span of time won't be deleted,
        including `search_gc_deletes` seconds timedelta. This ensures that only
        drafts fully removed from the search cluster can be hard-deleted (e.g. when
        `td` is very short), avoiding search conflicts.

        :param int search_gc_deletes: time in seconds, corresponding to the search cluster
            setting `index.gc_deletes` (see https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-delete.html#delete-versioning),
            default to 60 seconds. Search cluster caches deleted documents for `index.gc_deletes` seconds.
        """
        timestamp = datetime.utcnow() - td - timedelta(seconds=search_gc_deletes)
        draft_model = cls.model_cls
        models = draft_model.query.filter(
            draft_model.is_deleted == True,  # noqa
            draft_model.updated < timestamp,
        ).all()

        # we need to clear the foreign keys in the version info
        for model in models:
            draft = cls(model.data, model=model)
            draft.versions.clear_next()

        # now we can delete the drafts without violating foreign keys
        ids = [model.id for model in models]
        draft_model.query.filter(draft_model.id.in_(ids)).delete(
            synchronize_session=False
        )
