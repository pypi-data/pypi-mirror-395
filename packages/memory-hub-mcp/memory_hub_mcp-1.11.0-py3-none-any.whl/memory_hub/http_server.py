"""
HTTP REST API Server for Memory Hub using FastAPI
Provides authenticated access to Memory Hub functionality via HTTP
"""

import logging
from typing import Optional, Dict, Any
from fastapi import FastAPI, Header, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .core.auth import AuthManager, AuthenticationError, AuthorizationError, User
from .core.services import AppConfig
from .core.models import (
    MemoryItemIn, MemorySearchRequest, GetProjectMemoriesRequest,
    UpdateMemoryRequest, GetRecentMemoriesRequest, ListMemoryTypesRequest,
    HierarchyOverviewRequest, ExportMemoriesRequest,
    SessionResumeRequest, SessionHandoffRequest, SessionUpdateRequest
)
from .core.handlers.memory import (
    add_memory as add_memory_handler,
    search_memories as search_memories_handler,
    get_project_memories as get_project_memories_handler,
    update_memory as update_memory_handler,
    get_recent_memories as get_recent_memories_handler,
    get_hierarchy_overview as get_hierarchy_overview_handler,
    export_memories as export_memories_handler,
    get_quick_start_info as get_quick_start_info_handler,
    session_resume as session_resume_handler,
    session_handoff as session_handoff_handler,
    session_update as session_update_handler,
)
from .core.handlers.list_handlers import (
    list_app_ids as list_app_ids_handler,
    list_project_ids as list_project_ids_handler,
    list_ticket_ids as list_ticket_ids_handler,
    list_memory_types as list_memory_types_handler,
    get_memory_type_guide as get_memory_type_guide_handler
)
from .core.handlers.health_handlers import health_check as health_check_handler

logger = logging.getLogger(__name__)

# Version constant
VERSION = "1.11.0"

class MemoryHubHTTPServer:
    """Memory Hub HTTP REST API Server"""

    def __init__(self, config: AppConfig, auth_manager: AuthManager):
        self.config = config
        self.auth = auth_manager
        self.app = self._create_app()

    def _create_app(self) -> FastAPI:
        """Create and configure FastAPI application"""
        app = FastAPI(
            title="Memory Hub HTTP API",
            description="Authenticated HTTP REST API for Memory Hub MCP Server",
            version=VERSION
        )

        # Add CORS middleware
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Configure as needed
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # Authentication dependency
        async def get_current_user(
            x_memory_hub_user: Optional[str] = Header(None)
        ) -> User:
            """Dependency to authenticate user from header"""
            try:
                user = self.auth.authenticate(x_memory_hub_user)
                return user
            except AuthenticationError as e:
                raise HTTPException(status_code=e.status_code, detail=e.detail)

        # Public endpoints (no authentication)
        @app.get("/api/health")
        async def health():
            """Health check endpoint"""
            try:
                result = await health_check_handler(self.config)
                return result
            except Exception as e:
                logger.error(f"Health check failed: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @app.get("/api/version")
        async def version():
            """Get server version"""
            return {"version": VERSION}

        # Protected endpoints (require authentication)
        @app.post("/api/add_memory")
        async def add_memory(
            memory_item: MemoryItemIn,
            user: User = Depends(get_current_user)
        ):
            """Add memory with semantic chunking"""
            try:
                # Check tool authorization
                self.auth.authorize_tool(user, "add_memory")

                # Check path authorization
                self.auth.authorize_path(
                    user,
                    memory_item.metadata.get("app_id"),
                    memory_item.metadata.get("project_id"),
                    memory_item.metadata.get("ticket_id"),
                    memory_item.metadata.get("run_id")
                )

                result = await add_memory_handler(memory_item, self.config)
                return result

            except (AuthenticationError, AuthorizationError) as e:
                raise HTTPException(status_code=e.status_code, detail=e.detail)
            except Exception as e:
                logger.error(f"add_memory failed: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @app.post("/api/search_memories")
        async def search_memories(
            search_request: MemorySearchRequest,
            user: User = Depends(get_current_user)
        ):
            """Search memories with keyword enhancement"""
            try:
                # Check tool authorization
                self.auth.authorize_tool(user, "search_memories")

                # Check path authorization if metadata filters provided
                if search_request.metadata_filters:
                    self.auth.authorize_path(
                        user,
                        search_request.metadata_filters.get("app_id"),
                        search_request.metadata_filters.get("project_id"),
                        search_request.metadata_filters.get("ticket_id"),
                        search_request.metadata_filters.get("run_id")
                    )

                result = await search_memories_handler(search_request, self.config)
                return result

            except (AuthenticationError, AuthorizationError) as e:
                raise HTTPException(status_code=e.status_code, detail=e.detail)
            except Exception as e:
                logger.error(f"search_memories failed: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @app.post("/api/get_project_memories")
        async def get_project_memories(
            request: GetProjectMemoriesRequest,
            user: User = Depends(get_current_user)
        ):
            """Retrieve all memories for app/project/ticket/run"""
            try:
                # Check tool authorization
                self.auth.authorize_tool(user, "get_project_memories")

                # Check path authorization
                self.auth.authorize_path(
                    user,
                    request.app_id,
                    request.project_id,
                    request.ticket_id,
                    request.run_id
                )

                result = await get_project_memories_handler(request, self.config)
                return result

            except (AuthenticationError, AuthorizationError) as e:
                raise HTTPException(status_code=e.status_code, detail=e.detail)
            except Exception as e:
                logger.error(f"get_project_memories failed: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @app.post("/api/update_memory")
        async def update_memory(
            request: UpdateMemoryRequest,
            user: User = Depends(get_current_user)
        ):
            """Update existing memory (increments version)"""
            try:
                # Check tool authorization
                self.auth.authorize_tool(user, "update_memory")

                # Check path authorization
                self.auth.authorize_path(
                    user,
                    request.app_id,
                    request.project_id,
                    request.ticket_id,
                    request.run_id
                )

                result = await update_memory_handler(request, self.config)
                return result

            except (AuthenticationError, AuthorizationError) as e:
                raise HTTPException(status_code=e.status_code, detail=e.detail)
            except Exception as e:
                logger.error(f"update_memory failed: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @app.post("/api/get_recent_memories")
        async def get_recent_memories(
            request: GetRecentMemoriesRequest,
            user: User = Depends(get_current_user)
        ):
            """Retrieve memories from last N hours"""
            try:
                # Check tool authorization
                self.auth.authorize_tool(user, "get_recent_memories")

                # Check path authorization if filters provided
                if request.app_id:
                    self.auth.authorize_path(
                        user,
                        request.app_id,
                        request.project_id,
                        request.ticket_id,
                        request.run_id
                    )

                result = await get_recent_memories_handler(request, self.config)
                return result

            except (AuthenticationError, AuthorizationError) as e:
                raise HTTPException(status_code=e.status_code, detail=e.detail)
            except Exception as e:
                logger.error(f"get_recent_memories failed: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @app.post("/api/get_hierarchy_overview")
        async def get_hierarchy_overview(
            request: HierarchyOverviewRequest,
            user: User = Depends(get_current_user)
        ):
            """Retrieve hierarchy children and counts for a scope"""
            try:
                self.auth.authorize_tool(user, "get_hierarchy_overview")
                self.auth.authorize_path(
                    user,
                    request.app_id,
                    request.project_id,
                    request.ticket_id
                )

                result = await get_hierarchy_overview_handler(request, self.config)
                return result
            except (AuthenticationError, AuthorizationError) as e:
                raise HTTPException(status_code=e.status_code, detail=e.detail)
            except Exception as e:
                logger.error(f"get_hierarchy_overview failed: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @app.post("/api/get_scope_overview")
        async def get_scope_overview(
            request: HierarchyOverviewRequest,
            user: User = Depends(get_current_user)
        ):
            """Retrieve hierarchy children and counts for a scope (alias)"""
            try:
                # Allow both tool names for auth
                try:
                    self.auth.authorize_tool(user, "get_scope_overview")
                except AuthorizationError:
                    self.auth.authorize_tool(user, "get_hierarchy_overview")

                self.auth.authorize_path(
                    user,
                    request.app_id,
                    request.project_id,
                    request.ticket_id
                )

                result = await get_hierarchy_overview_handler(request, self.config)
                return result
            except (AuthenticationError, AuthorizationError) as e:
                raise HTTPException(status_code=e.status_code, detail=e.detail)
            except Exception as e:
                logger.error(f"get_scope_overview failed: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @app.post("/api/export_memories")
        async def export_memories(
            request: ExportMemoriesRequest,
            user: User = Depends(get_current_user)
        ):
            """Export all memories for a scope as JSON"""
            try:
                self.auth.authorize_tool(user, "export_memories")
                self.auth.authorize_path(
                    user,
                    request.app_id,
                    request.project_id,
                    request.ticket_id,
                    request.run_id
                )

                result = await export_memories_handler(request, self.config)
                return result
            except (AuthenticationError, AuthorizationError) as e:
                raise HTTPException(status_code=e.status_code, detail=e.detail)
            except Exception as e:
                logger.error(f"export_memories failed: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @app.get("/api/get_quick_start")
        async def get_quick_start(
            user: User = Depends(get_current_user)
        ):
            """Quick-start guidance for tool selection and usage."""
            try:
                # Allow either tool name for auth clarity
                try:
                    self.auth.authorize_tool(user, "get_quick_start")
                except AuthorizationError:
                    self.auth.authorize_tool(user, "get_quickstart")

                result = await get_quick_start_info_handler(self.config)
                return result
            except (AuthenticationError, AuthorizationError) as e:
                raise HTTPException(status_code=e.status_code, detail=e.detail)
            except Exception as e:
                logger.error(f"get_quick_start failed: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @app.get("/api/list_app_ids")
        async def list_app_ids(user: User = Depends(get_current_user)):
            """List all unique app_ids (filtered by user access)"""
            try:
                # Check tool authorization
                self.auth.authorize_tool(user, "list_app_ids")

                result = await list_app_ids_handler(self.config)

                # Filter results by user access
                filtered_ids = self.auth.filter_ids_by_access(
                    user, result.ids, "app_id"
                )

                return {
                    "ids": filtered_ids,
                    "total_count": len(filtered_ids),
                    "points_scanned": result.points_scanned
                }

            except (AuthenticationError, AuthorizationError) as e:
                raise HTTPException(status_code=e.status_code, detail=e.detail)
            except Exception as e:
                logger.error(f"list_app_ids failed: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @app.get("/api/list_project_ids")
        async def list_project_ids(user: User = Depends(get_current_user)):
            """List all unique project_ids (filtered by user access)"""
            try:
                # Check tool authorization
                self.auth.authorize_tool(user, "list_project_ids")

                result = await list_project_ids_handler(self.config)

                # Filter results by user access
                filtered_ids = self.auth.filter_ids_by_access(
                    user, result.ids, "project_id"
                )

                return {
                    "ids": filtered_ids,
                    "total_count": len(filtered_ids),
                    "points_scanned": result.points_scanned
                }

            except (AuthenticationError, AuthorizationError) as e:
                raise HTTPException(status_code=e.status_code, detail=e.detail)
            except Exception as e:
                logger.error(f"list_project_ids failed: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @app.get("/api/list_ticket_ids")
        async def list_ticket_ids(user: User = Depends(get_current_user)):
            """List all unique ticket_ids (filtered by user access)"""
            try:
                # Check tool authorization
                self.auth.authorize_tool(user, "list_ticket_ids")

                result = await list_ticket_ids_handler(self.config)

                # Filter results by user access
                filtered_ids = self.auth.filter_ids_by_access(
                    user, result.ids, "ticket_id"
                )

                return {
                    "ids": filtered_ids,
                    "total_count": len(filtered_ids),
                    "points_scanned": result.points_scanned
                }

            except (AuthenticationError, AuthorizationError) as e:
                raise HTTPException(status_code=e.status_code, detail=e.detail)
            except Exception as e:
                logger.error(f"list_ticket_ids failed: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @app.post("/api/list_memory_types")
        async def list_memory_types(
            request: ListMemoryTypesRequest,
            user: User = Depends(get_current_user)
        ):
            """List memory types with metadata"""
            try:
                # Check tool authorization
                self.auth.authorize_tool(user, "list_memory_types")

                # Check path authorization if filters provided
                if request.app_id:
                    self.auth.authorize_path(
                        user,
                        request.app_id,
                        request.project_id
                    )

                result = await list_memory_types_handler(request, self.config)
                return result

            except (AuthenticationError, AuthorizationError) as e:
                raise HTTPException(status_code=e.status_code, detail=e.detail)
            except Exception as e:
                logger.error(f"list_memory_types failed: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @app.get("/api/get_memory_type_guide")
        async def get_memory_type_guide(user: User = Depends(get_current_user)):
            """Get memory type recommendations"""
            try:
                # Check tool authorization
                self.auth.authorize_tool(user, "get_memory_type_guide")

                result = await get_memory_type_guide_handler(self.config)
                return result

            except (AuthenticationError, AuthorizationError) as e:
                raise HTTPException(status_code=e.status_code, detail=e.detail)
            except Exception as e:
                logger.error(f"get_memory_type_guide failed: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        # Session Management Endpoints
        @app.post("/api/session_resume")
        async def session_resume(
            request: SessionResumeRequest,
            user: User = Depends(get_current_user)
        ):
            """Resume a session - returns complete context for incoming agent"""
            try:
                self.auth.authorize_tool(user, "session_resume")
                self.auth.authorize_path(user, request.app_id, request.project_id)

                result = await session_resume_handler(request, self.config)
                return result

            except (AuthenticationError, AuthorizationError) as e:
                raise HTTPException(status_code=e.status_code, detail=e.detail)
            except Exception as e:
                logger.error(f"session_resume failed: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @app.post("/api/session_handoff")
        async def session_handoff(
            request: SessionHandoffRequest,
            user: User = Depends(get_current_user)
        ):
            """Record a handoff - agent is ending, context is clearing"""
            try:
                self.auth.authorize_tool(user, "session_handoff")
                self.auth.authorize_path(user, request.app_id, request.project_id)

                result = await session_handoff_handler(request, self.config)
                return result

            except (AuthenticationError, AuthorizationError) as e:
                raise HTTPException(status_code=e.status_code, detail=e.detail)
            except Exception as e:
                logger.error(f"session_handoff failed: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @app.post("/api/session_update")
        async def session_update(
            request: SessionUpdateRequest,
            user: User = Depends(get_current_user)
        ):
            """Quick checkpoint - partial update to session state"""
            try:
                self.auth.authorize_tool(user, "session_update")
                self.auth.authorize_path(user, request.app_id, request.project_id)

                result = await session_update_handler(request, self.config)
                return result

            except (AuthenticationError, AuthorizationError) as e:
                raise HTTPException(status_code=e.status_code, detail=e.detail)
            except Exception as e:
                logger.error(f"session_update failed: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        return app

def create_http_server(config: AppConfig, auth_manager: AuthManager) -> MemoryHubHTTPServer:
    """Create an instance of the Memory Hub HTTP Server"""
    return MemoryHubHTTPServer(config, auth_manager)
