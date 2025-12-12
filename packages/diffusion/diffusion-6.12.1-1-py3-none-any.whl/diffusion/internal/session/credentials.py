#  Copyright (c) 2020 - 2025 DiffusionData Ltd., All Rights Reserved.
#
#  Use is subject to licence terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of DiffusionData. The intellectual and technical
#  concepts contained herein are proprietary to DiffusionData and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

""" Credentials module. """
import enum
from base64 import b64encode
from typing import Union

from diffusion.internal.encoded_data import Byte, Bytes


@enum.unique
class CredentialsType(enum.IntEnum):
    """ Type codes for credentials. """

    NONE = 0
    PLAIN_PASSWORD = 1
    CUSTOM = 2


class Credentials:
    """Simple wrapper class to encapsulate server credentials.

    Args:
        value: value: The value of the credentials.

    Examples:
        >>> cred1 = Credentials("bar")
        >>> cred1.type
        <CredentialsType.PLAIN_PASSWORD: 1>
        >>> cred1.password
        'AQNiYXI='
        >>> tuple(cred1)
        (1, b'bar')
        >>> cred2 = Credentials(b"bla")
        >>> cred2.type
        <CredentialsType.CUSTOM: 2>
        >>> cred2.password
        'AgNibGE='

    """

    def __init__(self, value: Union[str, bytes] = b""):
        if not value:
            self.type = CredentialsType.NONE
            self._bytes = b""
        else:
            if isinstance(value, str):
                value = value.encode()
                self.type = CredentialsType.PLAIN_PASSWORD
            else:
                self.type = CredentialsType.CUSTOM
            self._bytes = value

    @property
    def password(self) -> str:
        """ The base64-encoded textual representation of the credentials. """
        if self._bytes:
            pwd = Byte(self.type).to_bytes() + Bytes(self._bytes).to_bytes()
        else:
            pwd = self._bytes
        return b64encode(pwd).decode("ascii")

    def __iter__(self):
        return iter((self.type.value, self._bytes))

    def __repr__(self):
        return f"{self.type.name} credentials"
