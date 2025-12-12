#  Copyright (c) 2021 - 2025 DiffusionData Ltd., All Rights Reserved.
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
import attr
from typing import Optional

import structlog
from attr.exceptions import NotAnAttrsClassError

from diffusion.internal.services import Service, UnknownServiceError


LOG = structlog.get_logger()
ServiceLocatorBase = object
try:
    from diffusion.internal.generated.services import ServiceLocatorStatic as ServiceLocatorBase
except ImportError:  # pragma: no cover
    from builtins import object as ServiceLocatorBase  # NOQA: N812
    LOG.warn("Cannot find prebuilt service locator, falling back to dynamic")


class ServiceLocator(ServiceLocatorBase):
    """A mapping of services used by a feature.

    Lazily instantiates a service when requested.
    """

    def __getattr__(self, item) -> typing.Any:
        try:
            result = object.__getattribute__(self, item)
            ServiceLocator._mapping(self)[item] = result
            return result
        except AttributeError:
            return self[item]

    @staticmethod
    def _mapping(self):
        try:
            mapping = object.__getattribute__(self, "_dict")
        except AttributeError:
            try:
                mapping = attr.asdict(self)
            except NotAnAttrsClassError:
                mapping = {}
            object.__setattr__(self, "_dict", mapping)
        return mapping

    def __getitem__(self, item_orig: str) -> Service:
        item = item_orig.upper()
        mapping = ServiceLocator._mapping(self)
        result = mapping.get(item)
        if not result:
            try:
                result = getattr(ServiceLocatorBase, item)
            except AttributeError:
                result = Service.get_by_name(item)()
            mapping[item] = result

        return result

    def get(self, item: str, default=None) -> Optional[Service]:
        try:
            return self[item]
        except UnknownServiceError:
            return default

    def __iter__(self):
        return iter(ServiceLocator._mapping(self).items())
