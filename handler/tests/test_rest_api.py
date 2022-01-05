"""Tests for the REST API."""
import unittest
from unittest.mock import Mock, call, patch
from importlib import reload
from os import environ

from flask import json

from dummy_queue import DummyQueue
from handler import rest
from handler.workqueue import (TASK_ST_RUNNING, TASK_ST_COMPLETED,
                               RequestError)

class RestApiTest(unittest.TestCase):
    """Test the REST API for requests."""

    def setUp(self):
        """Create the test HTTP client"""
        self.wqueue = DummyQueue()
        self.app = rest.get_app(self.wqueue)
        self.app.testing = True
        self.client = self.app.test_client()

    def post_json(self, route, data):
        """Encode a dict into json and post it to a given self.app endpoint"""
        json_body = json.dumps(data)
        return self.client.post(
            route, content_type="application/json", data=json_body
        )

    def assert_http_status_code(self, response, expected_response_code):
        """Assert that a response has the expected status code"""
        self.assertEqual(response.status_code, expected_response_code)

    def check_response(self, response, id, status, errno=None, message=None):
        expected_response = {
            "request_id": id,
            "status": status,
            "eta": rest.DEFAULT_ETA_MS,
            "errno": errno,
            "message": message
        }
        self.assertEqual(response, expected_response)

    def test_create_success_if_empty(self):
        """Test /requests for a valid empty request"""
        empty_rq = []
        resp = self.post_json('/requests', empty_rq)
        self.assertEqual(resp.status_code, 304)

    def test_create_success(self):
        """Test /requests for a valid request"""
        valid_rqs = [
            {"file_id": "foo1", "action": "put", "backend": "blob"},
            {"file_id": "foo2", "action": "get", "backend": "blob"},
            {"file_id": "foo3", "action": "delete", "backend": "blob"},
        ]
        resp = self.post_json('/requests', valid_rqs)
        self.assertEqual(resp.status_code, 201)
        rq_resps = json.loads(resp.data)

        # Check rq_resps fits :
        # [
        #     {"request_id": "XXXX", "status": "running",
        #      "errno": None, "message": None},
        #     {"request_id": "XXXX", "status": "running",
        #      "errno": None, "message": None},
        # ]
        self.assertEqual(len(rq_resps), 3)
        for r in rq_resps:
            self.assertIn("request_id", r)
            self.assertEqual(r["status"], "running")
            self.assertEqual(r["eta"], rest.DEFAULT_ETA_MS)
            self.assertIsNone(r["errno"])
            self.assertIsNone(r["message"])

    def test_create_bad_mime(self):
        """Test /requests when the mime type is not application/json."""
        good_body = [{"file_id": "foo", "action": "put", "backend": "blob"}]
        self.assert_http_status_code(
            self.client.post('/requests', data=json.dumps(good_body)),
            400,
        )

    def test_create_bad_json(self):
        """Test /requests when the content of the json is invalid."""
        self.assert_http_status_code(
            self.client.post(
                '/requests',
                data="not json!",
                content_type="application/json",
            ),
            400,
        )

    def test_create_bad_content(self):
        """Test /requests when the content of the json is invalid."""
        bad_bodies = [
            # Not a list
            {},
            # Not a list
            {"file_id": "foo", "action": "put", "backend": "blob"},
            # Missing file_id
            [{"action": "put", "backend": "blob"}],
            # Missing action
            [{"file_id": "foo", "backend": "blob"}],
            # Missing backend
            [{"file_id": "foo", "action": "put"}],
            # Bad hint
            [{"file_id": "foo", "action": "blob", "backend": "blob"}],
        ]

        for body in bad_bodies:
            self.assert_http_status_code(self.post_json('/requests', body),
                                         400)

    def test_status_success_if_empty(self):
        """Test /requests for a valid empty request"""
        empty_status = []
        resp = self.post_json('/requests/status', empty_status)
        self.assertEqual(resp.status_code, 200)
        status_resp = json.loads(resp.data)
        self.assertEqual(status_resp, [])

    def test_status_success(self):
        """Test /requests/status with a valid request."""
        # Test every possible request status kind by mocking the dummy queue
        statuses = (TASK_ST_RUNNING,
                    TASK_ST_COMPLETED,
                    RequestError(16, "test"))
        self.wqueue.status = Mock(side_effect=statuses)

        valid_status_request = [
            {"request_id": "0"},
            {"request_id": "1"},
            {"request_id": "2"},
        ]
        resp = self.post_json('/requests/status', valid_status_request)
        self.assert_http_status_code(resp, 200)
        resp = json.loads(resp.data)

        # check status call args
        self.assertEqual(
            self.wqueue.status.call_args_list,
            [call("0"), call("1"), call("2")]
        )

        # check response
        self.assertEqual(len(resp), 3)
        self.check_response(resp[0], "0", "running")
        self.check_response(resp[1], "1", "completed")
        self.check_response(resp[2], "2", "error", 16, "test")

    def test_status_bad_mime(self):
        """Test /requests/status when the mime type is not application/json."""
        good_body = [{"request_id": "GATTACA"}]
        self.assert_http_status_code(
            self.client.post('/requests/status', data=json.dumps(good_body)),
            400,
        )

    def test_status_bad_json(self):
        """Test /requestsi/status when the content of the json is invalid."""
        self.assert_http_status_code(
            self.client.post(
                '/requests/status',
                data="not json!",
                content_type="application/json",
            ),
            400,
        )

    def test_status_bad_content(self):
        """Test /requests/status when the content of the json is invalid."""
        bad_bodies = [
            # Not a list
            {},
            # Not a list
            {"request_id": "GATTACA", "file_id": "bar_fid", "backend": "blob"},
            # Missing request_id
            [{"not_request_id": "WHYNOTGATTACA"}],
        ]

        for body in bad_bodies:
            self.assert_http_status_code(
                self.post_json('/requests/status', body),
                400,
            )

    def test_default_eta(self):
        """Test rest.DEFAULT_ETA_MS without GRH_DEFAULT_ETA_MS from environment"""
        try:
            with patch.dict(environ):
                # Be sure GRH_DEFAULT_ETA_MS is not set
                environ.pop("GRH_DEFAULT_ETA_MS", None)
                reload(rest)
                self.assertEqual(rest.DEFAULT_ETA_MS,
                                 rest.DEFAULT_ETA_MS_PRESET)
        finally:
            reload(rest)

    def test_default_eta_from_env(self):
        """Test rest.DEFAULT_ETA_MS is set by GRH_DEFAULT_ETA_MS"""
        try:
            with patch.dict(environ, {"GRH_DEFAULT_ETA_MS": "27"}):
                reload(rest)
                self.assertEqual(rest.DEFAULT_ETA_MS, 27)
        finally:
            reload(rest)
