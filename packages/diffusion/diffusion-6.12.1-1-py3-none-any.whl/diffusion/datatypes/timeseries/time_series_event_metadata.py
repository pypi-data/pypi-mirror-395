#  Copyright (c) 2022 - 2023 DiffusionData Ltd., All Rights Reserved.
#
#  Use is subject to licence terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of DiffusionData. The intellectual and technical
#  concepts contained herein are proprietary to DiffusionData and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

from __future__ import annotations

import typing

from diffusion.internal.serialisers.pydantic import MarshalledModel

if typing.TYPE_CHECKING:
    from diffusion.datatypes.timeseries.time_series_event import Offsets


class EventMetadata(MarshalledModel):
    """
    Time series event metadata.
    """

    sequence: int
    """
    Sequence number identifying this event within its time series.
    Assigned by the server when the event is created.

    Sequence numbers are unique within a time series. Each event appended
    to a time series is assigned a sequence number that is is equal to
    the sequence number of the preceding event plus one.
    """

    timestamp: int
    """
    Event timestamp. Assigned by the server when the event is created.

    Events do not have unique timestamps. Events with different sequence
    numbers may have the same timestamp.

    Subsequent events in a time series usually have timestamps that are
    greater or equal to the timestamps of earlier events, but this is not
    guaranteed due to changes to the time source used by the server.

    Timestamps represent the difference, measured in milliseconds, between
    the time the server added the event to the time series and midnight,
    January 1, 1970 UTC
    """

    author: str
    """
    Server-authenticated identity of the session that created the event.

    If the session that created the event was not authenticated, the author
    will be an empty string.
    """

    class Config(MarshalledModel.Config):
        alias = "time-series-event-metadata"
        allow_mutation = False
        frozen = True

        @classmethod
        def attr_mappings_all(cls, modelcls):
            return {
                "time-series-event-metadata": {
                    "time-series-event-metadata.time-series-sequence": "sequence",
                    "time-series-event-metadata.timestamp": "timestamp",
                    "time-series-event-metadata.author": "author",
                },
                "time-series-update-response": {
                    "time-series-event-metadata.time-series-sequence": "sequence",
                    "time-series-event-metadata.timestamp": "timestamp",
                    "time-series-event-metadata.author": "author",
                },
            }

    def offset(self, offsets: Offsets) -> EventMetadata:
        return self.copy(
            update={
                "timestamp": self.timestamp + offsets.timestamp,
                "sequence": self.sequence + offsets.sequence,
            }
        )
