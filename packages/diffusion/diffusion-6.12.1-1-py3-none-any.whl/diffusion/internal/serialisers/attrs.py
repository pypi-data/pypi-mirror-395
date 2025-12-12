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

import functools
import typing
from collections.abc import Hashable

import attr

from diffusion.handlers import LOG
from diffusion.internal.serialisers.generic_model import (
    GenericModel,
    GenericConfig,
)

if typing.TYPE_CHECKING:
    from diffusion.internal.services import ServiceValue
    from diffusion.internal.serialisers import Serialiser

AttrsModel_T = typing.TypeVar("AttrsModel_T", bound="MarshalledModel")
AttrsModel_T_Other = typing.TypeVar("AttrsModel_T_Other", bound="MarshalledModel")


@attr.s
class MarshalledModel(GenericModel):
    class Config(GenericConfig["MarshalledModel"]):
        @classmethod
        def find_aliases(
            cls, modelcls: typing.Type[MarshalledModel], serialiser: Serialiser
        ) -> typing.Mapping[str, str]:
            assert isinstance(modelcls, Hashable)
            return cls._find_aliases(modelcls, serialiser)

        @classmethod
        @functools.lru_cache(maxsize=None)
        def _find_aliases(
            cls, modelcls: typing.Type[MarshalledModel], serialiser: Serialiser
        ) -> typing.Mapping[str, str]:
            serialiser = cls.check_serialiser(serialiser)
            updates = {}
            for x in attr.fields(modelcls):  # type: ignore
                if x.metadata:
                    target = x.metadata.get(
                        getattr(serialiser, "name") or cls.alias, x.metadata.get("alias")
                    )
                    updates[target] = x.name
            return updates

        @classmethod
        def from_service_value(
            cls,
            modelcls: typing.Type[MarshalledModel],
            item: ServiceValue,
        ) -> MarshalledModel:
            fields = dict(cls.get_fields(item, modelcls))
            for field_name, field_value in fields.items():
                try:
                    field = attr.fields_dict(modelcls).get(field_name)
                    if field and field.converter:
                        # attrs plugin should take care of this but doesn't
                        assert callable(field.converter)
                        fields[field.name] = field.converter(fields[field.name])
                except Exception as e:  # pragma: no cover
                    LOG.error(f"Got exception {e}")
                    raise
            try:
                return typing.cast(MarshalledModel, modelcls.from_fields(
                    **fields)
                )
            except Exception as e:  # pragma: no cover
                LOG.error(f"Got exception {e}")
                raise
