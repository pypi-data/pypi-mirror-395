# Copyright 2023 Luminary Cloud, Inc. All Rights Reserved.

import grpc

from .._auth import Auth0Client


class AuthenticationPlugin(grpc.AuthMetadataPlugin):
    """
    Adds authentication headers for each outgoing RPC.

    Supports two authentication methods:
    1. Bearer token authentication using Auth0
    2. API key authentication using x-api-key header

    The __call__ function is invoked for every outgoing call. If using Bearer token
    and the token has expired or doesn't exist, the Auth0 client tries to acquire
    a new one.
    """

    def __init__(self, auth0_client: Auth0Client, api_key: str | None = None):
        super(AuthenticationPlugin, self).__init__()
        self.auth0_client = auth0_client
        self.api_key = api_key

    def __call__(
        self,
        context: grpc.AuthMetadataContext,
        # Takes the list of headers to add as tuples
        callback: grpc.AuthMetadataPluginCallback,
    ) -> None:
        try:
            if self.api_key and isinstance(self.api_key, str):
                metadata = [("x-api-key", self.api_key)]
            else:
                access_token = self.auth0_client.fetch_access_token()
                metadata = [("authorization", "Bearer " + access_token)]
            callback(metadata, None)
        except Exception as err:
            callback(None, err)


class AuthInterceptor(
    grpc.UnaryUnaryClientInterceptor,
    grpc.UnaryStreamClientInterceptor,
    grpc.StreamUnaryClientInterceptor,
    grpc.StreamStreamClientInterceptor,
):
    """
    I need this as a workaround for container-to-host connections because I need to create a channel
    that uses CallCredentials but doesn't use any ChannelCredentials. I.e. I need to authenticate
    the requests, but I need the connection to be unencrypted. This is because the grpc server on
    the native host isn't using SSL, so I can't use grpc.ssl_channel_credentials(), but it's also
    not reachable on a loopback interface, so I can't use grpc.local_channel_credentials() either.
    So I need to use a grpc.insecure_channel(), but you can't use CallCredentials with an insecure
    channel. So the workaround is to use an interceptor instead of CallCredentials.

    Also, I don't care about auth0, so I'm only supporting an API key.
    """

    def __init__(self, api_key: str):
        self._api_key = api_key

    def _augment(self, metadata):
        return metadata + [("x-api-key", self._api_key)]

    def intercept_unary_unary(self, continuation, client_call_details, request):
        new_details = client_call_details._replace(
            metadata=self._augment(client_call_details.metadata or [])
        )
        return continuation(new_details, request)

    def intercept_unary_stream(self, continuation, client_call_details, request):
        new_details = client_call_details._replace(
            metadata=self._augment(client_call_details.metadata or [])
        )
        return continuation(new_details, request)

    def intercept_stream_unary(self, continuation, client_call_details, request_iter):
        new_details = client_call_details._replace(
            metadata=self._augment(client_call_details.metadata or [])
        )
        return continuation(new_details, request_iter)

    def intercept_stream_stream(self, continuation, client_call_details, request_iter):
        new_details = client_call_details._replace(
            metadata=self._augment(client_call_details.metadata or [])
        )
        return continuation(new_details, request_iter)
