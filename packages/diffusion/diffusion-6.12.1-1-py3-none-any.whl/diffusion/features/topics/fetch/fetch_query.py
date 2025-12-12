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
import functools
import typing

from diffusion.internal.pydantic_compat.v1 import dataclasses
import diffusion.internal.pydantic_compat.v1 as pydantic

import diffusion.datatypes
from diffusion.features.topics.fetch.types import FetchQueryValueType
from diffusion.internal.serialisers.base import ChoiceProvider, Serialiser
from diffusion.internal.serialisers.generic_model import GenericModel, GenericConfig
from diffusion.internal.utils import BaseConfig
from diffusion.internal.validation.pydantic import (
    SignedInt32,
    MaximumResultSize,
    NonNegativeSignedInt32,
)
from typing import Optional

Exists = typing.Literal[0, 1]
Exists_T = typing.TypeVar("Exists_T", bound=Exists)


class Limit(GenericModel):
    """
    The range limit for a fetch request.

    """

    class Config(typing.Generic[Exists_T], GenericConfig, ChoiceProvider[Exists_T]):
        @classmethod
        def as_tuple(
            cls, item: Limit, serialiser: Optional[Serialiser] = None
        ) -> typing.Tuple[typing.Any, ...]:
            body = super().as_tuple(item, serialiser)
            return cls.id(), *body

        @classmethod
        def __class_getitem__(
            cls: typing.Type["Limit.Config"], identifier: Exists_T
        ) -> typing.Type["Limit.Config[Exists_T]"]:
            args = typing.get_args(identifier)
            if args and len(args) == 1:
                final_identifier = args[0]
            else:
                final_identifier = identifier

            class Result(cls):  # type: ignore
                @classmethod
                def id(cls) -> Exists_T:
                    return final_identifier

            return typing.cast(typing.Type["Limit.Config[Exists_T]"], Result)


class NotALimit(Limit):
    class Config(Limit.Config[typing.Literal[0]]):
        @classmethod
        def as_tuple(
            cls, item: Limit, serialiser: Optional[Serialiser] = None
        ) -> typing.Tuple[typing.Any, ...]:
            return (cls.id(),)

    def __copy__(self):
        return self  # pragma: no cover

    def __deepcopy__(self, memodict):
        return self

    def __bool__(self):
        return False


NOT_A_LIMIT = NotALimit()


@dataclasses.dataclass(frozen=True, config=BaseConfig)
class LimitExisting(Limit):
    path: str = dc.field()
    """The path."""
    includes_path: bool = dc.field()
    """Whether the path is included or not."""

    class Config(Limit.Config[typing.Literal[1]]):
        @classmethod
        def attr_mappings_all(cls, modelcls):
            return {
                "fetch-range-limit": {
                    "fetch-range-limit.path": "path",
                    "fetch-range-limit.fetch-range-includes-path.boolean": "includes_path",
                }
            }


@dataclasses.dataclass(frozen=True, config=BaseConfig)
class FetchRange(GenericModel):
    """
    The fetch range.

    """

    class Config(GenericConfig):
        @classmethod
        def attr_mappings_all(cls, modelcls):
            return {
                "fetch-range": {
                    "fetch-range.fetch-range-from": "from_",
                    "fetch-range.fetch-range-to": "to",
                }
            }

    @classmethod
    @functools.lru_cache(maxsize=None)
    def unbounded(cls) -> FetchRange:
        return cls(NOT_A_LIMIT, NOT_A_LIMIT)

    from_: typing.Union[LimitExisting, NotALimit] = dataclasses.Field(
        default=NOT_A_LIMIT
    )
    to: typing.Union[LimitExisting, NotALimit] = dataclasses.Field(default=NOT_A_LIMIT)

    def __repr__(self):
        return f"{type(self).__name__}(from_={self.from_ or 'start'}, to={self.to or 'end'})"


SignedInt32_Validator: SignedInt32 = typing.cast(
    SignedInt32, pydantic.conint(ge=SignedInt32.ge, le=SignedInt32.le)
)


@dataclasses.dataclass(frozen=True, config=BaseConfig, validate_on_init=False)
class FetchQuery(GenericModel):
    """
    The fetch request.

    """

    selector: pydantic.StrictStr = dc.field()
    """The topic selector."""
    range: FetchRange = dc.field()
    """The fetch range."""
    topic_types: typing.FrozenSet[typing.Type[FetchQueryValueType]] = dc.field()
    """The topic types."""
    with_values: pydantic.StrictBool = dc.field()
    """Whether values are required."""
    with_properties: pydantic.StrictBool = dc.field()
    """Whether properties are required."""
    limit: SignedInt32 = SignedInt32(0)
    """Optional limit. 0 = none. Positive = first, negative = last."""
    maximum_result_size: MaximumResultSize = MaximumResultSize(0)
    """Optional maximum result size. 0 = taken from server maximum message
    size. If specified must be >= 1024."""
    deep_branch_depth: NonNegativeSignedInt32 = NonNegativeSignedInt32.max()
    """The minimum number of parts in a path that belongs to a "deep" branch.
    [NonNegativeSignedInt32.max]
    [diffusion.internal.validation.pydantic.NonNegativeSignedInt32.max]
    if the query is not depth limited.
    """
    deep_branch_limit: NonNegativeSignedInt32 = NonNegativeSignedInt32.max()

    """The maximum number of paths to return for each deep branch.
    Int32.MAX_VALUE if the query is not depth limited.
    """
    with_unpublished_delayed_topics: pydantic.StrictBool = dc.field(default=False)
    """Whether unpublished delayed topics should be included in the results."""

    @property
    def topic_types_bitfield(self):
        return FetchQuerySerializer.to_int64(self.topic_types)

    @property
    def limit_encoded(self):
        return self.limit

    class Config(GenericConfig):
        P15_FQUERY = "protocol16-fetch-query.protocol15-fetch-query."

        mappings = {
            "protocol18-fetch-query": {
                f"{P15_FQUERY}topic-selector": "selector",
                f"{P15_FQUERY}fetch-range.fetch-range-from.fetch-range-element": "range_from",
                f"{P15_FQUERY}fetch-range.fetch-range-to.fetch-range-element": "range_to",
                f"{P15_FQUERY}topic-type-set": "topic_types_bitfield",
                f"{P15_FQUERY}fetch-with-values.boolean": "with_values",
                f"{P15_FQUERY}fetch-with-properties.boolean": "with_properties",
                f"{P15_FQUERY}fetch-limit": "limit_encoded",
                f"{P15_FQUERY}fetch-maximum-result-size": "maximum_result_size",
                "fetch-branch-depth-parameters.fetch-deep-branch-depth": "deep_branch_depth",
                "fetch-branch-depth-parameters.fetch-deep-branch-limit": "deep_branch_limit",
                "fetch-with-unpublished-delayed-topics.boolean": "with_unpublished_delayed_topics",  # noqa: F401, E501
            }
        }

        @classmethod
        def attr_mappings_all(cls, modelcls):
            return cls.mappings

    @property
    def range_from(self) -> Limit:
        return self.range.from_

    @property
    def range_to(self) -> Limit:
        return self.range.to

    def __post_init__(self):
        topic_types = self.topic_types
        self.__pydantic_validate_values__()
        object.__setattr__(self, "topic_types", topic_types)


class FetchQuerySerializer(GenericConfig[FetchQuery]):
    """
    The [FetchQuery][diffusion.features.topics.fetch.fetch_query.FetchQuery] serializer.

    """

    @classmethod
    def to_int64(
        cls, types: typing.FrozenSet[typing.Type[diffusion.datatypes.AbstractDataType]]
    ):
        representable_types = {x.type_code for x in types if hasattr(x, "type_code")}
        result = 0
        for type in representable_types:
            b = 1 << (int(type) & 255)
            result |= b
        return result
