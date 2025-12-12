import asyncio
import signal
import sys

from .common import logger, mcp, sp_context


def _verify_sharepoint_connection() -> bool:
    """Verify SharePoint connection on startup."""
    try:
        web = sp_context.web
        sp_context.load(web, ["Title", "Url"])
        sp_context.execute_query()
        logger.info(f"Connected to SharePoint: {web.title}")
        logger.info(f"Site URL: {web.url}")
        return True
    except Exception as e:
        error_msg = str(e)
        if "401" in error_msg or "Unauthorized" in error_msg:
            logger.error("Authentication failed - check SHP_ID_APP and SHP_ID_APP_SECRET")
        elif "403" in error_msg or "AccessDenied" in error_msg:
            logger.error("Access denied - app needs site-level permission")
            logger.error("Grant access at: <site>/_layouts/15/appinv.aspx")
        elif "404" in error_msg:
            logger.error("Site not found - check SHP_SITE_URL")
        else:
            logger.error(f"SharePoint connection failed: {e}")
        return False


async def main():
    """Main entry point for the MCP server."""
    logger.info("Starting SharePoint MCP server...")

    # Verify connection on startup
    if not _verify_sharepoint_connection():
        logger.warning("Starting server anyway - tools will fail until access is granted")

    # Import tools to register them with MCP
    from . import tools  # noqa: F401

    # Run the MCP server
    logger.info("MCP server ready - waiting for connections...")
    await mcp.run_stdio_async()


def run():
    """Run the server with graceful shutdown handling."""

    def handle_shutdown(_signum, _frame):
        logger.info("Shutting down...")
        sys.exit(0)

    # Handle Ctrl+C gracefully
    signal.signal(signal.SIGINT, handle_shutdown)
    signal.signal(signal.SIGTERM, handle_shutdown)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Shutting down...")
        sys.exit(0)


if __name__ == "__main__":
    run()
