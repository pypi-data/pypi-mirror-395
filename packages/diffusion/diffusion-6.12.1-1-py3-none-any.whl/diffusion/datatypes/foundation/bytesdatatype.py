#  Copyright (c) 2024 - 2025 DiffusionData Ltd., All Rights Reserved.
#
#  Use is subject to licence terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of DiffusionData. The intellectual and technical
#  concepts contained herein are proprietary to DiffusionData and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

from __future__ import annotations

import typing

from diffusion.datatypes.foundation.abstract import A_T
from diffusion.datatypes.foundation.ibytesdatatype import IBytes as IBytesParent


@typing.final
class Bytes(IBytesParent):
    """
    Represents a basic, bytes-only implementation of
    [IBytes][diffusion.datatypes.foundation.ibytesdatatype.IBytes]

    Effectively a lower bound on IBytes types.
    """

    type_name = "Bytes"

    @classmethod
    def encode(cls, value: typing.Any) -> bytes:
        return value

    @classmethod
    def decode(cls: typing.Type[A_T], data: bytes) -> typing.Any:
        return data
