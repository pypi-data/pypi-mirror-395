#  Copyright (c) 2022 - 2025 DiffusionData Ltd., All Rights Reserved.
#
#  Use is subject to licence terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of DiffusionData. The intellectual and technical
#  concepts contained herein are proprietary to DiffusionData and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

import abc
import typing

from diffusion.datatypes import AbstractDataType
from diffusion.internal.topics.constraints import UpdateConstraintType

from diffusion.features.topics.update.constraints import (
    NoValueConstraint,
    NoTopicConstraint,
    PartialJSON,
    BinaryValueConstraint,
    ConjunctionConstraint,
    Unconstrained, LockConstraint,
)
import diffusion.datatypes
from diffusion.internal.utils import validate_member_arguments


class ConstraintFactory(abc.ABC):
    """
    The factory for the update constraint types.
    """

    @property
    def json_value(self) -> PartialJSON:
        """
        Gets the constraint that partially matches the current topic value.

        Notes:
            The topic must be a [diffusion.datatypes.JSON][] topic.
            The [diffusion.features.topics.update.constraints.PartialJSON][] partially
            describes the structure of a [diffusion.datatypes.JSON][] value.

        Returns:
            The constraint.
        """
        return self._JSONValue

    JSONValue = json_value

    @property
    def no_value(self) -> NoValueConstraint:
        """
        Gets the constraint requiring the topic to have no value.

        Notes:
            This is useful when setting the first value of a topic.
            This constraint is unsatisfied if no topic is present at the path,
            making it unsuitable for operations that try to add topics.

        Returns:
            The constraint.
        """
        return NoValueConstraint.Instance

    @property
    def no_topic(self) -> NoTopicConstraint:
        """
        Gets the constraint requiring the path to have no topic.

        Notes:
            This is useful when setting the first value of a topic being added using
            [Topics.add_and_set_topic][diffusion.features.topics.Topics.add_and_set_topic]
            without changing the value if the topic already exists.
            This constraint is unsatisfied if a topic is present at the path,
            making it unsuitable for operations that try to set topics without adding them.

        Returns:
            The constraint.
        """
        return NoTopicConstraint.Instance

    def __init__(self, data_types=None):
        self.dataTypes = data_types or diffusion.datatypes.get
        self._JSONValue = PartialJSON(tuple(), frozenset())

    locked = LockConstraint

    @validate_member_arguments
    def value(self, value: typing.Union[AbstractDataType, bytes]) -> BinaryValueConstraint:
        """
        Creates a constraint requiring the current value of the topic
        to match the supplied value.

        Notes:
            When a None value, the topic is set to
            have no value. Use the
            [NoValueConstraint][diffusion.features.topics.update.constraints.NoValueConstraint]
            constraint to check if the topic has no value.

            This is useful when changing the value of a topic.
            This constraint is unsatisfied if no topic is present at
            the path, making it unsuitable for operations that try to add topics.

        Args:
            value: The value.

        Returns:
            The update constraint.
        """
        if value is None:
            raise ValueError("value")
        return BinaryValueConstraint(bytes(value))  # type: ignore

    def from_type(self, param: UpdateConstraintType, *args):
        action = {
            UpdateConstraintType.NO_VALUE_CONSTRAINT: self.no_value,
            UpdateConstraintType.NO_TOPIC_CONSTRAINT: self.no_topic,
            UpdateConstraintType.BINARY_VALUE_CONSTRAINT: self.value,
            UpdateConstraintType.PARTIAL_JSON_CONSTRAINT: self.JSON,
            UpdateConstraintType.LOCKED_CONSTRAINT: self.locked,
            UpdateConstraintType.CONJUNCTION_CONSTRAINT: ConjunctionConstraint,
            UpdateConstraintType.UNCONSTRAINED_CONSTRAINT: Unconstrained.Instance,
        }.get(param)
        assert action is not None
        return action(*args)

    def JSON(self, *args):  # noqa: N802
        return self.json(*args)

    def json(self, *args):
        return PartialJSON(tuple(args[0].items()), next(iter(args[1:]), frozenset()))
