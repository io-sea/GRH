"""A work queue using celery to defer requests"""
from json import dumps, loads
from math import ceil
from redis import from_url
from time import time

from subprocess import CalledProcessError

from .. import WorkQueue, TASK_ST_RUNNING, TASK_ST_COMPLETED, RequestError
from .worker import app, handle

class CeleryWorkQueue(WorkQueue):
    """This work queue defers the task to celery_migrator app"""

    def __init__(self, backend, broker):
        super(CeleryWorkQueue, self).__init__()
        app.conf.result_backend = backend
        app.conf.broker_url = broker

    def push(self, task):
        return handle.delay(task["file_id"], task["action"],
                            task["backend"]).id

    def status(self, task_id):
        result = app.AsyncResult(task_id)
        if not result.ready():
            return TASK_ST_RUNNING

        if not result.failed():
            return TASK_ST_COMPLETED

        result = result.result
        assert isinstance(result, CalledProcessError), \
                "expected %s to be a CalledProcessError, but it is instead a %s" % \
                (result, result.__class__.__name__)
        raise RequestError(result.returncode, result.output)
