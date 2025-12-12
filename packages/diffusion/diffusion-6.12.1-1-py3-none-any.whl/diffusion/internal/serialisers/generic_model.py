#  Copyright (c) 2022 - 2025 DiffusionData Ltd., All Rights Reserved.
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

import functools
import inspect
import io
import os
import subprocess
import traceback
import typing
from collections.abc import Hashable

import typing_extensions

import stringcase  # type: ignore[import-untyped]

import diffusion.datatypes
from diffusion.handlers import LOG
from diffusion.internal.utils import BaseConfig, decode
from typing import Optional
from .compound import GenericMapSerialiser
from .generic_model_protocol import GenericModel_Args_T, GenericModelProtocol, \
    ConversationFactory, CombinedMapping

if typing.TYPE_CHECKING:  # pragma: no cover
    from diffusion.internal.services.abstract import (
        ServiceValue,
    )
    from ..protocol.conversations import Conversation

    from diffusion.internal.serialisers.base import Serialiser, Resolver
    from .attrs import MarshalledModel as AttrsModel
    from .pydantic import MarshalledModel as PydanticModel
    from .dataclass_model import DataclassWithConfig

    Model_Variants = typing.Union[
        AttrsModel, PydanticModel, DataclassWithConfig, GenericModelProtocol
    ]
    Model_Variants_T = typing.TypeVar("Model_Variants_T", bound=Model_Variants)


GenericModelOrProtocol = typing.Union["GenericModelProtocol", "GenericModel"]
GenericModel_T = typing.TypeVar("GenericModel_T", bound="GenericModelOrProtocol")
GenericModel_T_co = typing.TypeVar(
    "GenericModel_T_co", bound="GenericModelOrProtocol", covariant=True
)
GenericModel_T_Other = typing.TypeVar("GenericModel_T_Other", bound="GenericModelOrProtocol")

@dataclasses.dataclass(frozen=True)
class PreparedModelAndConversation(typing.Generic[GenericModel_T_co]):
    model: GenericModel_T_co
    conversation: typing.Optional[Conversation]

class GenericConfig(
    typing.Generic[GenericModel_T],
    BaseConfig,
):
    """
    Adds Serialiser support to Model.Config
    'alias' defines the name of the serialiser to map to
    """

    alias: typing.ClassVar[str]
    allow_population_by_field_name = True
    alias_generator = stringcase.spinalcase

    @classmethod
    def verify_item(cls, item: ServiceValue, modelcls: typing.Type[GenericModel_T]):
        try:
            assert (
                cls.attr_mappings_final(modelcls, item._serialiser)
            )
        except Exception as e:  # pragma: no cover
            LOG.error(f"Got exception {e}")
            raise

    @classmethod
    @functools.lru_cache(maxsize=None)
    def serialiser(cls, name=None, resolver: Optional[Resolver] = None) -> "Serialiser":
        from diffusion.internal.serialisers.base import Serialiser

        if not name:
            if not isinstance(getattr(cls, "alias", None), str):  # pragma: no cover
                raise RuntimeError(f"{cls} has no 'alias'")
        return Serialiser.by_name(name or cls.alias, resolver=resolver)

    @classmethod
    def to_bytes(cls, item: GenericModel_T, serialiser: Optional[Serialiser] = None) -> bytes:
        serialiser = cls.check_serialiser(serialiser)
        as_tuple = cls.as_tuple(item, serialiser=serialiser)
        return serialiser.to_bytes(*as_tuple)

    @classmethod
    def check_serialiser(cls, serialiser: typing.Optional[Serialiser]) -> Serialiser:
        from diffusion.internal.serialisers.base import Serialiser
        if serialiser is None:
            return cls.serialiser()
        assert isinstance(serialiser, Serialiser)
        return serialiser

    @classmethod
    def from_service_value(
        cls,
        modelcls: typing.Type[GenericModel_T],
        item: ServiceValue,
    ) -> GenericModel_T:
        fields = cls.get_fields(item, modelcls)
        try:
            return typing.cast(GenericModel_T, modelcls.from_fields(**fields))
        except Exception as e:  # pragma: no cover
            LOG.error(f"Got exception {e}: {traceback.format_exc()}")
            raise

    @classmethod
    def get_fields(cls, item, modelcls):
        cls.verify_item(item, modelcls)
        mapping = cls.get_model_to_serialiser_mapping(modelcls, serialiser=item._serialiser)
        fields = cls.gen_fields(
            item,
            mapping,
            modelcls,
        )
        try:
            assert all(x is not None for x in fields.keys())
        except Exception as e:  # pragma: no cover
            LOG.error(f"Got exception {e}")
            raise
        return fields

    @classmethod
    def gen_fields(cls, item, model_to_serialiser_mapping, modelcls):
        try:
            result = {
                model_key: modelcls.Config.decode(
                    item[serialiser.name],
                    modelcls,
                    model_key=model_key,
                    serialiser=serialiser,
                )
                for model_key, serialiser in model_to_serialiser_mapping.items()
                if serialiser
            }
            assert all(x is not None for x in result.keys())
            return result
        except Exception as e:  # pragma: no cover
            LOG.error(f"Got exception {e}")
            raise

    @classmethod
    def from_tuple(
        cls,
        modelcls: typing.Type[GenericModel_T],
        tp: typing.Tuple[typing.Any, ...],
        serialiser: Optional[Serialiser] = None,
    ) -> GenericModel_T:
        serialiser = cls.check_serialiser(serialiser)
        sv = cls.service_value(serialiser).evolve(*tp)
        result = cls.from_service_value(modelcls, sv)
        return result

    @classmethod
    def fields_from_tuple(
        cls,
        modelcls: typing.Type[GenericModel_T_Other],
        tp: typing.Tuple[typing.Any, ...],
        serialiser: Optional[Serialiser] = None,
    ) -> typing.Mapping[str, typing.Any]:
        sv = cls.service_value(serialiser).evolve(*tp)
        result = cls.get_fields(sv, modelcls)
        return result

    @classmethod
    def read(
        cls,
        modelcls: typing.Type[GenericModel_T],
        stream: io.BytesIO,
        serialiser: Optional[Serialiser] = None,
    ) -> GenericModel_T:
        serialiser = cls.check_serialiser(serialiser)
        return cls.from_tuple(modelcls, tuple(serialiser.read(stream)), serialiser)

    @classmethod
    def find_aliases(
        cls, modelcls: typing.Type[GenericModel_T], serialiser: Serialiser
    ) -> typing.Mapping[str, str]:
        assert isinstance(
            modelcls, Hashable
        )  # see: https://github.com/python/mypy/issues/11470
        # noinspection PyTypeChecker
        return cls._find_aliases(modelcls, serialiser)

    @classmethod
    @functools.lru_cache(maxsize=None)
    def _find_aliases(
        cls, modelcls: typing.Type[GenericModel_T], serialiser: Serialiser
    ) -> typing.Mapping[str, str]:
        return {}

    @classmethod
    def get_model_to_serialiser_mapping(
        cls,
        modelcls: typing.Type[GenericModel_T],
        serialiser: typing.Optional[Serialiser] = None,
    ) -> typing.Mapping[str, Serialiser]:
        assert isinstance(modelcls, Hashable)
        # noinspection PyTypeChecker
        return cls._get_model_to_serialiser_mapping(modelcls, serialiser)

    @classmethod
    @functools.lru_cache(maxsize=None)
    def _get_model_to_serialiser_mapping(
        cls,
        modelcls: typing.Type[GenericModel_T],
        serialiser: typing.Optional[Serialiser] = None,
    ) -> typing.Mapping[str, Serialiser]:
        cls.assert_model(modelcls)
        LOG.info(
            f"Evaluating {id(cls)}: {cls=}, {id(modelcls)}, {modelcls=}, "
            f"{id(serialiser)}, {serialiser=}"
        )
        try:
            serialiser = cls.check_serialiser(serialiser)
            final_mapping = cls.attr_mappings_final(modelcls, serialiser=serialiser)
            result = {}
            for serialiser_key, model_key in final_mapping.message.items():
                final_model_key = getattr(model_key, "__name__", model_key)
                final_serialiser_key = cls.sanitize_key(serialiser_key, serialiser)
                if not (final_serialiser_key and final_model_key):
                    continue
                result.update(
                    {
                        final_model_key: cls.serialiser(
                            final_serialiser_key, resolver=serialiser.resolver
                        )
                    }
                )

            assert all(x is not None for x in result.keys())
            assert all(x is not None for x in result.values())
            return result
        except Exception as e:  # pragma: no cover
            LOG.error(f"Got {e}: {traceback.format_exc()}")
            raise

    @classmethod
    def assert_model(cls, modelcls: typing.Type[GenericModel_T]):
        assert all(hasattr(modelcls, x) for x in {"from_fields", "Config"})
        assert issubclass(modelcls.Config, GenericConfig)
        if os.getenv("DIFFUSION_ASSERT_CONFIG"):  # pragma: no cover
            cls.assert_config_matches(modelcls)

    @classmethod
    def assert_config_matches(cls, modelcls):  # pragma: no cover
        if modelcls.Config is not cls:
            try:
                import objgraph  # type: ignore[import-not-found]

                objgraph.show_refs([modelcls.Config, cls], filename="ownership.dot")
                subprocess.check_output(["gv2gml"])
            except ImportError:
                pass
            raise AssertionError(
                f"{modelcls}.Config ({modelcls.Config})@{id(modelcls)}: "
                f"{modelcls.Config.__dict__} is not {cls}@{id(cls)}: {cls.__dict__}"
            )
        assert modelcls.Config is cls

    @classmethod
    def sanitize_key(cls, name: str, serialiser: Optional[Serialiser] = None):
        sv = cls.service_value(serialiser)
        result = sv.sanitize_key(name)
        if result:
            return result
        if cls.alias_generator:
            result = sv.sanitize_key(cls.alias_generator(name))
        if not result:  # pragma: no cover
            LOG.error(f"Couldn't find {name} in {sv.spec}")
        return result

    @classmethod
    def get_service_value_args(
        cls, item: GenericModel_T, serialiser: typing.Optional[Serialiser] = None
    ):
        model_to_serialiser_mapping = cls.get_model_to_serialiser_mapping(
            type(item), serialiser=serialiser
        )
        try:
            mappings = {
                v.name: cls.as_service_value_field(getattr(item, k), serialiser=v)
                for k, v in model_to_serialiser_mapping.items()
            }  # NOQA
        except Exception as e:  # pragma: no cover
            raise e
        return mappings

    @classmethod
    def decode(
        cls,
        item,
        modelcls: typing.Type[Model_Variants],
        model_key: str,
        serialiser: Optional[Serialiser] = None,
    ):
        return decode(item)

    @classmethod
    def get_field_type(cls, modelcls: typing.Type[Model_Variants], model_key: str):
        result = typing_extensions.get_type_hints(modelcls).get(model_key)
        return result

    @classmethod
    def decode_complex(
        cls,
        item,
        modelcls: typing.Type[Model_Variants],
        model_key: str,
        serialiser: Serialiser,
    ) -> typing.Union[typing.List, typing.Mapping]:
        from diffusion.internal.serialisers.base import ListEncoder, ChoiceEncoder

        if len(serialiser.spec.values()) == 1:
            sub_encoder = next(iter(serialiser.spec.values()), None)

            if inspect.isclass(sub_encoder):
                if issubclass(sub_encoder, GenericMapSerialiser):
                    map_dest = cls.get_mapping_key_value(modelcls)
                    try:
                        return sub_encoder.from_tuple(item, map_dest)
                    except Exception as e:  # pragma: no cover
                        LOG.error(f"Got {e}: {traceback.format_exc()}")
                        raise
                if issubclass(sub_encoder, ChoiceEncoder):
                    return sub_encoder.from_tuple(item, modelcls, model_key, serialiser)
                if issubclass(sub_encoder, ListEncoder):
                    item_type = cls.get_field_type(modelcls, model_key).__args__[0]

                    return typing.cast(typing.Type[ListEncoder], sub_encoder).from_tuple(
                        item, item_type
                    )
        return decode(item)

    @classmethod
    def get_mapping_key_value(cls, modelcls):
        assert isinstance(modelcls, Hashable)
        return cls._get_mapping_key_value(typing.cast(typing.Hashable, modelcls))

    @classmethod
    @functools.lru_cache(maxsize=None)
    def _get_mapping_key_value(cls, modelcls):
        generic_bases_candidates = getattr(modelcls, "__orig_bases__", None)
        import collections.abc

        if generic_bases_candidates:
            try:
                for x in generic_bases_candidates:
                    origin = typing_extensions.get_origin(x)
                    if (
                        inspect.isclass(origin)
                        and issubclass(origin, collections.abc.Mapping)
                        and len(typing_extensions.get_args(x)) == 2
                    ):
                        return typing_extensions.get_args(x)
            except Exception as e:  # pragma: no cover
                LOG.error(f"Got {e}: {traceback.format_exc()}")
                raise
        return object, object  # pragma: no cover

    @classmethod
    def as_service_value_field(cls, item: GenericModel_T, serialiser: Serialiser):
        from diffusion.internal.serialisers.base import (
            ListEncoder,
            ChoiceEncoder,
        )

        sub_encoder = serialiser.get_encoder(ListEncoder, ChoiceEncoder)
        if sub_encoder:
            return sub_encoder.as_tuple(item)

        if isinstance(item, diffusion.datatypes.AbstractDataType):
            return item.encode(item.value)
        if isinstance(item, GenericModel):
            return item.Config.as_tuple(item, serialiser)
        return item

    @classmethod
    def as_service_value(
        cls: typing.Type[GenericConfig[GenericModel_T]],
        item: GenericModel_T,
        serialiser: Optional[Serialiser] = None,
    ) -> ServiceValue:
        sv = cls.service_value(serialiser)
        mappings = cls.get_service_value_args(item, serialiser=serialiser)
        try:
            return sv.evolve(**mappings)
        except Exception as e:  # pragma: no cover
            LOG.error(f"Caught exception {e}")
            raise

    @classmethod
    def as_tuple(
        cls, item: GenericModel_T, serialiser: Optional[Serialiser] = None
    ) -> typing.Tuple[typing.Any, ...]:
        from .generic_model_protocol import GenericModelProtocol

        return tuple(
            item.Config.as_service_value(
                typing.cast(GenericModelProtocol, item), serialiser=serialiser
            ).values()
        )

    @classmethod
    def attr_mappings_final(
        cls,
        modelcls: typing.Type[GenericModel_T],
        serialiser: typing.Optional[Serialiser] = None,
    ) -> CombinedMapping:
        assert isinstance(modelcls, Hashable)
        return cls._attr_mappings_final(modelcls, serialiser)

    @classmethod
    @functools.lru_cache(maxsize=None)
    def _attr_mappings_final(
        cls,
        modelcls: typing.Type[GenericModel_T],
        serialiser: typing.Optional[Serialiser] = None,
    ) -> CombinedMapping:
        try:
            assert hasattr(modelcls, "__hash__")
            serialiser = cls.check_serialiser(serialiser)
            result = cls.attr_mappings_combined(modelcls).get(
                serialiser.name, CombinedMapping({})
            )
            updates = cls.find_aliases(modelcls, serialiser)
            model_mapping = dict(result.message)
            model_mapping.update({
                k: v
                for k, v in updates.items()
                if cls.service_value(serialiser).sanitize_key(k) and v
            })
            result = dataclasses.replace(
                result,
                message=model_mapping,
            )
            assert all([x for x in result.message.keys()])
            assert all([x for x in result.message.values()])
            return result
        except Exception as e:  # pragma: no cover
            LOG.error(f"Got {e}: {traceback.format_exc()}")
            raise

    @classmethod
    @functools.lru_cache(maxsize=None)
    def service_value(cls, serialiser: Optional[Serialiser] = None):
        from diffusion.internal.services.abstract import ServiceValue

        return ServiceValue(cls.check_serialiser(serialiser))

    @classmethod
    def attr_mappings_all(cls, modelcls):
        alias = getattr(cls, "alias", None)
        return {alias: {}} if alias else {}

    @classmethod
    def attr_mappings_combined(cls, modelcls) -> typing.Mapping[str, CombinedMapping]:
        assert isinstance(modelcls, Hashable)
        return cls._attr_mappings_combined(modelcls)

    @classmethod
    @functools.lru_cache(maxsize=None)
    def _attr_mappings_combined(cls, modelcls) -> typing.Mapping[str, CombinedMapping]:
        return {k: CombinedMapping(v) for k, v in cls.attr_mappings_all(modelcls).items()}

    @classmethod
    def entry_from_list_of_choices_as_tuple(cls, event: GenericModel, serialiser: Serialiser):
        from diffusion.internal.serialisers.base import (
            ListEncoder,
            ChoiceEncoder,
        )
        from .generic_model_protocol import GenericModelProtocol

        encoder: typing.Type[ListEncoder] = serialiser.to_encoder(ListEncoder)
        choice_encoder = ChoiceEncoder.extract_from(encoder.serialiser)
        return choice_encoder.as_tuple(typing.cast(GenericModelProtocol, event))

    @classmethod
    async def prepare_conversation(
        cls, item: GenericModel_T, conversation_factory: ConversationFactory
    ) -> PreparedModelAndConversation[GenericModel_T]:
        return PreparedModelAndConversation(item, None)

    @classmethod
    def resolve_serialiser(
        cls, modelcls: typing.Type[GenericModel], raw_serialiser: Serialiser
    ):
        from diffusion.internal.serialisers.base import Serialiser
        from diffusion.internal.encoded_data.abstract import EncodingType

        final_serialiser = raw_serialiser
        if len(raw_serialiser.spec.values()) == 1:
            sole_serialiser = next(iter(raw_serialiser.spec.values()))
            if inspect.isclass(sole_serialiser):
                sole_serialiser_names = {raw_serialiser.name}
                if issubclass(sole_serialiser, EncodingType):
                    sole_serialiser_names = set(
                        sole_serialiser.get_serialiser_names().values()
                    )
                matching_serialisers = (
                    sole_serialiser_names
                    & modelcls.Config.attr_mappings_combined(type(modelcls)).keys()
                )
                assert (
                    len(matching_serialisers) == 1
                ), "Should have single unique match"
                final_serialiser = Serialiser.by_name(
                    next(iter(matching_serialisers)), raw_serialiser.resolver
                )
        return final_serialiser

    @classmethod
    async def respond_to_subfields(
            cls,
            item: GenericModel_T,
            conversation: typing.Optional[Conversation],
            serialiser: Serialiser,
    ):
        from diffusion.internal.serialisers.base import Serialiser

        fields = (
            cls.attr_mappings_combined(type(item))
            .get(serialiser.name, CombinedMapping())
            .message
        )
        for sub_serialiser_name, model_field_name in fields.items():
            subfield = getattr(item, model_field_name, None)
            if isinstance(subfield, GenericModel):
                raw_serialiser = Serialiser.by_name(
                    sub_serialiser_name, serialiser.resolver
                )
                await subfield.Config.respond_to_conversation(
                    subfield,
                    conversation,
                    subfield.Config.resolve_serialiser(
                        type(subfield), raw_serialiser
                    ),
                )
        return item

    @classmethod
    async def respond_to_conversation(
        cls,
        item: GenericModel_T,
        conversation: typing.Optional[Conversation],
        serialiser: Serialiser,
    ) -> GenericModel_T:
        if conversation:
            conversation.data.update(
                {
                    k: getattr(item, v)
                    for k, v in cls.attr_mappings_final(
                        type(item), serialiser
                    ).conversation.items()
                    if hasattr(item, v)
                }
            )

        return await cls.respond_to_subfields(item, conversation, serialiser)



class GenericModel(object):
    class Config(GenericConfig):
        pass

    def to_bytes(self) -> bytes:
        return self.Config.to_bytes(self)

    @classmethod
    def from_fields(
        cls: typing.Type[GenericModelProtocol[GenericModel_Args_T]],
        *args: GenericModel_Args_T.args,
        **kwargs: GenericModel_Args_T.kwargs,
    ) -> GenericModelProtocol[GenericModel_Args_T]:
        try:
            # noinspection PyArgumentList
            return typing.cast(
                GenericModelProtocol[GenericModel_Args_T], cls(**kwargs)
            )
        except Exception as e:  # pragma: no cover
            LOG.error(f"Got exception {e}")
            raise

    @classmethod
    def from_service_value(
        cls: typing.Type[GenericModel_T], item: ServiceValue
    ) -> GenericModel_T:
        return cls.Config.from_service_value(cls, item)

    @classmethod
    def from_tuple(
        cls, tp: typing.Tuple[typing.Any, ...], serialiser: Optional[Serialiser] = None
    ):
        result = cls.Config.from_tuple(cls, tp, serialiser=serialiser)
        return result
