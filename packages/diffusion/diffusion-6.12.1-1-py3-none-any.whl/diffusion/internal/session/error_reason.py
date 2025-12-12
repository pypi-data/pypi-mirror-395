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


@dataclasses.dataclass
class ErrorReasonPrototype:
    code: int
    description: str


class GenericErrorReason(enum.Enum):

    """
    Reason codes used to report error conditions.

    An application can check whether an ErrorReason is equal to some expected
    value using {@link Object#equals(Object)}. Equality is derived from the
    {@link #getReasonCode() reasonCode}, with instances with equal codes
    considered equal.

    Some common ErrorReason values are defined as constants in this class. More
    specific reasons may be defined by individual
    {@link com.pushtechnology.diffusion.client.session.Feature features}.

    @author DiffusionData Limited
    @since 5.1
    @see Callback#onError
    @see ServerHandler#onError
    """

    COMMUNICATION_FAILURE = ErrorReasonPrototype(
        100, "Communication with server failed"
    )
    """

    Communication with the server failed.
    """
    SESSION_CLOSED = ErrorReasonPrototype(101, "Session is closed")
    """

    Communication with the server failed because the session is closed.
    """

    REQUEST_TIME_OUT = ErrorReasonPrototype(102, "Request time out")
    """

    Communication with the server failed because a service request timed out.
    """
    ACCESS_DENIED = ErrorReasonPrototype(103, "Access denied")
    """

    The request was rejected because the caller has insufficient permissions.
    """
    UNSUPPORTED = ErrorReasonPrototype(104, "Unsupported service")

    """

    The request was rejected because the requested service is unsupported for this caller.
    @since 5.9

    """

    CALLBACK_EXCEPTION = ErrorReasonPrototype(
        105,
        "An application callback threw an exception. Check logs for more information.",
    )
    """

    An application callback threw an exception. Check logs for more information.
    @since 5.9

    """

    INVALID_DATA = ErrorReasonPrototype(106, "Invalid data.")
    """

    An operation failed because invalid data was received.
    @since 6.0

    """

    NO_SUCH_SESSION = ErrorReasonPrototype(107, "No session was found")
    """

    The session does not exist on the server.
    @since 6.0

    """

    INCOMPATIBLE_DATATYPE = ErrorReasonPrototype(108, "Datatype is incompatible")
    """

    A datatype operation has failed due to incompatibility.
    @since 6.0

    """

    UNHANDLED_MESSAGE = ErrorReasonPrototype(109, "A message was not handled")
    """

    A message was not handled by the server.
    @since 6.0

    """
    CLUSTER_REPARTITION = ErrorReasonPrototype(
        110, "The cluster was repartitioning and the request could not be routed."
    )

    """
    A cluster operation failed because partition ownership changed during
    processing.

    This is a transient error that occurs while the cluster is recovering
    from failure. The session can retry the operation.

    @since 6.0
    @see #CLUSTER_ROUTING
    """

    INCOMPATIBLE_STATE = ErrorReasonPrototype(
        111,
        "Topic operation not performed because it is managed by"
        "a component that prohibits external updates",
    )
    """
    A topic update could not be performed because the topic is managed by a
    component (for example, fan-out) which prohibits external updates.

    @since 6.0
    """

    CLUSTER_ROUTING = ErrorReasonPrototype(
        112, "The cluster operation could not be routed."
    )
    """
    A cluster operation failed to be routed to a server within the cluster
    due to a communication failure, or the server that owns a partition is
    not currently known.

    This is a transient error that occurs while the cluster is recovering
    from failure. The session can retry the operation.

    @since 6.5
    @see #CLUSTER_REPARTITION
    """

    TOPIC_TREE_REGISTRATION_CONFLICT = ErrorReasonPrototype(
        200, "A conflicting registration exists on the same branch of the topic tree"
    )
    """

    A conflicting registration exists on the same branch of the topic tree.
    """

    HANDLER_CONFLICT = ErrorReasonPrototype(201, "Conflict with existing handler")

    """
    A conflicting registration exists.
    """
    INVALID_PATH = ErrorReasonPrototype(202, "Invalid path")
    """

    An invalid path was supplied.
    """
