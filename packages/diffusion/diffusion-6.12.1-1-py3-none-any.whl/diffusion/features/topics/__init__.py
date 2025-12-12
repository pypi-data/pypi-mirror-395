#  Copyright (c) 2022 - 2025 DiffusionData Ltd., All Rights Reserved.
#
#  Use is subject to licence terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of DiffusionData. The intellectual and technical
#  concepts contained herein are proprietary to DiffusionData and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

""" Topics functionality. """
from __future__ import annotations

import traceback
from enum import IntEnum

import typing
from typing import Any, cast, TYPE_CHECKING

import attr
import diffusion.internal.utils
import structlog

import diffusion.datatypes as dt
from diffusion.features.topics.fetch.fetch_common import IVoidFetch
from diffusion.handlers import HandlerSet
from diffusion.internal.components import Component
from diffusion.features.topics.selectors import get_selector
from diffusion.internal.topics import spec_conv, Topic
from diffusion.internal.topics.constraints import UpdateConstraintType
from diffusion.features.topics.details.topic_specification import TopicSpecification
from diffusion.internal.serialisers.attrs import MarshalledModel
from diffusion.internal.utils import decode

if TYPE_CHECKING:  # pragma: no cover
    from diffusion.features.topics.fetch.fetch_request import FetchRequest
    from diffusion.session import Session
    from diffusion.datatypes import AbstractDataType
    from diffusion.datatypes import DataTypeArgument
    from diffusion.features.topics.update.constraints import Unconstrained
else:
    AbstractDataType = typing.ForwardRef("AbstractDataType")
    DataTypeArgument = typing.ForwardRef("DataTypeArgument")
    Session = typing.ForwardRef("Session")
from diffusion.features.topics.streams import ValueStreamHandler
from diffusion.features.topics.update import UpdateConstraint

LOG = structlog.get_logger()

T = typing.TypeVar("T", bound="AbstractDataType")

class UnsubscribeReason(IntEnum):
    """
    The reason that an unsubscription occurred.
    """

    REQUESTED = 0
    """
    Unsubscribed by the subscribing session.
    """
    CONTROL = 1
    """
    The unsubscription was requested either by another session
    or by the server.
    """
    REMOVAL = 2
    """
    The unsubscription occurred because the topic was removed.
    """
    AUTHORIZATION = 3
    """
    The unsubscription occurred because the session is
    no longer authorized to access the topic.
    """
    UNKNOWN_UNSUBSCRIBE_REASON = 4
    """
    A reason that is unsupported by the session.
    """
    BACK_PRESSURE = 5
    """
    The server has a significant backlog of messages for the session,
    and the topic specification has the conflation topic property set
    to "unsubscribe".
    """
    BRANCH_MAPPINGS = 6
    """
    The unsubscription occurred because branch mapping rules changed.
    """

    def __str__(self):
        return self.name

@attr.s(auto_attribs=True, slots=True)
class TopicRemovalResult:
    """Topic removal result

    Attributes:
         removed_count: number of topics removed
    """

    removed_count: int


class TopicAddResponse(IntEnum):
    """Possible server responses to TopicAdd service request."""

    CREATED = 0
    EXISTS = 1


def get_val(value, value_type_final: typing.Type[AbstractDataType]) -> AbstractDataType:
    value_final: AbstractDataType
    if not isinstance(value, value_type_final):
        value_final = value_type_final(value)  # type: ignore
    else:
        value_final = value  # type: ignore

    return value_final


def convert_constraints(
    constraints: typing.Optional[
        typing.Union[
            UpdateConstraint,
            int,
            typing.Tuple[typing.Union[int, UpdateConstraintType]],
        ]
    ],
    *args,
) -> UpdateConstraint:
    from .update.constraints import Unconstrained
    from diffusion.features.topics.update.constraint_factory import ConstraintFactory

    constraints = constraints or Unconstrained.Instance
    if isinstance(constraints, UpdateConstraint):
        return constraints
    elif isinstance(constraints, (UpdateConstraintType, int)):
        return ConstraintFactory().from_type(UpdateConstraintType(constraints), *args)
    elif isinstance(constraints, tuple):
        if len(constraints) == 1:
            return convert_constraints(constraints[0])
        else:
            return ConstraintFactory().from_type(
                UpdateConstraintType(constraints[0]),
                *decode(constraints[1:], collapse=True, skip_none=True),
            )
    elif isinstance(constraints, tuple) and len(constraints) == 1:
        return convert_constraints(constraints[0])
    else:
        raise ValueError(f"{constraints} not recognised")


@attr.s(auto_attribs=True, slots=True)
class TopicBase(MarshalledModel):
    topic_path: str = attr.ib(metadata={"alias": "topic-path"})
    specification: TopicSpecification = attr.ib(  # type: ignore
        converter=spec_conv,
    )

    @property
    def topic_type(self):
        return self.specification.topic_type.type_code

    @property
    def properties(self):
        return self.specification.properties_as_json()

    class Config(MarshalledModel.Config):
        @classmethod
        def attr_mappings_all(cls, modelcls):
            return {
                cls.alias: {
                    "protocol14-topic-specification.protocol14-topic-type": "topic_type",
                    "protocol14-topic-specification.topic-properties": "properties",
                }
            }


@attr.s(auto_attribs=True, slots=True)
class TopicBaseNum(MarshalledModel):
    topic_path: str = attr.ib(metadata={"alias": "topic-path"})

    specification: DataTypeArgument = attr.ib(
        converter=lambda x: dt.get(x).type_code,
        metadata={"alias": "protocol14-topic-type"},
    )


@attr.s(auto_attribs=True, slots=True)
class AddTopic(TopicBase):
    class Config(TopicBase.Config):
        alias = "protocol14-topic-add-request"


def unconstrained() -> Unconstrained:
    from diffusion.features.topics.update.constraints import Unconstrained

    return Unconstrained.Instance


@attr.s(auto_attribs=True, slots=True)
class SetTopic(TopicBaseNum):
    class Config(TopicBaseNum.Config):
        alias = "set-topic-request"

    value: typing.Union[bytes, AbstractDataType] = attr.ib(metadata={"alias": "bytes"})

    def __attrs_post_init__(self):
        if not isinstance(self.value, bytes):
            self.value = get_val(self.value, dt.get(self.specification)).to_bytes()

    update_constraint: typing.Optional[UpdateConstraint] = attr.ib(
        factory=unconstrained,
        converter=convert_constraints,
        metadata={"alias": "set-topic-request.update-constraint"},
    )


@attr.s(auto_attribs=True, slots=True)
class AddAndSetTopic(TopicBase):
    class Config(TopicBase.Config):
        alias = "add-and-set-topic-request"

    value: typing.Union[bytes, AbstractDataType] = attr.ib(metadata={"alias": "bytes"})

    def __attrs_post_init__(self):
        if not isinstance(self.value, bytes):
            self.value = get_val(self.value, dt.get(self.specification)).to_bytes()

    update_constraint: typing.Optional[UpdateConstraint] = attr.ib(
        factory=unconstrained,
        converter=convert_constraints,
        metadata={"alias": "update-constraint"},
    )


@attr.s(auto_attribs=True, slots=True)
class TopicAddResponseFull(MarshalledModel):
    class Config(MarshalledModel.Config):
        alias = "add-topic-result"

    value: TopicAddResponse = attr.ib(metadata={"alias": "add-topic-result"})


class Topics(Component):
    """Topics component.

    It is not supposed to be instantiated independently; an instance is available
    on each `Session` instance as `session.topics`.
    """

    CREATED = TopicAddResponse.CREATED
    EXISTS = TopicAddResponse.EXISTS

    def __init__(self, session: Session):
        from diffusion.features.topics.fetch.fetch_request import FetchRequest
        from diffusion.features.topics.fetch.fetch_common import IVoidFetch

        super().__init__(session)
        self.session.handlers[Topic] = HandlerSet()
        self.fetch_request_ = FetchRequest.create(
            session._internal,
            IVoidFetch,
            session.attributes.maximum_message_size,
        )

    @property
    def topics(self) -> dict:
        """Internal storage for registered topics."""
        return self.session.data[Topic]

    def fetch_request(self) -> FetchRequest[IVoidFetch]:
        """
        Gets an unconfigured fetch request.

        If the request is invoked by calling [FetchRequest.fetch][diffusion.features.topics.fetch.fetch_request.FetchRequest.fetch], the fetch result will
        provide the paths and types of all of the topics which the session has permission to read.

        You will usually want to restrict the query to a subset of the topic tree, and to retrieve the topic values
        and/or properties. This is achieved by applying one or more of the fluent builder methods to produce more
        refined requests.

        For example:

        ```pycon
        >>> result = asyncio.run(
        >>>    diffusion.sessions().open(DIFFUSION_URL).session.topics.
        >>>    fetch_request().with_values().fetch( "A/B//" )
        >>> )
        ```
        Returns: The unconfigured fetch request.
        See Also:
            [FetchRequest][diffusion.features.topics.fetch.fetch_request.FetchRequest]
        """  # noqa: E501, W291
        return self.fetch_request_

    async def add_topic(
        self,
        topic_path: str,
        specification: DataTypeArgument,
    ) -> TopicAddResponse:
        """Create a new topic of the given type and properties.

        Args:
            topic_path: The path to create the topic on.
            specification: Data type of the topic.
        """
        result = await self.services.TOPIC_ADD.invoke(
            self.session,
            AddTopic(
                topic_path=topic_path,
                specification=specification,
            ),
            TopicAddResponseFull,
        )
        return result.value

    async def add_and_set_topic(
        self,
        topic_path: str,
        specification: DataTypeArgument,
        value: Any,
        constraint: typing.Optional[UpdateConstraint] = None,
    ) -> TopicAddResponse:
        """Create a new topic of the given type and properties.

        Args:
            topic_path: The path to create the topic on.
            specification: Data type of the topic.
            value: Value to set when creating the topic. The value needs to
                   be compatible with the `topic_type`. If the topic already exists,
                   this will be set as its value.
            constraint: optional update constraint
        """
        return (
            await self.services.ADD_AND_SET_TOPIC.invoke(
                self.session,
                AddAndSetTopic(
                    topic_path=topic_path,
                    specification=specification,
                    value=value,
                    update_constraint=constraint,
                ),
                TopicAddResponseFull,
                strict_return=True,
            )
        ).value

    async def set_topic(
        self,
        topic_path: str,
        value: Any,
        specification: DataTypeArgument,
        constraint: typing.Optional[UpdateConstraint] = None,
    ) -> None:
        """
        Sets the topic to a specified value.

        `None` can only be passed to the `value` parameter
        when updating `STRING`, `INT64`, or `DOUBLE` topics.

        When a `STRING`, `INT64`, or `DOUBLE` topic is set to `None`, the
        topic will be updated to have no value. If a previous value was present
        subscribers will receive a notification that the new value is
        `None`. New subscribers will not receive a value notification.

        Args:
            topic_path: the path of the topic
            specification: Data type of the topic.
            value: the value. `STRING`, `INT64`, or `DOUBLE` topics accept
                `None`, as described above. Using `None` with
                other topic types is an error and will throw an
                `UnknownDataTypeError`.
            constraint: optional update constraint
        """

        await self.services.SET_TOPIC.invoke(
            self.session,
            SetTopic(
                specification=specification,
                topic_path=topic_path,
                value=value,
                update_constraint=constraint,
            ),
        )

    async def remove_topic(self, topic_selector: str) -> TopicRemovalResult:
        """Remove all the topics that match the given selector.

        Args:
            topic_selector: The topics matching this selector will be removed
                            from the server.

        Returns:
            An object detailing the results.
        """
        from diffusion.internal.serialisers.specific.topics import (
            RemoveTopic,
            Integer,
        )

        from diffusion.internal.validation import StrictStr

        result = await self.services.TOPIC_REMOVAL.invoke(
            self.session,
            request=RemoveTopic(typing.cast(StrictStr, topic_selector)),
            response_type=Integer,
        )
        return TopicRemovalResult(result.content)

    def add_value_stream(self, topic_selector: str, stream: ValueStreamHandler) -> None:
        """Registers a value stream handler for a topic selector.

        A value stream is a series of events associated with a registered topic. This
        method adds a
        [ValueStreamHandler][diffusion.features.topics.streams.ValueStreamHandler]
        which can handle those events.

        Args:
            topic_selector: The handler will react to the updates to all topics matching
                            this selector.
            stream: A handler for incoming events of the matching data type.
        """

        selector = get_selector(topic_selector)
        handler: HandlerSet = typing.cast(
            HandlerSet, self.session.handlers.get(selector)
        )
        if not handler:
            handler = HandlerSet()
            self.session.handlers[selector] = handler

        handler.add(stream)

    def add_fallback_stream(self, stream: ValueStreamHandler) -> None:
        """Registers a fallback stream handler for a topic type.

        A value stream is a series of events associated with a registered topic. This
        method makes it possible to register callbacks for each of those events.

        Args:
            stream: A handler for the matching data type.
        """
        cast(HandlerSet, self.session.handlers[Topic]).add(stream)

    async def subscribe(self, topic_selector: str):
        """Register the session to receive updates for the given topic.

        Args:
            topic_selector: The selector for topics to subscribe to.
        """
        service = self.services.SUBSCRIBE
        response = await service.invoke(
            self.session,
            service.request.evolve(topic_selector),
        )
        return response

    async def unsubscribe(self, topic_selector: str):
        """Unregister the session to stop receiving updates for the given topic.

        Args:
            topic_selector: The selector for topics to unsubscribe from.
        """
        from diffusion.internal.validation import StrictStr
        from diffusion.internal.serialisers.specific.topics import Unsubscribe

        return await self.services.UNSUBSCRIBE.invoke(
            self.session,
            request=Unsubscribe(typing.cast(StrictStr, topic_selector)),
        )

    @diffusion.internal.utils.validate_member_arguments
    async def remove_stream(self, stream: ValueStreamHandler):
        """
        Removes a stream.

        Notes:
            More formally, self method removes all streams that compare equal to the given stream, regardless of the
            topic selector for which they are registered. It will also remove any fallback stream equal to the given
            stream. If there are no such streams, no changes are made.

        Args:
            stream: The value stream to remove.
        """  # noqa: E501
        removed = set()
        for k, v in self.session.handlers.items():
            try:
                v.remove(stream)
                removed.add(stream)
            except KeyError:
                pass
        if removed:
            try:
                await stream.handle("close")
            except Exception as e:
                LOG.error(
                    f"Topic stream '{stream}' threw exception: {e}: {traceback.format_exc()}"
                )


