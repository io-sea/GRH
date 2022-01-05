"""This echo work queue only prints tasks on stdout."""

import uuid

from handler.workqueue import WorkQueue, TASK_ST_COMPLETED

class DummyQueue(WorkQueue):
    """DummyQueue returns a taskid on push and TASK_ST_COMPLETED on status"""

    def __init__(self):
        super(DummyQueue, self).__init__()

    def push(self, task):
        task_id = uuid.uuid4()
        return task_id.hex

    def status(self, task_id):
        return TASK_ST_COMPLETED
