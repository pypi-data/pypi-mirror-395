# Copyright 2023-2025 Luminary Cloud, Inc. All Rights Reserved.
from google.protobuf import empty_pb2

from ._proto.api.v0.luminarycloud.feature_flag import feature_flag_pb2
from ._client import get_default_client


def _get_feature_flags() -> dict[int, str]:
    """Get enabled feature flags for the authenticated user.

    Feature flags are used to control access to experimental and internal features.
    Each flag is identified by an experiment ID and a feature flag name.

    Returns
    -------
    dict[int, str]
        A dictionary mapping experiment IDs (uint64) to feature flag names.
        Returns an empty dictionary if no feature flags are enabled for the user.
    """
    req = empty_pb2.Empty()
    res = get_default_client().GetFeatureFlags(req)
    return dict(res.enabled_feature_flags)
