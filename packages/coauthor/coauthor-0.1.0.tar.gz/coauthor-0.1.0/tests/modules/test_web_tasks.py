import requests
import pytest
from unittest import mock, TestCase
import re
from coauthor.modules.web_tasks import check_redirection, replace_redirecting_links


def test_check_redirection_redirect():
    url = "https://oreil.ly/gKq4m"
    expected_location = "https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/"
    with mock.patch("requests.get") as mock_get:
        mock_response = mock.Mock()
        mock_response.status_code = 301
        mock_response.headers = {"Location": expected_location}
        mock_get.return_value = mock_response

        success, location = check_redirection(url)
        assert success is True
        assert location == expected_location


def test_check_redirection_no_redirect():
    url = "https://c2platform.org/"
    with mock.patch("requests.get") as mock_get:
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_get.return_value = mock_response

        success, location = check_redirection(url)
        assert success is False
        assert location == url


def test_check_redirection_exception():
    url = "https://invalid-url"
    with mock.patch("requests.get", side_effect=requests.RequestException("Error occurred")) as mock_get:
        with pytest.raises(Exception) as excinfo:
            check_redirection(url)
        assert "An error occurred: Error occurred" in str(excinfo.value)


def test_check_redirection_real_redirect():
    url = "https://httpbin.org/absolute-redirect/1"
    expected_location = "http://httpbin.org/get"

    success, location = check_redirection(url)
    assert success is True
    assert location == expected_location

    url = "https://httpbin.org/absolute-redirect/2"
    expected_location = "http://httpbin.org/absolute-redirect/1"

    success, location = check_redirection(url)
    assert success is True
    assert location == expected_location


def test_check_redirection_real_no_redirect():
    url = "https://httpbin.org/get"

    success, location = check_redirection(url)
    assert success is False
    assert location == url


def test_check_redirection_real_redirect_oreilly():
    url = "https://oreil.ly/gKq4m"
    expected_location = "https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/"

    success, location = check_redirection(url)
    assert success is True
    assert location == expected_location


def test_replace_redirecting_links_no_match():
    config_mock = {"current-task": {"path-modify-event": "test_path", "regex": r"(https?://[^\s]+)"}}
    logger_mock = mock.Mock()
    mock_open = mock.mock_open(read_data="No links here")

    with mock.patch("builtins.open", mock_open):
        result = replace_redirecting_links(config_mock, logger_mock)

    assert result is False
    logger_mock.debug.assert_any_call("No redirect links found")


def test_replace_redirecting_links_found_and_replaced():
    config_mock = {"current-task": {"path-modify-event": "test_path", "regex": r"(https?://[^\s]+)"}}
    logger_mock = mock.Mock()
    mock_open = mock.mock_open(read_data="Check this link: http://example.com/old")

    with mock.patch("builtins.open", mock_open):
        with mock.patch("coauthor.modules.web_tasks.check_redirection", return_value=(True, "http://example.com/new")):
            with mock.patch("time.sleep", return_value=None):
                result = replace_redirecting_links(config_mock, logger_mock)

    assert result is True
    mock_open().write.assert_called_with("Check this link: http://example.com/new")
    logger_mock.info.assert_any_call("Updated link http://example.com/old → http://example.com/new")


def test_replace_redirecting_links_found_not_replaced():
    config_mock = {"current-task": {"path-modify-event": "test_path", "regex": r"(https?://[^\s]+)"}}
    logger_mock = mock.Mock()
    mock_open = mock.mock_open(read_data="Check this link: http://example.com/same")

    with mock.patch("builtins.open", mock_open):
        with mock.patch(
            "coauthor.modules.web_tasks.check_redirection", return_value=(False, "http://example.com/same")
        ):
            result = replace_redirecting_links(config_mock, logger_mock)

    assert result is False
    logger_mock.debug.assert_any_call("Content is up to date. No links redirected")
