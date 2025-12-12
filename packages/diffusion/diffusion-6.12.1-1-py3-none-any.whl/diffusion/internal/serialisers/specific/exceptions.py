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

import abc
import dataclasses

import typing

from diffusion.internal.exceptions import DiffusionError
from diffusion.internal.protocol.conversations import Conversation
from diffusion.internal.serialisers.dataclass_model import DataclassConfigMixin
from diffusion.internal.serialisers.generic_model import GenericModel

if typing.TYPE_CHECKING:
    from diffusion.internal.serialisers import Serialiser

DiffusionError_T = typing.TypeVar(
    "DiffusionError_T", bound=DiffusionError
)


@dataclasses.dataclass(frozen=True)
class ErrorReportSerialiser(GenericModel):
    message: str
    line: int
    column: int

    class Config(
        typing.Generic[DiffusionError_T],
        DataclassConfigMixin["ErrorReportSerialiser"],
    ):
        @classmethod
        def attr_mappings_all(cls, modelcls):
            return {
                "error-report": {
                    "error-message": "message",
                    "error-line": "line",
                    "error-column": "column",
                }
            }


        @classmethod
        async def respond_to_conversation(
            cls,
            item: ErrorReportSerialiser,
            conversation: typing.Optional[Conversation],
            serialiser: Serialiser,
        ) -> ErrorReportSerialiser:
            if conversation:
                await conversation.discard(item.message)

            raise await cls.exception_to_raise(item)

        exception_type: typing.Type[DiffusionError_T]

        @classmethod
        @abc.abstractmethod
        async def exception_to_raise(
            cls, item: ErrorReportSerialiser
        ) -> DiffusionError_T: ...
