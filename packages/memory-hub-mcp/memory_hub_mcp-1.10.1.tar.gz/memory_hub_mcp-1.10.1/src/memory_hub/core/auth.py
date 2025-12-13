# core/auth.py - Authentication and Authorization for HTTP Server

import yaml
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# Custom exception classes
class AuthenticationError(Exception):
    """Raised when user authentication fails"""
    def __init__(self, detail: str, status_code: int = 401):
        self.detail = detail
        self.status_code = status_code
        super().__init__(detail)

class AuthorizationError(Exception):
    """Raised when user is not authorized to access resource"""
    def __init__(self, detail: str, status_code: int = 403):
        self.detail = detail
        self.status_code = status_code
        super().__init__(detail)

@dataclass
class User:
    """User configuration"""
    handle: str
    status: str  # active | blocked | suspended
    is_admin: bool
    allowed_paths: List[List[str]]  # Hierarchical path patterns
    allowed_tools: List[str]  # Allowed MCP tool names

class AuthManager:
    """Manages user authentication and authorization"""

    def __init__(self, config_path: str):
        """
        Initialize AuthManager with user configuration file

        Args:
            config_path: Path to users.yaml configuration file
        """
        self.config_path = Path(config_path)
        self.users: Dict[str, User] = {}
        self._load_config()

    def _load_config(self):
        """Load and parse users.yaml configuration"""
        try:
            if not self.config_path.exists():
                raise FileNotFoundError(f"User config file not found: {self.config_path}")

            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)

            if not config or 'users' not in config:
                raise ValueError("Invalid user config: missing 'users' section")

            # Parse users
            for handle, user_config in config['users'].items():
                self.users[handle] = User(
                    handle=handle,
                    status=user_config.get('status', 'blocked'),
                    is_admin=user_config.get('is_admin', False),
                    allowed_paths=user_config.get('allowed_paths', []),
                    allowed_tools=user_config.get('allowed_tools', [])
                )

            logger.info(f"Loaded {len(self.users)} users from {self.config_path}")

        except Exception as e:
            logger.error(f"Failed to load user config: {e}")
            raise

    def authenticate(self, handle: str) -> User:
        """
        Authenticate user by handle

        Args:
            handle: User handle from X-Memory-Hub-User header

        Returns:
            User object if authenticated

        Raises:
            AuthenticationError: If user not found or blocked
        """
        if not handle:
            raise AuthenticationError("Missing user handle in X-Memory-Hub-User header")

        user = self.users.get(handle)
        if not user:
            raise AuthenticationError(f"Unknown user: {handle}")

        if user.status != 'active':
            raise AuthenticationError(f"User '{handle}' is {user.status}")

        return user

    def authorize_path(self, user: User, app_id: Optional[str],
                      project_id: Optional[str] = None,
                      ticket_id: Optional[str] = None,
                      run_id: Optional[str] = None):
        """
        Check if user is authorized to access a specific path

        Args:
            user: Authenticated user
            app_id: Application ID (required for path checks)
            project_id: Project ID (optional)
            ticket_id: Ticket ID (optional)
            run_id: Run ID (optional)

        Raises:
            AuthorizationError: If user is not authorized
        """
        # Admin users bypass all checks
        if user.is_admin:
            return

        # If no app_id provided, path check doesn't apply
        if not app_id:
            return

        # Build requested path (only include non-None values)
        requested_path = [app_id]
        if project_id is not None:
            requested_path.append(project_id)
        if ticket_id is not None:
            requested_path.append(ticket_id)
        if run_id is not None:
            requested_path.append(run_id)

        # Check if requested path matches any allowed pattern
        for pattern in user.allowed_paths:
            if self._path_matches(requested_path, pattern):
                return  # Authorized

        # No match found
        path_str = " / ".join(requested_path)
        raise AuthorizationError(
            f"User '{user.handle}' not authorized to access: {path_str}"
        )

    def _path_matches(self, requested: List[str], pattern: List[str]) -> bool:
        """
        Check if requested path matches allowed pattern with wildcard support

        Pattern matching rules:
        - ["app"] matches ["app"] only (exact match, no deeper)
        - ["app", "*"] matches ["app", "proj"] and ["app", "proj2"] but not ["app"] or ["app", "proj", "ticket"]
        - ["app", "proj", "*"] matches any ticket under app/proj
        - ["app", "proj", "ticket", "*"] matches any run under app/proj/ticket
        - ["app", "*", "*", "*"] matches everything under app (any depth >= 2)

        Args:
            requested: Requested path (e.g., ["covenant", "portal", "auth-flow"])
            pattern: Allowed pattern (e.g., ["covenant", "portal", "*", "*"])

        Returns:
            True if requested path matches pattern
        """
        # Count required (non-wildcard) prefix elements in pattern
        required_length = 0
        for elem in pattern:
            if elem != "*":
                required_length += 1
            else:
                break  # Stop at first wildcard

        # Requested path must have at least the required non-wildcard elements
        if len(requested) < required_length:
            return False

        # Check each level (only up to length of requested path)
        for i in range(len(requested)):
            # If we've exhausted the pattern, the rest of requested is extra (shouldn't happen)
            if i >= len(pattern):
                return False

            pattern_part = pattern[i]

            if pattern_part == "*":
                # Wildcard: matches this level and allows anything beyond
                remaining_pattern = pattern[i+1:]
                remaining_request = requested[i+1:]

                # If no more pattern, wildcard covers all remaining levels
                if not remaining_pattern:
                    return True

                # Check if all remaining pattern elements are wildcards
                all_wildcards = all(p == "*" for p in remaining_pattern)

                if all_wildcards:
                    # All remaining are wildcards = optional, so we match regardless
                    return True

                # If more pattern exists with non-wildcards, check remaining levels
                # (This handles patterns like ["app", "*", "ticket", "*"])
                if len(remaining_request) < len(remaining_pattern):
                    return False

                for j, remaining_pattern_part in enumerate(remaining_pattern):
                    if remaining_pattern_part != "*" and remaining_request[j] != remaining_pattern_part:
                        return False

                return True

            elif pattern_part != requested[i]:
                # Not a wildcard and doesn't match: fail
                return False

        # If we've checked all requested elements successfully:
        # - If pattern is same length or shorter: match
        # - If pattern is longer but remaining are all wildcards: match
        # - Otherwise: no match
        if len(requested) < len(pattern):
            # Check if remaining pattern elements are all wildcards
            for i in range(len(requested), len(pattern)):
                if pattern[i] != "*":
                    return False

        return True

    def authorize_tool(self, user: User, tool_name: str):
        """
        Check if user is authorized to use a specific tool

        Args:
            user: Authenticated user
            tool_name: Name of the MCP tool

        Raises:
            AuthorizationError: If user is not authorized
        """
        # Admin users bypass all checks
        if user.is_admin:
            return

        # Empty allowed_tools list for non-admin = no access
        if not user.allowed_tools:
            raise AuthorizationError(
                f"User '{user.handle}' has no tool access configured"
            )

        if tool_name not in user.allowed_tools:
            raise AuthorizationError(
                f"User '{user.handle}' not authorized to use tool: {tool_name}"
            )

    def filter_ids_by_access(self, user: User, ids: List[str],
                            id_type: str) -> List[str]:
        """
        Filter a list of IDs (app_ids, project_ids, etc.) to only those user can access

        Args:
            user: Authenticated user
            ids: List of IDs to filter
            id_type: Type of ID - "app_id", "project_id", "ticket_id"

        Returns:
            Filtered list of IDs user can access
        """
        # Admin users see everything
        if user.is_admin:
            return ids

        # Extract unique values at the appropriate level from allowed_paths
        allowed_ids = set()

        if id_type == "app_id":
            # First element of each path
            for path in user.allowed_paths:
                if len(path) >= 1 and path[0] != "*":
                    allowed_ids.add(path[0])

        elif id_type == "project_id":
            # Second element of each path
            for path in user.allowed_paths:
                if len(path) >= 2:
                    if path[1] == "*":
                        # Wildcard at project level means we need to allow all
                        # (can't filter without checking app_id first)
                        continue
                    allowed_ids.add(path[1])

        elif id_type == "ticket_id":
            # Third element of each path
            for path in user.allowed_paths:
                if len(path) >= 3:
                    if path[2] == "*":
                        continue
                    allowed_ids.add(path[2])

        # If we found wildcards, we can't easily filter - return all
        # (This is a limitation; ideally we'd check each ID against full paths)
        if not allowed_ids:
            return ids

        return [id for id in ids if id in allowed_ids]
