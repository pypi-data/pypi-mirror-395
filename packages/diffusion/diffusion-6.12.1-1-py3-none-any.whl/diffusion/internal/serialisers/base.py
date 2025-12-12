#  Copyright (c) 2020 - 2025 DiffusionData Ltd., All Rights Reserved.
#
#  Use is subject to licence terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of DiffusionData. The intellectual and technical
#  concepts contained herein are proprietary to DiffusionData and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

""" Base classes for implementation of serialisers. """

from __future__ import annotations

import functools
import inspect
import io
import itertools
import os
import textwrap
import traceback
import typing
import typing_extensions
from typing import Any, cast, Iterable, Mapping, MutableMapping, Sequence

import structlog
from stringcase import pascalcase, snakecase  # type: ignore[import-untyped]
from typing_extensions import runtime_checkable, Protocol

from diffusion.internal.encoded_data import Byte, EncodingType, is_encoder, Int32
from diffusion.internal.utils import flatten_mapping, get_base_type_parameters
from diffusion.internal.hashable_dict import HashableDict, HashableElement
from .compound import (
    GenericMapSerialiser,
    GenericScalarSetSerialiser,
    KeyValue,
)
if typing.TYPE_CHECKING:
    from .generic_model import GenericModel_T, GenericModel, Model_Variants
    from .generic_model_protocol import GenericModelProtocol
from .spec_elements import (
    SerialiserMap,
    NULL_VALUE_KEY,
    Compound,
    CompoundSpec,
    SerialiserMapValue,
    MutableSerialiserMap,
)
from .spec import SERIALISER_SPECS
from diffusion.internal.encoded_data.abstract import (
    Enc_MetaType_Str,
    Enc_MetaType,
    EncodingProtocol,
    EncodingTypeConcreteVar,
    EncodingTypeOrProtocolVar, StrictHashable,
)
from diffusion.internal.encoded_data.exceptions import StreamExhausted

LOG = structlog.get_logger()

ID_Type = typing.TypeVar("ID_Type", bound=int, covariant=True)


def log(x: str):
    stack_length = len(inspect.stack(0)) - 30
    to_log = textwrap.indent(x, "    " * stack_length)
    if os.getenv("DEBUG_RESOLVER"):
        LOG.debug(to_log)


@runtime_checkable
class ChoiceProvider(Protocol[ID_Type]):
    @classmethod
    def id(cls) -> ID_Type:
        raise NotImplementedError()


class Serialiser:
    """Class for individual serialisers."""

    spec: SerialiserMap
    resolver: Resolver

    def __init__(
        self, name: str, spec: SerialiserMap, resolver: typing.Optional[Resolver] = None
    ):
        self.name = name
        self.spec = spec
        self.resolver = resolver or resolve

    def from_bytes(self, value: bytes):
        """Deserialise a bytes value."""
        yield from self.read(io.BytesIO(value))

    def read(self, stream: io.BytesIO):
        """Read the value from a binary stream."""
        yield from self._recurse_read(self.spec.values(), stream)

    def _recurse_read(self, types, stream):
        types = tuple(flatten_mapping(types))
        for item in types:
            if is_encoder(item):
                try:
                    result = item.read(stream).value
                    yield result
                except StreamExhausted:
                    break
            elif item is not None:
                yield tuple(self._recurse_read(item, stream))
            else:
                yield None

    def to_bytes(self, *values) -> bytes:
        """Serialise the value into bytes."""
        return self._recurse_write(self.spec.values(), values, self.spec.keys())

    def write(self, stream: io.BytesIO, *values) -> io.BytesIO:
        """Write the value into a binary stream."""
        stream.write(self.to_bytes(*values))
        return stream

    def _recurse_write(self, types, values, keys):
        result = b""
        types = tuple(flatten_mapping(types))
        for item, value, key in itertools.zip_longest(types, values, keys, fillvalue=None):
            if is_encoder(item):
                try:
                    result += item(value).to_bytes()
                except Exception as e:
                    LOG.error(
                        f"{key=}: {item=} {value=} failed with {e}: {traceback.format_exc()}"
                    )
                    raise
            elif item is not None and isinstance(value, Iterable):
                result += self._recurse_write(item, value, key)
        return result

    def __iter__(self):
        return iter(self.spec.items())

    @property
    def fields(self):
        """Returns a list of all the field names."""
        return list(self.spec)

    def __repr__(self):
        return f"<{type(self).__name__} name={self.name}>"

    @classmethod
    @functools.lru_cache(maxsize=None)
    def by_name(
        cls, name: str = NULL_VALUE_KEY, resolver: typing.Optional[Resolver] = None
    ) -> Serialiser:
        """Retrieve a serialiser instance based on the spec name."""
        resolver = resolver or resolve
        return Serialiser(name, resolver(name), resolver=resolver)

    def __bool__(self):
        return self.name != NULL_VALUE_KEY


    @functools.lru_cache(maxsize=None)
    def get_choice_encoder_from_list(self) -> typing.Type[ChoiceEncoder]:
        list_encoder = self.to_encoder(ListEncoder)
        return ChoiceEncoder.extract_from(list_encoder.serialiser)

    def get_encoder(
        self, *cls: typing.Type[EncodingTypeConcreteVar]
    ) -> typing.Optional[typing.Type[EncodingTypeConcreteVar]]:
        if not len(self.spec.values()) == 1:
            return None
        encoder_candidate = next(iter(self.spec.values()))

        if inspect.isclass(encoder_candidate) and issubclass(
            encoder_candidate, typing.cast(typing.Tuple[type, ...], cls)
        ):
            return typing.cast(typing.Type[EncodingTypeConcreteVar], encoder_candidate)
        return None

    def to_encoder(
        self, cls: typing.Type[EncodingTypeConcreteVar]
    ) -> typing.Type[EncodingTypeConcreteVar]:
        result = self.get_encoder(cls)
        assert result
        return result


class ChoiceEncoder(EncodingType[SerialiserMap, typing.Tuple]):
    """Special "encoding type" for choice-based values (i.e. `one-of')."""

    serialisers: Mapping[int, Serialiser]
    serialiser_names: Mapping[typing.Hashable, str]
    resolver: Resolver

    @classmethod
    def get_serialiser_names(cls) -> typing.Mapping[typing.Hashable, str]:
        return cls.serialiser_names

    def __init__(self, value: Sequence):
        assert isinstance(value, Sequence) and len(value) > 0
        super().__init__(tuple(value))

    @classmethod
    def read(cls, stream: io.BytesIO) -> typing_extensions.Self:
        """Read the encoded value from a binary stream.

        It converts the read value to the correct type and constructs a new
        instance of the encoding type.
        """
        choice = Byte.read(stream).value
        try:
            serialiser = cls.serialisers[choice]
        except Exception as e:  # pragma: no cover
            LOG.error(f"Got exception {e}")
            raise
        values: tuple = tuple(*cast(Iterable, serialiser.read(stream)))
        LOG.debug("Read choice values.", serialiser=serialiser, choice=choice, values=values)
        return cls((choice, *values))

    def to_bytes(self) -> bytes:
        """Convert the value into its bytes representation."""
        result = Byte(self.choice).to_bytes()
        result += self.serialiser.to_bytes(self.values)
        return result

    @property
    def choice(self):
        """Return the current value of the choice."""
        return self.value[0]

    @property
    def values(self):
        """Return the current collection of values."""
        return self.value[1:]

    @property
    def serialiser(self):
        """Return the serialises spec for the current choice."""
        return self.serialisers[self.choice]

    @classmethod
    def from_name(
        cls, serialiser_name: str, resolver: typing.Optional[Resolver] = None
    ) -> typing.Type[ChoiceEncoder]:
        """Instantiate the class by resolving the serialiser name."""
        resolver = resolver or resolve
        return resolver.resolve_generic(
            ChoiceEncoder, resolver(serialiser_name), serialiser_name
        )

    @classmethod
    def get_serialiser_by_id(cls, id: int, resolver: typing.Optional[Resolver] = None):
        serialiser_name = cls.serialiser_names.get(id)
        assert serialiser_name is not None
        return Serialiser.by_name(serialiser_name, resolver=resolver)

    @classmethod
    def get_serialiser_by_provider(
        cls, provider: typing.Union[ChoiceProvider, typing.Type[ChoiceProvider]]
    ):
        assert isinstance(provider, ChoiceProvider) or (
            inspect.isclass(provider)
            and issubclass(
                typing.cast(typing.Type[ChoiceProvider], provider), ChoiceProvider
            )
        )
        return cls.get_serialiser_by_id(provider.id(), resolver=cls.resolver)

    @classmethod
    def as_tuple(cls, item: GenericModelProtocol):
        return (
            item.Config.as_tuple(
                item,
                cls.get_serialiser_by_provider(typing.cast(ChoiceProvider, item.Config)),
            )
            if item is not None
            else ()
        )

    @classmethod
    def create(
        cls,
        spec: SerialiserMap,
        name: str,
        parents: typing.Optional[typing.Tuple[str, ...]] = None,
        resolver: typing.Optional[Resolver] = None,
    ) -> typing.Type[typing_extensions.Self]:
        """Construct a new choice encoder based on the serialiser specs."""
        result = cls._create_real(
            name, parents, resolver, tuple(spec.items())
        )
        return result

    @classmethod
    @functools.lru_cache(maxsize=None)
    def _create_real(
        cls,
        name: str,
        parents: typing.Optional[typing.Tuple[str, ...]],
        resolver: typing.Optional[Resolver],
        spec_tuples: typing.Tuple[typing.Tuple[str, SerialiserMapValue], ...],
    ):
        spec = dict(spec_tuples)
        details = f"{name=}, {spec=}, {parents=}"
        log(f"Resolving {details}")
        resolver = resolver or resolve
        serialisers: MutableMapping[int, Serialiser] = {}
        serialiser_names: MutableMapping[typing.Hashable, str] = {}
        for key, value in spec.items():
            if not (isinstance(key, int) and isinstance(value, Sequence)):  # pragma: no cover
                raise ValueError("Keys have to be integers and values have to be sequences.")
            serialiser_name = f"{name}.{key}"
            if len(value) > 0 and all(map(is_encoder, value)):
                sub_spec = value
            elif isinstance(value, CompoundSpec):
                sub_spec = resolver.resolve_compound(key, value)
            else:
                sub_spec = []
                if isinstance(value, str):
                    expanded_value = resolver(value)
                else:
                    expanded_value = value
                for num, val in enumerate(expanded_value):
                    if isinstance(val, CompoundSpec):
                        sub_spec.append(resolver.resolve_compound(str(num), val))
                    else:
                        sub_spec.append(resolver(val))
                sub_spec = tuple(sub_spec)
                if isinstance(value, str):
                    serialiser_names[key] = value
                elif isinstance(value, tuple) and len(value) == 1 and isinstance(value[0], str):
                    serialiser_names[key] = value[0]
                elif isinstance(value, tuple) and len(value) == 0:
                    serialiser_names[key] = "void"
            serialisers[key] = Serialiser(
                serialiser_name, {serialiser_name: sub_spec}, resolver=resolver
            )
        class_name = f"{pascalcase(snakecase(name))}ChoiceEncoder"
        result = typing.cast(
            typing.Type[ChoiceEncoder],
            type(
                class_name,
                (ChoiceEncoder,),
                {
                    "serialisers": serialisers,
                    "serialiser_names": serialiser_names,
                    "resolver": resolver,
                },
            ),
        )
        return result

    # noinspection PyUnusedLocal
    @classmethod
    def from_tuple(
        cls,
        item,
        modelcls: typing.Type[Model_Variants],
        model_key: str,
        serialiser: typing.Optional[Serialiser] = None,
    ):
        from .generic_model import GenericModel

        options = get_base_type_parameters(
            typing.cast(typing.Type[GenericModel], modelcls).Config.get_field_type(
                modelcls, model_key
            )
        )
        serialiser_name = cls.serialiser_names[item[0]]
        result = item[1]
        for x in options:

            if inspect.isclass(x) and issubclass(x, GenericModel):
                mapping = x.Config.attr_mappings_combined(x).get(serialiser_name)
                if mapping:
                    result = x.from_tuple(
                        item[1:],
                        Serialiser.by_name(serialiser_name, resolver=cls.resolver),
                    )
                    break
        return result

ListEncoder_T = typing.TypeVar("ListEncoder_T", bound="ListEncoder")


class ListEncoder(EncodingType[typing.Any, typing.Tuple]):
    """Special "encoding type" for choice-based values (i.e. `n-of')."""

    serialiser: Serialiser

    def __init__(self, value: Sequence):
        super().__init__(tuple(value) if value is not None else None)

    @classmethod
    def read(cls, stream: io.BytesIO) -> typing_extensions.Self:
        """Read the encoded value from a binary stream.

        It converts the read value to the correct type and constructs a new
        instance of the encoding type.
        """
        count = Int32.read(stream).value
        serialiser = cls.serialiser
        values = []
        for entry in range(0, count):
            deserialised = serialiser.read(stream)
            values.append(list(deserialised))
        return cls(values)

    def to_bytes(self) -> bytes:
        """Convert the value into its bytes representation."""
        if self.values is None:
            return b""
        result = Int32(len(self.values)).to_bytes()
        for value in self.values:
            serialiser = self.serialiser
            if inspect.isclass(serialiser):
                result += serialiser(value).to_bytes()
            else:
                result += serialiser.to_bytes(*value)
        return result

    @property
    def values(self) -> Sequence[Any]:
        """Return the current collection of values."""
        return self.value

    @classmethod
    def from_tuple(
        cls,
        item: typing.Iterable[typing.Tuple[typing.Any, ...]],
        item_type: typing.Type[GenericModel_T],
    ) -> typing.List[GenericModel_T]:
        from .generic_model import GenericModel_T
        from .generic_model_protocol import GenericModelProtocol

        assert hasattr(item, "__iter__")
        return typing.cast(
            typing.List[GenericModel_T],
            [
                item_type.Config.from_tuple(
                    typing.cast(typing.Type[GenericModelProtocol], item_type), x, cls.serialiser
                )
                for x in item
            ],
        )

    @classmethod
    def as_tuple(
        cls, item: typing.Iterable[GenericModel]
    ) -> typing.Tuple[typing.Tuple[typing.Any, ...], ...]:
        assert hasattr(item, "__iter__")
        return tuple(x.Config.as_tuple(x, cls.serialiser) for x in item)

    @classmethod
    def create(
        cls,
        spec: SerialiserMap,
        name: str,
        parents: typing.Optional[typing.Tuple[str, ...]] = None,
        resolver: typing.Optional[Resolver] = None,
    ) -> typing.Type[typing_extensions.Self]:
        """Construct a new list encoder based on the serialiser specs."""
        resolver = resolver or resolve
        hashed_name = f"{id(resolver)}{name}"
        if "conjunction" in name and resolver.name != "Default":
            log("Initialising conjunction")
        log(
            f"Constructing {cls.__name__}({name}, {spec}, {parents}, {resolver})="
            f"{hashed_name}"
        )
        if is_encoder(spec):
            serialiser = spec
        elif isinstance(spec, CompoundSpec):
            serialiser = resolver.resolve_compound(f"{name}.{spec.type.name}", spec)
        elif isinstance(spec, str):
            serialiser = Serialiser.by_name(spec, resolver=resolver)
        else:
            raise Exception(f"can't handle ListEncoder of {spec}")
        class_name = f"{pascalcase(snakecase(name))}ListSerialiser"
        if not isinstance(serialiser, Serialiser):
            log(f"{cls}: {serialiser} is not a Serialiser")
        else:
            log(f"{cls}: {serialiser} *is* a Serialiser")
        new_type = cast(
            typing.Type[typing_extensions.Self],
            type(class_name, (ListEncoder,), {"serialiser": serialiser}),
        )
        return new_type


class Resolver(StrictHashable):
    def __init__(
        self,
        name: str,
        specs: HashableDict[StrictHashable, HashableElement],
        cached: bool = True,
    ) -> None:
        self.name = name
        self.specs = HashableDict.create(specs)
        self.cached = cached
        self.cached_items: typing.Dict[str, typing.Type[EncodingProtocol]] = {}
        self.cached_resolve = functools.lru_cache(maxsize=None)(self.resolve)
        self.hash = hash((self.name, hash(self.specs), self.cached))

    def __hash__(self) -> int:
        return self.hash

    def __call__(self, *args, **kwargs):
        return self.cached_resolve(*args, **kwargs)

    def __repr__(self):
        return f"{type(self).__name__}({(self.name, id(self.specs))}) at {id(self)}"

    def resolve(
        self, serialiser_name: str, parents: typing.Optional[typing.Tuple[str, ...]] = None
    ) -> SerialiserMap:
        """Extract the serialiser types for any serialiser key in the spec.

        The `parents` argument is used internally to carry the list of all
        recursive parents, which is eventually concatenated to an internal key.

        The name must be a key in the serialiser spec. The value for a key is
        recursively expanded into a mapping of encoding type classes.
        """
        log(f"{self}: Resolving {serialiser_name}, parents {parents}")

        result: MutableSerialiserMap = {}
        if parents is None:
            parents = tuple()
        parents += (serialiser_name,)
        try:
            spec: Any = None
            found = False
            elements = serialiser_name.split(".")
            ser_name = ""
            while elements:
                ser_name = ".".join(elements)

                if ser_name in self.specs:
                    spec = self.specs.get(ser_name)
                    found = True
                    break
                elements.pop(0)
            if not found:
                raise IndexError(f"No such serialiser {ser_name}, {serialiser_name}")
        except Exception as e:  # pragma: no cover
            LOG.error(f"Got exception {e}")
            raise
        if not (spec is None or is_encoder(spec)):
            if isinstance(spec, str) or not isinstance(spec, Sequence):
                spec = [spec]
            if isinstance(spec, CompoundSpec):
                spec = self.resolve_compound(serialiser_name, spec)
            elif not all(map(is_encoder, spec)):
                for value in spec:
                    name = ".".join(parents)
                    if isinstance(value, CompoundSpec):
                        result[name] = self.resolve_compound(name, value)
                    elif is_encoder(value):
                        result[name] = value
                    else:
                        result.update(self(value, parents))
                return result
        return {".".join(parents): spec}

    def resolve_compound(self, name: str, spec: CompoundSpec) -> SerialiserMapValue:
        log(f"{self}: Resolving complex {name} and {spec}")
        if name == "conjunction-constraint" and self.name != "Default":
            log(f"{self}: Resolving complex {name} and {spec}")
        # this is where proper pattern matching would come in handy :)
        if spec.type is Compound.MAP_OF:
            key, value = typing.cast(
                typing.Tuple[Enc_MetaType_Str, Enc_MetaType_Str],
                tuple(self.specs.get(sp, sp) for sp in spec.args),
            )
            return self.resolve_generic(GenericMapSerialiser, KeyValue(key, value))
        if spec.type is Compound.SET_OF:
            set_spec = spec.args[0]
            serialiser = typing.cast(Enc_MetaType, self.specs.get(set_spec, set_spec))
            return self.resolve_generic(
                GenericScalarSetSerialiser, serialiser, serialiser.__name__
            )
        if spec.type is Compound.ONE_OF:
            return self.resolve_generic(ChoiceEncoder, spec.args[0], name)
        if spec.type is Compound.N_OF:
            return self.resolve_generic(ListEncoder, spec.args[0], name)
        raise NotImplementedError()

    def resolve_generic(
        self,
        encoding_type: typing.Type[EncodingTypeOrProtocolVar],
        spec: typing.Any,
        name: str = "",
    ) -> typing.Type[EncodingTypeOrProtocolVar]:
        if name == "":
            name = f"{spec}{encoding_type}"
        if name not in self.cached_items:
            result = encoding_type.create(spec, name, resolver=self)
            self.cached_items[name] = result
        return typing.cast(
            typing.Type[EncodingTypeOrProtocolVar], self.cached_items[name]
        )


resolve = Resolver("Default", SERIALISER_SPECS)
