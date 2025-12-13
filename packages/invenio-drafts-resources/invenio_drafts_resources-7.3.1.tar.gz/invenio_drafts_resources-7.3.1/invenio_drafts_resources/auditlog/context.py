# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 CERN.
#
# Invenio-Drafts-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Audit log context resolvers."""

from flask import current_app, request
from invenio_records.dictutils import dict_lookup, dict_set
from invenio_users_resources.entity_resolvers import UserResolver


class UserContext(object):
    """Payload generator for audit log using the user entity resolver."""

    def __init__(self, key="user"):
        """Ctor."""
        self.key = key
        self.resolver = UserResolver()

    def __call__(self, data, lookup_key="user_id", **kwargs):
        """Update data with resolved user data."""
        entity_ref = dict_lookup(data, lookup_key)
        entity_proxy = self.resolver.get_entity_proxy({self.key: entity_ref})
        entity_data = entity_proxy.resolve()
        dict_set(data, self.key, entity_data)


class RecordContext(object):
    """Payload generator for audit log to get record auditing metadata."""

    def __call__(self, data, **kwargs):
        """Update data with resolved record data."""
        record = kwargs["record"]
        if current_app.config["AUDIT_LOGS_METADATA_FIELDS"]["revision_id"]:
            record_versions = record.model.versions.all()
            dict_set(data, "metadata.revision_id", record_versions[-1].transaction_id)
        if current_app.config["AUDIT_LOGS_METADATA_FIELDS"]["parent_pid"]:
            dict_set(data, "metadata.parent_pid", record.parent.pid.pid_value)


class RequestContext(object):
    """Payload generator for audit log using the request context."""

    def __call__(self, data, **kwargs):
        """Update data with resolved request data."""
        # IMPORTANT! DON'T COPY THIS, PLEASE DON'T DO THIS EVER...
        if request:
            if current_app.config["AUDIT_LOGS_METADATA_FIELDS"]["ip_address"]:
                ip = request.headers.get("REMOTE_ADDR") or request.remote_addr
                if ip:
                    dict_set(data, "metadata.ip_address", ip)

            if current_app.config["AUDIT_LOGS_METADATA_FIELDS"]["session"]:
                session = request.cookies.get("SESSION") or request.cookies.get(
                    "session"
                )
                if session:
                    dict_set(data, "metadata.session", session)
