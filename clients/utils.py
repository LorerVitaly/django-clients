import logging

from rest_framework.exceptions import APIException
from retry.api import retry_call, decorator

logger = logging.getLogger(__name__)

RETRY_TRIES = 3
RETRY_DELAY = 1
RETRY_BACKOFF = 2


def base_api_retry(exceptions=(APIException),
                   tries=RETRY_TRIES, delay=RETRY_DELAY,
                   backoff=RETRY_BACKOFF, jitter=0, logger=logger):
    @decorator
    def retry_decorator(f, *fargs, **fkwargs):
        args = fargs if fargs else list()
        kwargs = fkwargs if fkwargs else dict()
        default_retry_kwargs = dict(exceptions=exceptions,
                                    tries=tries,
                                    delay=delay,
                                    backoff=backoff,
                                    jitter=jitter,
                                    logger=logger)
        retry_kwargs = dict(default_retry_kwargs, **(kwargs.pop('retry_kwargs', {}) or {}))

        return retry_call(f, args, kwargs, **retry_kwargs)

    return retry_decorator


def decorate_all_methods(decorator):
    def decorate(cls):
        for attr in cls.__dict__:
            if callable(getattr(cls, attr)):
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls

    return decorate


def get_from_json(json: dict, path: str):
    """
    Extracts a nested element from JSON.
    @param json: a json object
    @param path: a dot-separated path to the element
    """
    keys_order = path.split('.')
    item = json
    for key in keys_order:
        item = item[key]
    return item
