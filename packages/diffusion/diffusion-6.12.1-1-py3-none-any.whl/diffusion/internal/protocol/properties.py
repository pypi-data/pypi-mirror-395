#  Copyright (c) 2020 - 2025 DiffusionData Ltd., All Rights Reserved.
#
#  Use is subject to licence terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of DiffusionData. The intellectual and technical
#  concepts contained herein are proprietary to DiffusionData and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

""" Session properties abstraction. """
from __future__ import annotations

import enum
import typing
import warnings
from itertools import chain
from typing import (
    AbstractSet,
    Optional,
    Tuple,
    Any,
    Callable,
    Dict,
    Iterable,
    Sequence,
    Union,
    Mapping,
)

import structlog

from diffusion.internal.utils import get_fnmap, CollectionEnum

LOG = structlog.get_logger()


@enum.unique
class Fixed(str, enum.Enum, metaclass=CollectionEnum):
    """ Constants for fixed session property names. """

    SESSION_ID = "$SessionId"
    PRINCIPAL = "$Principal"
    ROLES = "$Roles"
    CLIENT_TYPE = "$ClientType"
    TRANSPORT = "$Transport"
    SERVER_NAME = "$ServerName"
    CONNECTOR = "$Connector"
    COUNTRY = "$Country"
    LANGUAGE = "$Language"
    CLIENT_IP = "$ClientIP"
    LATITUDE = "$Latitude"
    LONGITUDE = "$Longitude"
    MQTT_CLIENT_ID = "$MQTTClientId"
    START_TIME = "$StartTime"
    GATEWAY_TYPE = "$GatewayType"
    GATEWAY_ID = "$GatewayId"
    ENVIRONMENT = "$Environment"

    @property
    def is_settable(self) -> bool:
        """ Check if a property is settable. """
        return self in {Fixed.COUNTRY, Fixed.LANGUAGE, Fixed.LATITUDE, Fixed.LONGITUDE}

    @property
    def is_authenticator_settable(self) -> bool:
        """ Check if a property is authenticator-settable. """
        return self.is_settable or self in {Fixed.PRINCIPAL, Fixed.ROLES}


class SessionProperties(Mapping):
    """The session properties for a client.

    This is an immutable object representing a full set of the property values.
    If a property value changes then a new object needs to be generated.

    Note that this class deliberately has no equals implementation as object
    equality is what is required when it is used in a search collection.
    """

    def __init__(self, *args, **kwargs):
        if len(args) > 1:
            raise TypeError(f"Expected at most 1 positional argument, got {len(args)}.")
        props = {}
        props.update(next(iter(args), {}))
        props.update(kwargs)
        self._props = Transform.all(props)

    def __eq__(self, other) -> bool:
        warnings.warn(
            "It is recommended to compare SessionProperties"
            " using identity (is) rather than equality (==)."
        )
        return self is other

    def items(self):
        """ Key-value pairs for all currently set properties. """
        return self._props.items()

    def keys(self):
        """ Names of all currently set properties. """
        return self._props.keys()

    def values(self):
        """ Values of all currently set properties. """
        return self._props.values()

    def __contains__(self, item):
        return item in self._props

    def __getitem__(self, item):
        return self._props[item]

    def __len__(self) -> int:
        return len(self._props)

    def __iter__(self):
        return iter(self._props.items())

    def __str__(self):
        return Transform.map_to_string(self)

    def put_all(self, properties: Mapping) -> SessionProperties:
        """Creates a new mapping by combining the two.

        This is essentially an update of the mapping, with any values present
        in the current mapping being updated the values from the new one,
        and any new values added.
        """
        mapping = dict(self)
        mapping.update(**properties)
        return type(self)(mapping)

    def update(self, properties: Mapping) -> SessionProperties:
        """Creates a new mapping by updating only fixed properties, and adding new ones.

        Caveat: This is different from standard Python `Mapping.update` behaviour.
        Any non-fixed properties not present in the current mapping not present in the
        new one will be removed.
        """
        mapping = {key: value for key, value in self.items() if key in Fixed}
        mapping.update(**properties)
        return type(self)(mapping)

    def diff(self, properties: Mapping) -> Mapping:
        """Prepares a mapping of proposed changes.

        Given a map of proposed session properties this compares to current
        properties and returns a map of changes. The returned map will contain
        entries for the fixed and user properties that have changed with their
        new values. Where there is a user property present in the current
        properties that is not present in the supplied map then the there will be
        an entry in the returned map with a value of `None`.
        """
        diff = dict.fromkeys(set(properties.keys()) - set(self.keys()))
        diff.update(
            {
                key: value
                for key, value in self.items()
                if (key in properties or key not in Fixed) and value != properties.get(key)
            }
        )
        return diff

    @classmethod
    def filter_user_defined(cls, properties: Mapping) -> Mapping:
        """ Removes any fixed properties from a mapping of session properties. """
        return {key: value for key, value in properties.items() if key not in Fixed}

    @classmethod
    def is_authenticator_settable(cls, key: str) -> bool:
        """ Check if a key is a valid name for an authenticator-settable property. """
        return cls.is_valid_session_property(key) and (
            not key.startswith("$") or key in Fixed and Fixed(key).is_authenticator_settable
        )

    @classmethod
    def is_settable(cls, key: str) -> bool:
        """ Check if a key is a valid name for a settable property. """
        return cls.is_valid_session_property(key) and (
            not key.startswith("$") or key in Fixed and Fixed(key).is_settable
        )

    @classmethod
    def is_valid_session_property(cls, key: str) -> bool:
        """Check if a key is a valid session property name."""
        if not bool(len(key.lstrip("$"))):
            return False
        try:
            Transform.validate(key, strict=key not in Fixed.__members__.values())
            return True
        except ValueError:
            return False


class Transform:
    """Internal collection of utility methods for transforming properties.

    Not mentioned to be instantiated, all methods are either class or static.
    """

    PRINTABLE_CHARS_ESCAPE_MAPPING = {
        k: r"\{}".format(k) for k in ('\\', '"', "'")
    }
    CONTROL_CHARS_ESCAPE_MAPPING = {
        "\t": "\\t",
        "\n": "\\n",
        "\r": "\\r",
    }

    ALL_ESCAPE_MAPPING = {
        **PRINTABLE_CHARS_ESCAPE_MAPPING,
        **CONTROL_CHARS_ESCAPE_MAPPING
    }

    DISALLOWED_CHARS = frozenset(" (),") | set(ALL_ESCAPE_MAPPING) - {"\\"}

    UNKNOWN_COORDINATE = "NaN"

    @classmethod
    def all(cls, properties: Mapping):
        """ Transforms all the properties and returns a new mapping. """
        return dict(filter(None, map(cls.transform, properties.items())))

    @classmethod
    def sanitize(cls, value: str):
        return cls.escape(value, cls.CONTROL_CHARS_ESCAPE_MAPPING)

    @classmethod
    def validate(cls, value: str, strict: bool = True):
        proscribed_charset = (
            cls.DISALLOWED_CHARS
            if strict
            else cls.CONTROL_CHARS_ESCAPE_MAPPING.keys()
        )
        if strict:
            value_to_check = value
        else:
            value_to_check = cls.sanitize(value)

        illegal_chars = {val for val in proscribed_charset if val in value_to_check}
        if illegal_chars:
            raise ValueError(f"{value!r} contains {illegal_chars=}")
        return True

    @classmethod
    def transform(cls, key_and_value: Tuple[str, Any]) -> Optional[Tuple[str, Any]]:
        """Given a key/value pair, transforms the value and returns both.

        If a value can't be transformed, returns None.
        """
        transformers: Dict[Union[Fixed, str], Callable[[str], str]] = {
            Fixed.COUNTRY: str.upper,
            Fixed.LANGUAGE: str.lower,
            Fixed.LATITUDE: cls.parse_coordinate,
            Fixed.LONGITUDE: cls.parse_coordinate,
            Fixed.ROLES: get_fnmap(cls.string_to_set, cls.set_to_string),
        }
        key, value = key_and_value
        value = str(value)
        try:
            value = transformers.get(key, str)(value)
        except Exception as ex:
            LOG.info("Unable to parse session property.", key=key, value=value, error=str(ex))
            return None

        return key, value

    @classmethod
    def string_to_list(cls, value: str) -> tuple:
        """ Converts a formatted multi value property to an immutable list. """
        return tuple(map(cls.unescape, map(cls.unquote, cls.split(value))))

    @classmethod
    def split(cls, value: str) -> Sequence:
        """Splits a string of quoted strings, regardless of actual separator.

        >>> Transform.split('"val1","val2","val3"')
        ['val1', 'val2', 'val3']
        >>> Transform.split('"val1" "val2" "val3"')
        ['val1', 'val2', 'val3']
        >>> Transform.split('"val1""val2""val3"')
        ['val1', 'val2', 'val3']
        >>> Transform.split('"val1";"val2","val3"')
        ['val1', 'val2', 'val3']
        >>> Transform.split("'val1''val2''val3'")
        ['val1', 'val2', 'val3']
        """
        seq = []
        subvalue = ""
        quote = None
        escaped = False
        for char in value:
            if not escaped and char in "'\"":
                if char == quote:
                    seq.append(subvalue)
                    subvalue = ""
                    quote = None
                else:
                    quote = char
                continue
            escaped = char == "\\"
            if quote is not None:
                subvalue += char
        return seq

    @classmethod
    def string_to_set(cls, value: str) -> frozenset:
        """ Converts a formatted multi value property to an immutable set. """
        return frozenset(cls.string_to_list(value))

    @classmethod
    def set_to_string(cls, value: AbstractSet) -> str:
        """ Converts a set of values to a canonicalised, escaped string. """
        return cls.list_to_string(sorted(value))

    @classmethod
    def list_to_string(cls, value: Iterable[str]) -> str:
        """ Converts a set of values to a canonicalised, escaped string. """
        value = list(value)
        if any(map(lambda k: k is None, value)):
            raise ValueError("Keys and values are not allowed to be null.")
        return ",".join(map(cls.quote, map(cls.escape, value)))

    @classmethod
    def unquote(cls, value: str) -> str:
        """ Removes any quotes from either end of a string. """
        return value.strip("\"'")

    @classmethod
    def quote(cls, value: str) -> str:
        """ Wraps a string into double quotes. """
        return value.join('""')

    @classmethod
    def escape(
        cls, value: str, mapping: typing.Optional[typing.Mapping[str, str]] = None
    ) -> str:
        """Inserts escape characters into a string."""
        for old, new in (mapping or cls.ALL_ESCAPE_MAPPING).items():
            value = value.replace(old, new)
        return value

    @classmethod
    def unescape(
        cls, value: str, mapping: typing.Optional[typing.Mapping[str, str]] = None
    ) -> str:
        """Removes escape characters from a string."""
        for new, old in reversed(
            list((mapping or cls.ALL_ESCAPE_MAPPING).items())
        ):
            value = value.replace(old, new)
        return value

    @classmethod
    def parse_coordinate(cls, value: str) -> str:
        """ Converts a coordinate value into a float and back into string. """
        try:
            result = str(float(value))
        except ValueError:
            result = cls.UNKNOWN_COORDINATE
        return result

    @classmethod
    def string_to_map(cls, value: str) -> Mapping:
        """ Decode a string encoded using `map_to_string` into a map. """
        as_list = cls.string_to_list(value)
        return dict(zip(as_list[::2], as_list[1::2]))

    @classmethod
    def map_to_string(cls, value: Mapping) -> str:
        """Encode a string map into a single string.

        Each key and value are escaped and quoted. The string
        representation is that of a JSON object but can be
        decoded using `string_to_map`.
        """
        return cls.list_to_string(chain.from_iterable(value.items()))
