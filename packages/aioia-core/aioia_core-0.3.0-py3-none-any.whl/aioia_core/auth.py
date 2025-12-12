"""Authentication and authorization utilities for AIoIA projects."""

from enum import Enum
from typing import Protocol

from sqlalchemy.orm import Session


class UserRole(str, Enum):
    """Standard user roles for all AIoIA projects."""

    ADMIN = "admin"
    USER = "user"


class UserRoleProvider(Protocol):
    """
    Protocol for retrieving user roles and context.

    Projects implement this to integrate their user management system
    with BaseCrudRouter's authentication/authorization.
    """

    def get_user_role(  # pylint: disable=unnecessary-ellipsis
        self, user_id: str, db: Session
    ) -> UserRole | None:
        """
        Get user's role by ID.

        Args:
            user_id: User identifier
            db: Database session
        """
        ...

    def get_user_context(  # pylint: disable=unnecessary-ellipsis
        self, user_id: str, db: Session
    ) -> dict | None:
        """
        Get user context for monitoring/observability tools.

        Args:
            user_id: User identifier
            db: Database session
        """
        ...
