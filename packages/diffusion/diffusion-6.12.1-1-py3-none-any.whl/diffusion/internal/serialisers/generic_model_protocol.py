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

import dataclasses

import typing_extensions

import typing_extensions as typing
from typing import Optional

if typing.TYPE_CHECKING:
    from diffusion.internal.serialisers import Serialiser
    from diffusion.internal.services import ServiceValue
    from diffusion.internal.protocol.conversations import Conversation
    from diffusion.internal.serialisers.generic_model import PreparedModelAndConversation



GenericModel_Args_T = typing.ParamSpec("GenericModel_Args_T")
GenericModelProtocol_T = typing.TypeVar("GenericModelProtocol_T", bound="GenericModelProtocol")

@typing.runtime_checkable
class ConversationFactory(typing.Protocol):
    def __call__(self) -> typing_extensions.Awaitable[Conversation]: ...

ModelMapping = typing.Mapping[str, str]
ConversationMapping = typing.Mapping[str, typing.Any]

@dataclasses.dataclass(frozen=True)
class CombinedMapping(object):
    message: ModelMapping = dataclasses.field(default_factory=dict)
    conversation: ConversationMapping = dataclasses.field(default_factory=dict)

    def __bool__(self):
        return any(getattr(self, field.name, None) for field in dataclasses.fields(self))

LegacyMapping = typing.Mapping[str, ModelMapping]
FullCombinedMapping = typing.Mapping[str, CombinedMapping]


@typing.runtime_checkable
class GenericModelProtocol(typing.Protocol[GenericModel_Args_T]):
    class Config(typing.Protocol[GenericModelProtocol_T]):
        @classmethod
        def from_service_value(
                cls,
                modelcls: typing.Type[GenericModelProtocol_T],
                item: ServiceValue,
        ) -> GenericModelProtocol_T:
            raise NotImplementedError()

        @classmethod
        def as_service_value(
                cls: typing.Type[GenericModelProtocol.Config[GenericModelProtocol_T]],
                item: GenericModelProtocol_T,
                serialiser: Optional[Serialiser] = None,
        ) -> ServiceValue:
            raise NotImplementedError()

        @classmethod
        def as_tuple(
                cls, item: GenericModelProtocol_T, serialiser: Optional[Serialiser] = None
        ) -> typing.Tuple[typing.Any, ...]:
            raise NotImplementedError()

        @classmethod
        def from_tuple(
                cls,
                modelcls: typing.Type[GenericModelProtocol_T],
                tp: typing.Tuple[typing.Any, ...],
                serialiser: Optional[Serialiser] = None,
        ) -> GenericModelProtocol_T:
            raise NotImplementedError()

        @classmethod
        async def prepare_conversation(
                cls, item: GenericModelProtocol_T, conversation_factory: ConversationFactory
        ) -> PreparedModelAndConversation[GenericModelProtocol_T]:
            raise NotImplementedError()

        @classmethod
        async def respond_to_conversation(
            cls,
            item: GenericModelProtocol_T,
            conversation: typing.Optional[Conversation],
            serializer: Serialiser,
        ) -> GenericModelProtocol_T:
            raise NotImplementedError()

    @classmethod
    def from_fields(
        cls: typing.Type[GenericModelProtocol[GenericModel_Args_T]],
        *args: GenericModel_Args_T.args,
        **kwargs: GenericModel_Args_T.kwargs
    ) -> GenericModelProtocol[GenericModel_Args_T]:
        ...
