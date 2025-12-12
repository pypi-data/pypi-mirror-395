#  Copyright (c) 2025 - 2025 DiffusionData Ltd., All Rights Reserved.
#
#  Use is subject to licence terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of DiffusionData. The intellectual and technical
#  concepts contained herein are proprietary to DiffusionData and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

from __future__ import annotations

from typing import Optional

import typing

import dataclasses

from diffusion.features.control.metrics import TopicMetricCollector
from diffusion.internal.protocol.conversations import Conversation
from diffusion.internal.protocol.exceptions import ErrorReport, InvalidSessionFilterError
from diffusion.internal.serialisers.specific.exceptions import ErrorReportSerialiser
from diffusion.internal.serialisers.generic_model import GenericModel
from diffusion.internal.serialisers.dataclass_model import DataclassConfigMixin
from diffusion.internal.serialisers.generic_model_protocol import CombinedMapping
from diffusion.internal.serialisers.pydantic import MarshalledModel

if typing.TYPE_CHECKING:
    from diffusion.internal.serialisers.base import Serialiser
    from diffusion.internal.serialisers.generic_model import Model_Variants


@dataclasses.dataclass(frozen=True)
class PutResponse(GenericModel):
    content: typing.List[ErrorReportSerialiser] = dataclasses.field(default_factory=list)
    class Config(DataclassConfigMixin["PutResponse"]):
        @classmethod
        def attr_mappings_combined(cls, modelcls) -> typing.Mapping[str, CombinedMapping]:
            return {"error-report-list": CombinedMapping({"error-report-list": "content"})}

        @classmethod
        def decode(
        cls,
        item,
        modelcls: typing.Type[Model_Variants],
        model_key: str,
        serialiser: Optional[Serialiser] = None,
    ):
            serialiser = cls.check_serialiser(serialiser)
            return super().decode_complex(item, modelcls, model_key, serialiser)

        @classmethod
        async def respond_to_conversation(
            cls,
            item: PutResponse,
            conversation: typing.Optional[Conversation],
            serialiser: Serialiser,
        ) -> PutResponse:
            errors = [ErrorReport(**dataclasses.asdict(x)) for x in item.content]
            if not errors:
                return item
            raise InvalidSessionFilterError(errors)


class ListTopicMetricCollectors(MarshalledModel):
    entries: typing.List[TopicMetricCollector]

    class Config(MarshalledModel.Config):
        @classmethod
        def decode(
            cls,
            item,
            modelcls: typing.Type[Model_Variants],
            model_key: str,
            serialiser: typing.Optional[Serialiser] = None,
        ):
            serialiser = cls.check_serialiser(serialiser)
            return cls.decode_complex(item, modelcls, model_key, serialiser)

        @classmethod
        def attr_mappings_all(cls, modelcls):
            return {
                "protocol24-topic-metric-collectors": {
                    "protocol24-topic-metric-collectors": "entries"
                },
                "protocol25-topic-metric-collectors": {
                    "protocol25-topic-metric-collectors": "entries"
                },
            }

@dataclasses.dataclass(frozen=True)
class RemoveSessionMetricCollector(GenericModel):
    name: str
    class Config(DataclassConfigMixin["RemoveSessionMetricCollector"]):
        @classmethod
        def attr_mappings_combined(cls, modelcls) -> typing.Mapping[str, CombinedMapping]:
            return {"string": CombinedMapping({"string": "name"})}


@dataclasses.dataclass(frozen=True)
class RemoveTopicMetricCollector(GenericModel):
    name: str
    class Config(DataclassConfigMixin["RemoveTopicMetricCollector"]):
        @classmethod
        def attr_mappings_combined(cls, modelcls) -> typing.Mapping[str, CombinedMapping]:
            return {"string": CombinedMapping({"string": "name"})}
