#  Copyright (c) 2021 - 2025 DiffusionData Ltd., All Rights Reserved.
#
#  Use is subject to licence terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of DiffusionData. The intellectual and technical
#  concepts contained herein are proprietary to DiffusionData and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

from io import BytesIO
from typing import Any

import cbor2
import diffusion_core.cbor as diffusion_cbor  # type: ignore[import-not-found]
from typing_extensions import Protocol


class Encoder(Protocol):
    @staticmethod
    def load(buf: BytesIO) -> Any:
        pass

    @staticmethod
    def loads(buf: bytes) -> Any:
        pass

    @staticmethod
    def dumps(value: Any, *args: Any, **kwargs: Any) -> bytes:
        pass


class CBOR2(Encoder):
    @staticmethod
    def load(buf: BytesIO) -> Any:
        from diffusion.datatypes import InvalidDataError
        try:
            return cbor2.load(buf)
        except cbor2.CBORDecodeError as ex:
            raise InvalidDataError("Invalid CBOR data") from ex

    @staticmethod
    def loads(buf: bytes) -> Any:
        return cbor2.loads(buf)

    @staticmethod
    def dumps(value: Any, *args: Any, **kwargs: Any) -> bytes:
        return cbor2.dumps(value, *args, **kwargs)


class DiffCbor(CBOR2):
    @staticmethod
    def dumps(value: Any, *args: Any, **kwargs: Any) -> bytes:
        return diffusion_cbor.dumps(value, *args, **kwargs)


DefaultEncoder = DiffCbor
