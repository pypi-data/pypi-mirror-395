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

import dataclasses as dc
import traceback
import typing


import diffusion.datatypes
from diffusion.datatypes.foundation.datatype import TypeCode_Bound
from diffusion.datatypes.foundation.abstract import A_T
from diffusion.handlers import LOG
from typing import Optional

if typing.TYPE_CHECKING:
    from diffusion.internal.serialisers import Serialiser
    from diffusion.internal.serialisers.generic_model import Model_Variants

from diffusion.internal.pydantic_compat.v1 import dataclasses

from diffusion.internal.serialisers.dataclass_model import DataclassConfigMixin
from diffusion.internal.serialisers.generic_model import (
    GenericModel,
    GenericConfig,
    GenericModel_T,
)
from diffusion.internal.utils import BaseConfig


class StringMap(typing.Dict[str, str], GenericModel):
    class Config(GenericConfig["StringMap"]):
        alias = "topic-properties"

        @classmethod
        def decode(
            cls,
            item,
            modelcls: typing.Type[Model_Variants],
            model_key: str,
            serialiser: Optional[Serialiser] = None,
        ):
            serialiser = cls.check_serialiser(serialiser)
            return cls.decode_complex(item, modelcls, model_key, serialiser)

        @classmethod
        def attr_mappings_all(cls, modelcls):
            return {"topic-properties": {"topic-properties": "_innerdict"}}

    @classmethod
    def from_fields(
        cls: typing.Type[GenericModel_T], **kwargs: typing.Any
    ) -> GenericModel_T:
        _innerdict = kwargs.pop("_innerdict")
        return typing.cast(GenericModel_T, cls(**_innerdict))

    def __hash__(self):
        return hash(tuple(self.items()))


FetchTopicResult_T = typing.TypeVar("FetchTopicResult_T", bound="FetchTopicResult")


@dataclasses.dataclass(frozen=True, config=BaseConfig)
class FetchTopicResult(typing.Generic[A_T], GenericModel):
    """
    The single topic result from a [FetchQuery][diffusion.features.topics.fetch.fetch_query.FetchQuery].

    """  # NOQA: E501

    path: str
    type: typing.Type[A_T]
    value: typing.Optional[bytes]
    properties_index: typing.Any

    @classmethod
    def from_fields(
        cls: typing.Type[FetchTopicResult_T],
        *,
        path: str,
        type: TypeCode_Bound,
        value: typing.Union[typing.Tuple[int], typing.Tuple[int, bytes]],
        properties_index: int,
        **kwargs
    ) -> FetchTopicResult_T:
        tp = diffusion.datatypes.get(type)
        try:
            if value[0]:
                assert len(value) > 1
                bytes_value = typing.cast(bytes, value[1])

                val_final = bytes_value
            else:
                val_final = None

            return typing.cast(FetchTopicResult_T, cls(path, tp, val_final, properties_index))
        except Exception as e:  # pragma: no cover
            LOG.error(f"Got {e}: {traceback.format_exc()}")
            raise

    class Config(GenericConfig["FetchTopicResult"]):
        @classmethod
        def attr_mappings_all(cls, modelcls):
            return {
                "fetch-topic-result": {
                    "path": "path",
                    "protocol14-topic-type": "type",
                    "fetch-topic-value": "value",
                    "fetch-properties-index": "properties_index",
                }
            }

        @classmethod
        def decode(
            cls,
            item,
            modelcls: typing.Type[Model_Variants],
            model_key: str,
            serialiser: Optional[Serialiser] = None,
        ):
            return item


FetchTopicResult.__pydantic_model__.update_forward_refs(A_T=A_T)  # type: ignore


@dataclasses.dataclass(frozen=True, config=BaseConfig, validate_on_init=False)
class FetchQueryResult(GenericModel):
    """
    The result from a [FetchQuery][diffusion.features.topics.fetch.fetch_query.FetchQuery].

    """

    class Config(DataclassConfigMixin["FetchQueryResult"]):
        @classmethod
        def decode(
            cls,
            item,
            modelcls: typing.Type[Model_Variants],
            model_key: str,
            serialiser: Optional[Serialiser] = None,
        ):
            serialiser = cls.check_serialiser(serialiser)

            return cls.decode_complex(item, modelcls, model_key, serialiser)

        @classmethod
        def attr_mappings_all(cls, modelcls):
            return {
                "fetch-query-result": {
                    "fetch-topic-properties": "properties",
                    "fetch-topic-results": "results",
                    "fetch-has-more.true-boolean": "has_more",
                }
            }

    def __post_init__(self):
        try:
            # noinspection PyUnresolvedReferences
            self.__pydantic_validate_values__()
        except Exception as e:  # pragma: no cover
            LOG.error(f"Got {e}: {traceback.format_exc()}")
            raise

    properties: typing.Tuple[StringMap, ...] = dc.field(
        metadata=dict(alias="fetch-topic-properties")
    )
    results: typing.Tuple[FetchTopicResult, ...] = dc.field(
        metadata=dict(alias="fetch-topic-results")
    )
    has_more: bool
