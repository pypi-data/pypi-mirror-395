import inspect
import logging
from django_rq import job as rq_job
from functools import wraps


def job_with_meta(queue='default', **job_kwargs):
    """
    A drop-in @django_rq.job replacement that automatically saves meta after .delay().
    Raises an error if the decorated function already has a 'job_meta' parameter.
    """
    def decorator(func):
        # Check for parameter conflicts
        sig = inspect.signature(func)
        if 'job_meta' in sig.parameters:
            raise TypeError(f"Cannot decorate '{func.__name__}': it already has a parameter named 'job_meta'")

        # Create the base RQ job
        base = rq_job(queue, **job_kwargs)(func)

        # store original delay
        orig_delay = base.delay

        # Patch .delay() to handle job_meta
        @wraps(base.delay)
        def delay_with_meta(*args, job_meta=None, **kwargs):
            # pass normally to .delay
            job = orig_delay(*args, **kwargs)
            if job_meta:
                if not isinstance(job_meta, dict):
                    raise TypeError("job_meta must be a dict")
                # Merge with existing meta if needed
                job.meta.update(job_meta)
                job.save_meta()
            return job

        # Monkey-patch .delay() on the decorated function
        base.delay = delay_with_meta
        return base

    return decorator
