# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# Invenio-Jobs is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Tasks."""

import traceback
from datetime import datetime

from celery import shared_task
from flask import g
from invenio_db import db

from invenio_jobs.errors import TaskExecutionError, TaskExecutionPartialError
from invenio_jobs.models import Run, RunStatusEnum
from invenio_jobs.proxies import current_jobs


# TODO 1. Move to service? 2. Don't use kwargs?
def update_run(run, **kwargs):
    """Method to update and commit run updates."""
    if not run:
        return
    for kw, value in kwargs.items():
        setattr(run, kw, value)
    db.session.commit()


@shared_task(bind=True, ignore_result=True)
def execute_run(self, run_id, kwargs=None):
    """Execute and manage a run state and task."""
    run = Run.query.filter_by(id=run_id).one_or_none()
    task = current_jobs.registry.get(run.job.task).task
    update_run(run, status=RunStatusEnum.RUNNING, started_at=datetime.utcnow())
    try:
        result = task.apply(kwargs=run.args, throw=True)
    except SystemExit as e:
        sentry_event_id = getattr(g, "sentry_event_id", None)
        message = (
            f"{e.message} Sentry Event ID: {sentry_event_id}"
            if sentry_event_id
            else e.message
        )
        update_run(
            run,
            status=RunStatusEnum.CANCELLED,
            finished_at=datetime.utcnow(),
            message=message,
        )
        raise e
    except (TaskExecutionPartialError, TaskExecutionError) as e:
        sentry_event_id = getattr(g, "sentry_event_id", None)
        message = (
            f"{e.message} Sentry Event ID: {sentry_event_id}"
            if sentry_event_id
            else e.message
        )
        update_run(
            run,
            status=RunStatusEnum.PARTIAL_SUCCESS,
            finished_at=datetime.utcnow(),
            message=message,
        )
        return
    except Exception as e:
        sentry_event_id = getattr(g, "sentry_event_id", None)
        message = f"{e.__class__.__name__}: {str(e)}\n{traceback.format_exc()}"
        if sentry_event_id:
            message += f" Sentry Event ID: {sentry_event_id}"
        update_run(
            run,
            status=RunStatusEnum.FAILED,
            finished_at=datetime.utcnow(),
            message=message,
        )
        return

    update_run(
        run,
        status=RunStatusEnum.SUCCESS,
        finished_at=datetime.utcnow(),
    )
