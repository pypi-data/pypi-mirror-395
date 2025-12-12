#  Copyright (c) 2025 - 2025 DiffusionData Ltd., All Rights Reserved.
#
#  Use is subject to licence terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of DiffusionData. The intellectual and technical
#  concepts contained herein are proprietary to DiffusionData and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

import typing

import dataclasses

from diffusion.internal.serialisers.generic_model import GenericModel
from diffusion.internal.serialisers.dataclass_model import DataclassConfigMixin
from diffusion.internal.serialisers.generic_model_protocol import (
    CombinedMapping,
)
from diffusion.internal.validation import StrictStr
from diffusion.internal.validation.pydantic import SignedInt32


@dataclasses.dataclass(frozen=True)
class RemoveTopic(GenericModel):
    topic_selector: StrictStr

    class Config(DataclassConfigMixin["RemoveTopic"]):
        @classmethod
        def attr_mappings_combined(
            cls, modelcls
        ) -> typing.Mapping[str, CombinedMapping]:
            return {
                "remove-topics-request": CombinedMapping(
                    {"topic-selector": "topic_selector"}
                )
            }


@dataclasses.dataclass(frozen=True)
class Integer(GenericModel):
    content: SignedInt32

    class Config(DataclassConfigMixin["Integer"]):
        @classmethod
        def attr_mappings_combined(
            cls, modelcls
        ) -> typing.Mapping[str, CombinedMapping]:
            return {"integer": CombinedMapping({"integer": "content"})}


@dataclasses.dataclass(frozen=True)
class Unsubscribe(GenericModel):
    topic_selector: StrictStr

    class Config(DataclassConfigMixin["Unsubscribe"]):
        @classmethod
        def attr_mappings_combined(
            cls, modelcls
        ) -> typing.Mapping[str, CombinedMapping]:
            return {
                "string": CombinedMapping(
                    {"string": "topic_selector"}
                )
            }
