# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Drafts-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Draft Models API."""

from datetime import datetime

from invenio_db import db
from invenio_records.models import RecordMetadataBase
from sqlalchemy.dialects import mysql
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy_utils.types import UUIDType


class ParentRecordMixin:
    """A mixin factory that add the foreign keys to the parent record.

    Usage:

    .. code-block:: python

        class MyRecord(db.Model, RecordMetadataBase, ParentRecordMixin):
            __parent_record_model__ = ParentRecordMetadata
    """

    __parent_record_model__ = None

    @declared_attr
    def parent_id(cls):
        """Parent identifier."""
        # We restrict deletion of the parent record in case a record or draft
        # exists via database-level trigger.
        return db.Column(
            UUIDType, db.ForeignKey(cls.__parent_record_model__.id, ondelete="RESTRICT")
        )

    @declared_attr
    def parent(cls):
        """Relationship to parent record."""
        return db.relationship(cls.__parent_record_model__)

    index = db.Column(db.Integer, nullable=True)
    """The version index of the record."""


class ParentRecordStateMixin:
    """Database model mixin to keep the state of the latest and next version.

    We keep this data outside the parent record itself, because we want to
    update it without impacting the parent record's version counter. The
    version counter in the parent record we use to determine if we have to
    reindex all record versions.

    Usage:

    .. code-block:: python

        class MyParentState(db.Model, ParentRecordState):
            __parent_record_model__ = MyParentRecord
            __draft_model__ = MyDraft
            __record_model__ = MyRecord
    """

    __parent_record_model__ = None
    __record_model__ = None
    __draft_model__ = None

    @declared_attr
    def parent_id(cls):
        """Parent record identifier."""
        return db.Column(
            UUIDType,
            # 1) If the parent record is deleted, we automatically delete
            # the state as well via database-level on delete trigger.
            # 2) A parent can only be deleted, if it has no drafts/records via
            # FKs from drafts/records to the parent.
            db.ForeignKey(cls.__parent_record_model__.id, ondelete="CASCADE"),
            primary_key=True,
        )

    @declared_attr
    def latest_id(cls):
        """UUID of the latest published record/draft.

        Note, since a record and draft share the same UUID, the UUID can be
        used to get both the record or the draft. It's a foreign key to the
        record to ensure that the record exists (and thus is published).

        If no record has been published, the value is None.
        """
        return db.Column(
            UUIDType,
            db.ForeignKey(cls.__record_model__.id),
            nullable=True,
        )

    latest_index = db.Column(db.Integer, nullable=True)
    """The index of the latest published record.

    If no record has been published, the value is None.
    """

    @declared_attr
    def next_draft_id(cls):
        """UUID of the draft for the next version (yet to be published).

        Note, since a record and draft share the same UUID, the UUID can be
        used to get both the record or the draft. It's a foreign key to the
        draft, because we use it to track if a draft has been created for the
        next version.

        If no draft for the next version has been created, the value is None.
        """
        return db.Column(
            UUIDType,
            db.ForeignKey(cls.__draft_model__.id),
            nullable=True,
        )


class DraftMetadataBase(RecordMetadataBase):
    """Represent a base class for draft metadata."""

    fork_version_id = db.Column(db.Integer)
    """Version ID of the record."""

    expires_at = db.Column(
        db.DateTime().with_variant(mysql.DATETIME(fsp=6), "mysql"),
        default=datetime.utcnow,
        nullable=True,
    )
    """Specifies when the draft expires. If `NULL` the draft doesn't expire."""
