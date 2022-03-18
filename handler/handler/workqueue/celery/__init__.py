"""A work queue using celery to defer requests"""
from json import dumps, loads
from math import ceil
from redis import from_url
from time import time

from .. import WorkQueue, TASK_ST_RUNNING, TASK_ST_COMPLETED, RequestError
from .worker import app, dispatch

class CeleryWorkQueue(WorkQueue):
    """This work queue defers the task to celery_migrator app"""

    def __init__(self, backend, broker):
        super(CeleryWorkQueue, self).__init__()
        app.conf.result_backend = backend
        app.conf.broker_url = broker

    def push(self, task, backends_ctx):
        return dispatch.delay(task["file_id"], task["action"],
                              task["backend"], backends_ctx).id

    def status(self, task_id):
        result = app.AsyncResult(task_id)

        if not result.ready():
            return TASK_ST_RUNNING

        if not result.failed():
            return TASK_ST_COMPLETED

        result = result.result
        assert isinstance(result, RuntimeError), \
            "expected %s to be a RuntimeError, but it is instead a %s" % \
            (result, result.__class__.__name__)

        errcode, errmsg = str(result).split(' ', 1)
        raise RequestError(errcode, errmsg)
