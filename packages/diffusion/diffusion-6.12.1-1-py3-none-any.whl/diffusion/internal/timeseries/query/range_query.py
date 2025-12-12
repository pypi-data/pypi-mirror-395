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

import enum
import typing

import attr

from diffusion.datatypes.timeseries import VT
from diffusion.internal.session import InternalSession

if typing.TYPE_CHECKING:
    from diffusion.internal.timeseries.query.range_query_parameters import (
        RangeQueryParameters,
        Range,
    )


class RangeQueryMode(enum.IntEnum):
    """
    The range query mode.

    Since:
        6.9
    """

    VIEW_RANGE = 0x00
    """
    The range query is in view range mode.
    """
    EDIT_RANGE = 0x01
    """
    The range query is in edit range mode.
    """

    def type_name(self):
        return "value" if self == RangeQueryMode.VIEW_RANGE else "edit"

    def change_current_range(
        self,
        original: RangeQueryParameters,
        range_selector: typing.Callable[[Range], Range],
    ) -> RangeQueryParameters:
        """
        Changes the given
        [RangeQueryParameters][diffusion.internal.timeseries.query.range_query.RangeQueryParameters]
        into this
        [RangeQueryMode][diffusion.features.timeseries.query.range_query.RangeQueryMode]

        Args:
            original: The range query parameters to change the mode of.
            range_selector: The range selector function.
        Returns:

            The new RangeQueryParameters
        Raises:
            ArgumentError: this mode is invalid for the RangeQuery.
        """

        if self == RangeQueryMode.VIEW_RANGE:
            return original.with_view_range(range_selector(original.view_range))
        elif self == RangeQueryMode.EDIT_RANGE:
            return original.with_edit_range(range_selector(original.edit_range))
        raise NotImplementedError()


@attr.s(auto_attribs=True, eq=True, hash=True, slots=True, frozen=True)
class RangeQueryBase(typing.Generic[VT]):
    session: InternalSession
    parameters: RangeQueryParameters
    mode: RangeQueryMode
    tp: typing.Type[VT]
