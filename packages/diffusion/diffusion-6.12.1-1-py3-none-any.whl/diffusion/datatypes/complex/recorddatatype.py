#  Copyright (c) 2021 - 2025 DiffusionData Ltd., All Rights Reserved.
#
#  Use is subject to licence terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of DiffusionData. The intellectual and technical
#  concepts contained herein are proprietary to DiffusionData and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

from diffusion.datatypes.foundation.ibytesdatatype import IBytes
from diffusion.features.topics import TopicSpecification


class RecordDataType(
    IBytes[
        TopicSpecification["RecordDataType"], "RecordDataType", "RecordDataType"
    ],
):
    """Diffusion record data type implementation."""

    type_code = 20
    type_name = "record_v2"
