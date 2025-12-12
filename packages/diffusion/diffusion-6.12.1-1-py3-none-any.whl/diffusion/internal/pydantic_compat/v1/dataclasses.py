#  Copyright (c) 2024 - 2025 DiffusionData Ltd., All Rights Reserved.
#
#  Use is subject to licence terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of DiffusionData. The intellectual and technical
#  concepts contained herein are proprietary to DiffusionData and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

from diffusion.internal.pydantic_compat.shared import IS_PYDANTIC_V2

if IS_PYDANTIC_V2:
    # noinspection PyUnresolvedReferences
    from pydantic.v1.dataclasses import *  # noqa: F403
else:
    # noinspection PyUnresolvedReferences
    from pydantic.dataclasses import *  # type: ignore[no-redef, assignment, import-not-found] # noqa: F403
