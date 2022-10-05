"""Tests for the RedisDeduplicationLog (needs a ready redis backend)"""
from json import dumps, loads
from time import sleep
from unittest import TestCase

from handler.deduplicationlog.redis import RedisDeduplicationLog
from handler.rest import get_app, DEFAULT_ETA_MS
from dummy_queue import DummyQueue

DEDUP_SLOT_MS=500
REDIS_DEDUP_BACKEND="redis://localhost"

class RedisDeduplicationLogTest(TestCase):
    """Test the RedisDeduplicationLog"""

    def setUp(self):
        """Create the test HTTP client"""
        self.app = get_app(
            DummyQueue(),
            RedisDeduplicationLog(DEDUP_SLOT_MS, REDIS_DEDUP_BACKEND),
        )
        self.app.testing = True
        self.client = self.app.test_client()

    def post_json(self, route, data):
        """Encode a dict into json and post it to a given self.app endpoint"""
        json_body = dumps(data)
        return self.client.post(
            route, content_type="application/json", data=json_body
        )

    def check_successful_requests_response(self, requests, nb_requests):
        self.assertEqual(len(requests), nb_requests)
        for rq in requests:
            self.assertIn("request_id", rq)
            self.assertEqual(rq["status"], "running")
            self.assertEqual(rq["eta"], DEFAULT_ETA_MS)
            self.assertIsNone(rq["errno"])
            self.assertIsNone(rq["message"])

    def test_dedup_two_consecutive_similar_requests(self):
        request_1 = [
            {"file_id": "file", "action": "put", "backend": "empty"},
        ]
        request_2 = request_1
        resp_1 = self.post_json('/requests', request_1)
        resp_2 = self.post_json('/requests', request_2)
        # check requests are successfull
        for resp in (resp_1, resp_2):
            self.assertEqual(resp_1.status_code, 201)

        rqs_1 = loads(resp_1.data)
        rqs_2 = loads(resp_2.data)
        self.check_successful_requests_response(rqs_1, 1)
        self.check_successful_requests_response(rqs_2, 1)
        # check that the dedup returns the same taskid
        self.assertEqual(rqs_1[0]["request_id"], rqs_2[0]["request_id"])

    def test_dedup_two_distant_similar_requests(self):
        request_1 = [
            {"file_id": "file_bis", "action": "put", "backend": "empty"},
        ]
        request_2 = request_1
        resp_1 = self.post_json('/requests', request_1)
        sleep(0.001 * DEDUP_SLOT_MS + 1)
        resp_2 = self.post_json('/requests', request_2)
        # check requests are successfull
        for resp in (resp_1, resp_2):
            self.assertEqual(resp_1.status_code, 201)

        rqs_1 = loads(resp_1.data)
        rqs_2 = loads(resp_2.data)
        self.check_successful_requests_response(rqs_1, 1)
        self.check_successful_requests_response(rqs_2, 1)
        # check that the dedup returns two different taskids
        self.assertNotEqual(rqs_1[0]["request_id"],
                            rqs_2[0]["request_id"])
