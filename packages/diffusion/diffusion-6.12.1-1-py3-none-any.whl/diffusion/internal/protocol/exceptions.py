#  Copyright (c) 2020 - 2024 DiffusionData Ltd., All Rights Reserved.
#
#  Use is subject to licence terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of DiffusionData. The intellectual and technical
#  concepts contained herein are proprietary to DiffusionData and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.


""" Protocol-related exceptions. """
import typing

import attr
from typing import List
from diffusion.internal.exceptions import DiffusionError


class ProtocolError(ConnectionError, DiffusionError):
    """ General protocol error. """


class ServerConnectionError(ProtocolError):
    """ General error when connecting to server. """


class ServerDisconnectedError(ProtocolError):
    """ General error when server disconnected """
    def __init__(self):
        super().__init__("Not connected to Diffusion server!")


class ServerConnectionResponseError(ServerConnectionError):
    """ Error when the server returns a non-OK code on connection. """

    def __init__(self, response_code):
        super().__init__(f"Failed to connect: {response_code.name}")
        self.response_code = response_code


class ServiceMessageError(ProtocolError):
    """ Error when handling service messages. """

    default_description = "Service error message: {message}"

    def __init__(
        self,
        message: typing.Optional[str] = "",
        reason_code: typing.Optional[int] = None,
        *args,
        **kwargs,
    ):
        super().__init__(
            self.description(message=message, reason_code=reason_code, **kwargs), *args
        )

    @classmethod
    def description(
        cls,
        message: typing.Optional[str] = "",
        reason_code: typing.Optional[int] = None,
        **kwargs,
    ):
        return cls.default_description.format(
            message=(message or f"reason code = {reason_code}"), **kwargs
        )


@attr.s(auto_attribs=True)
class ErrorReport(object):
    message: str
    line: int
    column: int


class ReportsError(DiffusionError):
    def __init__(self, reports: List[ErrorReport], msg: typing.Optional[str] = None):
        super().__init__(msg or f"{msg or type(self)} caused by {reports}")
        self.reports = reports


class InvalidSessionFilterError(ReportsError):
    def __init__(self, reports: List[ErrorReport], msg: typing.Optional[str] = None):
        super().__init__(reports, msg)


class AbortMessageError(ServiceMessageError):
    """ Abort message received from the server. """


# Conversation errors.


class ConversationError(DiffusionError):
    """ Base conversation error. """


class CIDGeneratorExhaustedError(ConversationError):
    """ Error stating that a CID generator was exhausted. """


class NoSuchConversationError(ConversationError):
    """ The conversation with this CID does not exist in the `ConversationSet`. """

    def __init__(self, cid):
        super().__init__(f"Unknown conversation {cid}")
