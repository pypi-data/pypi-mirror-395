import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from office365.sharepoint.client_context import ClientContext

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger("mcp_sharepoint")

# Load environment variables
load_dotenv()

# Configuration
SHP_ID_APP = os.getenv("SHP_ID_APP")
SHP_ID_APP_SECRET = os.getenv("SHP_ID_APP_SECRET")
SHP_SITE_URL = os.getenv("SHP_SITE_URL")
SHP_DOC_LIBRARY = os.getenv("SHP_DOC_LIBRARY", "Shared Documents/mcp_server")
SHP_TENANT_ID = os.getenv("SHP_TENANT_ID")

# Certificate auth settings (preferred)
SHP_CERT_PATH = os.getenv("SHP_CERT_PATH")
SHP_CERT_THUMBPRINT = os.getenv("SHP_CERT_THUMBPRINT")

if not SHP_SITE_URL:
    logger.error("SHP_SITE_URL environment variable not set.")
    raise ValueError("SHP_SITE_URL environment variable not set.")
if not SHP_ID_APP:
    logger.error("SHP_ID_APP environment variable not set.")
    raise ValueError("SHP_ID_APP environment variable not set.")
if not SHP_TENANT_ID:
    logger.error("SHP_TENANT_ID environment variable not set.")
    raise ValueError("SHP_TENANT_ID environment variable not set.")

# Initialize MCP server
mcp = FastMCP(
    name="mcp_sharepoint",
    instructions=f"This server provides tools to interact with SharePoint documents and folders in {SHP_DOC_LIBRARY}",
)


def _create_sharepoint_context() -> ClientContext:
    """Create SharePoint context using certificate auth (preferred) or client secret."""
    ctx = ClientContext(SHP_SITE_URL)

    # Try certificate authentication first (required for Azure AD app-only)
    if SHP_CERT_PATH and SHP_CERT_THUMBPRINT and SHP_TENANT_ID:
        cert_path = Path(SHP_CERT_PATH)
        if cert_path.exists():
            logger.info("Using certificate authentication")
            return ctx.with_client_certificate(
                tenant=SHP_TENANT_ID,
                client_id=SHP_ID_APP,
                thumbprint=SHP_CERT_THUMBPRINT,
                cert_path=str(cert_path),
            )
        else:
            logger.warning(f"Certificate not found at {SHP_CERT_PATH}")

    # Fall back to client secret (works with SharePoint app-only registration)
    if SHP_ID_APP_SECRET:
        logger.info("Using client secret authentication")
        from office365.runtime.auth.client_credential import ClientCredential

        credentials = ClientCredential(SHP_ID_APP, SHP_ID_APP_SECRET)
        return ctx.with_credentials(credentials)

    raise ValueError(
        "No valid authentication configured. "
        "Set SHP_CERT_PATH + SHP_CERT_THUMBPRINT for certificate auth, "
        "or SHP_ID_APP_SECRET for client secret auth."
    )


# Initialize SharePoint context
sp_context = _create_sharepoint_context()
