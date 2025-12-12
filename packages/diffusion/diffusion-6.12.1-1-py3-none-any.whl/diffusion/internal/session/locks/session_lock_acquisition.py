#  Copyright (c) 2022 - 2023 DiffusionData Ltd., All Rights Reserved.
#
#  Use is subject to licence terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of DiffusionData. The intellectual and technical
#  concepts contained herein are proprietary to DiffusionData and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

from diffusion.internal.serialisers.pydantic import MarshalledModel
from diffusion.session import SessionLockScope


class SessionLockAcquisition(MarshalledModel):
    """
    The successful response of a
    [SessionLockRequest][diffusion.session.locks.session_lock_request.SessionLockRequest]
    """

    lock_name: str
    sequence: int
    scope: SessionLockScope

    class Config(MarshalledModel.Config):
        frozen = True
        alias_generator = None

        @classmethod
        def attr_mappings_all(cls, modelcls):
            return {
                "session-lock-acquisition": {
                    "session-lock-name": "lock_name",
                    "session-lock-sequence": "sequence",
                    "session-lock-scope": "scope",
                }
            }

    def __str__(self):
        return (
            f"""SessionLockAcquisition[{self.lock_name}, {self.sequence}, {self.scope}"""
        )
