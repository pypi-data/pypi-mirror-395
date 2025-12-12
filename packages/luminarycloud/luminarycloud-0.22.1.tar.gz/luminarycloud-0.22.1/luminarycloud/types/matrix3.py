# Copyright 2023-2024 Luminary Cloud, Inc. All Rights Reserved.
from dataclasses import dataclass, field

from .._proto.base import base_pb2 as basepb
from .vector3 import Vector3


@dataclass
class Matrix3:
    """Represents a 3x3 matrix."""

    a: Vector3 = field(default_factory=Vector3)
    b: Vector3 = field(default_factory=Vector3)
    c: Vector3 = field(default_factory=Vector3)

    def _to_proto(self) -> basepb.Matrix3:
        return basepb.Matrix3(
            a=basepb.Vector3(x=self.a.x, y=self.a.y, z=self.a.z),
            b=basepb.Vector3(x=self.b.x, y=self.b.y, z=self.b.z),
            c=basepb.Vector3(x=self.c.x, y=self.c.y, z=self.c.z),
        )

    def _to_ad_proto(self) -> basepb.AdMatrix3:
        return basepb.AdMatrix3(
            a=self.a._to_ad_proto(),
            b=self.b._to_ad_proto(),
            c=self.c._to_ad_proto(),
        )

    def _from_proto(self, proto: basepb.Matrix3) -> None:
        self.a = Vector3(x=proto.a.x, y=proto.a.y, z=proto.a.z)
        self.b = Vector3(x=proto.b.x, y=proto.b.y, z=proto.b.z)
        self.c = Vector3(x=proto.c.x, y=proto.c.y, z=proto.c.z)

    def _from_ad_proto(self, proto: basepb.AdMatrix3) -> None:
        self.a = Vector3.from_ad_proto(proto.a)
        self.b = Vector3.from_ad_proto(proto.b)
        self.c = Vector3.from_ad_proto(proto.c)
