# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
# Copyright (C) 2024 University of Münster.
# Copyright (C) 2025 Graz University of Technology.
# Copyright (C) 2025 KTH Royal Institute of Technology.
#
# Invenio-Jobs is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Service definitions."""

import uuid

import sqlalchemy as sa
from flask import current_app
from invenio_db import db
from invenio_records_resources.services.base import LinksTemplate
from invenio_records_resources.services.base.utils import map_search_params
from invenio_records_resources.services.records import RecordService
from invenio_records_resources.services.uow import (
    ModelCommitOp,
    ModelDeleteOp,
    TaskOp,
    TaskRevokeOp,
    unit_of_work,
)

from invenio_jobs.logging.jobs import EMPTY_JOB_CTX, with_job_context
from invenio_jobs.services.uow import JobContextOp
from invenio_jobs.tasks import execute_run

from ..api import AttrDict
from ..models import Job, Run, RunStatusEnum, Task
from .errors import (
    JobNotFoundError,
    RunNotFoundError,
    RunStatusChangeError,
)


class BaseService(RecordService):
    """Base service class for DB-backed services.

    NOTE: See https://github.com/inveniosoftware/invenio-records-resources/issues/583
    for future directions.
    """

    def rebuild_index(self, identity, uow=None):
        """Raise error since services are not backed by search indices."""
        raise NotImplementedError()


class TasksService(BaseService):
    """Tasks service."""

    def read_registered_task_arguments(self, identity, registered_task_id):
        """Return arguments allowed for given task."""
        self.require_permission(identity, "read")

        task = Task.get(registered_task_id)
        if task.arguments_schema:
            return task.arguments_schema()


def get_job(job_id):
    """Get a job by id."""
    job = db.session.get(Job, job_id)
    if job is None:
        raise JobNotFoundError(job_id)
    return job


def get_run(run_id=None, job_id=None):
    """Get a job by id."""
    run = db.session.get(Run, run_id)
    if isinstance(job_id, str):
        job_id = uuid.UUID(job_id)

    if run is None or run.job_id != job_id:
        raise RunNotFoundError(run_id, job_id=job_id)
    return run


class JobsService(BaseService):
    """Jobs service."""

    @unit_of_work()
    def create(self, identity, data, uow=None):
        """Create a job."""
        self.require_permission(identity, "create")

        # TODO: See if we need extra validation (e.g. tasks, args, etc.)
        valid_data, errors = self.schema.load(
            data,
            context={"identity": identity},
            raise_errors=True,
        )

        job = Job(**valid_data)
        uow.register(ModelCommitOp(job))
        return self.result_item(self, identity, job, links_tpl=self.links_item_tpl)

    def search(self, identity, params):
        """Search for jobs."""
        self.require_permission(identity, "search")

        filters = []
        search_params = map_search_params(self.config.search, params)

        query_param = search_params["q"]
        if query_param:
            filters.append(
                sa.or_(
                    Job.title.ilike(f"%{query_param}%"),
                    Job.description.ilike(f"%{query_param}%"),
                )
            )

        jobs = (
            Job.query.filter(*filters)
            .order_by(
                search_params["sort_direction"](
                    sa.text(",".join(search_params["sort"]))
                )
            )
            .paginate(
                page=search_params["page"],
                per_page=search_params["size"],
                error_out=False,
            )
        )

        return self.result_list(
            self,
            identity,
            jobs,
            params=search_params,
            links_tpl=LinksTemplate(self.config.links_search, context={"args": params}),
            links_item_tpl=self.links_item_tpl,
        )

    def read(self, identity, id_):
        """Retrieve a job."""
        self.require_permission(identity, "read")
        job = get_job(id_)
        return self.result_item(self, identity, job, links_tpl=self.links_item_tpl)

    @unit_of_work()
    def update(self, identity, id_, data, uow=None):
        """Update a job."""
        self.require_permission(identity, "update")

        job = get_job(id_)

        valid_data, errors = self.schema.load(
            data,
            context={"identity": identity, "job": job},
            raise_errors=True,
        )

        for key, value in valid_data.items():
            setattr(job, key, value)
        uow.register(ModelCommitOp(job))
        return self.result_item(self, identity, job, links_tpl=self.links_item_tpl)

    @unit_of_work()
    def delete(self, identity, id_, uow=None):
        """Delete a job."""
        self.require_permission(identity, "delete")
        job = get_job(id_)

        # TODO: Check if we can delete the job (e.g. if there are still active Runs).
        # That also depends on the FK constraints in the DB.
        uow.register(ModelDeleteOp(job))

        return True


class RunsService(BaseService):
    """Runs service."""

    def search(self, identity, job_id, params):
        """Search for runs."""
        self.require_permission(identity, "search")

        filters = [
            Run.job_id == job_id,
        ]
        search_params = map_search_params(self.config.search, params)

        query_param = search_params["q"]
        if query_param:
            filters.append(
                sa.or_(
                    Run.id.ilike(f"%{query_param}%"),
                    Run.task_id.ilike(f"%{query_param}%"),
                )
            )

        runs = (
            Run.query.filter(*filters)
            .order_by(
                search_params["sort_direction"](
                    sa.text(",".join(search_params["sort"]))
                )
            )
            .paginate(
                page=search_params["page"],
                per_page=search_params["size"],
                error_out=False,
            )
        )

        return self.result_list(
            self,
            identity,
            runs,
            params=search_params,
            links_tpl=LinksTemplate(self.config.links_search, context={"args": params}),
            links_item_tpl=self.links_item_tpl,
        )

    def read(self, identity, job_id, run_id):
        """Retrieve a run."""
        self.require_permission(identity, "read")
        run = get_run(job_id=job_id, run_id=run_id)
        run_dict = run.dump()
        run_record = AttrDict(run_dict)
        return self.result_item(
            self, identity, run_record, links_tpl=self.links_item_tpl
        )

    @with_job_context(EMPTY_JOB_CTX)
    @unit_of_work()
    def create(self, identity, job_id, data, uow=None):
        """Create a run."""
        self.require_permission(identity, "create")

        job = get_job(job_id)
        # TODO: See if we need extra validation (e.g. tasks, args, etc.)
        valid_data, errors = self.schema.load(
            data,
            context={"identity": identity, "job": job},
            raise_errors=True,
        )

        run = Run.create(
            job=job,
            id=str(uuid.uuid4()),
            task_id=str(uuid.uuid4()),
            started_by_id=identity.id,
            status=RunStatusEnum.QUEUED,
            **valid_data,
        )

        uow.register(ModelCommitOp(run))
        uow.register(
            TaskOp.for_async_apply(
                execute_run,
                kwargs={"run_id": run.id},
                task_id=str(run.task_id),
                queue=run.queue,
            )
        )
        # Make sure this is the last operation in the unit of work
        # so tht the post_commit (that is resetting the job context)
        # is executed after the TaskOp post_commit.
        uow.register(JobContextOp({"run_id": str(run.id), "job_id": str(job_id)}))
        current_app.logger.debug("Run created")

        return self.result_item(self, identity, run, links_tpl=self.links_item_tpl)

    @unit_of_work()
    def update(self, identity, job_id, run_id, data, uow=None):
        """Update a run."""
        self.require_permission(identity, "update")

        run = get_run(job_id=job_id, run_id=run_id)

        valid_data, errors = self.schema.load(
            data,
            context={"identity": identity, "run": run, "job": run.job},
            raise_errors=True,
        )

        for key, value in valid_data.items():
            setattr(run, key, value)

        uow.register(ModelCommitOp(run))
        return self.result_item(self, identity, run, links_tpl=self.links_item_tpl)

    @unit_of_work()
    def delete(self, identity, job_id, run_id, uow=None):
        """Delete a run."""
        self.require_permission(identity, "delete")
        run = get_run(job_id=job_id, run_id=run_id)

        # TODO: Check if we can delete the run (e.g. if it's still running).
        uow.register(ModelDeleteOp(run))

        return True

    @unit_of_work()
    def stop(self, identity, job_id, run_id, uow=None):
        """Stop a run."""
        self.require_permission(identity, "stop")
        run = get_run(job_id=job_id, run_id=run_id)

        if run.status not in (RunStatusEnum.QUEUED, RunStatusEnum.RUNNING):
            raise RunStatusChangeError(run, RunStatusEnum.CANCELLING)

        run.status = RunStatusEnum.CANCELLING
        uow.register(ModelCommitOp(run))
        uow.register(TaskRevokeOp(str(run.task_id)))

        return self.result_item(self, identity, run, links_tpl=self.links_item_tpl)


class JobLogService(BaseService):
    """Job log service."""

    def search(self, identity, params):
        """Search for app logs."""
        self.require_permission(identity, "search")
        search_after = params.pop("search_after", None)
        search = self._search(
            "search",
            identity,
            params,
            None,
            permission_action="read",
        )
        max_docs = current_app.config["JOBS_LOGS_MAX_RESULTS"]
        batch_size = current_app.config["JOBS_LOGS_BATCH_SIZE"]

        # Clone and strip version before counting
        count_search = search._clone()
        count_search._params.pop("version", None)  # strip unsupported param
        total = count_search.count()

        # Track if we're truncating results
        truncated = total > max_docs

        search = search.sort("@timestamp", "_id").extra(size=batch_size)
        if search_after:
            search = search.extra(search_after=search_after)

        final_results = None
        fetched_count = 0

        # Keep fetching until we have max_docs or no more results
        while fetched_count < max_docs:
            results = search.execute()
            hits = results.hits
            if not hits:
                if final_results is None:
                    final_results = results
                break

            if not final_results:
                final_results = results  # keep metadata from first page
            else:
                final_results.hits.extend(hits)
                final_results.hits.hits.extend(hits.hits)

            fetched_count += len(hits)

            # Stop if we've reached the limit
            if fetched_count >= max_docs:
                # Trim to exact max_docs
                final_results.hits.hits = final_results.hits.hits[:max_docs]
                final_results.hits[:] = final_results.hits[:max_docs]
                break

            search = search.extra(search_after=hits[-1].meta.sort)

        # Store truncation info in the result for the AppLogsList to use
        if final_results and truncated:
            final_results._truncated = True
            final_results._total_available = total
            final_results._max_docs = max_docs

        return self.result_list(
            self,
            identity,
            final_results,
            links_tpl=self.links_item_tpl,
        )
