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

from diffusion.internal.hashable_dict import TransparentHashableDict
from diffusion.internal.serialisers.generic_model import (
    GenericConfig,
    GenericModel,
)
from diffusion.internal.utils import _KT, _VT_co, validate_member_arguments


class ImmutableMapping(
    typing.Generic[_KT, _VT_co],
    TransparentHashableDict[_KT, _VT_co],
    GenericModel,
):

    @classmethod
    def __class_getitem__(
        cls, item: typing.Tuple[_KT, _VT_co]
    ) -> typing.Type[ImmutableMapping[_KT, _VT_co]]:
        return typing.cast("typing.Type[ImmutableMapping[_KT, _VT_co]]", cls)

    @validate_member_arguments
    def __init__(
        self, innerdict: typing.Optional[typing.Dict[_KT, _VT_co]] = None
    ):
        super().__init__(innerdict or {})

    class Config(GenericConfig["ImmutableMapping"]):
        @classmethod
        def attr_mappings_all(cls, modelcls):
            return {"fetch-topic-properties": {"topic-properties": "_value"}}
