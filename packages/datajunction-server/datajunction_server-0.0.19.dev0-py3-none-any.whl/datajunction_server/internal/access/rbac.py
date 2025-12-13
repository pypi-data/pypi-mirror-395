"""
Core RBAC (Role-Based Access Control) implementation for DataJunction
"""

from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from datajunction_server.database.rbac import PrincipalMembership, Role, RoleAssignment
from datajunction_server.database.user import PrincipalKind, User
from datajunction_server.models.access import ResourceType


class RBACService:
    """
    Service class for RBAC operations like assigning roles, managing groups, etc.
    """

    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    async def assign_role(
        self,
        principal_id: int,
        role_name: str,
        scope_type: ResourceType,
        scope_value: Optional[str] = None,
        granted_by_id: int = None,
    ) -> RoleAssignment:
        """Assign a role to a principal"""

        # Validate role exists
        role = await Role.get_by_name(self.session, role_name)
        if not role:
            raise ValueError(f"Role '{role_name}' does not exist")

        # Create assignment
        assignment = RoleAssignment(
            principal_id=principal_id,
            role_name=role_name,
            scope_type=scope_type,
            scope_value=scope_value,
            granted_by_id=granted_by_id,
        )

        self.session.add(assignment)
        await self.session.commit()
        return assignment

    async def assign_namespace_owners(
        self,
        namespace: str,
        principal_ids: List[int],
        granted_by_id: int,
    ) -> List[RoleAssignment]:
        """Convenient method to assign ownership of a namespace to multiple principals"""

        assignments = []
        for principal_id in principal_ids:
            assignment = await self.assign_role(
                principal_id=principal_id,
                role_name=f"owner-{namespace}",
                scope_type=ResourceType.NAMESPACE,
                scope_value=namespace,
                granted_by_id=granted_by_id,
            )
            assignments.append(assignment)

        return assignments

    async def create_group(
        self,
        name: str,
        display_name: str,
        created_by_id: int,
    ) -> User:
        """Create a new group principal"""

        group = User(
            username=name,
            name=display_name,
            kind=PrincipalKind.GROUP,
            created_by_id=created_by_id,
        )

        self.session.add(group)
        await self.session.commit()
        return group

    async def add_to_group(
        self,
        member_id: int,
        group_id: int,
        added_by_id: int,
    ) -> PrincipalMembership:
        """Add a principal to a group"""

        membership = PrincipalMembership(
            member_id=member_id,
            group_id=group_id,
            added_by_id=added_by_id,
        )

        self.session.add(membership)
        await self.session.commit()
        return membership

    async def get_resource_owners(
        self,
        resource_type: str,
        resource_name: str,
    ) -> List[User]:
        """Get all principals who have owner role on a resource"""

        assignments = await RoleAssignment.get_assignments_for_resource(
            self.session,
            resource_type,
            resource_name,
        )

        owners = []
        for assignment in assignments:
            if assignment.role_name == "owner":
                owners.append(assignment.principal)

        return owners

    async def auto_assign_ownership_on_create(
        self,
        resource_type: ResourceType,
        resource_name: str,
        creator: User,
    ) -> RoleAssignment:
        """
        Automatically assign ownership when a resource is created

        Logic:
        1. If creator is in groups, assign ownership to primary group
        2. Otherwise, assign ownership to creator
        3. Scope can be namespace or node level based on resource
        """

        # Get creator's groups
        user_groups = await self.group_resolver.get_user_groups(
            self.session,
            creator.id,
        )

        if user_groups:
            # Assign to primary group (first group)
            owner_id = user_groups[0]
        else:
            # Assign to creator
            owner_id = creator.id

        # Create ownership assignment
        return await self.assign_role(
            principal_id=owner_id,
            role_name=f"owner-{resource_name}",
            scope_type=resource_type,
            scope_value=resource_name,
            granted_by_id=creator.id,
        )

    async def setup_team_namespace_ownership(
        self,
        team_group: User,  # Group principal
        namespace: str,
        granted_by: User,
    ) -> RoleAssignment:
        """
        Set up a team to own an entire namespace

        Example: growth-dse team owns growth.* namespace
        """
        return await self.assign_role(
            principal_id=team_group.id,
            role_name=f"owner-{namespace}",
            scope_type=ResourceType.NAMESPACE,
            scope_value=namespace,
            granted_by_id=granted_by.id,
        )

    async def migrate_existing_ownership(self) -> None:
        """
        Migrate existing node ownership to RBAC system
        This should be run once when enabling RBAC
        """
        from sqlalchemy import select
        from datajunction_server.database.node import Node
        from datajunction_server.database.nodeowner import NodeOwner

        # Migrate node creators to owners
        nodes_with_creators = await self.session.execute(select(Node))

        for node in nodes_with_creators.scalars():
            try:
                await self.assign_role(
                    principal_id=node.created_by_id,
                    role_name=f"owner-{node.name}",
                    scope_type=ResourceType.NODE,
                    scope_value=node.name,
                    granted_by_id=node.created_by_id,  # Self-granted
                )
            except Exception:
                # Skip if assignment already exists
                pass

        # Migrate existing node_owners table if it exists
        try:
            existing_owners = await self.session.execute(select(NodeOwner))

            for owner_rel in existing_owners.scalars():
                try:
                    await self.assign_role(
                        principal_id=owner_rel.user_id,
                        role_name=f"owner-{owner_rel.node.name}",
                        scope_type=ResourceType.NODE,
                        scope_value=owner_rel.node.name,
                        granted_by_id=owner_rel.user_id,  # Self-granted
                    )
                except Exception:
                    # Skip if assignment already exists
                    pass
        except Exception:
            # NodeOwner table might not exist, skip
            pass
