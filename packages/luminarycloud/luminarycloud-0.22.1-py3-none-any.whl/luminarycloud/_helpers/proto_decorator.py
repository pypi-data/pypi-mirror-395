# Copyright 2025 Luminary Cloud, Inc. All Rights Reserved.
from typing import (
    Generic,
    TypeVar,
    get_type_hints,
    get_origin,
)

from google.protobuf.message import Message

from luminarycloud.types import Vector3
from luminarycloud.types.adfloat import _to_ad_proto
from luminarycloud.types.vector3 import _to_vector3_ad_proto
from .._proto.base.base_pb2 import AdFloatType, AdVector3

P = TypeVar("P", bound=Message)
C = TypeVar("C")


class proto_decorator(Generic[P]):
    """
    A decorator that adds a `to_proto` method to a class.

    NOTE: only works for primitive and basepb.Vector3 fields right now.
    """

    proto_type: type[P]

    def __init__(decorator, proto_type: type[P]):
        decorator.proto_type = proto_type

    def __call__(decorator, cls: type[C]) -> type[C]:
        type_hints = get_type_hints(cls)
        fields = decorator.proto_type.DESCRIPTOR.fields

        def _to_proto(self: type[C]) -> P:
            proto = decorator.proto_type()
            for field in fields:
                _type = type_hints.get(field.name, None)
                if _type:
                    value = getattr(self, field.name)
                    proto_value = getattr(proto, field.name)
                    if issubclass(_type, float) and isinstance(proto_value, AdFloatType):
                        proto_value.CopyFrom(_to_ad_proto(value))
                    elif issubclass(_type, Vector3):
                        if isinstance(proto_value, AdVector3):
                            proto_value.CopyFrom(_to_vector3_ad_proto((value.x, value.y, value.z)))
                        else:
                            proto_value.x = value.x
                            proto_value.y = value.y
                            proto_value.z = value.z
                    else:
                        setattr(proto, field.name, value)
            return proto

        setattr(cls, "_to_proto", _to_proto)
        return cls
