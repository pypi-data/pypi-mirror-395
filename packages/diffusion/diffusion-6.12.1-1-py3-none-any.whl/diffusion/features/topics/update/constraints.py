#  Copyright (c) 2022 - 2024 DiffusionData Ltd., All Rights Reserved.
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
import itertools
import typing

from diffusion.internal.pydantic_compat.v1 import dataclasses as pydantic_v1_dataclasses
from diffusion.internal.pydantic_compat.v1 import StrictStr, StrictBytes
from typing_extensions import overload, Literal

from diffusion.datatypes import AbstractDataType
from diffusion.features.topics.update import UpdateConstraint, UpdateConstraint_T
from diffusion.internal.serialisers.generic_model import (
    GenericConfig
)
from diffusion.internal.services import ServiceValue
from diffusion.internal.topics.constraints import UpdateConstraintType
from diffusion.internal.utils import (
    validate_member_arguments_configured,
    BaseConfig,
)
from diffusion.internal.validation import StrictNonNegativeInt
from diffusion.session.locks.session_locks import SessionLock
if typing.TYPE_CHECKING:
    from diffusion.internal.serialisers import Serialiser


TypeGetter = typing.Callable[[typing.Any], typing.Type["AbstractDataType"]]


class ConstraintSingleton(typing.Generic[UpdateConstraint_T]):
    @functools.lru_cache(maxsize=None)
    def __get__(self, instance, owner) -> UpdateConstraint_T:
        return (owner or type(instance))()


class Unconstrained(UpdateConstraint):
    """
    The unconstrained update constraint.
    """

    Instance = typing.cast(typing.ClassVar[ConstraintSingleton], ConstraintSingleton())

    def __str__(self):
        return "Unconstrained"

    class Config(UpdateConstraint.Config["Unconstrained"]):
        @classmethod
        def id(cls) -> Literal[UpdateConstraintType.UNCONSTRAINED_CONSTRAINT]:
            return UpdateConstraintType.UNCONSTRAINED_CONSTRAINT

        @classmethod
        def attr_mappings_all(cls, modelcls):
            return {"unconstrained-constraint": {}}


ConjunctionConstraint_T = typing.TypeVar(
    "ConjunctionConstraint_T", bound="ConjunctionConstraint"
)


@pydantic_v1_dataclasses.dataclass(config=BaseConfig, eq=True, frozen=True)
class ConjunctionConstraint(UpdateConstraint):
    constraints: typing.Tuple[UpdateConstraint, ...]

    def __init__(
        self,
        constraints_begin: typing.Union[
            UpdateConstraint, typing.Tuple[UpdateConstraint, ...]
        ] = tuple(),
        second_term: typing.Optional[
            typing.Union[UpdateConstraint, typing.Tuple[UpdateConstraint, ...]]
        ] = tuple(),
    ):
        if isinstance(constraints_begin, UpdateConstraint):
            constraints_final = self.process_constraints(
                (*constraints_begin,), second_term
            )
        elif isinstance(constraints_begin, tuple):
            constraints_final = self.process_constraints(constraints_begin, second_term)
        else:
            constraints_final = constraints_begin
        object.__setattr__(self, "constraints", constraints_final)
        self.__pydantic_validate_values__()  # type: ignore
        object.__setattr__(self, "constraints", constraints_final)
        topic_constraints = self.get_topic_constraints()
        if len(list(zip(topic_constraints, range(2)))) > 1:
            raise ValueError(
                "Multiple topic constraints found: "
                f"{' and '.join(map(str, self.get_topic_constraints()))}."
            )

    @classmethod
    def process_constraints(
        cls, constraints_final, second_term
    ) -> typing.Tuple[UpdateConstraint, ...]:
        if not hasattr(second_term, "__iter__"):
            second_term = (second_term,)
        constraints_final += sum(
            ((*y,) if y is not None else (None,) for y in itertools.chain(second_term)),
            (),
        )
        return constraints_final

    def __str__(self):
        return f"Constraints=({', '.join(str(x) for x in self.constraints)})"

    def __iter__(self):
        return iter(self.constraints)

    class Config(UpdateConstraint.Config):
        @classmethod
        def id(cls) -> Literal[UpdateConstraintType.CONJUNCTION_CONSTRAINT]:
            return UpdateConstraintType.CONJUNCTION_CONSTRAINT

        @classmethod
        def as_service_value(
            cls: typing.Type[GenericConfig[ConjunctionConstraint_T]],
            item: ConjunctionConstraint_T,
            serialiser: typing.Optional[Serialiser] = None,
        ) -> ServiceValue:
            serialiser = cls.check_serialiser(serialiser)
            result = (
                typing.cast(GenericConfig[ConjunctionConstraint_T], super())
            ).as_service_value(item, serialiser)
            if len(item.constraints):
                constraint_tuples: typing.Tuple[typing.Any, ...] = sum(
                    (
                        (cls.entry_from_list_of_choices_as_tuple(x, serialiser),)
                        for x in item.constraints
                    ),
                    typing.cast(typing.Tuple[typing.Any, ...], tuple()),
                )
                result = result.evolve(**{"conjunction-constraint": constraint_tuples})
            return result


@pydantic_v1_dataclasses.dataclass(frozen=True, eq=True)
class BinaryValueConstraint(UpdateConstraint):
    """
    The update constraint that requires the exact binary value.
    """

    bytes: StrictBytes
    IsTopicConstraint: typing.ClassVar[bool] = True

    def __iter__(self):
        return iter((self,))

    def __str__(self):
        return f"Bytes={self.bytes}"

    class Config(
         UpdateConstraint.Config
    ):
        @classmethod
        def id(cls) -> Literal[UpdateConstraintType.BINARY_VALUE_CONSTRAINT]:
            return UpdateConstraintType.BINARY_VALUE_CONSTRAINT
        alias = "topic-value-constraint"

        @classmethod
        def attr_mappings_all(cls, modelcls: typing.Type[BinaryValueConstraint]):
            return {"topic-value-constraint": {"bytes": "bytes"}}


class NoValueConstraint(UpdateConstraint):
    """
    The update constraint that requires a topic to have no value.
    """

    Instance = typing.cast(typing.ClassVar["NoValueConstraint"], ConstraintSingleton())
    IsTopicConstraint: typing.ClassVar[bool] = True

    def __str__(self):
        return "NoValue"

    class Config(UpdateConstraint.Config["NoValueConstraint"]):
        @classmethod
        def id(cls) -> Literal[UpdateConstraintType.NO_VALUE_CONSTRAINT]:
            return UpdateConstraintType.NO_VALUE_CONSTRAINT

        # noinspection PyUnusedLocal
        @classmethod
        @functools.lru_cache(maxsize=None)
        def field_names(
            cls,
            modelcls: typing.Type[NoValueConstraint],
            serialiser: typing.Optional[Serialiser] = None,
        ) -> typing.List[str]:
            return []

        @classmethod
        def attr_mappings_all(cls, modelcls: typing.Type[NoValueConstraint]):
            return {"no-value-constraint": {}}


@pydantic_v1_dataclasses.dataclass(frozen=True)
class LockConstraint(UpdateConstraint):
    """
    The constraint on a [SessionLock][diffusion.session.locks.session_locks.SessionLock]
    """

    name: StrictStr
    sequence: StrictNonNegativeInt

    def _frozen_init(self, name: StrictStr, sequence: StrictNonNegativeInt):
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "sequence", sequence)

    @overload
    def __init__(self, session_lock: SessionLock):
        self._frozen_init(session_lock.name, session_lock.sequence)

    @overload
    def __init__(self, name: StrictStr, sequence: StrictNonNegativeInt):
        self._frozen_init(name, sequence)

    @validate_member_arguments_configured(check_overloads=True)
    def __init__(
        self,
        *args: typing.Union[StrictStr, StrictNonNegativeInt, SessionLock],
        **kwargs: typing.Union[StrictStr, StrictNonNegativeInt, SessionLock],
    ):
        raise NotImplementedError()  # pragma: no cover

    def __str__(self):
        return f"{type(self).__name__}(name='{self.name}', sequence={self.sequence})"

    class Config(UpdateConstraint.Config):
        @classmethod
        def id(cls) -> Literal[UpdateConstraintType.LOCKED_CONSTRAINT]:
            return UpdateConstraintType.LOCKED_CONSTRAINT

        @classmethod
        def attr_mappings_all(cls, modelcls: typing.Type[LockConstraint]):
            return {
                "locked-constraint": {
                    "session-lock-name": "name",
                    "session-lock-sequence": "sequence",
                }
            }


class NoTopicConstraint(UpdateConstraint):
    """
    The update constraint that requires the path to have no topic.
    """

    Instance = typing.cast(typing.ClassVar["NoTopicConstraint"], ConstraintSingleton())
    IsTopicConstraint: typing.ClassVar[bool] = True

    def __str__(self):
        return "NoTopic"

    class Config(UpdateConstraint.Config):
        @classmethod
        def id(cls) -> Literal[UpdateConstraintType.NO_TOPIC_CONSTRAINT]:
            return UpdateConstraintType.NO_TOPIC_CONSTRAINT

        @classmethod
        def attr_mappings_all(cls, modelcls: typing.Type[NoTopicConstraint]):
            return {"no-topic-constraint": {}}


WithValuesType = typing.Tuple[typing.Tuple[str, bytes], ...]


PartialJSONType = typing.TypeVar("PartialJSONType")
"""
Instance of PartialJSON or any subclasses
"""


@pydantic_v1_dataclasses.dataclass(config=BaseConfig, frozen=True, eq=True)
class PartialJSON(UpdateConstraint):
    """
    The constraint requiring the current value of the
    [JSON][diffusion.datatypes.JSON] topic to match the
    partially described value.
    """

    IsTopicConstraint: typing.ClassVar[bool] = True

    with_values: WithValuesType
    without_values: typing.FrozenSet[str]

    @property
    def with_values_dict(self) -> typing.Mapping[str, typing.Any]:
        return dict(self.with_values)

    def __init__(
        self, with_values, without_values: typing.FrozenSet[str] = frozenset()
    ):
        object.__setattr__(self, "with_values", with_values)
        object.__setattr__(self, "without_values", without_values)
        self.__pydantic_validate_values__()  # type: ignore
        object.__setattr__(self, "with_values", with_values)
        object.__setattr__(self, "without_values", without_values)

    @validate_member_arguments_configured(
        deferred=lambda: dict(PartialJSONType=PartialJSONType)
    )
    def with_(
        self: PartialJSONType, pointer: StrictStr, value: AbstractDataType
    ) -> "PartialJSONType":
        """
        Requires a value at a specific position in the JSON object.

        Notes:
            The `pointer` is a JSON Pointer (https://tools.ietf.org/html/rfc6901) syntax reference
            locating the `value` in the JSON object.

            The `pointer` syntax is not being verified for correctness.

        Args:
            pointer: The pointer expression.
            value: The value.

        Returns:
            The constraint including the specified `pointer`.
        """  # NOQA
        assert isinstance(self, PartialJSON)
        return typing.cast(PartialJSONType, self._with_impl(pointer, value))

    def _with_impl(self, pointer: StrictStr, value: AbstractDataType):
        new_with_values: typing.Dict[str, bytes] = {**dict(self.with_values)}
        new_without_values = frozenset(self.without_values)
        for k, v in self.with_values:
            new_with_values[k] = v
        new_with_values[pointer] = value.to_bytes()
        final_without_values = new_without_values - frozenset({pointer})
        return type(self)(tuple(new_with_values.items()), final_without_values)

    @validate_member_arguments_configured(
        deferred=lambda: dict(PartialJSON=PartialJSON, PartialJSONType=PartialJSONType)
    )
    def without(self: PartialJSONType, pointer: StrictStr) -> "PartialJSONType":
        """
        Requires a specific position in the JSON object to be empty.

        Notes:
            The `pointer` is a JSON Pointer (https://tools.ietf.org/html/rfc6901) syntax reference
            that should have no value in the JSON object.

            The `pointer` syntax is not being verified for correctness.

        Args:
            pointer: The pointer expression.

        Returns:
            The constraint including the specified `pointer`.
        """  # NOQA
        assert isinstance(self, PartialJSON)
        new_with_values = {k: v for k, v in self.with_values if k is not pointer}
        return typing.cast(PartialJSONType, type(self)(
            tuple(new_with_values.items()),
            self.without_values.union(frozenset({pointer})),
        ))

    def __str__(self):
        return f"with_values={self.with_values}, without_values={self.without_values}"

    class Config(UpdateConstraint.Config):
        @classmethod
        def id(cls) -> Literal[UpdateConstraintType.PARTIAL_JSON_CONSTRAINT]:
            return UpdateConstraintType.PARTIAL_JSON_CONSTRAINT

        @classmethod
        def attr_mappings_all(cls, modelcls: typing.Type[PartialJSON]):
            return {
                "partial-json-constraint": {
                    "partial-json-constraint-with": "with_values",
                    "partial-json-constraint-without": "without_values",
                }
            }
