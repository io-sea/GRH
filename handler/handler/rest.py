"""A Flask server implementing the grh REST API."""

import json

import jsonschema

from flask import Flask, Response, json, request, current_app
from werkzeug.exceptions import BadRequest

from .workqueue import TASK_ST_RUNNING, TASK_ST_COMPLETED, RequestError
from . import init

from os import environ

# Default number of milliseconds the handler indicates to client as estimated
# duration before asked requests are ended.
DEFAULT_ETA_MS_PRESET = 10
DEFAULT_ETA_MS_ENV_NAME = "GRH_DEFAULT_ETA_MS"
DEFAULT_ETA_MS = int(environ.get(DEFAULT_ETA_MS_ENV_NAME,
                                 DEFAULT_ETA_MS_PRESET))

# /requests json body schema for jsonschema validation
REQUEST_JSON_SCHEMA = {
    "type": "object",
    "properties": {
        "file_id": {"type": "string"},
        "action": {"type": "string"},
        "backend": {"type": "string"},
    },
    "required": ["file_id", "action", "backend"],
}

REQUESTS_JSON_SCHEMA = {
    "type": "array",
    "items": REQUEST_JSON_SCHEMA,
}

# /requests/status json body schema for jsonschema validation
STATUS_JSON_SCHEMA = {
    "type": "object",
    "properties": {
        "request_id": {"type": "string"},
    },
    "required": ["request_id"],
}

STATUSES_JSON_SCHEMA = {
    "type": "array",
    "items": STATUS_JSON_SCHEMA,
}

# Valid actions for early validation
VALID_ACTIONS = ["put", "get", "delete"]

# Valid backends for early validation
VALID_BACKENDS = ["phobos", "s3", "empty"]

TASK_STATUS = {
    TASK_ST_RUNNING: "running",
    TASK_ST_COMPLETED: "completed",
}

# Currently, only "empty" is implemented, but the goal is to use VALID_BACKENDS
# in place of this list
backend_list = ["empty"]
backends_ctx = {}

def validate_request_list(requests):
    """Validates a request list and raises a BadRequest error if the list
    does not follow the following format:
    [
        {
            "file_id": "<unique_file_identifier>",
            "action": "<unique_action_identifier>",
            "backend": "<unique_backend_identifier>",
        },
        ...
    ]

    Arguments:
        requests: a parsed json to be validated; expected to be a list of
            dicts, as described by MIGRATIONS_JSON_SCHEMA.

    Raises:
        BadRequest if requests is not a valid list of requests.
    """
    try:
        jsonschema.validate(instance=requests, schema=REQUESTS_JSON_SCHEMA)
    except jsonschema.ValidationError as exc:
        raise BadRequest(str(exc))
    for rq in requests:
        if rq["action"] not in VALID_ACTIONS:
            raise BadRequest(
                "Unsupported action: %s, choose from %s" % (rq["action"],
                                                            VALID_ACTIONS)
            )
        if rq["backend"] not in VALID_BACKENDS:
            raise BadRequest(
                "Unsupported backend: %s, choose from %s" % (rq["backend"],
                                                            VALID_BACKENDS)
            )

def validate_status_list(statuses):
    """Validates a status list and raises a BadRequest error if the list
    does not follow the following format:
    [
        {
            "request_id": "<unique_request_identifier>"
        },
        ...
    ]

    Arguments:
        statuses: a parsed json to be validated; expected to be a list of
            dicts, as described by STATUSES_JSON_SCHEMA.

    Raises:
        BadRequest if statuses is not a valid list of status requests.
    """
    try:
        jsonschema.validate(instance=statuses, schema=STATUSES_JSON_SCHEMA)
    except jsonschema.ValidationError as exc:
        raise BadRequest(str(exc))

def build_request_response(request_id, status, eta=DEFAULT_ETA_MS,
                             errno=None, message=None):
    """Build a request response json corresponding to a provided request, with
    the given status, errno, message and eta.
    """
    return {
        "request_id": request_id,
        "status": status,
        "eta": eta,
        "errno": errno,
        "message": message,
    }

class JsonResponse(Response): # pylint: disable=too-many-ancestors
    """Utility wrapper to return HTTP responses with a json body"""

    def __init__(self, json_data, status=200):
        """Return an HTTP response with a given `status` code and serialize
        `json_data` as the body of the response.
        """
        super(JsonResponse, self).__init__(
            response=json.dumps(json_data),
            status=status,
            mimetype="application/json"
        )

def create_request():
    """Implements the /requests route: takes a list of requests and pushes
    them in a work queue. Expected to be run in the MigratorFlaskApp context,
    as it relies on `current_app.work_queue` and flask's magic `request`
    variable.
    """
    request_ids = []
    requests = request.get_json()
    validate_request_list(requests)
    current_app.logger.info("Adding %d requests" % (len(requests),))

    # Push requests to the work queue
    for rq in requests:
        request_id = None
        if current_app.deduplication_log:
            request_id = current_app.deduplication_log.get_task(rq)

        if not request_id:
            request_id = current_app.work_queue.push(rq, backends_ctx)
            if current_app.deduplication_log:
                current_app.deduplication_log.register_task(rq, request_id)

        request_ids.append(request_id)

    # Build request responses
    rq_resps = [
        build_request_response(request_id, "running")
        for request_id in request_ids
    ]

    #return 304 if no error and no created or existing request
    if not rq_resps:
        return JsonResponse(rq_resps, 304)

    return JsonResponse(rq_resps, 201)

def get_status():
    """Implements the /requests/status route

    Takes a list of request identifiers and gets their current status
    from the work queue. Expected to be run in the MigratorFlaskApp
    context, as it relies on `current_app.work_queue` and flask's magic
    `request` variable.
    """
    request_ids = request.get_json()
    validate_status_list(request_ids)
    current_app.logger.info("Getting %s statuses", len(request_ids))

    stat_resps = []
    for request_id in map(lambda r: r["request_id"], request_ids):
        try:
            status = current_app.work_queue.status(request_id)
        except RequestError as exc:
            response = build_request_response(request_id, "error",
                                              errno=exc.errno,
                                              message=exc.message)
        else:
            response = build_request_response(request_id, TASK_STATUS[status])

        stat_resps.append(response)

    return JsonResponse(stat_resps, 200)

class HandlerFlaskApp(Flask):
    """A subclass of Flask specialized for the handler app. It is mainly used
    to store additional attribute, such as `work_queue` or `deduplication_log`.
    """

    def __init__(self, work_queue, deduplication_log=None, *args, **kwargs):
        """Initialize the application with a given work queue, deduplication_log
        and Flask args and kwargs.

        The `work_queue` argument must implement the
        `handler.workqueue.WorkQueue` API and be thread safe.

        The `deduplication_log` argument must implement the
        `handler.deduplicationlog.DeduplicationLog` API or be None. If None, no
        deduplication is done.
        """
        super(HandlerFlaskApp, self).__init__(*args, **kwargs)
        self.work_queue = work_queue
        self.deduplication_log = deduplication_log

def get_app(work_queue, deduplication_log=None):
    """Build and return a Flask web application for the handler service.

    This service will use the given work_queue, which must implement the
    WorkQueue API, and the given deduplication_log, which must implement the
    DeduplicationLog API.
    If deduplication_log is None, no deduplication is done.
    """
    handler_app = HandlerFlaskApp(work_queue, deduplication_log, "grh_handler")
    handler_app.add_url_rule(
        '/requests', 'create', create_request, methods=['POST'],
    )
    handler_app.add_url_rule(
        '/requests/status', 'status', get_status, methods=['POST'],
    )

    backends_ctx.update(init(backend_list))

    return handler_app
