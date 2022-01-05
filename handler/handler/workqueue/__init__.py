"""Work queue interface definition and implementations.

A work queue is an abstraction used by the REST frontend to defer tasks and
check their status
"""

# Request states
TASK_ST_RUNNING = "running"
TASK_ST_COMPLETED = "completed"

class Empty(Exception):
    """Raised when a work queue is empty and the caller asked not to wait."""
    pass

class RequestError(Exception):
    """Raised when querying the status of a request that failed."""

    def __init__(self, errno, message, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.errno = errno
        self.message = message

class WorkQueue(object):
    """Generic API for a work queue that allows queueing and testing tasks.
    The underlying queue may be a python Queue, files, Kafka, Redis, PostgreSQL,
    celery, etc.  Depending on the implementation, tasks may need to be
    serializable with `pickle` or `json`.
    """

    def push(self, task):
        """Push the task into the queue.

        Return a task_id as a string of 64 characters maximum"""
        raise NotImplementedError()

    def status(self, task_id):
        """Return the status as:

        TASK_ST_RUNNING
        TASK_ST_COMPLETED

        or raises a RequestError exception
        """
        raise NotImplementedError()
