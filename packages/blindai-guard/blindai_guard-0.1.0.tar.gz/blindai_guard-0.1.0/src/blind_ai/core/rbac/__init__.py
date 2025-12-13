"""RBAC (Role-Based Access Control) module for Blind AI."""

from .authorizer import AuthorizationError, RBACAuthorizer
from .models import Permission, Role, UserContext

__all__ = [
    "UserContext",
    "Role",
    "Permission",
    "RBACAuthorizer",
    "AuthorizationError",
]
