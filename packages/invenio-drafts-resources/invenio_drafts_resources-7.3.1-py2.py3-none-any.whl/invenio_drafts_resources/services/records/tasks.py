# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CERN.
#
# Invenio-Drafts-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Celery tasks to manage drafts."""

from datetime import timedelta

from celery import shared_task
from invenio_records_resources.proxies import current_service_registry


@shared_task(ignore_result=True)
def cleanup_drafts(seconds=3600, search_gc_deletes=60):
    """Hard delete of soft deleted drafts.

    :param int seconds: numbers of seconds that should pass since the
        last update of the draft in order to be hard deleted.
    :param int search_gc_deletes: time in seconds, corresponding to the search cluster
        setting `index.gc_deletes` (see https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-delete.html#delete-versioning),
        default to 60 seconds. Search cluster caches deleted documents for `index.gc_deletes` seconds.
    """
    timedelta_param = timedelta(seconds=seconds)
    service = current_service_registry.get("records")
    service.cleanup_drafts(timedelta_param, search_gc_deletes=search_gc_deletes)
