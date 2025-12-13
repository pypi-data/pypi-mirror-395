# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CERN.
# Copyright (C) 2021 TU Wien.
# Copyright (C) 2024 KTH Royal Institute of Technology.
#
# Invenio-Drafts-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Error classes and handlers."""

import json

from flask_resources.errors import HTTPJSONException
from invenio_i18n import gettext as _
from invenio_pidstore.errors import PIDDoesNotExistError


class RedirectException(HTTPJSONException):
    """Trigger a redirect to the latest record version.

    The `create_latest_version_redirect_error_handler` handles this exception
    defined in the `RecordVersionsResourceConfig.error_map`. The handler is
    redirecting to the location instructed by the raised Exception.
    """

    code = 301

    def __init__(self, location, **kwargs):
        """Constructor."""
        self.location = location
        kwargs.setdefault("description", _("Redirecting..."))
        super().__init__(**kwargs)

    def get_headers(self, environ=None, scope=None):
        """Get response headers."""
        return [("Content-Type", "application/json"), ("Location", self.location)]

    def get_body(self, environ=None, scope=None):
        """Get the request body."""
        body = {
            "status": self.code,
            "message": self.get_description(environ),
            "location": self.location,
        }
        return json.dumps(body)


class DraftNotCreatedError(PIDDoesNotExistError):
    """Draft is not created for published record error."""
