"""Certificate setup for SharePoint MCP Server with Typer + Rich CLI."""

import json
import subprocess
import sys
from pathlib import Path

import typer
from rich import print as rprint
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.syntax import Syntax
from rich.table import Table

app = typer.Typer(
    name="mcp-sharepoint-cert-setup",
    help="Setup wizard for SharePoint MCP Server",
    add_completion=False,
)
console = Console()

# AI client configurations
AI_CLIENTS: dict[str, dict[str, str | bool]] = {
    "claude-desktop": {
        "name": "Claude Desktop",
        "method": "Config file",
        "manual": False,
    },
    "claude-code": {
        "name": "Claude Code (CLI)",
        "method": "CLI command",
        "manual": False,
    },
    "cursor": {
        "name": "Cursor",
        "method": "Config file",
        "manual": True,
    },
    "windsurf": {
        "name": "Windsurf",
        "method": "Config file",
        "manual": True,
    },
    "other": {
        "name": "Other AI Assistant",
        "method": "Manual",
        "manual": True,
    },
}


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
        rprint("[red]Error: openssl not found. Please install OpenSSL.[/red]")
        rprint("  macOS: [cyan]brew install openssl[/cyan]")
        rprint("  Ubuntu: [cyan]sudo apt install openssl[/cyan]")
        raise typer.Exit(1) from None
    except subprocess.CalledProcessError as e:
        rprint(f"[red]Error generating certificate: {e.stderr.decode()}[/red]")
        raise typer.Exit(1) from e

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
        subprocess.run(["pbcopy"], input=text.encode(), check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        pass

    try:
        subprocess.run(["xclip", "-selection", "clipboard"], input=text.encode(), check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        pass

    try:
        subprocess.run(["xsel", "--clipboard", "--input"], input=text.encode(), check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        pass

    return False


def generate_mcp_config(
    app_id: str,
    tenant_id: str,
    site_url: str,
    doc_library: str,
    pem_path: str,
    thumbprint: str,
) -> dict:
    """Generate the MCP server configuration."""
    return {
        "mcpServers": {
            "sharepoint": {
                "command": "uvx",
                "args": ["mcp-sharepoint-cert"],
                "env": {
                    "SHP_ID_APP": app_id,
                    "SHP_TENANT_ID": tenant_id,
                    "SHP_SITE_URL": site_url,
                    "SHP_DOC_LIBRARY": doc_library,
                    "SHP_CERT_PATH": pem_path,
                    "SHP_CERT_THUMBPRINT": thumbprint,
                },
            }
        }
    }


def generate_ai_prompt(
    client: str,
    config: dict,
    cert_path: str,
) -> str:
    """Generate a prompt for an AI assistant to configure the MCP server."""
    client_info = AI_CLIENTS.get(client, AI_CLIENTS["other"])
    config_json = json.dumps(config, indent=2)

    prompt = f"""# SharePoint MCP Server - Installation Request

I've just set up the SharePoint MCP Server and need help adding it to my AI assistant configuration.

## My Setup Details
- **AI Client**: {client_info["name"]}
- **Certificate Location**: {cert_path}

## MCP Server Configuration
```json
{config_json}
```

## What I Need You To Do
"""

    if client == "claude-desktop":
        # Platform-specific config paths
        if sys.platform == "darwin":
            path = "~/Library/Application Support/Claude/claude_desktop_config.json"
        elif sys.platform == "win32":
            path = "%APPDATA%/Claude/claude_desktop_config.json"
        else:
            path = "~/.config/Claude/claude_desktop_config.json"

        prompt += f"""
1. Read my Claude Desktop config file at: `{path}`
2. Merge the SharePoint MCP server configuration above into the existing `mcpServers` object
3. Save the updated configuration
4. Tell me to restart Claude Desktop

**Important**: Preserve any existing MCP servers in the config - just add the new "sharepoint" entry.
"""

    elif client == "claude-code":
        prompt += """
1. Run the following command to add the SharePoint MCP server:
```bash
claude mcp add sharepoint uvx -- mcp-sharepoint-cert
```

2. Then set the required environment variables for the MCP server:
```bash
claude mcp update sharepoint --env SHP_ID_APP="{app_id}" --env SHP_TENANT_ID="{tenant_id}" --env SHP_SITE_URL="{site_url}" --env SHP_DOC_LIBRARY="{doc_library}" --env SHP_CERT_PATH="{cert_path}" --env SHP_CERT_THUMBPRINT="{thumbprint}"
```

Replace the placeholder values with the ones from the configuration above.
""".format(**config["mcpServers"]["sharepoint"]["env"])

    elif client == "cursor":
        prompt += """
1. Open Cursor Settings (Cmd/Ctrl + ,)
2. Search for "MCP" in settings
3. Add the SharePoint MCP server configuration from above
4. Save and restart Cursor

If Cursor uses a JSON config file, merge the `mcpServers` object above into it.
"""

    elif client == "windsurf":
        prompt += """
1. Open or create the Windsurf MCP config at: `~/.codeium/windsurf/mcp_config.json`
2. Merge the SharePoint MCP server configuration above into the existing config
3. Save and restart Windsurf
"""

    else:
        prompt += """
1. Find where your AI assistant stores MCP server configurations
2. Add the SharePoint MCP server configuration from above
3. Restart your AI assistant to load the new server

The configuration follows the standard MCP server format with:
- `command`: The executable to run (`uvx`)
- `args`: Arguments to pass (`mcp-sharepoint-cert`)
- `env`: Environment variables for authentication
"""

    prompt += """
## Verification
After configuration, verify the SharePoint server is connected by checking if these tools are available:
- List_SharePoint_Folders
- List_SharePoint_Documents
- Get_Document_Content
- Upload_Document

Let me know when the configuration is complete!
"""

    return prompt


def display_client_menu() -> str:
    """Display AI client selection menu and return choice."""
    table = Table(title="Select Your AI Assistant", show_header=True, header_style="bold magenta")
    table.add_column("#", style="cyan", width=4)
    table.add_column("AI Assistant", style="green")
    table.add_column("Config Method", style="yellow")

    clients = list(AI_CLIENTS.items())
    for i, (_key, info) in enumerate(clients, 1):
        method = str(info.get("method", "Config file"))
        if info.get("manual"):
            method += " (manual)"
        table.add_row(str(i), str(info["name"]), method)

    console.print(table)
    console.print()

    choice = Prompt.ask(
        "Enter number",
        choices=[str(i) for i in range(1, len(clients) + 1)],
        default="1",
    )

    return clients[int(choice) - 1][0]


@app.command()
def setup(
    output_dir: str = typer.Option("certs", "--output", "-o", help="Certificate output directory"),
    days: int = typer.Option(365, "--days", "-d", help="Certificate validity in days"),
    skip_cert: bool = typer.Option(False, "--skip-cert", help="Skip certificate generation"),
):
    """Interactive setup wizard for SharePoint MCP Server."""
    console.print()
    console.print(
        Panel.fit(
            "[bold blue]SharePoint MCP Server[/bold blue]\n[dim]Setup Wizard[/dim]",
            border_style="blue",
        )
    )
    console.print()

    # Step 1: Generate certificate
    if skip_cert:
        console.print("[yellow]Skipping certificate generation...[/yellow]")
        pem_path = Prompt.ask("Path to existing .pem file")
        thumbprint = Prompt.ask("Certificate thumbprint")
        cert = {"pem_path": pem_path, "thumbprint": thumbprint, "cert_path": pem_path}
    else:
        with console.status("[bold green]Generating certificate...", spinner="dots"):
            cert = generate_certificate(output_dir, days)

        console.print(f"[green]✓[/green] Certificate: [cyan]{cert['cert_path']}[/cyan]")
        console.print(f"[green]✓[/green] Thumbprint: [cyan]{cert['thumbprint']}[/cyan]")
        console.print()

    # Step 2: Azure instructions
    console.print(
        Panel(
            "[bold]Upload certificate to Azure[/bold]\n\n"
            "1. Go to [link=https://portal.azure.com]portal.azure.com[/link]\n"
            "2. App registrations → New registration (or select existing)\n"
            "3. Certificates & secrets → Certificates → Upload\n"
            f"   [cyan]{cert['cert_path']}[/cyan]\n"
            "4. API permissions → Add → SharePoint → Application\n"
            "   → Sites.FullControl.All → Grant admin consent\n"
            "5. Copy the Application ID and Tenant ID",
            title="[bold yellow]Step 1: Azure Setup[/bold yellow]",
            border_style="yellow",
        )
    )
    console.print()

    if not Confirm.ask("Have you completed the Azure setup?"):
        rprint("[yellow]Please complete Azure setup first, then run this wizard again.[/yellow]")
        raise typer.Exit(0)

    console.print()

    # Step 3: Collect Azure details
    console.print("[bold]Step 2: Enter Azure App Details[/bold]")
    console.print()

    app_id = Prompt.ask("Application (client) ID")
    while not app_id:
        app_id = Prompt.ask("[red]Required:[/red] Application (client) ID")

    tenant_id = Prompt.ask("Directory (tenant) ID")
    while not tenant_id:
        tenant_id = Prompt.ask("[red]Required:[/red] Directory (tenant) ID")

    site_url = Prompt.ask(
        "SharePoint site URL", default="https://company.sharepoint.com/sites/MySite"
    )
    while not site_url or site_url == "https://company.sharepoint.com/sites/MySite":
        site_url = Prompt.ask(
            "[red]Required:[/red] SharePoint site URL (e.g., https://company.sharepoint.com/sites/MySite)"
        )

    doc_library = Prompt.ask("Document library", default="Shared Documents")

    console.print()

    # Step 4: Select AI client
    console.print("[bold]Step 3: Select Your AI Assistant[/bold]")
    console.print()
    client = display_client_menu()
    console.print()

    # Generate config
    config = generate_mcp_config(
        app_id=app_id,
        tenant_id=tenant_id,
        site_url=site_url,
        doc_library=doc_library,
        pem_path=cert["pem_path"],
        thumbprint=cert["thumbprint"],
    )

    config_json = json.dumps(config, indent=2)

    # Save config file
    config_file = Path("sharepoint_mcp_config.json")
    config_file.write_text(config_json)

    console.print(f"[green]✓[/green] Config saved: [cyan]{config_file.absolute()}[/cyan]")

    # Generate AI prompt
    ai_prompt = generate_ai_prompt(client, config, cert["pem_path"])

    # Save AI prompt
    prompt_file = Path("INSTALL_WITH_AI.md")
    prompt_file.write_text(ai_prompt)

    console.print(f"[green]✓[/green] AI prompt saved: [cyan]{prompt_file.absolute()}[/cyan]")

    # Copy to clipboard
    if copy_to_clipboard(ai_prompt):
        console.print("[green]✓[/green] AI prompt copied to clipboard!")

    console.print()

    # Display the config
    console.print(
        Panel(
            Syntax(config_json, "json", theme="monokai", line_numbers=False),
            title="[bold green]MCP Configuration[/bold green]",
            border_style="green",
        )
    )

    console.print()

    # Final instructions
    client_info = AI_CLIENTS[client]
    console.print(
        Panel(
            f"[bold]Next Steps for {client_info['name']}[/bold]\n\n"
            "1. Open your AI assistant\n"
            f"2. Paste the contents of [cyan]INSTALL_WITH_AI.md[/cyan]\n"
            "   (already copied to clipboard!)\n"
            "3. Let your AI assistant configure the MCP server for you\n"
            "4. Restart your AI assistant\n\n"
            "[dim]The AI prompt includes all the details needed for your\n"
            "assistant to automatically configure the SharePoint connection.[/dim]",
            title="[bold blue]Setup Complete![/bold blue]",
            border_style="blue",
        )
    )

    console.print()
    rprint(
        "[bold green]Done![/bold green] Paste the AI prompt into your assistant to finish setup."
    )
    console.print()


def main():
    """Entry point for the setup command."""
    app()


if __name__ == "__main__":
    main()
