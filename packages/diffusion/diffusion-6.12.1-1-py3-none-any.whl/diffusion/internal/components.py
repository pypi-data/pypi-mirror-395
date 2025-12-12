#  Copyright (c) 2020 - 2025 DiffusionData Ltd., All Rights Reserved.
#
#  Use is subject to licence terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of DiffusionData. The intellectual and technical
#  concepts contained herein are proprietary to DiffusionData and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

""" Base features module."""

from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:  # pragma: no cover
    from diffusion.session import Session
    from .services.locator import ServiceLocator
    from .session import InternalSession


class Component:
    """A base class for various Diffusion "components".

    Args:
        session: The active `Session` to operate on.
    """

    def __init__(self, session: Session):
        self.session: InternalSession = session._internal

    @property
    def services(self) -> ServiceLocator:
        """Alias for the internal session's service locator."""
        return self.session.services
