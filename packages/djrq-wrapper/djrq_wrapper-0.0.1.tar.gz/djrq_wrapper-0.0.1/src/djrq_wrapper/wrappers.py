import logging

import django_rq.settings
import django_rq.utils
import django_rq.jobs
from rq.command import send_stop_job_command
from rq.registry import (
    BaseRegistry,
    DeferredJobRegistry,
    FailedJobRegistry,
    FinishedJobRegistry,
    ScheduledJobRegistry,
    StartedJobRegistry
)


def serialize_job(job: django_rq.jobs.Job|dict) -> dict:
    # Serialize
    from django.core.serializers.json import DjangoJSONEncoder
    import json

    safe_list = []
    # Skip private attributes
    raw = {k: getattr(job, k) for k in dir(job) if not k.startswith("_")}
    safe = {}
    for k, v in raw.items():
        # Skip Methods
        if callable(v):
            continue
        try:
            json.dumps(v, cls=DjangoJSONEncoder)
            safe[k] = v
        except Exception:
            pass

    # Custom
    if type(job) is django_rq.jobs.Job:
        safe["status"] = job.get_status()
    else:
        logging.info("It's not JOB", job)

    return safe


def JobSerializer(job: django_rq.jobs.Job|dict|list, many=False) -> dict|list[dict]:
   if many:
       return [serialize_job(j) for j in job]
   else:
       return serialize_job(job)



def get_queue_list() -> list["dict"]:
    return django_rq.settings.QUEUES_LIST


def get_queue_list_names() -> list[str]:
    return [queue["name"] for queue in get_queue_list()]


def get_queue_by_name(name: str) -> django_rq.queues.Queue:
    return django_rq.get_queue(name)


def _get_queued_jobs_matching_kwargs(queue: django_rq.queues.Queue, kwargs: dict, _format: str) -> list[django_rq.jobs.Job]:
    jobs_matching = []
    for job in queue.jobs:
        if all([k in job.kwargs and job.kwargs[k] == v for k, v in kwargs.items()]):
            if _format == "json":
                jobs_matching.append(JobSerializer(job=job))
            else:
                jobs_matching.append(job)
    return jobs_matching


def _get_jobs_matching_meta_from_registry(queue: django_rq.queues.Queue, registry: BaseRegistry, metas: dict, _format: str = "Job") -> list[django_rq.jobs.Job]:
    """
    This function check each jobs of the given registry of a queue, for all given metas
    @param queue: Queue to fetch jobs from
    @param registry: Registry to get jobs id from
    @param metas: {"key1", "value1", }
    @param _format: can be "Job" or "json"
    @return: [job, ]
    """
    jobs_matching = []
    for job_id in registry.get_job_ids():
        job: django_rq.jobs.Job = queue.fetch_job(job_id)
        meta_not_matched = False
        for k in metas.keys():
            if k in job.meta and job.meta[str(k)] == metas[str(k)]:
                pass
            else:
                # a meta key is missing or the value isn't the awaited one.
                meta_not_matched = True
                break

        # Adding jobs to the list
        if not meta_not_matched:
            if _format.lower() == "json":
                jobs_matching.append(JobSerializer(job=job))
            else:
                jobs_matching.append(job)

    return jobs_matching


def _get_jobs_with_meta_from_queue(queue: django_rq.queues.Queue, metas: dict, jobs_type: list = None, _format: str = "Job", flat=False) -> dict | list[django_rq.jobs.Job]:
    """

    @param queue:
    @param metas:
    @param _format:
    @return: {'finished_jobs': [Job, ]} if flat == False else [Job, ]
    """
    if jobs_type is None:
        jobs_type = ["finished_jobs", "started_jobs", "deferred_jobs", "failed_jobs", "scheduled_jobs", "queued_jobs"]

    connection = queue.connection
    if not flat:
        queue_data = {}
    else:
        queue_data = []

    if "finished_jobs" in jobs_type:
        finished_job_registry = FinishedJobRegistry(queue.name, connection)
        jobs = _get_jobs_matching_meta_from_registry(queue=queue, registry=finished_job_registry, metas=metas, _format=_format)
        if not flat:
            queue_data['finished_jobs'] = jobs
        else:
            queue_data.extend(jobs)

    if "started_jobs" in jobs_type:
        started_job_registry = StartedJobRegistry(queue.name, connection)
        jobs = _get_jobs_matching_meta_from_registry(queue=queue, registry=started_job_registry,
                                                                          metas=metas, _format=_format)
        if not flat:
            queue_data['started_jobs'] = jobs
        else:
            queue_data.extend(jobs)

    if "deferred_jobs" in jobs_type:
        deferred_job_registry = DeferredJobRegistry(queue.name, connection)
        jobs = _get_jobs_matching_meta_from_registry(queue=queue, registry=deferred_job_registry,
                                                                           metas=metas, _format=_format)
        if not flat:
            queue_data['deferred_jobs'] = jobs
        else:
            queue_data.extend(jobs)

    if "failed_jobs" in jobs_type:
        failed_job_registry = FailedJobRegistry(queue.name, connection)
        jobs = _get_jobs_matching_meta_from_registry(queue=queue, registry=failed_job_registry,
                                                                         metas=metas, _format=_format)
        if not flat:
            queue_data['failed_jobs'] = jobs
        else:
            queue_data.extend(jobs)

    if "scheduled_jobs" in jobs_type:
        scheduled_job_registry = ScheduledJobRegistry(queue.name, connection)
        jobs = _get_jobs_matching_meta_from_registry(queue=queue, registry=scheduled_job_registry,
                                                                           metas=metas, _format=_format)
        if not flat:
            queue_data['scheduled_jobs'] = jobs
        else:
            queue_data.extend(jobs)

    if "queued_jobs" in jobs_type:
        jobs = _get_queued_jobs_matching_kwargs(queue=queue, kwargs=metas, _format=_format)
        if not flat:
            queue_data['queued_jobs'] = jobs
        else:
            queue_data.extend(jobs)

    return queue_data


def get_jobs_matching_meta(metas: dict, jobs_type: list = None, _format: str = "Job", queues_to_include=None, flat=False) -> list[dict] | list[django_rq.jobs.Job]:
    """
    Return all jobs matching given metas (key, values) sorted by queue and registry
    @param metas: {"key1": "value1", }
    @param _format: return format for the job
    @param queues_to_include: list of queues to include (all if None)
    @return:
    if flat == False
      [{"name":"queue1", "index": 0, "jobs": {"finished_jobs": [Job, ], }}]
    else
      [Job, ]
    """
    if metas is None:
        metas = {}
    queues = []
    idx = -1
    queues_list = get_queue_list()
    if queues_to_include is None:
        queues_to_include = [q["name"] for q in queues_list]

    for q in queues_list:
        if q["name"] in queues_to_include:
            idx += 1
            queue = get_queue_by_name(q["name"])
            jobs_in_queue = _get_jobs_with_meta_from_queue(queue=queue, metas=metas, jobs_type=jobs_type, _format=_format, flat=flat)

            if not flat:
                queue_data = {"name": q["name"], "index": idx,
                              "jobs": jobs_in_queue}
                queues.append(queue_data)

            else:
                queues.extend(jobs_in_queue)

        else:
            logging.debug(f"Queue {q['name']} not included")

    return queues

def get_job_by_id(job_id: str) -> django_rq.jobs.Job:
    return django_rq.jobs.Job.fetch(job_id, connection=django_rq.utils.get_connection())


def stop_job(job_id: str) -> None:
    logging.debug(f"Stopping running job {job_id}")
    send_stop_job_command(django_rq.utils.get_connection(), job_id)
