#  Copyright (c) 2022 - 2025 DiffusionData Ltd., All Rights Reserved.
#
#  Use is subject to licence terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of DiffusionData. The intellectual and technical
#  concepts contained herein are proprietary to DiffusionData and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

import dataclasses
import enum
import functools
import typing

from diffusion.features.control.session_trees.invalid_branch_mapping_exception import (
    InvalidBranchMappingError,
)
from diffusion.internal.hashable_dict import HashableDict
from diffusion.internal.serialisers import get_serialiser
from diffusion.internal.serialisers.generic_model_protocol import CombinedMapping
from diffusion.internal.session.error_reason import (
    ErrorReasonPrototype,
    GenericErrorReason,
)

from diffusion import DiffusionError
from diffusion.datatypes import IncompatibleDatatypeError
from diffusion.internal.protocol.exceptions import ServiceMessageError
from diffusion.internal.serialisers.pydantic import MarshalledModel
from diffusion.session.exceptions import (
    IncompatibleTopicError,
    UpdateFailedError,
    NoSuchTopicError,
    NoSuchEventError,
    ExistingTopicError,
    InvalidTopicPathError,
    InvalidTopicSpecificationError,
    TopicLicenseLimitError,
    IncompatibleExistingTopicError,
    AddTopicError,
    UnsatisfiedConstraintError,
    InvalidUpdateStreamError,
    IncompatibleTopicStateError,
    HandlerConflictError,
    UnhandledMessageError,
    NoSuchSessionError,
    CancellationError,
    RejectedRequestError,
)
from diffusion.exceptions import ClusterRoutingError, ClusterRepartitionError


class ErrorReason(MarshalledModel):
    reason_code: int
    description: typing.Optional[str]

    class Config(MarshalledModel.Config):
        alias = "error-reason"

        @classmethod
        def attr_mappings_combined(
            cls, modelcls
        ) -> typing.Mapping[str, CombinedMapping]:
            return {
                "error-reason": CombinedMapping(
                    {"reason-code": "reason_code", "description": "description"}
                )
            }


class ErrorReasonEnum(enum.Enum):
    INCOMPATIBLE_UPDATE = ErrorReasonPrototype(
        500, "Update type is incompatible with topic type"
    )
    """
    Used by TopicUpdate operations.
    """

    UPDATE_FAILED = ErrorReasonPrototype(
        501, "Update failed - possible content incompatibility"
    )
    """
    Used by TopicUpdate operations.

    """

    MISSING_TOPIC = ErrorReasonPrototype(503, "Topic does not exist")
    """
    Used by TopicUpdate operations.
    """

    DELTA_WITHOUT_VALUE = ErrorReasonPrototype(
        505,
        "An attempt has been made to apply a delta to a topic that does not yet have a value",
    )
    """
    Only used in deprecated server services - no need to retain in client
    after 6.6.
    """

    NO_SUCH_TOPIC = ErrorReasonPrototype(9000, "No topic was found")
    """
    Error reason.
    """

    NOT_A_TIMESERIES_TOPIC = ErrorReasonPrototype(
        9001, "Topic is not a time series topic"
    )
    """
    Error reason.
    """

    NO_SUCH_EVENT = ErrorReasonPrototype(9002, "No time series event was found")
    """
    Error reason.
    """

    REJECTED_REQUEST = ErrorReasonPrototype(
        9003, "A request has been rejected by the recipient session"
    )
    """
    Error reason.
    """

    TOPIC_EXISTS_MISMATCH = ErrorReasonPrototype(
        9004,
        "A topic could not be added because one already exists with a different specification",
    )
    """
    Error reason.
    """

    TOPIC_PATH_INVALID = ErrorReasonPrototype(
        9005, "A topic could not be added because an invalid path was specified"
    )
    """
    Error reason.
    """

    TOPIC_SPECIFICATION_INVALID = ErrorReasonPrototype(
        9006, "A topic could not be added because an invalid specification was supplied"
    )
    """
    Error reason.
    """

    TOPIC_LICENSE_LIMIT = ErrorReasonPrototype(
        9007,
        "A topic could not be added because the topic would breach a licensing limit",
    )
    """
    Error reason.
    """

    INCOMPATIBLE_TOPIC_EXISTS = ErrorReasonPrototype(
        9010,
        "A topic could not be added because an incompatible topic"
        "already exists at the specified path",
    )
    """
    This differs from {@link #TOPIC_EXISTS_MISMATCH} as the reason is that
    the existing topic is owned by something that prevents the caller
    managing. The specification of the existing topic may be the same.
    """

    UNEXPECTED_TOPIC_ADD_FAILURE = ErrorReasonPrototype(
        9011, "An unexpected error occurred when creating a topic"
    )
    """
    Error reason.
    """

    UNSATISFIED_CONSTRAINT = ErrorReasonPrototype(
        9012, "The topic update failed because the constraint was not satisfied"
    )
    """
    Error reason.
    @since 6.2
    """

    INVALID_UPDATE_STREAM = ErrorReasonPrototype(
        9013, "The topic update failed because the update stream is no longer valid"
    )
    """
    Error reason.
    @since 6.2
    """

    INVALID_JSON_PATCH = ErrorReasonPrototype(9014, "Parsing the JSON patch failed")
    """
    Error reason.
    @since 6.4
    """

    APPLY_PATCH_FAIL = ErrorReasonPrototype(
        9015,
        "The JSON patch failed to apply. This happens when attempting "
        + "to parse an illegal CBOR value.",
    )
    """
    Error reason.
    @since 6.4
    """

    REMOTE_SERVER_EXISTS = ErrorReasonPrototype(
        9016, "A remote server with the specified name already exists"
    )
    """
    Error reason.
    @since 6.4

    """

    INVALID_BRANCH_MAPPING = ErrorReasonPrototype(
        9017, "An invalid branch mapping was supplied"
    )
    """
    Error reason.
    @since 6.7
    """


@dataclasses.dataclass
class ReasonPrototypeBase(object):
    description: str
    target_type: typing.Type[DiffusionError] = ServiceMessageError
    extra: typing.Optional[str] = None


class ErrorReasonException(object):
    REASON_TO_EXCEPTION_MAPPING: typing.Mapping[
        typing.Union[ErrorReasonEnum, GenericErrorReason],
        typing.Type[DiffusionError],
    ] = {
        ErrorReasonEnum.MISSING_TOPIC: NoSuchTopicError,
        ErrorReasonEnum.NO_SUCH_TOPIC: NoSuchTopicError,
        # ordering is important so that NoSuchTopicException -> NO_SUCH_TOPIC
        GenericErrorReason.HANDLER_CONFLICT: HandlerConflictError,
        # ordering is important so that IncompatibleTopicException -> INCOMPATIBLE_UPDATE
        ErrorReasonEnum.NOT_A_TIMESERIES_TOPIC: IncompatibleTopicError,
        ErrorReasonEnum.INCOMPATIBLE_UPDATE: IncompatibleTopicError,
        ErrorReasonEnum.UPDATE_FAILED: UpdateFailedError,
        ErrorReasonEnum.NO_SUCH_EVENT: NoSuchEventError,
        GenericErrorReason.NO_SUCH_SESSION: NoSuchSessionError,
        GenericErrorReason.UNHANDLED_MESSAGE: UnhandledMessageError,
        GenericErrorReason.INCOMPATIBLE_DATATYPE: IncompatibleDatatypeError,
        ErrorReasonEnum.REJECTED_REQUEST: RejectedRequestError,
        GenericErrorReason.REQUEST_TIME_OUT: CancellationError,
        GenericErrorReason.CLUSTER_ROUTING: ClusterRoutingError,
        GenericErrorReason.CLUSTER_REPARTITION: ClusterRepartitionError,
        ErrorReasonEnum.TOPIC_EXISTS_MISMATCH: ExistingTopicError,
        ErrorReasonEnum.TOPIC_PATH_INVALID: InvalidTopicPathError,
        ErrorReasonEnum.TOPIC_SPECIFICATION_INVALID: InvalidTopicSpecificationError,
        ErrorReasonEnum.TOPIC_LICENSE_LIMIT: TopicLicenseLimitError,
        ErrorReasonEnum.INCOMPATIBLE_TOPIC_EXISTS: IncompatibleExistingTopicError,
        ErrorReasonEnum.UNEXPECTED_TOPIC_ADD_FAILURE: AddTopicError,
        ErrorReasonEnum.UNSATISFIED_CONSTRAINT: UnsatisfiedConstraintError,
        GenericErrorReason.INCOMPATIBLE_STATE: IncompatibleTopicStateError,
        ErrorReasonEnum.INVALID_UPDATE_STREAM: InvalidUpdateStreamError,
        ErrorReasonEnum.INVALID_BRANCH_MAPPING: InvalidBranchMappingError,
    }

    CODE_TO_EXCEPTION_MAPPING: typing.Mapping[int, ReasonPrototypeBase] = {
        k.value.code: ReasonPrototypeBase(k.value.description, v)
        for k, v in REASON_TO_EXCEPTION_MAPPING.items()
    }

    @classmethod
    def convert_exception(
        cls, reason: ErrorReason, message: typing.Optional[str]
    ) -> typing.Union[ServiceMessageError, DiffusionError]:
        reason_type = cls.CODE_TO_EXCEPTION_MAPPING.get(
            reason.reason_code, ReasonPrototypeBase("", ServiceMessageError)
        )
        message = message or reason.description or reason_type.description
        target_type = reason_type.target_type

        return target_type(message, reason_code=reason.reason_code)

    @classmethod
    @functools.lru_cache
    def reverse_mapping(
        cls,
    ) -> typing.Mapping[
        typing.Type[DiffusionError],
        typing.Union[ErrorReasonEnum, GenericErrorReason],
    ]:
        return ~HashableDict(cls.REASON_TO_EXCEPTION_MAPPING)


    @classmethod
    def from_exception(
        cls, exc: DiffusionError
    ) -> typing.Optional[ErrorReason]:
        entry: typing.Optional[typing.Union[ErrorReasonEnum, GenericErrorReason]] = (
            cls.reverse_mapping().get(type(exc), None)
        )
        if not entry:
            return None
        return ErrorReason(
            reason_code=entry.value.code, description=next(iter(exc.args), str(exc))
        )


    @classmethod
    def read(
        cls, stream, message: typing.Optional[str] = None
    ) -> typing.Union[ServiceMessageError, DiffusionError]:
        reason = ErrorReason.Config.read(
            ErrorReason, stream, get_serialiser("error-reason")
        )
        return cls.convert_exception(reason, message)
