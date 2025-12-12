"""CLI for dossier-tools."""

from __future__ import annotations

import http
import json
import sys
from collections import OrderedDict
from pathlib import Path
from typing import Any

import click
import frontmatter

from .core import (
    ChecksumStatus,
    ParseError,
    calculate_checksum,
    parse_content,
    parse_file,
    validate_file,
    validate_frontmatter,
    verify_checksum,
)
from .logging import configure_logging
from .registry import (
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
from .signing import (
    SignatureStatus,
    ensure_dossier_dir,
    key_exists,
    load_signer,
    save_key_pair,
    sign_dossier,
    verify_dossier_signature,
)
from .signing.ed25519 import Ed25519Signer

# Command categories for help organization
COMMAND_SECTIONS: dict[str, list[str]] = OrderedDict(
    [
        ("Local Commands", ["init", "generate-keys", "create", "validate", "checksum", "sign", "verify", "info"]),
        ("Registry Commands", ["list", "get", "pull", "publish", "login", "logout", "whoami"]),
    ]
)


class SectionedGroup(click.Group):
    """A Click group that organizes commands into sections in help output."""

    def format_commands(self, ctx: click.Context, formatter: click.HelpFormatter) -> None:
        """Write all commands organized by section."""
        commands = []
        for subcommand in self.list_commands(ctx):
            cmd = self.get_command(ctx, subcommand)
            if cmd is None or cmd.hidden:
                continue
            commands.append((subcommand, cmd))

        if not commands:
            return

        # Build a lookup for quick access
        cmd_lookup = dict(commands)

        for section, cmd_names in COMMAND_SECTIONS.items():
            section_commands = []
            for name in cmd_names:
                if name in cmd_lookup:
                    cmd = cmd_lookup[name]
                    help_text = cmd.get_short_help_str(limit=formatter.width)
                    section_commands.append((name, help_text))

            if section_commands:
                with formatter.section(section):
                    formatter.write_dl(section_commands)


@click.group(cls=SectionedGroup)
@click.version_option()
def main() -> None:
    """Dossier tools for validating, signing, and verifying .ds.md files."""
    configure_logging()


@main.command()
def init() -> None:
    """Initialize ~/.dossier directory."""
    dossier_dir = ensure_dossier_dir()
    click.echo(f"Initialized dossier directory: {dossier_dir}")


@main.command("generate-keys")
@click.option("--name", default="default", help="Key name (default: 'default')")
@click.option("--force", is_flag=True, help="Overwrite existing keys")
def generate_keys(name: str, force: bool) -> None:
    """Generate a new Ed25519 key pair."""
    if key_exists(name) and not force:
        click.echo(f"Error: Key '{name}' already exists. Use --force to overwrite.", err=True)
        sys.exit(1)

    signer = Ed25519Signer.generate()
    private_path, public_path = save_key_pair(signer, name)

    click.echo(f"Generated key pair '{name}':")
    click.echo(f"  Private key: {private_path}")
    click.echo(f"  Public key:  {public_path}")
    click.echo()
    click.echo("Public key (for sharing):")
    click.echo(f"  {signer.get_public_key()}")


def _validate_create_frontmatter(fm: dict[str, Any]) -> None:
    """Validate frontmatter for create command, exit on error."""
    required = [("name", "--name"), ("title", "--title"), ("objective", "--objective")]
    for field, flag in required:
        if field not in fm:
            click.echo(f"Error: {flag} is required (or provide in --meta)", err=True)
            sys.exit(1)

    if "authors" not in fm or not fm["authors"]:
        click.echo("Error: --author is required (or provide in --meta)", err=True)
        sys.exit(1)

    for i, author in enumerate(fm["authors"]):
        if isinstance(author, str):
            click.echo(f"Error: authors[{i}] must be an object with 'name', not a string", err=True)
            click.echo('  Example: --meta with {"authors": [{"name": "Alice"}]}', err=True)
            sys.exit(1)
        if isinstance(author, dict) and "name" not in author:
            click.echo(f"Error: authors[{i}] missing required 'name' field", err=True)
            sys.exit(1)


@main.command()
@click.argument("input_file", type=click.Path(exists=True, path_type=Path))
@click.option("-o", "--output", type=click.Path(path_type=Path), help="Output file (default: .ds.md extension)")
@click.option("--meta", type=click.Path(exists=True, path_type=Path), help="JSON file with frontmatter fields")
@click.option("--name", "dossier_name", help="Dossier slug (lowercase, hyphens, e.g., 'my-workflow')")
@click.option("--title", help="Dossier title")
@click.option("--version", "doc_version", default="1.0.0", help="Version (default: 1.0.0)")
@click.option("--status", default="draft", help="Status (default: draft)")
@click.option("--objective", help="Objective description")
@click.option("--author", "authors", multiple=True, help="Author name (can be repeated)")
@click.option("--sign", "do_sign", is_flag=True, help="Sign the dossier after creation")
@click.option("--key", "key_name", default="default", help="Key name for signing (default: 'default')")
@click.option("--signed-by", help="Signer identity (required if --sign)")
def create(
    input_file: Path,
    output: Path | None,
    meta: Path | None,
    dossier_name: str | None,
    title: str | None,
    doc_version: str,
    status: str,
    objective: str | None,
    authors: tuple[str, ...],
    do_sign: bool,
    key_name: str,
    signed_by: str | None,
) -> None:
    """Create a dossier from a text file and metadata."""
    # Read body content
    body = input_file.read_text(encoding="utf-8")

    # Build frontmatter from meta file and/or options
    fm: dict[str, Any] = {}

    if meta:
        fm = json.loads(meta.read_text(encoding="utf-8"))

    # CLI options override meta file
    if dossier_name:
        fm["name"] = dossier_name
    if title:
        fm["title"] = title
    if objective:
        fm["objective"] = objective
    if authors:
        # Convert CLI author strings to objects with 'name'
        fm["authors"] = [{"name": a} for a in authors]

    # Set defaults
    fm.setdefault("schema_version", "1.0.0")
    fm["version"] = doc_version
    fm["status"] = status

    # Validate required fields and authors format
    _validate_create_frontmatter(fm)

    # Calculate checksum
    checksum_hash = calculate_checksum(body)
    fm["checksum"] = {"algorithm": "sha256", "hash": checksum_hash}

    # Build dossier content
    post = frontmatter.Post(body, **fm)
    content = frontmatter.dumps(post)

    # Optionally sign
    if do_sign:
        if not signed_by:
            click.echo("Error: --signed-by is required when using --sign", err=True)
            sys.exit(1)
        if not key_exists(key_name):
            click.echo(f"Error: Key '{key_name}' not found. Run 'dossier generate-keys' first.", err=True)
            sys.exit(1)
        signer = load_signer(key_name)
        content = sign_dossier(content, signer, signed_by)

    # Determine output path
    if output is None:
        output = input_file if input_file.name.endswith(".ds.md") else input_file.with_suffix(".ds.md")

    output.write_text(content, encoding="utf-8")
    click.echo(f"Created: {output}")


@main.command()
@click.argument("file", type=click.Path(exists=True, path_type=Path))
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def validate(file: Path, as_json: bool) -> None:
    """Validate dossier schema."""
    result = validate_file(file)

    if as_json:
        click.echo(json.dumps({"valid": result.valid, "errors": result.errors}))
    elif result.valid:
        click.echo(f"Valid: {file}")
    else:
        click.echo(f"Invalid: {file}", err=True)
        for error in result.errors:
            click.echo(f"  - {error}", err=True)

    sys.exit(0 if result.valid else 1)


@main.command()
@click.argument("file", type=click.Path(exists=True, path_type=Path))
@click.option("--update", "do_update", is_flag=True, help="Update checksum in file (default: verify)")
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def checksum(file: Path, do_update: bool, as_json: bool) -> None:
    """Verify or update dossier checksum."""
    content = file.read_text(encoding="utf-8")

    try:
        parsed = parse_content(content)
    except ParseError as e:
        if as_json:
            click.echo(json.dumps({"error": str(e)}))
        else:
            click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    if do_update:
        # Calculate and update checksum
        new_hash = calculate_checksum(parsed.body)
        parsed.frontmatter.setdefault("checksum", {})
        parsed.frontmatter["checksum"]["algorithm"] = "sha256"
        parsed.frontmatter["checksum"]["hash"] = new_hash

        post = frontmatter.Post(parsed.body, **parsed.frontmatter)
        file.write_text(frontmatter.dumps(post), encoding="utf-8")

        if as_json:
            click.echo(json.dumps({"updated": True, "hash": new_hash}))
        else:
            click.echo(f"Updated checksum: {new_hash}")
        sys.exit(0)

    # Verify mode
    result = verify_checksum(parsed.body, parsed.frontmatter)

    if as_json:
        click.echo(
            json.dumps(
                {
                    "status": result.status.value,
                    "valid": result.valid,
                    "expected": result.expected,
                    "actual": result.actual,
                }
            )
        )
    elif result.status == ChecksumStatus.VALID:
        click.echo(f"Checksum valid: {file}")
    elif result.status == ChecksumStatus.MISSING:
        click.echo(f"Checksum missing: {file}", err=True)
    else:
        click.echo(f"Checksum invalid: {file}", err=True)
        click.echo(f"  Expected: {result.expected}", err=True)
        click.echo(f"  Actual:   {result.actual}", err=True)

    sys.exit(0 if result.valid else 1)


@main.command()
@click.argument("file", type=click.Path(exists=True, path_type=Path))
@click.option("--key", "key_name", default="default", help="Key name from ~/.dossier/ (default: 'default')")
@click.option("--key-file", type=click.Path(exists=True, path_type=Path), help="Path to PEM key file")
@click.option("--signed-by", required=True, help="Signer identity (e.g., email)")
@click.option("-o", "--output", type=click.Path(path_type=Path), help="Output file (default: modify in place)")
def sign(file: Path, key_name: str, key_file: Path | None, signed_by: str, output: Path | None) -> None:
    """Sign a dossier."""
    # Load signer
    if key_file:
        signer = Ed25519Signer.from_pem_file(key_file)
    else:
        if not key_exists(key_name):
            click.echo(f"Error: Key '{key_name}' not found. Run 'dossier generate-keys' first.", err=True)
            sys.exit(1)
        signer = load_signer(key_name)

    # Read and sign
    content = file.read_text(encoding="utf-8")
    signed_content = sign_dossier(content, signer, signed_by)

    # Write output
    output_path = output or file
    output_path.write_text(signed_content, encoding="utf-8")

    if output:
        click.echo(f"Signed: {file} -> {output}")
    else:
        click.echo(f"Signed: {file}")


@main.command()
@click.argument("file", type=click.Path(exists=True, path_type=Path))
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def verify(file: Path, as_json: bool) -> None:
    """Verify dossier checksum and signature."""
    content = file.read_text(encoding="utf-8")

    try:
        parsed = parse_content(content)
    except ParseError as e:
        if as_json:
            click.echo(json.dumps({"error": str(e)}))
        else:
            click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    # Validate schema
    schema_result = validate_frontmatter(parsed.frontmatter)

    # Verify checksum
    checksum_result = verify_checksum(parsed.body, parsed.frontmatter)

    # Verify signature
    sig_result = verify_dossier_signature(content)

    # Determine overall validity
    all_valid = (
        schema_result.valid
        and checksum_result.valid
        and sig_result.status in (SignatureStatus.VALID, SignatureStatus.UNSIGNED)
    )

    if as_json:
        output_data = {
            "valid": all_valid,
            "schema": {"valid": schema_result.valid, "errors": schema_result.errors},
            "checksum": {
                "status": checksum_result.status.value,
                "valid": checksum_result.valid,
            },
            "signature": {
                "status": sig_result.status.value,
                "valid": sig_result.valid,
                "signed_by": sig_result.signed_by,
                "timestamp": sig_result.timestamp.isoformat() if sig_result.timestamp else None,
            },
        }
        click.echo(json.dumps(output_data))
    else:
        click.echo(f"File: {file}")
        click.echo()

        # Schema
        if schema_result.valid:
            click.echo("Schema:    valid")
        else:
            click.echo("Schema:    invalid", err=True)
            for error in schema_result.errors:
                click.echo(f"  - {error}", err=True)

        # Checksum
        if checksum_result.status == ChecksumStatus.VALID:
            click.echo("Checksum:  valid")
        elif checksum_result.status == ChecksumStatus.MISSING:
            click.echo("Checksum:  missing")
        else:
            click.echo("Checksum:  invalid", err=True)

        # Signature
        if sig_result.status == SignatureStatus.VALID:
            click.echo(f"Signature: valid (signed by: {sig_result.signed_by})")
        elif sig_result.status == SignatureStatus.UNSIGNED:
            click.echo("Signature: unsigned")
        else:
            click.echo(f"Signature: invalid ({sig_result.error})", err=True)

    sys.exit(0 if all_valid else 1)


def _display_metadata(fm: dict[str, Any], source: str, as_json: bool) -> None:
    """Display frontmatter metadata."""
    if as_json:
        click.echo(json.dumps(fm, default=str))
        return

    click.echo(f"Source: {source}")
    click.echo()

    # Core fields
    if "name" in fm:
        click.echo(f"Name:      {fm['name']}")
    if "title" in fm:
        click.echo(f"Title:     {fm['title']}")
    if "version" in fm:
        click.echo(f"Version:   {fm['version']}")
    if "status" in fm:
        click.echo(f"Status:    {fm['status']}")
    if "objective" in fm:
        click.echo(f"Objective: {fm['objective']}")

    # Authors
    if "authors" in fm:
        authors = fm["authors"]
        if isinstance(authors, list):
            # Handle both string authors and dict authors (with 'name' key)
            author_names = []
            for author in authors:
                if isinstance(author, dict):
                    author_names.append(author.get("name", str(author)))
                else:
                    author_names.append(str(author))
            click.echo(f"Authors:   {', '.join(author_names)}")
        else:
            click.echo(f"Authors:   {authors}")

    # Checksum
    if "checksum" in fm:
        cs = fm["checksum"]
        if isinstance(cs, dict):
            click.echo(f"Checksum:  {cs.get('algorithm', 'unknown')}:{cs.get('hash', 'unknown')[:16]}...")
        else:
            click.echo(f"Checksum:  {cs}")

    # Signature
    if "signature" in fm:
        sig = fm["signature"]
        if isinstance(sig, dict):
            click.echo(f"Signed by: {sig.get('signed_by', 'unknown')}")
            if "timestamp" in sig:
                click.echo(f"Signed at: {sig['timestamp']}")


@main.command()
@click.argument("file", type=click.Path(exists=True, path_type=Path))
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def info(file: Path, as_json: bool) -> None:
    """Display local dossier metadata."""
    try:
        parsed = parse_file(file)
    except ParseError as e:
        if as_json:
            click.echo(json.dumps({"error": str(e)}))
        else:
            click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    _display_metadata(parsed.frontmatter, str(file), as_json)


# --- Registry commands ---


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

    _display_metadata(result, f"registry:{dossier_name}", as_json)


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
    click.echo(f"Downloaded: {output}")

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
        from .registry import Credentials, save_credentials  # noqa: PLC0415

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


if __name__ == "__main__":
    main()
