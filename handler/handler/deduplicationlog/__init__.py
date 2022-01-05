"""Deduplication log interface definition and implementations.

A deduplication log is an abstraction used by the REST frontend to detect tasks
that have been already asked not too long ago.
"""

class DeduplicationLog(object):
    """Generic API for a deduplication log to detect already created tasks.

    A deduplication log allows to register a task_id and a timestamp associated
    with a created task which is identified by a JSON serializable value.

    A deduplication log can detect if an existing similar task was already
    register not too long ago, less than a deduplication slot time.
    """

    def __init__(self, dedup_slot_ms=0):
        """Creates a new log with a deduplication slot in milliseconds"""
        self.dedup_slot_s = 0.001 * dedup_slot_ms

    def register_task(self, task, task_id):
        """Store the task in the log with associated task_id and a timestamp

        The task and the task_id are JSON serializable values.
        The registered timestamp is the current time.
        """
        raise NotImplementedError()

    def get_task(self, task):
        """Return existing task_id from deduplication log or None

        Return task_id if the same task already exists in the deduplication log
        with a timestamp younger than the dedup slot, else return None.
        """
        raise NotImplementedError()
