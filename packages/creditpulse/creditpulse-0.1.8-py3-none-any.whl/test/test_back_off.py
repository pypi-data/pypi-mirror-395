from creditpulse.requests.request_manager import RequestManager, RequestActionManager

import unittest
import requests


class SimpleCheck(RequestActionManager):

    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.success_called = False
        self.error_called = False

    def on_execute(self) -> requests.Response:
        return requests.get(self.endpoint)

    def success_callback(self, response: requests.Response) -> None:
        self.success_called = True

    def error_callback(self, response: requests.Response) -> None:
        self.error_called = True

    def is_request_successful(self, response: requests.Response) -> bool:
        return response.status_code in [200, 201]


class TestRequestManager(unittest.TestCase):

    def test_request_success(self):
        check = SimpleCheck(endpoint='https://httpbin.org/get')
        manager = RequestManager(
            manager=check,
            max_retries=1
        )

        manager.start()

        self.assertTrue(check.success_called, "Success callback was not called")

    def test_request_error(self):
        self.error_callback_code = 200
        self.retries = 3
        check = SimpleCheck(endpoint='https://httpbin.org/status/500')

        manager = RequestManager(
            manager=check,
            max_retries=self.retries,
        )

        manager.start()
        self.assertTrue(check.error_called, "Success callback was not called")
        self.assertEqual(manager.retry_count, self.retries)


if __name__ == '__main__':
    unittest.main()
