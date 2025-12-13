# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Invenio-Drafts-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio Drafts Resources module to create REST APIs."""

from flask import g
from flask_resources import (
    JSONSerializer,
    ResponseHandler,
    resource_requestctx,
    response_handler,
    route,
    with_content_negotiation,
)
from invenio_records_resources.resources import RecordResource as RecordResourceBase
from invenio_records_resources.resources import (
    RecordResourceConfig as RecordResourceConfigBase,
)
from invenio_records_resources.resources.records.headers import etag_headers
from invenio_records_resources.resources.records.resource import (
    request_data,
    request_extra_args,
    request_headers,
    request_read_args,
    request_search_args,
    request_view_args,
)
from invenio_records_resources.resources.records.utils import search_preference

from .errors import RedirectException


class RecordResource(RecordResourceBase):
    """Draft-aware RecordResource."""

    def create_blueprint(self, **options):
        """Create the blueprint."""
        # We avoid passing url_prefix to the blueprint because we need to
        # install URLs under both /records and /user/records. Instead we
        # add the prefix manually to each route (which is anyway what Flask
        # does in the end)
        options["url_prefix"] = ""
        return super().create_blueprint(**options)

    def create_url_rules(self):
        """Create the URL rules for the record resource."""
        routes = self.config.routes

        def p(route):
            """Prefix a route with the URL prefix."""
            return f"{self.config.url_prefix}{route}"

        def s(route):
            """Suffix a route with the URL prefix."""
            return f"{route}{self.config.url_prefix}"

        rules = [
            route("GET", p(routes["list"]), self.search),
            route("POST", p(routes["list"]), self.create),
            route("GET", p(routes["item"]), self.read),
            route("PUT", p(routes["item"]), self.update),
            route("DELETE", p(routes["item"]), self.delete),
            route("GET", p(routes["item-versions"]), self.search_versions),
            route("POST", p(routes["item-versions"]), self.new_version),
            route("GET", p(routes["item-latest"]), self.read_latest),
            route("GET", p(routes["item-draft"]), self.read_draft),
            route("POST", p(routes["item-draft"]), self.edit),
            route("PUT", p(routes["item-draft"]), self.update_draft),
            route("DELETE", p(routes["item-draft"]), self.delete_draft),
            route("POST", p(routes["item-publish"]), self.publish),
            route("GET", s(routes["user-prefix"]), self.search_user_records),
        ]

        if self.service.draft_files:
            rules.append(
                route(
                    "POST",
                    p(routes["item-files-import"]),
                    self.import_files,
                    apply_decorators=False,
                )
            )

        return rules

    @request_extra_args
    @request_search_args
    @request_view_args
    @response_handler(many=True)
    def search_user_records(self):
        """Perform a search over the record's versions.

        GET /user/records
        """
        hits = self.service.search_drafts(
            identity=g.identity,
            params=resource_requestctx.args,
            search_preference=search_preference(),
            expand=resource_requestctx.args.get("expand", False),
        )
        return hits.to_dict(), 200

    @request_extra_args
    @request_search_args
    @request_view_args
    @response_handler(many=True)
    def search_versions(self):
        """Perform a search over the record's versions.

        GET /records/:pid_value/versions
        """
        hits = self.service.search_versions(
            g.identity,
            resource_requestctx.view_args["pid_value"],
            params=resource_requestctx.args,
            search_preference=search_preference(),
            expand=resource_requestctx.args.get("expand", False),
        )
        return hits.to_dict(), 200

    @request_extra_args
    @request_view_args
    @response_handler()
    def new_version(self):
        """Create a new version.

        POST /records/:pid_value/versions
        """
        item = self.service.new_version(
            g.identity,
            resource_requestctx.view_args["pid_value"],
            expand=resource_requestctx.args.get("expand", False),
        )
        return item.to_dict(), 201

    @request_extra_args
    @request_view_args
    @response_handler()
    def edit(self):
        """Edit a record.

        POST /records/:pid_value/draft
        """
        item = self.service.edit(
            g.identity,
            resource_requestctx.view_args["pid_value"],
            expand=resource_requestctx.args.get("expand", False),
        )
        return item.to_dict(), 201

    @request_extra_args
    @request_view_args
    @response_handler()
    def publish(self):
        """Publish the draft."""
        item = self.service.publish(
            g.identity,
            resource_requestctx.view_args["pid_value"],
            expand=resource_requestctx.args.get("expand", False),
        )
        return item.to_dict(), 202

    @request_view_args
    @with_content_negotiation(
        response_handlers={
            "application/vnd.inveniordm.v1+json": RecordResourceConfigBase.response_handlers[
                "application/json"
            ],
            **RecordResourceConfigBase.response_handlers,
        },
        default_accept_mimetype="application/json",
    )
    @response_handler(many=True)
    def import_files(self):
        """Import files from previous record version."""
        files = self.service.import_files(
            g.identity,
            resource_requestctx.view_args["pid_value"],
        )
        return files.to_dict(), 201

    @request_extra_args
    @request_view_args
    def read_latest(self):
        """Redirect to latest record.

        GET /records/:pid_value/versions/latest
        """
        item = self.service.read_latest(
            g.identity,
            resource_requestctx.view_args["pid_value"],
            expand=resource_requestctx.args.get("expand", False),
        )
        raise RedirectException(item["links"]["self"])

    @request_extra_args
    @request_read_args
    @request_view_args
    @response_handler()
    def read_draft(self):
        """Edit a draft.

        GET /records/:pid_value/draft
        """
        item = self.service.read_draft(
            g.identity,
            resource_requestctx.view_args["pid_value"],
            expand=resource_requestctx.args.get("expand", False),
        )
        return item.to_dict(), 200

    @request_extra_args
    @request_headers
    @request_view_args
    @request_data
    @response_handler()
    def update_draft(self):
        """Update a draft.

        PUT /records/:pid_value/draft
        """
        item = self.service.update_draft(
            g.identity,
            resource_requestctx.view_args["pid_value"],
            resource_requestctx.data or {},
            revision_id=resource_requestctx.headers.get("if_match"),
            expand=resource_requestctx.args.get("expand", False),
        )
        return item.to_dict(), 200

    @request_headers
    @request_view_args
    def delete_draft(self):
        """Delete a draft.

        DELETE /records/:pid_value/draft
        """
        self.service.delete_draft(
            g.identity,
            resource_requestctx.view_args["pid_value"],
            revision_id=resource_requestctx.headers.get("if_match"),
        )
        return "", 204
