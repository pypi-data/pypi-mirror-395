#  Copyright (c) 2025 - 2025 DiffusionData Ltd., All Rights Reserved.
#
#  Use is subject to licence terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of DiffusionData. The intellectual and technical
#  concepts contained herein are proprietary to DiffusionData and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

import dataclasses
import typing

from  diffusion.internal.serialisers.generic_model import GenericModel, CombinedMapping
from diffusion.internal.serialisers.dataclass_model import DataclassConfigMixin
@dataclasses.dataclass
class GetBranchMappingTable(GenericModel):
    name: str
    class Config(DataclassConfigMixin["GetBranchMappingTable"]):
        @classmethod
        def attr_mappings_combined(cls, modelcls) -> typing.Mapping[str, CombinedMapping]:
            return {"string": CombinedMapping({"string": "name"})}
