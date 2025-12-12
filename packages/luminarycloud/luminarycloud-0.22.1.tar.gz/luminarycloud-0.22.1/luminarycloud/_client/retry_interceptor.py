# Copyright 2023-2025 Luminary Cloud, Inc. All Rights Reserved.
from collections.abc import Callable
from time import sleep
from typing import Any
import logging

import grpc
from grpc import (
    ClientCallDetails,
    UnaryUnaryClientInterceptor,
)
from grpc_status.rpc_status import GRPC_DETAILS_METADATA_KEY

from luminarycloud.exceptions import AuthenticationError
from luminarycloud._proto.base import base_pb2


def _is_rate_limited(call: grpc.Call) -> bool:
    """
    Check if a gRPC call failed due to rate limiting.

    Rate limit errors are identified with the SUBCODE_RATE_LIMITED subcode and UNAVAILABLE status.

    Args:
        call: The gRPC call to check

    Returns:
        True if the error is a rate limit error, False otherwise
    """
    if call.code() != grpc.StatusCode.UNAVAILABLE:
        return False

    try:
        # Get the trailing metadata which contains error details
        # Metadata is a sequence of tuples (key, value)
        for key, value in call.trailing_metadata() or []:
            if key != GRPC_DETAILS_METADATA_KEY or not isinstance(value, bytes):
                continue

            status = base_pb2.Status()
            status.ParseFromString(value)
            for any_detail in status.details:
                if any_detail.Is(base_pb2.StatusPayload.DESCRIPTOR):
                    payload = base_pb2.StatusPayload()
                    any_detail.Unpack(payload)
                    if payload.subcode == base_pb2.SUBCODE_RATE_LIMITED:
                        return True
    except Exception:
        pass
    return False


logger = logging.getLogger(__name__)


class RetryInterceptor(UnaryUnaryClientInterceptor):
    def __init__(self, log_retries: bool = False):
        self.log_retries = log_retries
        super().__init__()

    """
    A retry interceptor that retries on rate limit errors and other retryable errors.

    This interceptor handles:
    1. Rate limit errors (UNAVAILABLE with SUBCODE_RATE_LIMITED) - always retried
    2. [grpc.StatusCode.RESOURCE_EXHAUSTED, grpc.StatusCode.UNAVAILABLE] - retried

    This is required because, while the retry policy for the gRPC client is configurable via
    https://github.com/grpc/grpc-proto/blob/master/grpc/service_config/service_config.proto,
    the initial backoff is selected randomly between 0 and the configured value (also the
    number of attempts is capped at 5). We currently have a fixed-window rate-limiting system,
    and there's no way to guarantee that a retry will be attempted outside the current window
    using the service config.

    Note: the default retry policy is to retry on UNAVAILABLE (i.e. transient unavailability),
    which is why that status is not being handled here.

    Another note: although AFAIK not documented explicitly, each call made by this interceptor is
    subject to the retry policy of the underlying channel. (Glancing at the source, interceptors
    just call the underlying channel, and the service config is passed to the underlying channel,
    e.g. grpc.secure_channel.) So each "inner" retry handles transient failures while the "outer"
    calls handled by this interceptor handles failures due to rate-limiting.
    """

    def intercept_unary_unary(
        self,
        continuation: Callable[[ClientCallDetails, Any], grpc.Call],
        client_call_details: ClientCallDetails,
        request: Any,
    ) -> grpc.Call:
        retryable_codes = [grpc.StatusCode.RESOURCE_EXHAUSTED, grpc.StatusCode.UNAVAILABLE]
        n_max_retries = 20
        max_retry_seconds = 20
        backoffs = [min(i * 2, max_retry_seconds) for i in range(1, n_max_retries)]
        backoff_index = 0
        while True:
            if backoff_index >= len(backoffs):
                break
            call = continuation(client_call_details, request)
            if call.code() not in retryable_codes:
                break
            if call.code() == grpc.StatusCode.UNAVAILABLE:
                # if the auth plugin errors, that unfortunately shows up here as UNAVAILABLE, so we
                # have to check for auth plugin exceptions that shouldn't be retried by matching
                # their name in the details string
                details = call.details() or ""
                if "InteractiveAuthException" in details:
                    break
            backoff = backoffs[backoff_index]
            if self.log_retries:
                logger.info(
                    f"Retrying {client_call_details.method} in {backoff} seconds (last response: {call.code()}, {call.details()})"
                )
            sleep(backoff)
            # Keep retrying rate-limited calls while increasing the backoff up to the max.
            backoff_index += 1
            if _is_rate_limited(call):
                backoff_index = max(min(backoff_index, len(backoffs) - 2), 0)

        try:
            call.result()
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.UNAUTHENTICATED:
                raise AuthenticationError(e.details(), e.code()) from None
            raise
        return call
