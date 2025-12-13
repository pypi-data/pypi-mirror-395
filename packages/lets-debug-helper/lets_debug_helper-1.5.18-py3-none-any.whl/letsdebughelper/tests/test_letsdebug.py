#!/usr/bin/env python3
import json
import unittest
from typing import Any, Dict, Optional
from unittest.mock import Mock, patch

from requests import Response

from letsdebughelper import letsdebug


class TestLetsdebug(unittest.TestCase):

    def setUp(self) -> None:
        self.url = "https://letsdebug.net"
        self.domain = "jeffistotallyawesome.space"
        self.test_id = 359646
        self.post_data: Dict[str, str] = {"method": "http-01", "domain": self.domain}
        self.bad_post_data: Dict[str, str] = {"metho": "http=01", "domain": self.domain}
        self.test_id_url: str = f"{self.url}/{self.domain}/{self.test_id}"
        self.get_bad_result: str = "Invalid request parameters.\n"
        self.post_result_text: str = '{"Domain":"jeffistotallyawesome.space","ID":359640}\n'
        self.post_bad_result: str = "Please provide a valid domain name and validation method.\n"

        self.get_result_dict: Dict[str, Any] = dict(
            id=self.test_id,
            domain=self.domain,
            method="http-01",
            status="Complete",
            created_at="2020-11-16T20:39:19.970198Z",
            started_at="2020-11-16T20:39:19.973775Z",
            completed_at="2020-11-16T20:39:22.855617Z",
            result=dict(problems=[
                dict(
                    name="CloudflareCDN",
                    explanation=(f"The domain {self.domain} is being served through Cloudflare CDN. "
                                 "Any Let's Encrypt certificate installed on the origin server will only encrypt "
                                 "traffic between the server and Cloudflare. It is strongly recommended that the SSL "
                                 "option 'Full SSL (strict)' be enabled."),
                    detail=("https://support.cloudflare.com/hc/en-us/articles/"
                            "200170416-What-do-the-SSL-options-mean-"),
                    severity="Warning",
                ),
            ], ),
        )
        self.get_result_text: str = json.dumps(self.get_result_dict)

    def _mock_response(
        self,
        status: int = 200,
        text: Optional[str] = None,
        json_data: Optional[str] = None,
        raise_for_status: Optional[bool] = None,
    ) -> Mock:
        mock_resp = Mock()
        # mock raise_for_status call w/optional error
        mock_resp.raise_for_status = Mock()
        if raise_for_status:
            mock_resp.raise_for_status.side_effect = raise_for_status
        # set status code and content
        mock_resp.status_code = status
        # add json data if provided
        mock_resp.json = Mock(return_value=json_data)
        mock_resp.text = text
        return mock_resp

    @patch("requests.get")
    def test_le_get_call(self, mock_get: Mock) -> None:
        mock_resp: Mock = self._mock_response(text=self.get_result_text)
        mock_get.return_value = mock_resp
        result: Response = letsdebug.le_get_call(check_url=self.test_id_url)
        self.assertEqual(result.text, self.get_result_text)

    @patch("requests.get")
    def test_fail_le_get_call(self, mock_get: Mock) -> None:
        mock_resp: Mock = self._mock_response(status=400, text=self.get_bad_result)
        mock_get.return_value = mock_resp
        result: Response = letsdebug.le_get_call(check_url=self.test_id_url)
        self.assertEqual(result.text, self.get_bad_result)

    @patch("requests.post")
    def test_le_post_call(self, mock_post: Mock) -> None:
        mock_resp: Mock = self._mock_response(text=self.post_result_text)
        mock_post.return_value = mock_resp
        result: Response = letsdebug.le_post_call(post_data=self.post_data)
        self.assertEqual(result.text, self.post_result_text)

    @patch("requests.post")
    def test_fail_le_post_call(self, mock_post: Mock) -> None:
        mock_resp: Mock = self._mock_response(status=400, text=self.post_bad_result)
        mock_post.return_value = mock_resp
        result: Response = letsdebug.le_post_call(post_data=self.bad_post_data)
        self.assertEqual(result.text, self.post_bad_result)

    @patch("requests.get")
    def test_success_decode_result(self, mock_get: Mock) -> None:
        mock_resp: Mock = self._mock_response(json_data=json.loads(self.get_result_text))
        mock_get.return_value = mock_resp
        result: Response = letsdebug.le_get_call(check_url=self.test_id_url)
        actual: Dict[str, Any] = letsdebug.decode_result(result=result)
        self.assertEqual(actual, self.get_result_dict)

    @patch("requests.get")
    def test_fail_decode_result(self, mock_get: Mock) -> None:
        mock_resp: Mock = self._mock_response(text="Bad Data")
        mock_get.return_value = mock_resp
        actual: Dict[str, Any] = letsdebug.decode_result(result=mock_get.return_value)
        self.assertIsNone(actual)

    @patch("requests.get")
    def test_success_check_status(self, mock_get: Mock) -> None:
        mock_resp: Mock = self._mock_response(text=self.get_result_text)
        mock_get.return_value = mock_resp
        result: Response = letsdebug.le_get_call(check_url=self.test_id_url)
        actual: None = letsdebug.check_status(result=result, result_json=self.get_bad_result)  # type: ignore
        self.assertIsNone(actual)

    @patch("builtins.print")
    @patch("requests.get")
    def test_fail_check_status(self, mock_print: Mock, mock_get: Mock) -> None:
        mock_resp = self._mock_response(status=400, text=self.get_bad_result)
        mock_get.return_value = mock_resp
        result = letsdebug.le_get_call(check_url=self.test_id_url)
        with self.assertRaises(SystemExit):
            letsdebug.check_status(result=result, result_json=self.get_bad_result)  # type: ignore
