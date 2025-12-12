#  Copyright (c) 2020 - 2025 DiffusionData Ltd., All Rights Reserved.
#
#  Use is subject to licence terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of DiffusionData. The intellectual and technical
#  concepts contained herein are proprietary to DiffusionData and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

""" Diffusion Python client library. """

from .internal.exceptions import DiffusionError
from .internal.protocol import SessionId
from .internal.session import Credentials
from .session import Session
from .session.session_factory import sessions
