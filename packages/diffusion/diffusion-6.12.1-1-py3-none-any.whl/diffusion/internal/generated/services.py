#  Copyright (c) 2020 - 2025 DiffusionData Ltd., All Rights Reserved.
#
#  Use is subject to licence terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of DiffusionData. The intellectual and technical
#  concepts contained herein are proprietary to DiffusionData and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

import attr

from diffusion.internal.serialisers import get_serialiser
from diffusion.internal.services.abstract import OutboundService
from diffusion.internal.services.messaging import (
    FilterResponse,
    MessagingFilterSender,
    MessagingReceiverClient,
    MessagingReceiverControlRegistration,
    MessagingReceiverServer,
    MessagingSend,
)
from diffusion.internal.services.session import ChangePrincipal, SystemPing, UserPing
from diffusion.internal.services.topics import (
    AddAndSetTopic,
    NotifySubscription,
    NotifyUnsubscription,
    Subscribe,
    TopicAdd,
    TopicRemoval,
    Unsubscribe,
)


class RangeQuery(OutboundService):
    service_id = 84
    name = "RANGE_QUERY"
    request_serialiser_map = {12: "range-query-request", 24: "range-query-request"}
    response_serialiser_map = {12: "range-query-result", 24: "range-query-result"}
    request_serialiser = get_serialiser("range-query-request")
    response_serialiser = get_serialiser("range-query-result")


class TimeSeriesAppend(OutboundService):
    service_id = 99
    name = "TIME_SERIES_APPEND"
    request_serialiser_map = {
        12: "time-series-append-request",
        24: "time-series-append-request",
    }
    response_serialiser_map = {
        12: "time-series-update-response",
        24: "time-series-update-response",
    }
    request_serialiser = get_serialiser("time-series-append-request")
    response_serialiser = get_serialiser("time-series-update-response")


class TimeSeriesEdit(OutboundService):
    service_id = 100
    name = "TIME_SERIES_EDIT"
    request_serialiser_map = {12: "time-series-edit-request", 24: "time-series-edit-request"}
    response_serialiser_map = {
        12: "time-series-update-response",
        24: "time-series-update-response",
    }
    request_serialiser = get_serialiser("time-series-edit-request")
    response_serialiser = get_serialiser("time-series-update-response")


class AcquireSessionLock(OutboundService):
    service_id = 114
    name = "ACQUIRE_SESSION_LOCK"
    request_serialiser_map = {
        25: "session-lock-request",
        16: "session-lock-request",
        15: "session-lock-request",
        14: "session-lock-request",
    }
    response_serialiser_map = {
        25: "session-lock-acquisition",
        16: "session-lock-acquisition",
        15: "session-lock-acquisition",
        14: "session-lock-acquisition",
    }
    request_serialiser = get_serialiser("session-lock-request")
    response_serialiser = get_serialiser("session-lock-acquisition")


class CancelAcquireSessionLock(OutboundService):
    service_id = 115
    name = "CANCEL_ACQUIRE_SESSION_LOCK"
    request_serialiser_map = {
        25: "session-lock-request-cancellation",
        16: "session-lock-request-cancellation",
        15: "session-lock-request-cancellation",
        14: "session-lock-request-cancellation",
    }
    response_serialiser_map = {25: "void", 16: "void", 15: "void", 14: "void"}
    request_serialiser = get_serialiser("session-lock-request-cancellation")
    response_serialiser = get_serialiser("void")


class ReleaseSessionLock(OutboundService):
    service_id = 116
    name = "RELEASE_SESSION_LOCK"
    request_serialiser_map = {
        25: "session-lock-acquisition",
        16: "session-lock-acquisition",
        15: "session-lock-acquisition",
        14: "session-lock-acquisition",
    }
    response_serialiser_map = {25: "boolean", 16: "boolean", 15: "boolean", 14: "boolean"}
    request_serialiser = get_serialiser("session-lock-acquisition")
    response_serialiser = get_serialiser("boolean")


class FetchQuery(OutboundService):
    service_id = 117
    name = "FETCH_QUERY"
    request_serialiser_map = {
        15: "protocol15-fetch-query",
        16: "protocol16-fetch-query",
        17: "protocol17-fetch-query",
        18: "protocol18-fetch-query",
        28: "protocol28-fetch-query",
    }
    response_serialiser_map = {
        15: "fetch-query-result",
        16: "fetch-query-result",
        17: "fetch-query-result",
        18: "fetch-query-result",
        28: "protocol28-fetch-query-result",
    }
    request_serialiser = get_serialiser("protocol18-fetch-query")
    response_serialiser = get_serialiser("fetch-query-result")


class SetTopic(OutboundService):
    service_id = 118
    name = "SET_TOPIC"
    request_serialiser_map = {
        15: "set-topic-request",
        16: "set-topic-request",
        22: "set-topic-request",
        26: "protocol26-set-topic-request",
        27: "protocol27-set-topic-request",
    }
    response_serialiser_map = {15: "void", 16: "void", 22: "void", 26: "void", 27: "void"}
    request_serialiser = get_serialiser("set-topic-request")
    response_serialiser = get_serialiser("void")


class PutSessionMetricCollector(OutboundService):
    service_id = 135
    name = "PUT_SESSION_METRIC_COLLECTOR"
    request_serialiser_map = {
        16: "protocol16-session-metric-collector",
        22: "protocol16-session-metric-collector",
        24: "session-metric-collector",
    }
    response_serialiser_map = {
        16: "error-report-list",
        22: "error-report-list",
        24: "error-report-list",
    }
    request_serialiser = get_serialiser("session-metric-collector")
    response_serialiser = get_serialiser("error-report-list")


class RemoveSessionMetricCollector(OutboundService):
    service_id = 136
    name = "REMOVE_SESSION_METRIC_COLLECTOR"
    request_serialiser_map = {16: "string", 22: "string"}
    response_serialiser_map = {16: "void", 22: "void"}
    request_serialiser = get_serialiser("string")
    response_serialiser = get_serialiser("void")


class ListSessionMetricCollectors(OutboundService):
    service_id = 137
    name = "LIST_SESSION_METRIC_COLLECTORS"
    request_serialiser_map = {16: "void", 22: "void", 24: "void"}
    response_serialiser_map = {
        16: "protocol16-session-metric-collectors",
        22: "protocol16-session-metric-collectors",
        24: "session-metric-collectors",
    }
    request_serialiser = get_serialiser("void")
    response_serialiser = get_serialiser("session-metric-collectors")


class PutTopicMetricCollector(OutboundService):
    service_id = 146
    name = "PUT_TOPIC_METRIC_COLLECTOR"
    request_serialiser_map = {
        16: "protocol16-topic-metric-collector",
        22: "protocol16-topic-metric-collector",
        24: "protocol24-topic-metric-collector",
        25: "protocol25-topic-metric-collector",
    }
    response_serialiser_map = {16: "void", 22: "void", 24: "void", 25: "void"}
    request_serialiser = get_serialiser("protocol25-topic-metric-collector")
    response_serialiser = get_serialiser("void")


class RemoveTopicMetricCollector(OutboundService):
    service_id = 147
    name = "REMOVE_TOPIC_METRIC_COLLECTOR"
    request_serialiser_map = {16: "string", 22: "string"}
    response_serialiser_map = {16: "void", 22: "void"}
    request_serialiser = get_serialiser("string")
    response_serialiser = get_serialiser("void")


class ListTopicMetricCollectors(OutboundService):
    service_id = 148
    name = "LIST_TOPIC_METRIC_COLLECTORS"
    request_serialiser_map = {16: "void", 22: "void", 24: "void", 25: "void"}
    response_serialiser_map = {
        16: "protocol16-topic-metric-collectors",
        22: "protocol16-topic-metric-collectors",
        24: "protocol24-topic-metric-collectors",
        25: "protocol25-topic-metric-collectors",
    }
    request_serialiser = get_serialiser("void")
    response_serialiser = get_serialiser("protocol25-topic-metric-collectors")


class TimeSeriesTimestampAppend(OutboundService):
    service_id = 166
    name = "TIME_SERIES_TIMESTAMP_APPEND"
    request_serialiser_map = {
        19: "time-series-timestamp-append-request",
        24: "time-series-timestamp-append-request",
    }
    response_serialiser_map = {
        19: "time-series-update-response",
        24: "time-series-update-response",
    }
    request_serialiser = get_serialiser("time-series-timestamp-append-request")
    response_serialiser = get_serialiser("time-series-update-response")


class PutBranchMappingTable(OutboundService):
    service_id = 176
    name = "PUT_BRANCH_MAPPING_TABLE"
    request_serialiser_map = {22: "branch-mapping-table"}
    response_serialiser_map = {22: "void"}
    request_serialiser = get_serialiser("branch-mapping-table")
    response_serialiser = get_serialiser("void")


class GetSessionTreeBranchesWithMappings(OutboundService):
    service_id = 177
    name = "GET_SESSION_TREE_BRANCHES_WITH_MAPPINGS"
    request_serialiser_map = {22: "void"}
    response_serialiser_map = {22: "session-tree-branch-list"}
    request_serialiser = get_serialiser("void")
    response_serialiser = get_serialiser("session-tree-branch-list")


class GetBranchMappingTable(OutboundService):
    service_id = 178
    name = "GET_BRANCH_MAPPING_TABLE"
    request_serialiser_map = {22: "string"}
    response_serialiser_map = {22: "branch-mapping-table"}
    request_serialiser = get_serialiser("string")
    response_serialiser = get_serialiser("branch-mapping-table")


@attr.s(auto_attribs=True, hash=True, eq=True)
class ServiceLocatorStatic(object):
    SUBSCRIBE: Subscribe = Subscribe()
    UNSUBSCRIBE: Unsubscribe = Unsubscribe()
    CHANGE_PRINCIPAL: ChangePrincipal = ChangePrincipal()
    NOTIFY_UNSUBSCRIPTION: NotifyUnsubscription = NotifyUnsubscription()
    SYSTEM_PING: SystemPing = SystemPing()
    USER_PING: UserPing = UserPing()
    TOPIC_REMOVAL: TopicRemoval = TopicRemoval()
    RANGE_QUERY: RangeQuery = RangeQuery()
    MESSAGING_SEND: MessagingSend = MessagingSend()
    MESSAGING_RECEIVER_SERVER: MessagingReceiverServer = MessagingReceiverServer()
    NOTIFY_SUBSCRIPTION: NotifySubscription = NotifySubscription()
    MESSAGING_RECEIVER_CLIENT: MessagingReceiverClient = MessagingReceiverClient()
    MESSAGING_RECEIVER_CONTROL_REGISTRATION: MessagingReceiverControlRegistration = (
        MessagingReceiverControlRegistration()
    )
    TIME_SERIES_APPEND: TimeSeriesAppend = TimeSeriesAppend()
    TIME_SERIES_EDIT: TimeSeriesEdit = TimeSeriesEdit()
    MESSAGING_FILTER_SENDER: MessagingFilterSender = MessagingFilterSender()
    FILTER_RESPONSE: FilterResponse = FilterResponse()
    TOPIC_ADD: TopicAdd = TopicAdd()
    ACQUIRE_SESSION_LOCK: AcquireSessionLock = AcquireSessionLock()
    CANCEL_ACQUIRE_SESSION_LOCK: CancelAcquireSessionLock = CancelAcquireSessionLock()
    RELEASE_SESSION_LOCK: ReleaseSessionLock = ReleaseSessionLock()
    FETCH_QUERY: FetchQuery = FetchQuery()
    SET_TOPIC: SetTopic = SetTopic()
    ADD_AND_SET_TOPIC: AddAndSetTopic = AddAndSetTopic()
    PUT_SESSION_METRIC_COLLECTOR: PutSessionMetricCollector = PutSessionMetricCollector()
    REMOVE_SESSION_METRIC_COLLECTOR: RemoveSessionMetricCollector = (
        RemoveSessionMetricCollector()
    )
    LIST_SESSION_METRIC_COLLECTORS: ListSessionMetricCollectors = ListSessionMetricCollectors()
    PUT_TOPIC_METRIC_COLLECTOR: PutTopicMetricCollector = PutTopicMetricCollector()
    REMOVE_TOPIC_METRIC_COLLECTOR: RemoveTopicMetricCollector = RemoveTopicMetricCollector()
    LIST_TOPIC_METRIC_COLLECTORS: ListTopicMetricCollectors = ListTopicMetricCollectors()
    TIME_SERIES_TIMESTAMP_APPEND: TimeSeriesTimestampAppend = TimeSeriesTimestampAppend()
    PUT_BRANCH_MAPPING_TABLE: PutBranchMappingTable = PutBranchMappingTable()
    GET_SESSION_TREE_BRANCHES_WITH_MAPPINGS: GetSessionTreeBranchesWithMappings = (
        GetSessionTreeBranchesWithMappings()
    )
    GET_BRANCH_MAPPING_TABLE: GetBranchMappingTable = GetBranchMappingTable()
