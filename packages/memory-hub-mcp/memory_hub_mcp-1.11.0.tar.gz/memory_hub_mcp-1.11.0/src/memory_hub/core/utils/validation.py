# validation.py - Validation utilities for Memory Hub hierarchical structure

from typing import Optional

class HierarchyValidationError(Exception):
    """Raised when hierarchical memory rules are violated"""
    def __init__(self, detail: str, status_code: int = 400):
        self.detail = detail
        self.status_code = status_code
        super().__init__(detail)


def validate_hierarchy(
    app_id: Optional[str],
    project_id: Optional[str],
    ticket_id: Optional[str],
    run_id: Optional[str] = None
) -> None:
    """
    Validates hierarchical memory structure rules.

    Rules:
    - app_id is always required if project_id, ticket_id, or run_id is provided
    - project_id is required if ticket_id or run_id is provided
    - ticket_id is required if run_id is provided
    - Cannot specify project_id without app_id
    - Cannot specify ticket_id without both app_id and project_id
    - Cannot specify run_id without app_id, project_id, and ticket_id

    Args:
        app_id: Application identifier
        project_id: Project identifier (optional, but requires app_id)
        ticket_id: Ticket identifier (optional, but requires app_id and project_id)
        run_id: Run identifier (optional, but requires app_id, project_id, and ticket_id)

    Raises:
        HierarchyValidationError: If hierarchy rules are violated
    """
    # If run_id is provided, app_id, project_id, and ticket_id are all required
    if run_id:
        if not app_id:
            raise HierarchyValidationError(
                detail="run_id requires app_id to be specified. "
                       "Runs must belong to a ticket within a project within an app."
            )
        if not project_id:
            raise HierarchyValidationError(
                detail="run_id requires project_id to be specified. "
                       "Runs must belong to a ticket within a project."
            )
        if not ticket_id:
            raise HierarchyValidationError(
                detail="run_id requires ticket_id to be specified. "
                       "Runs must belong to a specific ticket (e.g., AutoStack execution per ticket)."
            )

    # If ticket_id is provided, both app_id and project_id are required
    if ticket_id:
        if not app_id:
            raise HierarchyValidationError(
                detail="ticket_id requires app_id to be specified. "
                       "Tickets must belong to both an app and a project."
            )
        if not project_id:
            raise HierarchyValidationError(
                detail="ticket_id requires project_id to be specified. "
                       "Tickets must belong to a project within an app."
            )

    # If project_id is provided, app_id is required
    if project_id and not app_id:
        raise HierarchyValidationError(
            detail="project_id requires app_id to be specified. "
                   "Projects must belong to an app (e.g., 'crossroads', 'motiv')."
        )

    # All validations passed
    return None
