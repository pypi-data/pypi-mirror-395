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

import diffusion.internal.pydantic_compat.v1 as pydantic
from typing import Optional

if typing.TYPE_CHECKING:
    from diffusion.internal.serialisers import Serialiser

from diffusion.internal.serialisers.generic_model import GenericConfig, GenericModel
MarshalledModel_T = typing.TypeVar("MarshalledModel_T", bound="MarshalledModel")


class MarshalledModel(pydantic.BaseModel, GenericModel):
    class Config(GenericConfig["MarshalledModel_T"]):
        allow_population_by_field_name = True

        @classmethod
        @functools.lru_cache(maxsize=None)
        def find_aliases(
            cls, modelcls: typing.Type[MarshalledModel_T], serialiser: typing.Optional[str]
        ) -> typing.Mapping[str, str]:
            return {
                cls.lookup_alias(modelcls, key, serialiser): key
                for key, field in modelcls.__fields__.items()
            }

        # noinspection PyUnusedLocal
        @classmethod
        @functools.lru_cache(maxsize=None)
        def lookup_alias(
            cls,
            modelcls: typing.Type[MarshalledModel_T],
            name: str,
            serialiser: Optional[Serialiser] = None,
        ):
            field = modelcls.__fields__.get(name, None)
            if field and field.has_alias and field.alias:
                return field.alias
            return None
