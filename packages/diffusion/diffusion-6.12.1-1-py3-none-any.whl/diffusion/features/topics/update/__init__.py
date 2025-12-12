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

import abc
import typing

from diffusion.internal.serialisers.base import ChoiceProvider, ChoiceEncoder
from diffusion.internal.serialisers.generic_model import GenericConfig, GenericModel, \
    GenericModel_T
from diffusion.internal.topics.constraints import UpdateConstraintType

if typing.TYPE_CHECKING:
    from diffusion.internal.serialisers import Serialiser

from diffusion.internal.serialisers.generic_model_protocol import GenericModelProtocol


class TopicCreationResult:
    CREATED = 0
    EXISTS = 1


UpdateConstraint_T = typing.TypeVar("UpdateConstraint_T", bound="UpdateConstraint")


class UpdateConstraint(abc.ABC, GenericModel):
    """
    The constraint to be applied to an update operation or the creation of an update stream.

    Notes:
        Constraints describe a condition that must be satisfied for an operation to succeed. Constraints can be applied
        to the setting of a value or creation of an update stream. Constraints are only evaluated on the server.

        The constraints are evaluated using the:

        - active session locks
        - existence of the topic
        - current value of the topic

        The value of a topic can be described in several ways. The value can be described as an exact value, a partial
        value or an unset value.

        Constraints can be composed with one another. It is only possible to construct logical ANDs of constraints.
        Constraints can only be composed if the resulting constraint is satisfiable. Multiple session locks can be held
        but a topic can only have a single value. Constraints specifying multiple topic values can't be constructed.

        Constraints can be created using a [ConstraintFactory][diffusion.features.topics.update.constraint_factory.ConstraintFactory].

    """  # NOQA

    @property
    def values(self):
        return self.Config.as_tuple(self)[1:]

    @classmethod
    def __get_validators__(cls):
        def validator(instance):
            if not isinstance(instance, cls):
                raise ValueError(f"{instance} is not a {cls}")
            return instance

        yield validator

    def __call__(self):
        return self

    def __rand__(self, other: UpdateConstraint) -> UpdateConstraint:
        return other & self

    def __and__(self, other: UpdateConstraint) -> UpdateConstraint:
        """
        Creates a composed constraint that represents a logical AND of this constraint and another.
        
        Notes:
            You must use the binary `&` form to invoke this due to short-circuiting.

        Args:
            other: The constraint that will be logically-ANDed with the current constraint.

        Returns:
            The newly composed constraint that represents a logical AND of the current constraint and the
                `other` constraint.

        """  # NOQA
        from diffusion.features.topics.update.constraints import ConjunctionConstraint
        if other is None:
            raise ValueError("other")
        return ConjunctionConstraint(self, other)

    def __iter__(self):
        return iter([self])

    IsTopicConstraint: typing.ClassVar[bool] = False

    def get_topic_constraints(self):
        return filter(lambda x: x.IsTopicConstraint is True, self)

    def to_bytes(self):
        return self.Config.to_bytes(self, self.Config.serialiser("update-constraint"))

    class Config(typing.Generic[GenericModel_T], GenericConfig[GenericModel_T],
                 ChoiceProvider[UpdateConstraintType]):
        alias = "update-constraint"

        @classmethod
        def attr_mappings_all(cls, modelcls: typing.Type[GenericModel_T]):
            return {
                "update-constraint": {
                    cls.serialiser("update-constraint")
                    .to_encoder(ChoiceEncoder)
                    .get_serialiser_by_provider(
                        typing.cast(UpdateConstraint.Config, modelcls.Config)
                    ): modelcls
                }
            }

        @classmethod
        def as_tuple(
            cls, item: GenericModel_T, serialiser: typing.Optional[Serialiser] = None
        ) -> typing.Tuple[typing.Any, ...]:

            return (typing.cast(UpdateConstraint, item).Config.id(),) + super().as_tuple(
                item, serialiser
            )

        @classmethod
        def to_bytes(
            cls, item: GenericModel_T, serialiser: typing.Optional[Serialiser] = None
        ) -> bytes:
            serialiser = cls.check_serialiser(serialiser)
            as_tuple = serialiser.to_encoder(ChoiceEncoder).as_tuple(
                typing.cast(GenericModelProtocol, item)
            )
            return serialiser.to_bytes(as_tuple)
