# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-H76
# Copyright IBM Corp. 2025
# The source code for this program is not published or other-wise divested of its trade
# secrets, irrespective of what has been deposited with the U.S. Copyright Office.
# ----------------------------------------------------------------------------------------------------

from http import HTTPStatus

from aiohttp import ClientConnectionError, ServerDisconnectedError
from aiohttp_retry import ExponentialRetry, RetryClient


class RestAsyncUtil:

    RETRY_COUNT = 6
    START_TIMEOUT = 0.5
    BACK_OFF_FACTOR = 0.5
    RETRY_AFTER_STATUS_CODES = (
        HTTPStatus.BAD_GATEWAY,
        HTTPStatus.SERVICE_UNAVAILABLE,
        HTTPStatus.GATEWAY_TIMEOUT,
    )

    @classmethod
    def get_retry_client(cls) -> RetryClient:
        retry_options = ExponentialRetry(
            cls.RETRY_COUNT,
            statuses=cls.RETRY_AFTER_STATUS_CODES,
            exceptions={ServerDisconnectedError, ClientConnectionError},
            start_timeout=cls.START_TIMEOUT,
        )
        retry_client = RetryClient(retry_options=retry_options)

        return retry_client
