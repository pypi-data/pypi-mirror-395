"""
CLI entry point for Memory Hub MCP Server (stdio only)
Designed specifically for ZenCoder and other MCP clients
"""

import asyncio
import argparse
import sys
import logging

from .mcp_server import create_server
from .core.services import AppConfig

# Configure file-based logging (stdio transport can't use stdout)
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='/tmp/memory-hub-mcp.log',
    filemode='a'
)
logger = logging.getLogger(__name__)
logger.info("Memory Hub MCP Server starting...")

async def run_server(config: AppConfig):
    """Run MCP server with stdio transport"""
    try:
        server = create_server(config)
        await server.run()
    except KeyboardInterrupt:
        logger.info("Server shutdown by user")
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        sys.exit(1)

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Memory Hub MCP Server - stdio transport for ZenCoder and MCP clients"
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Logging level"
    )
    parser.add_argument(
        "--qdrant-url",
        type=str,
        default=None,
        help="URL for the Qdrant service (e.g., http://localhost:6333)"
    )
    parser.add_argument(
        "--lm-studio-url",
        type=str,
        default=None,
        help="Base URL for the LM Studio service (e.g., http://localhost:1234/v1)"
    )
    
    args = parser.parse_args()
    
    # Set logging level
    logging.getLogger().setLevel(getattr(logging, args.log_level))
    
    # Create config object
    config = AppConfig(
        qdrant_url=args.qdrant_url,
        lm_studio_url=args.lm_studio_url
    )
    
    logger.info(f"Starting Memory Hub MCP Server (stdio mode) with config: {config}")
    
    try:
        asyncio.run(run_server(config))
    except KeyboardInterrupt:
        logger.info("Shutdown complete")
    except Exception as e:
        logger.error(f"Fatal error during server run: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main() 