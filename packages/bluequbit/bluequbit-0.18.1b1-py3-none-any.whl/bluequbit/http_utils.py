import logging
import time

import requests

from .exceptions import BQAPIError, BQUnauthorizedAccessError

logger = logging.getLogger("bluequbit-python-sdk")

DEFAULT_TIMEOUT = (15.0, 300.0)
NUMBER_OF_RETRIES = 5


def exponential_backoff(retry_num, backoff_factor=1.0):
    return backoff_factor * (2**retry_num - 1)


def request_retriable(method, url, **kwargs):
    retry_num = 0
    resp = requests.Response()

    def _send():
        nonlocal retry_num
        nonlocal method
        nonlocal kwargs
        nonlocal resp
        if retry_num > 0:
            time.sleep(exponential_backoff(retry_num - 1))
        retry_num += 1
        try:
            resp = requests.request(method, url, timeout=DEFAULT_TIMEOUT, **kwargs)
            if resp.ok:
                return resp
            logger.debug(
                f"HTTP request from BlueQubit SDK error. Request {method} {url}. Response {resp.status_code} {resp.text}"
            )
            if retry_num <= NUMBER_OF_RETRIES and resp.status_code in [
                429,
                502,
                503,
                504,
            ]:
                logger.warning(
                    "Retrying. Num retries: %s. HTTP status code: %s.",
                    retry_num,
                    resp.status_code,
                )
                return _send()
            if resp.status_code == 401:
                raise BQUnauthorizedAccessError(
                    kwargs.get("headers", {}).get("X-Request-ID", "")
                )
            resp.raise_for_status()
        except requests.ConnectTimeout as e:
            if retry_num <= NUMBER_OF_RETRIES:
                logger.warning(
                    "Retrying. Num retries %s. ConnectTimeout: %s", retry_num, e
                )
                return _send()
            raise
        except requests.RequestException as e:
            if retry_num <= NUMBER_OF_RETRIES and method in [
                "HEAD",
                "GET",
                "PUT",
                "DELETE",
                "OPTIONS",
                "TRACE",
            ]:
                logger.warning(
                    "Retrying. Num retries %s. RequestException: %s.", retry_num, e
                )
                return _send()
            raise

    try:
        return _send()
    except Exception as e:
        if isinstance(e, BQUnauthorizedAccessError):
            raise
        raise BQAPIError(
            resp.status_code,
            resp.text,
            kwargs.get("headers", {}).get("X-Request-ID", ""),
        ) from e
