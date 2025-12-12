"""Certificate setup for SharePoint MCP Server."""

import json
import subprocess
import sys
from pathlib import Path


def generate_certificate(output_dir: str = "certs", days: int = 365) -> dict[str, str]:
    """Generate a self-signed certificate for SharePoint authentication."""
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    key_file = output_path / "sharepoint.key"
    crt_file = output_path / "sharepoint.crt"
    pem_file = output_path / "sharepoint.pem"

    try:
        subprocess.run(
            [
                "openssl",
                "req",
                "-x509",
                "-sha256",
                "-nodes",
                "-days",
                str(days),
                "-newkey",
                "rsa:2048",
                "-keyout",
                str(key_file),
                "-out",
                str(crt_file),
                "-subj",
                "/CN=mcp-sharepoint/O=MCP SharePoint Server",
            ],
            check=True,
            capture_output=True,
        )
    except FileNotFoundError:
        print("Error: openssl not found. Please install OpenSSL.")
        print("  macOS: brew install openssl")
        print("  Ubuntu: sudo apt install openssl")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error generating certificate: {e.stderr.decode()}")
        sys.exit(1)

    with pem_file.open("w") as pem:
        pem.write(crt_file.read_text())
        pem.write(key_file.read_text())

    result = subprocess.run(
        ["openssl", "x509", "-in", str(crt_file), "-fingerprint", "-sha1", "-noout"],
        capture_output=True,
        text=True,
        check=True,
    )
    thumbprint = result.stdout.strip().replace("sha1 Fingerprint=", "").replace(":", "")

    return {
        "cert_path": str(crt_file.absolute()),
        "pem_path": str(pem_file.absolute()),
        "thumbprint": thumbprint,
    }


def copy_to_clipboard(text: str) -> bool:
    """Try to copy text to clipboard. Returns True if successful."""
    try:
        # macOS
        subprocess.run(["pbcopy"], input=text.encode(), check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        pass

    try:
        # Linux with xclip
        subprocess.run(["xclip", "-selection", "clipboard"], input=text.encode(), check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        pass

    try:
        # Linux with xsel
        subprocess.run(["xsel", "--clipboard", "--input"], input=text.encode(), check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        pass

    return False


def setup():
    """Interactive setup for SharePoint MCP Server."""
    print("=" * 60)
    print("SharePoint MCP Server - Setup Wizard")
    print("=" * 60)
    print()

    # Step 1: Generate certificate
    print("[1/4] Generating certificate...")
    cert = generate_certificate()
    print(f"  ✓ Certificate: {cert['cert_path']}")
    print(f"  ✓ Thumbprint: {cert['thumbprint']}")
    print()

    # Step 2: Instructions for Azure
    print("[2/4] Upload certificate to Azure")
    print("-" * 40)
    print("1. Go to: https://portal.azure.com")
    print("2. App registrations → New registration (or select existing)")
    print("3. Certificates & secrets → Certificates → Upload certificate")
    print(f"4. Upload: {cert['cert_path']}")
    print("5. API permissions → Add → SharePoint → Application permissions")
    print("   → Sites.FullControl.All → Grant admin consent")
    print()
    input("Press Enter when done...")
    print()

    # Step 3: Collect user input
    print("[3/4] Enter your Azure app details")
    print("-" * 40)

    app_id = input("Application (client) ID: ").strip()
    while not app_id:
        app_id = input("Application (client) ID (required): ").strip()

    tenant_id = input("Directory (tenant) ID: ").strip()
    while not tenant_id:
        tenant_id = input("Directory (tenant) ID (required): ").strip()

    site_url = input(
        "SharePoint site URL (e.g., https://company.sharepoint.com/sites/MySite): "
    ).strip()
    while not site_url:
        site_url = input("SharePoint site URL (required): ").strip()

    doc_library = input("Document library [Shared Documents]: ").strip() or "Shared Documents"
    print()

    # Step 4: Generate config
    print("[4/4] Generating configuration...")
    print()

    config = {
        "mcpServers": {
            "sharepoint": {
                "command": "uvx",
                "args": ["mcp-sharepoint-cert"],
                "env": {
                    "SHP_ID_APP": app_id,
                    "SHP_TENANT_ID": tenant_id,
                    "SHP_SITE_URL": site_url,
                    "SHP_DOC_LIBRARY": doc_library,
                    "SHP_CERT_PATH": cert["pem_path"],
                    "SHP_CERT_THUMBPRINT": cert["thumbprint"],
                },
            }
        }
    }

    config_json = json.dumps(config, indent=2)

    # Save to file
    config_file = Path("claude_mcp_config.json")
    config_file.write_text(config_json)
    print(f"✓ Config saved to: {config_file.absolute()}")

    # Try to copy to clipboard
    if copy_to_clipboard(config_json):
        print("✓ Config copied to clipboard!")

    print()
    print("=" * 60)
    print("Configuration (add to Claude/Cursor config):")
    print("=" * 60)
    print()
    print(config_json)
    print()
    print("=" * 60)
    print("Config file locations:")
    print("  Claude: ~/Library/Application Support/Claude/claude_desktop_config.json")
    print("  Cursor: Check Cursor MCP settings")
    print("=" * 60)
    print()
    print("Done! Restart Claude/Cursor to connect to SharePoint.")


if __name__ == "__main__":
    setup()
