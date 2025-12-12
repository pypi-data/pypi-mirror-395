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

import dataclasses

import traceback
import typing

from typing_extensions import Self, overload, Never
import diffusion.internal.pydantic_compat.v1 as pydantic

import diffusion.datatypes
from diffusion.datatypes import TimeSeriesEventDataType
from diffusion.features.topics.fetch.fetch_common import IVoidFetch
from diffusion.features.topics.fetch.fetch_query import (
    FetchQuery,
    FetchRange,
    LimitExisting,
)
from diffusion.features.topics.fetch.fetch_result import FetchResult, DecodedFetchResult
from diffusion.features.topics.fetch.types import (
    TValue,
    TopicTypeSet_Internal,
    ALL_TOPIC_TYPES,
    TNewValue,
    TNewValue_Not_IVoidFetch,
    FetchQueryValueType,
    FetchQueryValueType_Not_WildCard,
    TopicTypeSet,
    ALL_TOPIC_TYPES_NOT_IVOIDFETCH,
    FQVTWrapper
)
from diffusion.handlers import LOG
from diffusion.internal.serialisers.generic_model import GenericModel
from diffusion.internal.session import InternalSession
from diffusion.internal.utils import BaseConfig, validate_member_arguments
from diffusion.internal.validation import StrictNonNegativeInt, StrictStr
from diffusion.internal.validation.pydantic import (
    SignedInt32,
    MaximumResultSize,
    NonNegativeSignedInt32,
)


@dataclasses.dataclass
class FetchContext:
    session: InternalSession
    """ The internal session """
    maximum_message_size: StrictNonNegativeInt
    """ The maximum message size. """


FetchSelf = typing.TypeVar("FetchSelf", bound="FetchRequest")


@pydantic.dataclasses.dataclass(frozen=True, config=BaseConfig, validate_on_init=False)
class FetchRequest(typing.Generic[TValue], GenericModel):
    """

    The generic version of [FetchResult][diffusion.features.topics.fetch.fetch_result.FetchResult] that is typed to a particular value type.

    Notes:
    This defines a fetch request to be made to the server. A request can be created using the
    [FetchRequest][diffusion.features.topics.fetch.fetch_request.FetchRequest] property and modified to specify a range of topics and/or various levels of
    detail.

    The fetch request is issued to the server using the
    [fetch][diffusion.features.topics.fetch.fetch_request.FetchRequest.fetch] method supplying a topic
    selector which specifies the selection of topics.

    A range is defined as being between two points of the topic tree which is ordered in full path name order. So
    an example tree order would be:

    - a

    - a/b

    - a/c

    - a/c/x

    - a/c/y

    - a/d

    - a/e

    - b

    - b/a/x

    - b/b/x

    - c

    The start point of a range can be specified using [from_][diffusion.features.topics.fetch.fetch_request.FetchRequest.from_] or [after][diffusion.features.topics.fetch.fetch_request.FetchRequest.after]
    and an end point using [to][diffusion.features.topics.fetch.fetch_request.FetchRequest.to] or [before][diffusion.features.topics.fetch.fetch_request.FetchRequest.before]. [from_][diffusion.features.topics.fetch.fetch_request.FetchRequest.from_] and
    [to][diffusion.features.topics.fetch.fetch_request.FetchRequest.to] include any topic with the specified path in the selection, whereas
    [after][diffusion.features.topics.fetch.fetch_request.FetchRequest.after] and [before][diffusion.features.topics.fetch.fetch_request.FetchRequest.before] are non-inclusive and useful for paging through a
    potentially large range of topics. If no start point is specified, the start point is assumed to be the logical
    beginning of the topic tree. Similarly, if no end point is specified, the end point is the logical end of the
    topic tree. Ranges should be within the scope indicated by the topic selector used when issuing the fetch.

    As a minimum, the path and type of each topic selected will be returned. It is also possible to request that
    the topic values and/or properties are returned.

    If values are selected then the topic types selected are naturally constrained by the value class indicated. So
    if [OBJECT][diffusion.datatypes.OBJECT] will return values for all topic types.

    To select topic types when values are not required, or to further constrain the selection when values are
    required, it is also possible to specify exactly which topic types to select.

    A limit on the number of results returned can be specified using [first][diffusion.features.topics.fetch.fetch_request.FetchRequest.first]. This is advisable
    when the result set could potentially be large. When such a limit is used then the result will indicate whether
    more results for the same selection would be available via the [FetchResult.has_more][diffusion.features.topics.fetch.fetch_result.FetchResult.has_more] property.

    The request can be sent to the server using [fetch][diffusion.features.topics.fetch.fetch_request.FetchRequest.fetch] and the results are returned in
    path order, earliest path first, starting from the beginning of any range specified.

    It is also possible to request results from the end of the range indicated by specifying a limit to the number
    of results using [last][diffusion.features.topics.fetch.fetch_request.FetchRequest.last]. This returns up to the specified number of results from the end of
    the range, in path order. This is useful for paging backwards through a range of topics.

    If values are requested, the request and results are typed to the value type ([FetchRequest[TValue]][diffusion.features.topics.fetch.fetch_request.FetchRequest])
    and [FetchResult[TValue]][diffusion.features.topics.fetch.fetch_result.FetchResult] respectively), otherwise the
    non-generic versions of [FetchRequest][diffusion.features.topics.fetch.fetch_request.FetchRequest] and [FetchResult][diffusion.features.topics.fetch.fetch_result.FetchResult] are being used.

    ROUTING topics are *not supported*, and if encountered will be ignored (i.e.
    treated as if they did not exist).
    *

    [FetchRequest[TValue]][diffusion.features.topics.fetch.fetch_request.FetchRequest] instances are immutable and can be safely shared and reused.

    Added in version 6.11.
    """  # noqa: E501, W291

    tp_: typing.Type[TValue]
    fetch_context: FetchContext
    range: FetchRange
    topic_types_: TopicTypeSet_Internal
    with_properties_: pydantic.StrictBool = dataclasses.field()
    limit: SignedInt32 = SignedInt32.max()
    maximum_result_size_: MaximumResultSize = MaximumResultSize(0)
    deep_branch_depth: NonNegativeSignedInt32 = NonNegativeSignedInt32.max()
    deep_branch_limit: NonNegativeSignedInt32 = NonNegativeSignedInt32.max()
    with_unpublished_delayed_topics_: pydantic.StrictBool = False
    decode_timeseries: pydantic.StrictBool = False

    def __post_init__(self) -> None:
        topic_types = self.topic_types_

        try:
            # noinspection PyUnresolvedReferences
            self.__pydantic_validate_values__()  # type: ignore[attr-defined]
        except Exception as e:  # pragma: no cover
            LOG.error(f"Got {e}: {traceback.format_exc()}")
            raise
        object.__setattr__(self, "topic_types_", topic_types)

    @classmethod
    def can_read_as(
        cls,
        new_value_t: typing.Type[FetchQueryValueType],
        topic_type: typing.Type[FetchQueryValueType]
    ):
        from diffusion.datatypes.conversion.default import DEFAULT_CONVERTER
        new_value_t = typing.cast(
            typing.Type[FetchQueryValueType], DEFAULT_CONVERTER(new_value_t)
        )
        topic_type = typing.cast(
            typing.Type[FetchQueryValueType], DEFAULT_CONVERTER(topic_type)
        )
        if (
            not issubclass(new_value_t, TimeSeriesEventDataType)
            and new_value_t not in ALL_TOPIC_TYPES
        ):
            return False

        return (
            topic_type.can_read_as(
                typing.cast(typing.Type[FetchQueryValueType_Not_WildCard], new_value_t)
            )
            if topic_type is not None
            else False
        )

    def validate(self):
        for topic_type in self.topic_types_:
            if (
                self.tp_ != IVoidFetch
                and not self.can_read_as(topic_type=topic_type, new_value_t=self.tp_)
                and topic_type != diffusion.datatypes.TIME_SERIES
            ):
                raise ValueError(
                    f"Invalid topic type {topic_type}, not readable by {self.tp_}"
                )

    @classmethod
    def create(
        cls,
        internal_session: InternalSession,
        tp: typing.Type[TNewValue],
        max_message_size: MaximumResultSize,
    ) -> FetchRequest[TNewValue]:
        return FetchRequest(
            tp,
            FetchContext(internal_session, max_message_size),
            FetchRange.unbounded(),
            ALL_TOPIC_TYPES_NOT_IVOIDFETCH,
            False,
            SignedInt32.max(),
            max_message_size,
        )

    def from_(self, topic_path: StrictStr) -> FetchRequest[TValue]:
        """
        Specifies a logical start point within the topic tree.

        Notes:
            If specified, only results for topics with a path that is lexically equal to or 'after' the specified path
            will be returned.

            This is the inclusive equivalent of [after][diffusion.features.topics.fetch.fetch_request.FetchRequest.after] and if used will override any previous
            [after][diffusion.features.topics.fetch.fetch_request.FetchRequest.after] or [from_][diffusion.features.topics.fetch.fetch_request.FetchRequest.from_] constraint.

        Args:
            topic_path: The topic path from which results are to be returned.

        Returns:
            The fetch request derived from this fetch request but selecting only topics from the specified path onwards (inclusive).

        """  # noqa: E501, W291
        # see https://github.com/pydantic/pydantic/issues/7075
        result = dataclasses.replace(
            self,  # type: ignore
            range=FetchRange(LimitExisting(topic_path, True), self.range.to)
        )

        return typing.cast(FetchRequest[TValue], result)

    def after(self, topic_path: StrictStr) -> FetchRequest[TValue]:
        """
        Specifies a logical start point within the topic tree.

        Notes:
            If specified, only results for topics with a path that is lexically 'after' the specified path will be
            returned.

            This is the non-inclusive equivalent of [from_][diffusion.features.topics.fetch.fetch_request.FetchRequest.from_] and if used will override any previous
            [from_][diffusion.features.topics.fetch.fetch_request.FetchRequest.from_] or
            [after][diffusion.features.topics.fetch.fetch_request.FetchRequest.after] constraint.

        Args:
            topic_path: The topic path after which results are to be returned.

        Returns:
            The fetch request derived from this fetch request but selecting only topics after the specified path (not inclusive).

        """  # noqa: E501, W291
        # see https://github.com/pydantic/pydantic/issues/7075
        result = dataclasses.replace(
            self,  # type: ignore
            range=FetchRange(LimitExisting(topic_path, False),
                             self.range.to)
        )

        return typing.cast(FetchRequest[TValue], result)

    def to(self, topic_path: StrictStr) -> FetchRequest[TValue]:
        """
        Specifies a logical end point within the topic tree.

        Notes:
            If specified, only results for topics with a path that is lexically equal to or 'before' the specified path
            will be returned.

            This is the inclusive equivalent of [before][diffusion.features.topics.fetch.fetch_request.FetchRequest.before] and if used will override any previous
            [before][diffusion.features.topics.fetch.fetch_request.FetchRequest.before] or [to][diffusion.features.topics.fetch.fetch_request.FetchRequest.to] constraint.

        Args:
            topic_path: The topic path before which results are to be returned.

        Returns:
            The fetch request derived from this fetch request but selecting only topics including and before the specified path.
        """  # noqa: E501, W291

        # see https://github.com/pydantic/pydantic/issues/7075
        result = dataclasses.replace(
            self,  # type: ignore
            range=FetchRange(self.range.from_, LimitExisting(topic_path, True))
        )

        return typing.cast(FetchRequest[TValue], result)

    def before(self, topic_path: StrictStr) -> FetchRequest[TValue]:
        """
        Specifies a logical end point within the topic tree.

        Notes:
            If specified, only results for topics with a path that is lexically 'before' the specified path will be
            returned.

            This is the non-inclusive equivalent of [to][diffusion.features.topics.fetch.fetch_request.FetchRequest.to] and if used will override any previous
            [to][diffusion.features.topics.fetch.fetch_request.FetchRequest.to] or [before][diffusion.features.topics.fetch.fetch_request.FetchRequest.before] constraint.

        Args:
            topic_path: The topic path before which results are to be returned.

        Returns:
            The fetch request derived from this fetch request but selecting only topics before the specified path (not inclusive).
        """  # noqa: E501, W291

        # see https://github.com/pydantic/pydantic/issues/7075
        result = dataclasses.replace(
            self,  # type: ignore
            range=FetchRange(self.range.from_, LimitExisting(topic_path, False))
        )

        return typing.cast(FetchRequest[TValue], result)

    @validate_member_arguments
    def topic_types(self: FetchSelf, topic_types: TopicTypeSet) -> FetchSelf:
        """
        Specifies that only topics of the specified topic types should be returned.

        Notes:
            If this is not specified, all types will be returned (unless constrained by
            [with_values][diffusion.features.topics.fetch.fetch_request.FetchRequest.with_values]).

            If the specified topic type matches the event type of a time series
            topic it will also be returned. The value will be delivered without
            the associated metadata. To specify all time series topics use
            [diffusion.datatypes.TIME_SERIES][diffusion.datatypes.TIME_SERIES].

            This may be used instead to further constrain the results when using
            [with_values][diffusion.features.topics.fetch.fetch_request.FetchRequest.with_values]. For example, you can specify [JSON][diffusion.datatypes.JSON]
            to [with_values][diffusion.features.topics.fetch.fetch_request.FetchRequest.with_values] then specify [diffusion.datatypes.JSON][diffusion.datatypes.JSON] here to ensure
            that only JSON topics are returned and not those topics that are logically value subtypes of JSON (e.g.
            [diffusion.datatypes.STRING][diffusion.datatypes.STRING]).

            If [with_values][diffusion.features.topics.fetch.fetch_request.FetchRequest.with_values] has been specified then the types specified here must be
            compatible with the specified value type or the event type for time series topics.

            ROUTING may not be specified as only target topic types may be selected.

        Args:
            topic_types: The topic types to be selected.

        Returns:
            The fetch request derived from this fetch request but specifying that only topics of the specified topic types should be returned.
        """  # noqa: E501, W291
        topic_types_final = frozenset({getattr(x, 'value', x) for x in topic_types})

        # see https://github.com/pydantic/pydantic/issues/7075
        result = dataclasses.replace(
            self,  # type: ignore
            topic_types_=topic_types_final
        )
        result.validate()
        return typing.cast(FetchSelf, result)

    @overload
    def with_values(self) -> FetchRequest[IVoidFetch]:
        ...  # pragma: no cover

    @overload
    def with_values(
        self, tp_new: typing.Type[TNewValue_Not_IVoidFetch]
    ) -> FetchRequest[TNewValue_Not_IVoidFetch]:
        ...  # pragma: no cover


    def with_values(
        self,
        tp_new: typing.Union[
            typing.Type[IVoidFetch], typing.Type[TNewValue_Not_IVoidFetch]
        ] = IVoidFetch,
    ) -> typing.Union[
        FetchRequest[IVoidFetch], FetchRequest[TNewValue_Not_IVoidFetch]
    ]:
        """
        Specifies that values should be returned for selected topics.

        Args:
            tp_new: the type of values the fetch request should return.

        Notes:
            This constrains the selection to only those topics with a data type compatible with the specified
            [TNewValue][diffusion.features.topics.fetch.types.TNewValue]

            If [OBJECT][diffusion.datatypes.OBJECT] is specified, values will be returned for all topic types (unless constrained by
            [topic_types][diffusion.features.topics.fetch.fetch_request.FetchRequest.topic_types]).

            The specified value constraints the topic types. So, any topic types specified in a previous call to
            [topic_types][diffusion.features.topics.fetch.fetch_request.FetchRequest.topic_types] that cannot be read as the specified class will be removed
            from the list of topic types.

        Returns:
            The fetch request derived from this fetch request but specifying that only topics compatible with the specified type should be returned with values.
        """  # noqa: E501, W291
        if not issubclass(tp_new, IVoidFetch):
            try:
                tp_new = typing.cast(
                    typing.Type[TNewValue_Not_IVoidFetch],
                    FQVTWrapper.validate_tp(
                        typing.cast(typing.Type[FetchQueryValueType_Not_WildCard], tp_new)
                    ),
                )
            except ValueError as e:
                self.raise_type_rejection(tp_new, e)
        try:
            selected_types: typing.Set[
                typing.Type[FetchQueryValueType_Not_WildCard]
            ] = set(self.topic_types_)
            if tp_new != IVoidFetch:
                assert not issubclass(tp_new, IVoidFetch)
                for topic_type in self.topic_types_:
                    if not self.can_read_as(
                        typing.cast(typing.Type[FetchQueryValueType], tp_new),
                        topic_type,
                    ):
                        selected_types.remove(topic_type)
                if len(selected_types) == 0:
                    self.raise_type_rejection(tp_new)

            # see https://github.com/pydantic/pydantic/issues/7075
            # noinspection PyDataclass
            result = dataclasses.replace(
                self,
                tp_=typing.cast(typing.Type[TValue], tp_new),
                topic_types_=frozenset(selected_types),
            )
            result.validate()
            return typing.cast(
                typing.Union[
                    FetchRequest[IVoidFetch], FetchRequest[TNewValue_Not_IVoidFetch]
                ],
                result,
            )
        except Exception as e:
            LOG.error(f"Got {e}: {traceback.format_exc()}")
            raise

    def raise_type_rejection(
        self,
        tp_new: typing.Type,
        type_rejection: typing.Optional[ValueError] = None,
    ) -> Never:
        raise ValueError(
            f"No selected topic types can be read as {tp_new}."
        ) from type_rejection

    def without_values(self) -> FetchRequest[IVoidFetch]:
        """
        Specifies that no values should be returned for selected topics.

        Notes:
            This methods lifts previous data type constraints set by [with_values][diffusion.features.topics.fetch.fetch_request.FetchRequest.with_values].

        Returns:
            The fetch request derived from this fetch request but specifying that topics should not be returned with values.
        """  # noqa: E501, W291

        return self.with_values()

    def with_properties(self) -> FetchRequest[TValue]:
        """
        Specifies that all properties associated with each topic's [ITopicSpecification][diffusion.features.topics.details.topic_specification.TopicSpecification] should be
        returned.

        Returns:
            The fetch request derived from this fetch request but specifying that topic specification properties should be returned.
        """  # noqa: E501, W291

        # see https://github.com/pydantic/pydantic/issues/7075
        # noinspection PyDataclass
        result = dataclasses.replace(
            self,  # type: ignore
            with_properties_=True
        )
        return typing.cast(FetchRequest[TValue], result)

    @validate_member_arguments
    def first(self: FetchSelf, number: StrictNonNegativeInt) -> FetchSelf:
        """
        Specifies a maximum number of topic results to be returned from_ the start of the required range.

        Notes:
            If this is not specified, the number of results returned will only be limited by other constraints of the
            request.

            This should be used to retrieve results in manageable batches and prevent very large result sets.

            If there are potentially more results that would satisfy the other constraints then the fetch result will
            indicate so via the [FetchResult.has_more][diffusion.features.topics.fetch.fetch_result.FetchResult.has_more] property.

            Zero can be supplied to return no results. Such a request can be used together with
            [FetchResult.has_more][diffusion.features.topics.fetch.fetch_result.FetchResult.has_more] to query whether there are topics that match the selector provided to
            [fetch][diffusion.features.topics.fetch.fetch_request.FetchRequest.fetch], without retrieving the details of any of the topics. To
            retrieve unlimited topics use Int32.MaxValue which is the default value.

            Either this or [last][diffusion.features.topics.fetch.fetch_request.FetchRequest.last] may be specified. This will therefore override any previous
            [last][diffusion.features.topics.fetch.fetch_request.FetchRequest.last] or [first][diffusion.features.topics.fetch.fetch_request.FetchRequest.first] constraint.

        Args:
            number: The maximum number of results to return from the start of the range.

        Returns:
            The fetch request derived from this fetch request but selecting only the number of topics specified from the start of the range.
        """  # noqa: E501, W291

        # see https://github.com/pydantic/pydantic/issues/7075
        return dataclasses.replace(
            self,  # type: ignore
            limit=typing.cast(SignedInt32, number)
        )

    @validate_member_arguments
    def last(self: FetchSelf, number: StrictNonNegativeInt) -> FetchSelf:
        """
        Specifies a maximum number of topic results to be returned from_ the end of the required range.

        Notes:
            This is similar to [first][diffusion.features.topics.fetch.fetch_request.FetchRequest.first] except that the specified number of results are returned from_
            the end of the range. This is useful for paging backwards through a range of topics. The results will be
            returned in topic path order (not reverse order).

            Zero can be supplied to return no results. Such a request can be used together with
            [FetchResult.has_more][diffusion.features.topics.fetch.fetch_result.FetchResult.has_more] to query whether there are topics that match the selector provided to
            [fetch][diffusion.features.topics.fetch.fetch_request.FetchRequest.fetch], without retrieving the details of any of the topics. To
            retrieve unlimited topics use Int32.MaxValue which is the default value.

            Either this or [first][diffusion.features.topics.fetch.fetch_request.FetchRequest.first] may be specified. This will therefore override any previous
            [first][diffusion.features.topics.fetch.fetch_request.FetchRequest.first] or [last][diffusion.features.topics.fetch.fetch_request.FetchRequest.last] constraint.

        Args:
            number: The maximum number of results to return from the end of the range.

        Returns:
            The fetch request derived from this fetch request but selecting only the number of topics specified from the end of the range.
        """  # noqa: E501, W291

        # see https://github.com/pydantic/pydantic/issues/7075
        return dataclasses.replace(
            self,  # type: ignore
            limit=typing.cast(SignedInt32, -number)
        )

    @validate_member_arguments
    def maximum_result_size(
        self: FetchSelf, maximum: StrictNonNegativeInt
    ) -> FetchSelf:
        """
        Specifies the maximum data size of the result set.

        Notes:
            This may be used to constrain the size of the result. If not specified then by default the maximum message
            size for the session (as specified by [maximum_message_size][diffusion.session.session_attributes.SessionAttributes.maximum_message_size] is
            used.

            If a value greater than the session's maximum message size then the maximum message size will be used.

        Args:
            maximum: The maximum size of the result set in bytes.

        Returns:
            The fetch request derived from this fetch request but constraining the size of the result to the sspecified `maximum`.
        """  # noqa: E501, W291

        # see https://github.com/pydantic/pydantic/issues/7075
        return dataclasses.replace(
            self,  # type: ignore
            maximum_result_size_=typing.cast(
                MaximumResultSize, min(self.fetch_context.maximum_message_size, maximum)
            ),
        )

    def limit_deep_branches(
        self,
        deep_branch_depth: NonNegativeSignedInt32,
        deep_branch_limit: NonNegativeSignedInt32,
    ) -> FetchRequest[TValue]:
        """
        Specifies a limit on the number of results returned for each deep branch.

        Notes:
            A deep branch has a root path that has a number of parts equal to the `deep_branch_depth`
            parameter. The `deep_branch_limit` specifies the maximum number of results for each deep
            branch.

            This method is particularly useful for incrementally exploring a topic tree from the root, allowing a
            breadth-first search strategy.

            For example, given a topic tree containing the topics with the following paths:
            z.

            The z/5.

            The fetch result does not indicate whether this option caused some results to be filtered from deep
            branches. It has no effect on the [FetchResult.has_more][diffusion.features.topics.fetch.fetch_result.FetchResult.has_more] result. If the result set contains
            `deep_branch_limit` results for a particular deep branch, some topics from that branch may
            have been filtered.

        Args:
            deep_branch_depth: The number of parts in the root path of a branch for it to be considered deep.
            deep_branch_limit: The maximum number of results to return for each deep branch.

        Returns:
            The fetch request derived from this fetch request but restricting the number of results for deep sbranches.
        """  # noqa: E501, W291

        # see https://github.com/pydantic/pydantic/issues/7075
        return dataclasses.replace(
            self,  # type: ignore
            deep_branch_limit=deep_branch_limit,
            deep_branch_depth=deep_branch_depth,
        )

    def with_unpublished_delayed_topics(self) -> FetchRequest[TValue]:
        """
        Include the details of reference topics that are not yet published.

        Notes:
            [TopicViews][diffusion.features.topics.topic_views.TopicViews] that use the _delay by clause
            create reference topics in an unpublished state. The topics are
            published once the delay time has expired. A topic in the
            unpublished state prevents a lower priority topic view from creating
            a reference topic with the same path.
            _

            A reference topic in the unpublished state which matches the query
            will only be included in the fetch results if the session has
            [PathPermission.READ_TOPIC][diffusion.PathPermission.READ_TOPIC] permission for the
            reference's source topic as well as READ_TOPIC permission for
            the reference topic. Requiring READ_TOPIC permission for the
            source topic ensures less privileged sessions cannot derive
            information from the existence of the reference topic before the
            delay time has expired.
            _

            Added in version 6.11

        Returns:
            A fetch request derived from this fetch request, additionally specifying that unpublished reference topics should be included in the results
        """  # noqa: E501, W291

        # see https://github.com/pydantic/pydantic/issues/7075
        return dataclasses.replace(
            self,  # type: ignore
            with_unpublished_delayed_topics_=True
        )

    def _decode_timeseries(
        self,
        decode_timeseries: diffusion.internal.pydantic_compat.v1.StrictBool = True,
    ) -> Self:
        """
        Unofficial API - not supported

        Returns:
            A fetch request configured to decode timeseries values
        """
        return dataclasses.replace(self, decode_timeseries=decode_timeseries)

    async def fetch(self, topics: StrictStr) -> FetchResult[TValue]:
        """

        Sends a fetch request to the server.

        Args:
            topics: specifies a topic selector string which selects the
                topics to be fetched

        Returns:
            the results of the fetch operation.

        Raises:
            PermissionsException: if the calling session does not have `SELECT_TOPIC` permission for the
                path prefix of the selector expression;
            SessionClosedException: if the session is closed.
        """  # NOQA: E501
        from diffusion.features.topics.fetch.fetch_query_result import FetchQueryResult
        query = FetchQuery(
            topics,
            self.range,
            self.topic_types_,
            self.tp_ != IVoidFetch,
            self.with_properties_,
            self.limit,
            self.maximum_result_size_,
            self.deep_branch_depth,
            self.deep_branch_limit,
            self.with_unpublished_delayed_topics_,
        )
        result = await self.fetch_context.session.services.FETCH_QUERY.invoke(
            self.fetch_context.session, request=query, response_type=FetchQueryResult
        )
        result_type: typing.Type[FetchResult]
        if self.decode_timeseries:
            result_type = DecodedFetchResult
        else:
            result_type = FetchResult
        return result_type.create(self.tp_, result)
