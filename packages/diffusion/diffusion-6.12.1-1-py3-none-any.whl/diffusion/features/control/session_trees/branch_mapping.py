#  Copyright (c) 2021 - 2025 DiffusionData Ltd., All Rights Reserved.
#
#  Use is subject to licence terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of DiffusionData. The intellectual and technical
#  concepts contained herein are proprietary to DiffusionData and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

import attr


@attr.s(frozen=True, slots=True, auto_attribs=True)
class BranchMapping(object):
    """
    A session tree branch mapping.

    Branch mappings belong to branch mapping tables (BranchMappingTable).
    Each branch mapping is a pair of Session Filters and the
    target topic tree branch that applies to sessions matching the filter.

    Attributes:
        session_filter: the session filter
        topic_tree_branch: the topic tree branch in the topic tree
            for sessions matching the session filter

    See Also: SessionTrees
    """
    session_filter: str = attr.ib(validator=attr.validators.instance_of(str))
    topic_tree_branch: str = attr.ib(validator=attr.validators.instance_of(str))
