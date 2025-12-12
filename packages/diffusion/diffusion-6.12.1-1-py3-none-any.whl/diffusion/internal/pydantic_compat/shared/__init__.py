#  Copyright (c) 2024 - 2025 DiffusionData Ltd., All Rights Reserved.
#
#  Use is subject to licence terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of DiffusionData. The intellectual and technical
#  concepts contained herein are proprietary to DiffusionData and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.
import warnings

import typing

warnings.filterwarnings('ignore', category=DeprecationWarning)
warnings.filterwarnings('ignore', category=UserWarning)

import pydantic  # noqa: E402

IS_PYDANTIC_V2: typing.Literal[False, True] = pydantic.version.VERSION[0] == '2'
IS_PYDANTIC_V2_HASATTR = hasattr(pydantic, "_getattr_migration")
