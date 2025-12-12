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

from diffusion.features.control.session_trees.branch_mapping_table import (
    BranchMappingTable
)
from diffusion.features.control.session_trees.invalid_branch_mapping_exception import (
    InvalidBranchMappingException
)
from diffusion.internal.components import Component
from diffusion.internal.utils import assert_arg_type


class SessionTrees(Component):
    """
    This feature allows a client session to configure session trees.

    A session tree is a virtual view of the topic tree presented to a session by
    fetch and subscription operations. Custom session trees for different
    sessions can be configured using declarative rules maintained by the server
    to meet data security, data optimisation, or personalisation and localisation
    requirements. Each session can be presented with a unique session tree based
    on its session properties.

    A session tree is produced by applying **branch mappings** to the topic
    tree. Branch mappings are organised into **branch mapping tables**. Each
    branch mapping table is assigned to a unique path - the *session tree
    branch*.

    A session tree is composed of **session paths**. Each session path is
    mapped via the branch mapping tables to a unique **topic path**.

    A branch mapping table is an ordered list of (session filter, topic tree branch)
    pairs. For example, the branch mapping table for the session tree branch
    `market/prices` might be:
    <br></br>

    | Session filter                       | Topic tree branch         |
    | -------------------------------------| ------------------------- |
    | USER_TIER is '1' or $Country is 'DE' | backend/discounted_prices |
    | USER_TIER is '2'                     | backend/standard_prices   |
    | $Principal is ''                     | backend/delayed_prices    |

    <br></br>
    With this configuration, if an unauthenticated session
    (one that matches the `$Principal is ''` session filter) subscribes
    to the session path `market/prices/X`, and there is a topic bound to the
    topic path `backend/delayed_prices/X`, the subscription will complete.
    The session will receive a subscription notification under the session path
    `market/prices/X`, together with the topic properties and the value of the topic.
    The session is unaware that the data originates from a topic bound to a different
    topic path. If no topic is bound to `backend/delayed_prices/X`, the subscription
    will not resolve and the session will receive no data, even if there is a topic bound to
    `market/prices/X`.

    Session trees complement the data transformation capabilities of
    topic views. In our example, the time delayed time feed at
    `backend/delayed_prices` could be maintained by a topic view using the
    **delay by** clause.

    Branch mappings are persisted by the server and shared across a cluster, in a
    similar manner to topic views, security stores, and metric collectors. Branch
    mappings are editable using this feature, and via the management console.

    For a given session and session path, at most one branch mapping applies. The
    applicable branch mapping is chosen as follows:

    - Each branch mapping table with session tree branch that is a prefix of the
    session path is considered. For a given table, the first branch mapping with
    a session filter that matches the session's properties is the one that applies. A
    branch mapping table may have no applicable branch mappings for a session.

    - If there are several such branch mapping tables with a branch mapping
    that for the session, the one with the longest prefix of the session path
    applies.

    - If no branch mapping table has a branch mapping for the session, the
    session path is translated to the identical topic path.

    # Access control

    To subscribe to or fetch from a session path, a session must be granted the
    appropriate path permission to the session path for the operation
    `SELECT_TOPIC`, or `READ_TOPIC`. The session doesn't require
    any permissions to the topic path of the topic providing the data.

    To create or replace branch mappings, a session needs the
    `MODIFY_TOPIC` path permission for the session tree branch of the
    branch mapping table `EXPOSE_BRANCH` path permission for the
    topic tree branch of each branch mapping, and (if an existing table with the same
    session tree branch is being replaced) `EXPOSE_BRANCH` permission for each
    branch mapping of existing table.

    To retrieve a branch mapping table, a session needs the
    `READ_TOPIC` path permission for its session tree branch.

    # Accessing the feature

    This feature may be obtained from a `Session` as follows:

    session_trees: SessionTrees = session.session_trees

    """

    async def put_branch_mapping_table(
        self, branch_mapping_table: BranchMappingTable
    ) -> None:

        """
        Create or replace a branch mapping table.

        The server ensures that a session tree branch has at most one branch mapping
        table. Putting a new branch mapping table will replace any previous
        branch mapping table with the same session tree branch. To remove all branch
        mappings for a session tree branch, put an empty branch mapping table.

        Args:
            branch_mapping_table: the new table

        Raises:
            InvalidBranchMappingException: if
                branch_mapping_table or one of its branch mappings is invalid;
            SessionSecurityException: if the calling
                session does not have the `MODIFY_TOPIC` permission for the session tree
                branch of the branch  mapping table, `EXPOSE_BRANCH`
                permission for each branch mapping of branchMappingTable, and (if
                there is an existing table for the session tree branch)
                `EXPOSE_BRANCH` permission for
                each branch mapping of existing table;
            ClusterRoutingException: if the operation
                failed due to a transient cluster error;
            SessionClosedException: if the session is
                closed.
        Returns:
            a response from the server.

        """
        assert_arg_type(
            branch_mapping_table, BranchMappingTable
        )
        service = self.services.PUT_BRANCH_MAPPING_TABLE
        await service.invoke(
            self.session,
            service.request.evolve(
                branch_mapping_table.session_tree_branch,
                [
                    (x.session_filter, x.topic_tree_branch)
                    for x in branch_mapping_table.branch_mappings
                ],
            ),
        )

    async def get_session_tree_branches_with_mappings(
        self,
    ) -> typing.List[str]:
        """
        Retrieve the session tree branches of the server's branch mapping tables.
        The results will only include the session tree branches of branch mapping
        tables that have at least one branch mapping and for which the calling
        session has the `READ_TOPIC` path permission
        for the session tree branch.

        Individual branch mapping tables can be retrieved using
        `SessionTrees.get_branch_mapping_table`.

        Returns:
             a list of session tree branches in path order.

        Raises:
             SessionClosedException: if the session is closed.

        """
        response = await self.services.GET_SESSION_TREE_BRANCHES_WITH_MAPPINGS.invoke(
            self.session
        )
        result = list(
            item
            for k in response.values()
            for entry in k
            for item in entry
        )
        return result

    async def get_branch_mapping_table(
        self, session_tree_branch: str
    ) -> BranchMappingTable:
        """
        Retrieve a branch mapping table from the server.

        If there is no branch mapping table at the given session tree branch,
        this method will return an empty branch mapping table.

        Args:
            session_tree_branch: the session tree branch that identifies the
                branch mapping table

        Returns:
            the branch mapping table for session_tree_branch.

        Raises:
            SessionSecurityException: if the calling
                session does not have the `READ_TOPIC`
                permission for sessionTreeBranch;
            SessionClosedException: if the session is closed.
        """
        from diffusion.internal.serialisers.specific.session_trees import GetBranchMappingTable
        assert session_tree_branch is not None, "NoneType"
        service = self.services.GET_BRANCH_MAPPING_TABLE
        return await service.invoke(
            self.session,
            request=GetBranchMappingTable(session_tree_branch),
            response_type=BranchMappingTable
        )
