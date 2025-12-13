"""Registry and execution CLI commands for dossier-tools."""

from __future__ import annotations

import http
import json
import shutil
import subprocess
import sys
from pathlib import Path

import click

from ..core import (
    ParseError,
    parse_file,
    validate_frontmatter,
    verify_checksum,
)
from ..registry import (
    OAuthError,
    RegistryError,
    delete_credentials,
    get_client,
    get_registry_url,
    load_credentials,
    load_token,
    parse_name_version,
    run_oauth_flow,
)
from . import display_metadata, main


@main.command("list")
@click.option("--category", help="Filter by category")
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def list_cmd(category: str | None, as_json: bool) -> None:
    """List dossiers from the registry."""
    try:
        with get_client() as client:
            result = client.list_dossiers(category=category)
    except RegistryError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    dossiers = result.get("dossiers", [])

    if as_json:
        click.echo(json.dumps(result))
    elif not dossiers:
        click.echo("No dossiers found.")
    else:
        # Print as table
        for d in dossiers:
            name = d.get("name", "")
            version = d.get("version", "")
            title = d.get("title", "")
            click.echo(f"{name:30} {version:10} {title}")


@main.command()
@click.argument("name")
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def get(name: str, as_json: bool) -> None:
    """Get dossier metadata from the registry."""
    dossier_name, version = parse_name_version(name)

    try:
        with get_client() as client:
            result = client.get_dossier(dossier_name, version=version)
    except RegistryError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    display_metadata(result, f"registry:{dossier_name}", as_json)


@main.command()
@click.argument("name")
@click.option("-o", "--output", type=click.Path(path_type=Path), help="Output file")
def pull(name: str, output: Path | None) -> None:
    """Download a dossier from the registry."""
    dossier_name, version = parse_name_version(name)

    try:
        with get_client() as client:
            content, digest = client.pull_content(dossier_name, version=version)
    except RegistryError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    # Determine output path
    if output is None:
        # Use last part of name as filename
        filename = dossier_name.replace("/", "-") + ".ds.md"
        output = Path(filename)

    # Write file
    output.write_text(content, encoding="utf-8")
    click.echo(f"Downloaded: {output.resolve()}")

    if digest:
        click.echo(f"Digest: {digest}")


@main.command()
def login() -> None:
    """Authenticate with the registry via GitHub."""
    registry_url = get_registry_url()

    # Check if already logged in
    creds = load_credentials()
    if creds and not creds.is_expired():
        click.echo(f"Already logged in as {creds.username}")
        if not click.confirm("Login again?"):
            return

    click.echo("Opening browser for GitHub authentication...")

    try:
        result = run_oauth_flow(registry_url)

        # Save credentials
        from ..registry import Credentials, save_credentials  # noqa: PLC0415

        save_credentials(
            Credentials(
                token=result.token,
                username=result.username,
                orgs=result.orgs,
            )
        )

        click.echo(f"Logged in as {result.username}" + (f" ({result.email})" if result.email else ""))
        click.echo("Credentials saved to ~/.dossier/credentials")
    except OAuthError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@main.command()
def logout() -> None:
    """Remove saved authentication."""
    if delete_credentials():
        click.echo("Logged out successfully.")
    else:
        click.echo("Not logged in.")


@main.command()
def whoami() -> None:
    """Show current authenticated user."""
    creds = load_credentials()
    if not creds:
        click.echo("Not logged in. Run 'dossier login' to authenticate.")
        sys.exit(1)

    if creds.is_expired():
        click.echo("Session expired. Run 'dossier login' to re-authenticate.")
        sys.exit(1)

    click.echo(f"Logged in as: {creds.username}")
    if creds.orgs:
        click.echo(f"Orgs:         {', '.join(creds.orgs)}")


@main.command()
@click.argument("file", type=click.Path(exists=True, path_type=Path))
@click.option("--namespace", required=True, help="Target namespace (e.g., 'myuser/tools' or 'myorg/category')")
@click.option("--changelog", help="Changelog message for this version")
def publish(file: Path, namespace: str, changelog: str | None) -> None:
    """Publish a dossier to the registry."""
    token = load_token()
    if not token:
        click.echo("Not logged in. Run 'dossier login' first.", err=True)
        sys.exit(1)

    # Parse and validate file
    try:
        dossier = parse_file(file)
    except ParseError as e:
        click.echo(f"Error parsing file: {e}", err=True)
        sys.exit(1)

    # Validate schema
    schema_result = validate_frontmatter(dossier.frontmatter)
    if not schema_result.valid:
        click.echo("Validation errors:", err=True)
        for err in schema_result.errors:
            click.echo(f"  - {err}", err=True)
        sys.exit(1)

    # Verify checksum
    checksum_result = verify_checksum(dossier.body, dossier.frontmatter)
    if not checksum_result.valid:
        click.echo(f"Checksum error: {checksum_result.status.value}", err=True)
        sys.exit(1)

    # Get name from frontmatter for display
    name = dossier.frontmatter.get("name", file.stem)
    version = dossier.frontmatter.get("version", "unknown")

    # Publish
    try:
        with get_client(token=token) as client:
            content = file.read_text(encoding="utf-8")
            result = client.publish(namespace, content, changelog=changelog)
            full_name = result.get("name", f"{namespace}/{name}")
            click.echo(f"Published {full_name}@{version}")
            if "content_url" in result:
                click.echo(f"URL: {result['content_url']}")
            click.echo()
            click.echo("Note: It may take 1-2 minutes for the dossier to appear in 'dossier list'.")
    except RegistryError as e:
        if e.status_code == http.HTTPStatus.UNAUTHORIZED:
            click.echo("Session expired. Run 'dossier login' to re-authenticate.", err=True)
        elif e.status_code == http.HTTPStatus.FORBIDDEN:
            click.echo(f"Permission denied: {e}", err=True)
        elif e.status_code == http.HTTPStatus.CONFLICT:
            click.echo(f"Version conflict: {e}", err=True)
        else:
            click.echo(f"Error: {e}", err=True)
        sys.exit(1)


# --- Execution commands ---


@main.command()
@click.argument("name")
@click.option("--print-only", is_flag=True, help="Print the workflow content instead of running it")
def run(name: str, print_only: bool) -> None:
    """Run a dossier workflow using Claude Code.

    Pulls the workflow from the registry and starts an interactive Claude Code
    session with the workflow as the initial prompt.

    NAME can be 'workflow-name' or 'workflow-name@version'.

    Supported agents: Claude Code only (https://claude.ai/code)
    """
    # Check if claude is available
    claude_path = shutil.which("claude")
    if not claude_path and not print_only:
        click.echo("Error: Claude Code is not installed or not in PATH.", err=True)
        click.echo("", err=True)
        click.echo("To install Claude Code, visit: https://claude.ai/code", err=True)
        click.echo("", err=True)
        click.echo("Note: Currently, only Claude Code is supported as an execution agent.", err=True)
        sys.exit(1)

    # Pull the workflow from registry
    dossier_name, version = parse_name_version(name)

    try:
        with get_client() as client:
            content, _ = client.pull_content(dossier_name, version=version)
    except RegistryError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    if print_only:
        click.echo(content)
        return

    # Execute with Claude Code
    click.echo(f"Running workflow: {dossier_name}" + (f"@{version}" if version else ""))
    click.echo("Starting Claude Code...")
    click.echo()

    # Start interactive Claude Code session with workflow as initial prompt
    # claude_path is guaranteed to be set here (checked above)
    # Use "--" to signal end of options, since content may start with "---"
    result = subprocess.run(
        [claude_path, "--", content],
        check=False,
    )

    sys.exit(result.returncode)
