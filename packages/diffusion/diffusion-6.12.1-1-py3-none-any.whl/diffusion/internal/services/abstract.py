#  Copyright (c) 2020 - 2025 DiffusionData Ltd., All Rights Reserved.
#
#  Use is subject to licence terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of DiffusionData. The intellectual and technical
#  concepts contained herein are proprietary to DiffusionData and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

""" Module for abstract service definition. """

from __future__ import annotations

import typing_extensions

import copy
import inspect
import io
import typing
from abc import ABC, abstractmethod
from typing import (
    KeysView,
    Iterable,
    Mapping,
    Optional,
    Type,
    TYPE_CHECKING,
    Union,
    ValuesView,
    Any,
)

import structlog

from diffusion.datatypes.foundation.datatype import DataType

from diffusion.internal.utils import get_all_subclasses
from .exceptions import UnknownServiceError
# noinspection DuplicatedCode
from ..serialisers.generic_model import GenericModel, GenericModel_T
from ..serialisers.generic_model_protocol import ConversationFactory
from ..serialisers.spec_elements import (
    NULL_VALUE_KEY,
)

if TYPE_CHECKING:  # pragma: no cover
    from diffusion.internal.session import InternalSession
    from diffusion.internal.protocol.message_types import (
        ServiceMessage,
    )
    from diffusion.internal.serialisers.base import (
        Serialiser,
        SerialiserMap,
    )
    from diffusion.datatypes.foundation.abstract import (
        AbstractDataType,
    )


LOG = structlog.get_logger()

Service_T = typing.TypeVar("Service_T", bound="Service")


class Service(ABC):
    """Abstract service definition class."""

    __slots__ = (
        "request",
        "response",
        "message_type",
        "_outgoing_message_type",
        "error_serializer",
    )
    service_id: typing.ClassVar[int] = 0
    name: typing.ClassVar[str] = ""
    request_serialiser: typing.ClassVar[Serialiser]
    response_serialiser: typing.ClassVar[Serialiser]
    error_serializer: Serialiser
    request: ServiceValue
    response: ServiceValue
    message_type: Optional[Type[ServiceMessage]]
    _outgoing_message_type: Optional[Type[ServiceMessage]]

    def __init__(
        self,
        incoming_message_type: Optional[
            Type[ServiceMessage]
        ] = None,
    ):
        from ..serialisers import get_serialiser
        self.request = ServiceValue(self.request_serialiser)
        self.response = ServiceValue(
            self.response_serialiser
        )
        self.message_type = incoming_message_type
        self.error_serializer = get_serialiser("error-reason-outgoing")
        self._outgoing_message_type = None

    @property
    def outgoing_message_type(self):
        from diffusion.internal.protocol.message_types import (
            ServiceResponseMessage,
        )
        return self._outgoing_message_type or ServiceResponseMessage

    @outgoing_message_type.setter
    def outgoing_message_type(self, value):
        self._outgoing_message_type = value

    def __repr__(self) -> str:
        return f"{self.name}[{self.service_id}]"

    @abstractmethod
    async def consume(
        self: Service_T,
        stream: io.BytesIO,
        session: InternalSession,
    ) -> Service_T:
        """Consume an inbound message."""

    @abstractmethod
    async def produce(
        self, stream: io.BytesIO, session: InternalSession
    ) -> None:
        """Send an outbound message."""

    @classmethod
    def get_by_id(cls, service_id: int) -> Type[Service]:
        """ Locate and return a service class based on the service ID. """
        for subclass in get_all_subclasses(cls):
            if subclass.service_id == service_id:
                return subclass
        raise UnknownServiceError("Unknown service ID %s", service_id)

    @classmethod
    def get_by_name(cls, service_name: str) -> Type[Service]:
        """ Locate and return a service class based on the service name. """
        for subclass in get_all_subclasses(cls):
            if subclass.name == service_name:
                return subclass
        raise UnknownServiceError("Unknown service name '%s'", service_name)

    async def respond(self, session: InternalSession) -> None:
        """Send a response to a request.

        It is only needed for inbound messages, but is implemented
        here for the sake of type-checking. Does nothing by default.
        """
        ...  # pragma: no cover

    EvolveValue = typing.Union[GenericModel, "ServiceValue"]

    @typing_extensions.overload
    async def invoke(
            self,
            session: InternalSession,
            request: typing.Optional[typing.Union[ServiceValue, GenericModel]],
            response_type: None,
            conversation_factory: typing.Optional[ConversationFactory]
    ) -> ServiceValue: ...

    @typing_extensions.overload
    async def invoke(
            self,
            session: InternalSession,
            request: typing.Optional[typing.Union[ServiceValue, GenericModel]],
            response_type: typing.Type[GenericModel_T],
            conversation_factory: typing.Optional[ConversationFactory],
            strict_return: typing.Literal[False]
    ) -> typing.Optional[GenericModel_T]: ...

    @typing_extensions.overload
    async def invoke(
            self,
            session: InternalSession,
            request: typing.Optional[typing.Union[ServiceValue, GenericModel]],
            response_type: typing.Type[GenericModel_T],
            conversation_factory: typing.Optional[ConversationFactory],
            strict_return: typing.Literal[True]
    ) -> GenericModel_T: ...

    async def invoke(
        self,
        session: InternalSession,
        request: typing.Optional[typing.Union[ServiceValue, GenericModel]] = None,
        response_type: typing.Optional[typing.Type[GenericModel_T]] = None,
        conversation_factory: typing.Optional[ConversationFactory] = None,
        strict_return: bool = False
    ) -> typing.Union[ServiceValue, typing.Optional[GenericModel_T]]:
        item = self.evolve()
        if isinstance(request, GenericModel):
            async def get_conversation():
                mapping = request.Config.attr_mappings_final(
                    type(request), self.request_serialiser
                )

                result = await session.conversations.new_conversation(item)
                result.data.update(
                    {
                        k: getattr(request, str(v), v)
                        for k, v in mapping.conversation.items()
                    }
                )
                return result

            prep_result = await request.Config.prepare_conversation(
                request, conversation_factory or get_conversation
            )
            item.request = prep_result.model.Config.as_service_value(
                prep_result.model, self.request_serialiser
            )
            conversation = prep_result.conversation
        else:
            conversation = None
            if request:
                item.request = request

        sr_options = dict(conversation=conversation) if conversation else {}
        # noinspection PyProtectedMember
        response = await session._send_request(item, **sr_options)
        if (
            not response
            or self.response_serialiser.name
            == NULL_VALUE_KEY
        ):
            return response
        if not response_type:
            response_type = typing.cast(
                typing.Type[GenericModel_T],
                self.response_serialiser
            )

        if response_type:
            if inspect.isclass(response_type) and issubclass(
                response_type, GenericModel
            ):
                response_type_real = typing.cast(
                    "typing.Type[GenericModel_T]",
                    response_type,
                )
                result = response_type_real.Config.from_service_value(
                    response_type_real, response
                )
                result = await result.Config.respond_to_conversation(
                    result, conversation, item.response_serialiser
                )
                if strict_return:
                    if not isinstance(result, response_type_real):
                        raise ValueError(f"Got empty {response=} from {request=}")
                return result
        return response

    def __eq__(self, other):
        return self is other or (
            type(self) is type(other)
            and vars(self) == vars(other)
        )

    def evolve(
        self: Service_T,
        *,
        request: typing.Optional[EvolveValue] = None,
        response: typing.Optional[EvolveValue] = None,
    ) -> Service_T:
        try:
            item = copy.copy(self)
        except Exception as e:  # pragma: no cover
            LOG.error(f"Got exception {e}")
            raise
        if request:
            if isinstance(request, GenericModel):
                item.request = request.Config.as_service_value(
                    request, serialiser=self.request_serialiser
                )
            else:
                item.request = request
        if response:
            if isinstance(response, GenericModel):
                item.response = response.Config.as_service_value(
                    response, serialiser=self.response_serialiser
                )
            else:
                item.response = response
        return item

    @classmethod
    def __get_validators__(cls: typing.Type[Service]):
        def validate(val) -> Service:
            if isinstance(val, Service):
                return val
            raise TypeError(f"{val} is not a {cls}")
        yield validate


OutboundService_T = typing.TypeVar(
    "OutboundService_T", bound="OutboundService"
)


class OutboundService(Service):
    """Abstract class for client-to-server services."""

    def _write_request(self, stream: io.BytesIO) -> None:
        """Write the value of the request attribute to the stream."""
        self.request_serialiser.write(
            stream, *self.request.values()
        )

    def _read_response(
        self: OutboundService_T, stream: io.BytesIO
    ) -> OutboundService_T:
        """Read the value of the response attribute from the stream."""
        self.response = self.response.evolve(
            *self.response_serialiser.read(stream)
        )
        return self.evolve(response=self.response)

    async def consume(
        self: OutboundService_T,
        stream: io.BytesIO,
        session: InternalSession,
    ) -> OutboundService_T:
        """Receive the response from the server."""
        return self._read_response(stream)

    async def produce(
        self, stream: io.BytesIO, session: InternalSession
    ) -> None:
        """Send the request to the server."""
        self._write_request(stream)


InboundService_T = typing.TypeVar(
    "InboundService_T", bound="InboundService"
)


class InboundService(Service):
    """Abstract class for server-to-client services."""

    def _read_request(
        self: Service_T, stream: io.BytesIO
    ) -> Service_T:
        """Read the value of the request attribute from the stream."""
        result = self.request_serialiser.read(stream)
        try:
            self.request = self.request.evolve(*result)
            evolved = self.evolve(
                request=self.request.evolve(*result)
            )
            return evolved
        except Exception as e:  # pragma: no cover
            LOG.error(f"Got exception {e}")
            raise

    def _write_response(self, stream: io.BytesIO) -> None:
        """ Write the value of the response attribute to the stream. """
        self.response.write(stream)


    async def consume(
        self: InboundService_T,
        stream: io.BytesIO,
        session: InternalSession,
    ) -> InboundService_T:
        """Receive the request from the server."""
        return self._read_request(stream)

    async def produce(
        self, stream: io.BytesIO, session: InternalSession
    ) -> None:
        """Send the response to the server."""
        self._write_response(stream)


class ServiceValue(Mapping[Union[str, int], Any], Iterable):
    """Container for values of Service.request and Service.response fields.

    The exact contents are defined by the associated serialiser. The object
    behaves as both a mapping and an iterator: both the keys and the order
    of values are defined by the accompanying serialiser.
    """

    __slots__ = ["_serialiser", "_values"]

    def __init__(self, serialiser: Serialiser):
        self._serialiser = serialiser
        self._values = dict.fromkeys(serialiser.fields)

    def set(self, *args, **kwargs):
        """Sets the values from the passed arguments.

        Any keyword arguments will override any positional arguments. For
        example, if the first value is named `foo`, then
        `value.set(123, foo=456)` will set `foo` to 456 and not 123.
        """
        values = self.merge_args_kwargs(args, kwargs)
        for field, value in values.items():
            self[field] = value

    def merge_args_kwargs(self, args, kwargs):
        values = dict(zip(self._values, args))
        values.update(kwargs)
        return values

    def keys(self) -> KeysView:
        """Returns an iterable of all field names."""
        return self._values.keys()

    def values(self) -> ValuesView:
        """Returns an iterable of all values."""
        return self._values.values()

    def __len__(self) -> int:
        return len(self._values)

    def __iter__(self):
        return iter(self._values.keys())

    def __getitem__(self, item: Union[str, int]):
        if isinstance(item, int):
            return list(self.values())[item]
        return self._values[self._check_item_key(item)]

    def __setitem__(self, item: Union[str, int], value):
        from diffusion import datatypes as dt
        if isinstance(item, int):
            item = list(self.keys())[item]
        if isinstance(value, dt.DataType):
            self.serialised_value = value
        else:
            self._values[self._check_item_key(item)] = value

    def sanitize_key(self, key):
        item_key = key
        if item_key not in self._values:
            item_key = f"{self._serialiser.name}.{key}"
        if item_key not in self._values:
            return None
        return item_key

    def _check_item_key(self, key):
        """Check if an item key omits the serialiser name.

        Serialiser map keys include the serialiser name to ensure uniqueness.
        This allows the convenience of omitting the serialiser name when
        setting or getting an item, so instead of:

            value["messaging-client-forward-send-request.conversation-id"]

        one can use only:

            value["conversation-id"]
        """
        item_key = self.sanitize_key(key)
        if not item_key:
            raise KeyError(f"Unknown field '{item_key}'")
        return item_key

    def __contains__(self, item):
        return item in self._values

    def __repr__(self):
        return (
            f"{type(self).__name__}(serialiser={self._serialiser.name},"
            f" values={tuple(self._values.values())})"
        )

    @property
    def spec(self) -> SerialiserMap:
        """ Returns the serialiser's spec mapping. """
        return self._serialiser.spec

    @property
    def serialised_value(self) -> Optional[DataType]:
        """Retrieves the value of any serialised DataType field in the value.

        Raises a TypeError if there are no any such fields, or if there
        are more than one.
        """
        from diffusion import datatypes as dt
        serialised_fields = self._get_serialised_value_fields()
        data_type_name, bytes_value = serialised_fields.values()
        if bytes_value is None:
            return None
        return dt.get(data_type_name).from_bytes(bytes_value)

    @serialised_value.setter
    def serialised_value(self, value: AbstractDataType):
        """Sets the value of any serialised DataType field in the value.

        Raises a TypeError if there are no any such fields, or if there
        are more than one.
        """
        serialised_fields = self._get_serialised_value_fields()
        for key, value in zip(serialised_fields, value.serialised_value.values()):
            self[key] = value

    def _get_serialised_value_fields(self):
        serialised_fields = [field for field in self.spec if "serialised-value" in field]
        length = len(serialised_fields)
        if length > 2:
            raise TypeError(
                f"The '{self._serialiser.name}' serialiser has multiple serialised values."
            )
        if length < 2:
            raise TypeError(
                f"The '{self._serialiser.name}' serialiser does not have a serialised value."
            )
        return {field: self[field] for field in serialised_fields}

    def evolve(
        self: ServiceValue, *args, **kwargs
    ) -> ServiceValue:
        """Evolves the values from the passed arguments.

        Any keyword arguments will override any positional arguments. For
        example, if the first value is named `foo`, then
        `value.evolve(123, foo=456)` will set `foo` to 456 and not 123.
        """
        result = ServiceValue(self._serialiser)
        result._values = {**self._values}
        result.set(*args, **kwargs)
        return result

    def write(self, stream: io.BytesIO) -> None:
        self._serialiser.write(stream, *self.values())

