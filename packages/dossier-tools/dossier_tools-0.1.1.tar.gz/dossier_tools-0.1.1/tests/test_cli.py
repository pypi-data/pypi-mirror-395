"""Tests for the CLI."""

import json

import respx
from click.testing import CliRunner
from httpx import Response

from dossier_tools.cli import COMMAND_SECTIONS, main
from dossier_tools.signing import get_dossier_dir, get_private_key_path, get_public_key_path

from .conftest import FIXTURES_DIR


class TestCommandSections:
    """Tests for CLI command organization."""

    def test_all_commands_in_sections(self):
        """All commands should be listed in COMMAND_SECTIONS for help display."""
        # Get all registered commands
        registered_commands = set(main.commands.keys())

        # Get all commands listed in sections
        sectioned_commands = set()
        for cmd_list in COMMAND_SECTIONS.values():
            sectioned_commands.update(cmd_list)

        # Find commands missing from sections
        missing = registered_commands - sectioned_commands
        assert not missing, f"Commands not in COMMAND_SECTIONS: {missing}"

    def test_no_stale_commands_in_sections(self):
        """COMMAND_SECTIONS should not list non-existent commands."""
        registered_commands = set(main.commands.keys())

        sectioned_commands = set()
        for cmd_list in COMMAND_SECTIONS.values():
            sectioned_commands.update(cmd_list)

        # Find stale entries in sections
        stale = sectioned_commands - registered_commands
        assert not stale, f"Stale commands in COMMAND_SECTIONS: {stale}"


class TestInit:
    """Tests for init command."""

    def test_creates_dossier_directory(self, tmp_path, monkeypatch):
        """Should create ~/.dossier directory."""
        monkeypatch.setenv("HOME", str(tmp_path))
        runner = CliRunner()

        result = runner.invoke(main, ["init"])

        assert result.exit_code == 0
        assert (tmp_path / ".dossier").is_dir()
        assert "Initialized" in result.output


class TestGenerateKeys:
    """Tests for generate-keys command."""

    def test_generates_key_pair(self, tmp_path, monkeypatch):
        """Should generate key pair in ~/.dossier."""
        monkeypatch.setenv("HOME", str(tmp_path))
        runner = CliRunner()

        result = runner.invoke(main, ["generate-keys"])

        assert result.exit_code == 0
        assert (tmp_path / ".dossier" / "default.pem").exists()
        assert (tmp_path / ".dossier" / "default.pub").exists()
        assert "Generated key pair" in result.output

    def test_generates_named_key(self, tmp_path, monkeypatch):
        """Should generate key with custom name."""
        monkeypatch.setenv("HOME", str(tmp_path))
        runner = CliRunner()

        result = runner.invoke(main, ["generate-keys", "--name", "mykey"])

        assert result.exit_code == 0
        assert (tmp_path / ".dossier" / "mykey.pem").exists()
        assert (tmp_path / ".dossier" / "mykey.pub").exists()

    def test_fails_if_key_exists(self, tmp_path, monkeypatch):
        """Should fail if key already exists without --force."""
        monkeypatch.setenv("HOME", str(tmp_path))
        runner = CliRunner()

        # Generate first key
        runner.invoke(main, ["generate-keys"])

        # Try to generate again
        result = runner.invoke(main, ["generate-keys"])

        assert result.exit_code == 1
        assert "already exists" in result.output

    def test_force_overwrites_key(self, tmp_path, monkeypatch):
        """Should overwrite key with --force."""
        monkeypatch.setenv("HOME", str(tmp_path))
        runner = CliRunner()

        # Generate first key
        runner.invoke(main, ["generate-keys"])
        original_pub = (tmp_path / ".dossier" / "default.pub").read_text()

        # Force overwrite
        result = runner.invoke(main, ["generate-keys", "--force"])

        assert result.exit_code == 0
        new_pub = (tmp_path / ".dossier" / "default.pub").read_text()
        assert new_pub != original_pub


class TestCreate:
    """Tests for create command."""

    def test_missing_title(self, tmp_path, monkeypatch):
        """Should error when --title is missing."""
        monkeypatch.setenv("HOME", str(tmp_path))
        runner = CliRunner()

        input_file = tmp_path / "input.md"
        input_file.write_text("Body content.")

        result = runner.invoke(
            main,
            ["create", str(input_file), "--name", "test", "--objective", "Test", "--author", "test@example.com"],
        )

        assert result.exit_code == 1
        assert "--title is required" in result.output

    def test_missing_objective(self, tmp_path, monkeypatch):
        """Should error when --objective is missing."""
        monkeypatch.setenv("HOME", str(tmp_path))
        runner = CliRunner()

        input_file = tmp_path / "input.md"
        input_file.write_text("Body content.")

        result = runner.invoke(
            main,
            ["create", str(input_file), "--name", "test", "--title", "Test", "--author", "test@example.com"],
        )

        assert result.exit_code == 1
        assert "--objective is required" in result.output

    def test_missing_author(self, tmp_path, monkeypatch):
        """Should error when --author is missing."""
        monkeypatch.setenv("HOME", str(tmp_path))
        runner = CliRunner()

        input_file = tmp_path / "input.md"
        input_file.write_text("Body content.")

        result = runner.invoke(
            main,
            ["create", str(input_file), "--name", "test", "--title", "Test", "--objective", "Test objective"],
        )

        assert result.exit_code == 1
        assert "--author is required" in result.output

    def test_sign_without_signed_by(self, tmp_path, monkeypatch):
        """Should error when --sign used without --signed-by."""
        monkeypatch.setenv("HOME", str(tmp_path))
        runner = CliRunner()

        # Generate key first
        runner.invoke(main, ["generate-keys"])

        input_file = tmp_path / "input.md"
        input_file.write_text("Body content.")

        result = runner.invoke(
            main,
            [
                "create",
                str(input_file),
                "--name",
                "test",
                "--title",
                "Test",
                "--objective",
                "Test objective",
                "--author",
                "test@example.com",
                "--sign",
            ],
        )

        assert result.exit_code == 1
        assert "--signed-by is required" in result.output

    def test_sign_missing_key(self, tmp_path, monkeypatch):
        """Should error when signing key doesn't exist."""
        monkeypatch.setenv("HOME", str(tmp_path))
        runner = CliRunner()

        # Don't generate key
        input_file = tmp_path / "input.md"
        input_file.write_text("Body content.")

        result = runner.invoke(
            main,
            [
                "create",
                str(input_file),
                "--name",
                "test",
                "--title",
                "Test",
                "--objective",
                "Test objective",
                "--author",
                "test@example.com",
                "--sign",
                "--signed-by",
                "test@example.com",
            ],
        )

        assert result.exit_code == 1
        assert "not found" in result.output

    def test_creates_dossier_from_markdown(self, tmp_path, monkeypatch):
        """Should create dossier from markdown file."""
        monkeypatch.setenv("HOME", str(tmp_path))
        runner = CliRunner()

        # Create input file
        input_file = tmp_path / "input.md"
        input_file.write_text("# Hello World\n\nThis is the body.")

        result = runner.invoke(
            main,
            [
                "create",
                str(input_file),
                "--name",
                "test-dossier",
                "--title",
                "Test Dossier",
                "--objective",
                "Test objective",
                "--author",
                "test@example.com",
            ],
        )

        assert result.exit_code == 0
        output_file = tmp_path / "input.ds.md"
        assert output_file.exists()
        content = output_file.read_text()
        assert "name: test-dossier" in content
        assert "title: Test Dossier" in content
        assert "checksum:" in content

    def test_creates_dossier_with_meta_file(self, tmp_path, monkeypatch):
        """Should read metadata from JSON file."""
        monkeypatch.setenv("HOME", str(tmp_path))
        runner = CliRunner()

        # Create input file
        input_file = tmp_path / "input.md"
        input_file.write_text("Body content here.")

        # Create meta file
        meta_file = tmp_path / "meta.json"
        meta_file.write_text(
            json.dumps(
                {
                    "name": "from-meta",
                    "title": "From Meta",
                    "objective": "Meta objective",
                    "authors": [{"name": "meta@example.com"}],
                }
            )
        )

        result = runner.invoke(main, ["create", str(input_file), "--meta", str(meta_file)])

        assert result.exit_code == 0
        content = (tmp_path / "input.ds.md").read_text()
        assert "name: from-meta" in content
        assert "title: From Meta" in content

    def test_creates_and_signs(self, tmp_path, monkeypatch):
        """Should create and sign dossier with --sign."""
        monkeypatch.setenv("HOME", str(tmp_path))
        runner = CliRunner()

        # Generate key first
        runner.invoke(main, ["generate-keys"])

        # Create input file
        input_file = tmp_path / "input.md"
        input_file.write_text("Signed content.")

        result = runner.invoke(
            main,
            [
                "create",
                str(input_file),
                "--name",
                "signed-dossier",
                "--title",
                "Signed Dossier",
                "--objective",
                "Test objective",
                "--author",
                "test@example.com",
                "--sign",
                "--signed-by",
                "signer@example.com",
            ],
        )

        assert result.exit_code == 0
        content = (tmp_path / "input.ds.md").read_text()
        assert "signature:" in content


class TestValidate:
    """Tests for validate command."""

    def test_valid_file(self):
        """Should return 0 for valid file."""
        runner = CliRunner()
        result = runner.invoke(main, ["validate", str(FIXTURES_DIR / "valid" / "minimal.ds.md")])

        assert result.exit_code == 0
        assert "Valid" in result.output

    def test_invalid_file(self):
        """Should return 1 for invalid file."""
        runner = CliRunner()
        result = runner.invoke(main, ["validate", str(FIXTURES_DIR / "invalid" / "missing-title.ds.md")])

        assert result.exit_code == 1
        assert "Invalid" in result.output

    def test_json_output(self):
        """Should output JSON with --json."""
        runner = CliRunner()
        result = runner.invoke(main, ["validate", str(FIXTURES_DIR / "valid" / "minimal.ds.md"), "--json"])

        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["valid"] is True


class TestChecksum:
    """Tests for checksum command."""

    def test_parse_error(self, tmp_path):
        """Should show error for unparseable file."""
        runner = CliRunner()

        dst = tmp_path / "bad.ds.md"
        dst.write_text("no frontmatter")

        result = runner.invoke(main, ["checksum", str(dst)])

        assert result.exit_code == 1
        assert "Error" in result.output

    def test_parse_error_json(self, tmp_path):
        """Should show error in JSON format."""
        runner = CliRunner()

        dst = tmp_path / "bad.ds.md"
        dst.write_text("no frontmatter")

        result = runner.invoke(main, ["checksum", str(dst), "--json"])

        assert result.exit_code == 1
        data = json.loads(result.output)
        assert "error" in data

    def test_missing_checksum(self):
        """Should show missing status."""
        runner = CliRunner()
        result = runner.invoke(main, ["checksum", str(FIXTURES_DIR / "invalid" / "missing-checksum.ds.md")])

        assert result.exit_code == 1
        assert "missing" in result.output.lower()

    def test_update_json_output(self, tmp_path):
        """Should output JSON on update."""
        runner = CliRunner()

        src = FIXTURES_DIR / "valid" / "minimal.ds.md"
        dst = tmp_path / "test.ds.md"
        dst.write_text(src.read_text())

        result = runner.invoke(main, ["checksum", str(dst), "--update", "--json"])

        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["updated"] is True
        assert "hash" in data

    def test_verify_valid_checksum(self):
        """Should return 0 for valid checksum."""
        runner = CliRunner()
        result = runner.invoke(main, ["checksum", str(FIXTURES_DIR / "valid" / "minimal.ds.md")])

        assert result.exit_code == 0
        assert "valid" in result.output.lower()

    def test_update_checksum(self, tmp_path):
        """Should update checksum in file."""
        runner = CliRunner()

        # Copy file to temp
        src = FIXTURES_DIR / "valid" / "minimal.ds.md"
        dst = tmp_path / "test.ds.md"
        dst.write_text(src.read_text())

        # Modify body to invalidate checksum
        content = dst.read_text()
        content = content.replace("This is the body content.", "This is modified body content.")
        dst.write_text(content)

        # Verify it's invalid first
        result = runner.invoke(main, ["checksum", str(dst)])
        assert result.exit_code == 1

        # Update checksum
        result = runner.invoke(main, ["checksum", str(dst), "--update"])
        assert result.exit_code == 0
        assert "Updated" in result.output

        # Verify it's now valid
        result = runner.invoke(main, ["checksum", str(dst)])
        assert result.exit_code == 0

    def test_json_output(self):
        """Should output JSON with --json."""
        runner = CliRunner()
        result = runner.invoke(main, ["checksum", str(FIXTURES_DIR / "valid" / "minimal.ds.md"), "--json"])

        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["status"] == "valid"


class TestSign:
    """Tests for sign command."""

    def test_sign_missing_key(self, tmp_path, monkeypatch):
        """Should error when key doesn't exist."""
        monkeypatch.setenv("HOME", str(tmp_path))
        runner = CliRunner()

        # Don't generate key - just init
        (tmp_path / ".dossier").mkdir()

        src = FIXTURES_DIR / "valid" / "minimal.ds.md"
        dst = tmp_path / "test.ds.md"
        dst.write_text(src.read_text())

        result = runner.invoke(main, ["sign", str(dst), "--signed-by", "test@example.com"])

        assert result.exit_code == 1
        assert "not found" in result.output

    def test_sign_with_default_key(self, tmp_path, monkeypatch):
        """Should sign file with default key."""
        monkeypatch.setenv("HOME", str(tmp_path))
        runner = CliRunner()

        # Generate key
        runner.invoke(main, ["generate-keys"])

        # Copy file to temp
        src = FIXTURES_DIR / "valid" / "minimal.ds.md"
        dst = tmp_path / "test.ds.md"
        dst.write_text(src.read_text())

        result = runner.invoke(main, ["sign", str(dst), "--signed-by", "test@example.com"])

        assert result.exit_code == 0
        content = dst.read_text()
        assert "signature:" in content

    def test_sign_with_key_file(self, tmp_path, monkeypatch):
        """Should sign file with specific key file."""
        monkeypatch.setenv("HOME", str(tmp_path))
        runner = CliRunner()

        # Generate key
        runner.invoke(main, ["generate-keys"])

        # Copy file to temp
        src = FIXTURES_DIR / "valid" / "minimal.ds.md"
        dst = tmp_path / "test.ds.md"
        dst.write_text(src.read_text())

        key_file = tmp_path / ".dossier" / "default.pem"

        result = runner.invoke(main, ["sign", str(dst), "--key-file", str(key_file), "--signed-by", "test@example.com"])

        assert result.exit_code == 0

    def test_sign_to_output_file(self, tmp_path, monkeypatch):
        """Should write to output file without modifying original."""
        monkeypatch.setenv("HOME", str(tmp_path))
        runner = CliRunner()

        # Generate key
        runner.invoke(main, ["generate-keys"])

        # Copy file to temp
        src = FIXTURES_DIR / "valid" / "minimal.ds.md"
        original = tmp_path / "original.ds.md"
        original.write_text(src.read_text())
        original_content = original.read_text()

        output = tmp_path / "signed.ds.md"

        result = runner.invoke(main, ["sign", str(original), "--signed-by", "test@example.com", "-o", str(output)])

        assert result.exit_code == 0
        assert output.exists()
        assert "signature:" in output.read_text()
        # Original unchanged
        assert original.read_text() == original_content


class TestVerify:
    """Tests for verify command."""

    def test_verify_invalid_schema(self):
        """Should show schema errors."""
        runner = CliRunner()
        result = runner.invoke(main, ["verify", str(FIXTURES_DIR / "invalid" / "missing-title.ds.md")])

        assert result.exit_code == 1
        assert "Schema:" in result.output
        assert "invalid" in result.output.lower()

    def test_verify_invalid_checksum(self, tmp_path):
        """Should show checksum error."""
        runner = CliRunner()

        # Create file with wrong checksum
        dst = tmp_path / "test.ds.md"
        dst.write_text("""---
schema_version: "1.0.0"
title: Test Dossier
version: "1.0.0"
status: stable
objective: This is the objective
authors:
  - name: Test
checksum:
  algorithm: sha256
  hash: 0000000000000000000000000000000000000000000000000000000000000000
---

# Test

Body content.
""")

        result = runner.invoke(main, ["verify", str(dst)])

        assert result.exit_code == 1
        assert "Checksum:" in result.output
        assert "invalid" in result.output.lower()

    def test_verify_parse_error(self, tmp_path):
        """Should show parse error."""
        runner = CliRunner()

        dst = tmp_path / "bad.ds.md"
        dst.write_text("no frontmatter here")

        result = runner.invoke(main, ["verify", str(dst)])

        assert result.exit_code == 1
        assert "Error" in result.output

    def test_verify_parse_error_json(self, tmp_path):
        """Should show parse error in JSON."""
        runner = CliRunner()

        dst = tmp_path / "bad.ds.md"
        dst.write_text("no frontmatter here")

        result = runner.invoke(main, ["verify", str(dst), "--json"])

        assert result.exit_code == 1
        data = json.loads(result.output)
        assert "error" in data

    def test_verify_valid_unsigned(self):
        """Should verify valid unsigned dossier."""
        runner = CliRunner()
        result = runner.invoke(main, ["verify", str(FIXTURES_DIR / "valid" / "minimal.ds.md")])

        assert result.exit_code == 0
        assert "Schema:    valid" in result.output
        assert "Checksum:  valid" in result.output
        assert "unsigned" in result.output.lower()

    def test_verify_signed_dossier(self, tmp_path, monkeypatch):
        """Should verify signed dossier."""
        monkeypatch.setenv("HOME", str(tmp_path))
        runner = CliRunner()

        # Generate key and sign
        runner.invoke(main, ["generate-keys"])
        src = FIXTURES_DIR / "valid" / "minimal.ds.md"
        dst = tmp_path / "test.ds.md"
        dst.write_text(src.read_text())
        runner.invoke(main, ["sign", str(dst), "--signed-by", "test@example.com"])

        result = runner.invoke(main, ["verify", str(dst)])

        assert result.exit_code == 0
        assert "Signature: valid" in result.output

    def test_json_output(self):
        """Should output JSON with --json."""
        runner = CliRunner()
        result = runner.invoke(main, ["verify", str(FIXTURES_DIR / "valid" / "minimal.ds.md"), "--json"])

        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["valid"] is True
        assert data["schema"]["valid"] is True
        assert data["checksum"]["status"] == "valid"


class TestInfo:
    """Tests for info command."""

    def test_parse_error(self, tmp_path):
        """Should show error for unparseable file."""
        runner = CliRunner()

        dst = tmp_path / "bad.ds.md"
        dst.write_text("no frontmatter")

        result = runner.invoke(main, ["info", str(dst)])

        assert result.exit_code == 1
        assert "Error" in result.output

    def test_parse_error_json(self, tmp_path):
        """Should show error in JSON format."""
        runner = CliRunner()

        dst = tmp_path / "bad.ds.md"
        dst.write_text("no frontmatter")

        result = runner.invoke(main, ["info", str(dst), "--json"])

        assert result.exit_code == 1
        data = json.loads(result.output)
        assert "error" in data

    def test_displays_metadata(self):
        """Should display frontmatter fields."""
        runner = CliRunner()
        result = runner.invoke(main, ["info", str(FIXTURES_DIR / "valid" / "minimal.ds.md")])

        assert result.exit_code == 0
        assert "Title:" in result.output
        assert "Version:" in result.output
        assert "Status:" in result.output

    def test_json_output(self):
        """Should output JSON with --json."""
        runner = CliRunner()
        result = runner.invoke(main, ["info", str(FIXTURES_DIR / "valid" / "minimal.ds.md"), "--json"])

        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "title" in data
        assert "version" in data


class TestKeys:
    """Tests for keys.py helper functions."""

    def test_get_dossier_dir(self, tmp_path, monkeypatch):
        """Should return ~/.dossier path."""
        monkeypatch.setenv("HOME", str(tmp_path))
        assert get_dossier_dir() == tmp_path / ".dossier"

    def test_get_private_key_path(self, tmp_path, monkeypatch):
        """Should return path to private key."""
        monkeypatch.setenv("HOME", str(tmp_path))
        assert get_private_key_path("test") == tmp_path / ".dossier" / "test.pem"

    def test_get_public_key_path(self, tmp_path, monkeypatch):
        """Should return path to public key."""
        monkeypatch.setenv("HOME", str(tmp_path))
        assert get_public_key_path("test") == tmp_path / ".dossier" / "test.pub"


# --- Registry CLI tests ---


class TestList:
    """Tests for list command."""

    @respx.mock
    def test_list_empty(self, monkeypatch):
        """Should show message when no dossiers found."""
        monkeypatch.setenv("DOSSIER_REGISTRY_URL", "https://registry.test")

        respx.get("https://registry.test/api/v1/dossiers").mock(
            return_value=Response(
                200,
                json={"dossiers": [], "pagination": {"page": 1, "per_page": 20, "total": 0}},
            )
        )

        runner = CliRunner()
        result = runner.invoke(main, ["list"])

        assert result.exit_code == 0
        assert "No dossiers found" in result.output

    @respx.mock
    def test_list_registry_error(self, monkeypatch):
        """Should show error on registry failure."""
        monkeypatch.setenv("DOSSIER_REGISTRY_URL", "https://registry.test")

        respx.get("https://registry.test/api/v1/dossiers").mock(
            return_value=Response(500, json={"error": {"code": "INTERNAL_ERROR", "message": "Server error"}})
        )

        runner = CliRunner()
        result = runner.invoke(main, ["list"])

        assert result.exit_code == 1
        assert "Error" in result.output

    @respx.mock
    def test_list_dossiers(self, monkeypatch):
        """Should list dossiers from registry."""
        monkeypatch.setenv("DOSSIER_REGISTRY_URL", "https://registry.test")

        respx.get("https://registry.test/api/v1/dossiers").mock(
            return_value=Response(
                200,
                json={
                    "dossiers": [
                        {"name": "myorg/deploy", "version": "1.0.0", "title": "Deploy"},
                        {"name": "myorg/backup", "version": "2.0.0", "title": "Backup"},
                    ],
                    "pagination": {"page": 1, "per_page": 20, "total": 2},
                },
            )
        )

        runner = CliRunner()
        result = runner.invoke(main, ["list"])

        assert result.exit_code == 0
        assert "myorg/deploy" in result.output
        assert "myorg/backup" in result.output

    @respx.mock
    def test_list_json_output(self, monkeypatch):
        """Should output JSON with --json."""
        monkeypatch.setenv("DOSSIER_REGISTRY_URL", "https://registry.test")

        respx.get("https://registry.test/api/v1/dossiers").mock(
            return_value=Response(
                200,
                json={"dossiers": [], "pagination": {"page": 1, "per_page": 20, "total": 0}},
            )
        )

        runner = CliRunner()
        result = runner.invoke(main, ["list", "--json"])

        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "dossiers" in data


class TestGet:
    """Tests for get command."""

    @respx.mock
    def test_get_dossier(self, monkeypatch):
        """Should display dossier metadata."""
        monkeypatch.setenv("DOSSIER_REGISTRY_URL", "https://registry.test")

        respx.get("https://registry.test/api/v1/dossiers/myorg/deploy").mock(
            return_value=Response(
                200,
                json={
                    "name": "myorg/deploy",
                    "title": "Deploy to Production",
                    "version": "1.2.0",
                    "status": "stable",
                },
            )
        )

        runner = CliRunner()
        result = runner.invoke(main, ["get", "myorg/deploy"])

        assert result.exit_code == 0
        assert "myorg/deploy" in result.output
        assert "Deploy to Production" in result.output
        assert "1.2.0" in result.output

    @respx.mock
    def test_get_with_version(self, monkeypatch):
        """Should request specific version."""
        monkeypatch.setenv("DOSSIER_REGISTRY_URL", "https://registry.test")

        route = respx.get("https://registry.test/api/v1/dossiers/myorg/deploy").mock(
            return_value=Response(200, json={"name": "myorg/deploy", "version": "1.0.0"})
        )

        runner = CliRunner()
        result = runner.invoke(main, ["get", "myorg/deploy@1.0.0"])

        assert result.exit_code == 0
        assert route.calls[0].request.url.params["version"] == "1.0.0"

    @respx.mock
    def test_get_json_output(self, monkeypatch):
        """Should output JSON with --json."""
        monkeypatch.setenv("DOSSIER_REGISTRY_URL", "https://registry.test")

        respx.get("https://registry.test/api/v1/dossiers/myorg/deploy").mock(
            return_value=Response(200, json={"name": "myorg/deploy", "version": "1.0.0"})
        )

        runner = CliRunner()
        result = runner.invoke(main, ["get", "myorg/deploy", "--json"])

        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["name"] == "myorg/deploy"

    @respx.mock
    def test_get_not_found(self, monkeypatch):
        """Should error on 404."""
        monkeypatch.setenv("DOSSIER_REGISTRY_URL", "https://registry.test")

        respx.get("https://registry.test/api/v1/dossiers/myorg/missing").mock(
            return_value=Response(404, json={"error": {"code": "DOSSIER_NOT_FOUND", "message": "Dossier not found"}})
        )

        runner = CliRunner()
        result = runner.invoke(main, ["get", "myorg/missing"])

        assert result.exit_code == 1
        assert "not found" in result.output.lower()


class TestPull:
    """Tests for pull command."""

    @respx.mock
    def test_pull_dossier(self, tmp_path, monkeypatch):
        """Should download dossier to file."""
        monkeypatch.setenv("DOSSIER_REGISTRY_URL", "https://registry.test")
        monkeypatch.chdir(tmp_path)

        content = """---
title: Deploy
version: "1.0.0"
---

# Deploy
"""
        respx.get("https://registry.test/api/v1/dossiers/myorg/deploy/content").mock(
            return_value=Response(200, text=content, headers={"X-Dossier-Digest": "sha256:abc123"})
        )

        runner = CliRunner()
        result = runner.invoke(main, ["pull", "myorg/deploy"])

        assert result.exit_code == 0
        assert "Downloaded" in result.output

        # Check file was created
        output_file = tmp_path / "myorg-deploy.ds.md"
        assert output_file.exists()
        assert output_file.read_text() == content

    @respx.mock
    def test_pull_with_output(self, tmp_path, monkeypatch):
        """Should save to specified output file."""
        monkeypatch.setenv("DOSSIER_REGISTRY_URL", "https://registry.test")

        respx.get("https://registry.test/api/v1/dossiers/myorg/deploy/content").mock(
            return_value=Response(200, text="content", headers={})
        )

        output_file = tmp_path / "custom.ds.md"

        runner = CliRunner()
        result = runner.invoke(main, ["pull", "myorg/deploy", "-o", str(output_file)])

        assert result.exit_code == 0
        assert output_file.exists()
        assert output_file.read_text() == "content"

    @respx.mock
    def test_pull_with_version(self, tmp_path, monkeypatch):
        """Should request specific version."""
        monkeypatch.setenv("DOSSIER_REGISTRY_URL", "https://registry.test")
        monkeypatch.chdir(tmp_path)

        route = respx.get("https://registry.test/api/v1/dossiers/myorg/deploy/content").mock(
            return_value=Response(200, text="content", headers={})
        )

        runner = CliRunner()
        result = runner.invoke(main, ["pull", "myorg/deploy@1.0.0"])

        assert result.exit_code == 0
        assert route.calls[0].request.url.params["version"] == "1.0.0"

    @respx.mock
    def test_pull_not_found(self, monkeypatch):
        """Should error on 404."""
        monkeypatch.setenv("DOSSIER_REGISTRY_URL", "https://registry.test")

        respx.get("https://registry.test/api/v1/dossiers/myorg/missing/content").mock(
            return_value=Response(404, json={"error": {"code": "DOSSIER_NOT_FOUND", "message": "Dossier not found"}})
        )

        runner = CliRunner()
        result = runner.invoke(main, ["pull", "myorg/missing"])

        assert result.exit_code == 1


class TestLogout:
    """Tests for logout command."""

    def test_logout_removes_credentials(self, tmp_path, monkeypatch):
        """Should remove credentials file."""
        monkeypatch.setattr("dossier_tools.signing.keys.Path.home", lambda: tmp_path)

        # Create credentials
        dossier_dir = tmp_path / ".dossier"
        dossier_dir.mkdir()
        (dossier_dir / "credentials").write_text('{"token": "my-token", "username": "alice", "orgs": []}')

        runner = CliRunner()
        result = runner.invoke(main, ["logout"])

        assert result.exit_code == 0
        assert "Logged out" in result.output
        assert not (dossier_dir / "credentials").exists()

    def test_logout_not_logged_in(self, tmp_path, monkeypatch):
        """Should show message when not logged in."""
        monkeypatch.setattr("dossier_tools.signing.keys.Path.home", lambda: tmp_path)

        runner = CliRunner()
        result = runner.invoke(main, ["logout"])

        assert result.exit_code == 0
        assert "Not logged in" in result.output


class TestWhoami:
    """Tests for whoami command."""

    def test_whoami_not_logged_in(self, tmp_path, monkeypatch):
        """Should error when not logged in."""
        monkeypatch.setattr("dossier_tools.signing.keys.Path.home", lambda: tmp_path)

        runner = CliRunner()
        result = runner.invoke(main, ["whoami"])

        assert result.exit_code == 1
        assert "Not logged in" in result.output

    def test_whoami_shows_user(self, tmp_path, monkeypatch):
        """Should display user info from local credentials."""
        monkeypatch.setattr("dossier_tools.signing.keys.Path.home", lambda: tmp_path)

        # Create credentials
        dossier_dir = tmp_path / ".dossier"
        dossier_dir.mkdir()
        (dossier_dir / "credentials").write_text('{"token": "my-token", "username": "alice", "orgs": ["org1", "org2"]}')

        runner = CliRunner()
        result = runner.invoke(main, ["whoami"])

        assert result.exit_code == 0
        assert "alice" in result.output
        assert "org1" in result.output

    def test_whoami_expired_credentials(self, tmp_path, monkeypatch):
        """Should show expired message for expired credentials."""
        monkeypatch.setattr("dossier_tools.signing.keys.Path.home", lambda: tmp_path)

        # Create expired credentials
        dossier_dir = tmp_path / ".dossier"
        dossier_dir.mkdir()
        (dossier_dir / "credentials").write_text(
            '{"token": "my-token", "username": "alice", "orgs": [], "expires_at": "2020-01-01T00:00:00+00:00"}'
        )

        runner = CliRunner()
        result = runner.invoke(main, ["whoami"])

        assert result.exit_code == 1
        assert "expired" in result.output.lower()


class TestPublish:
    """Tests for publish command."""

    def test_publish_not_logged_in(self, tmp_path, monkeypatch):
        """Should error when not logged in."""
        monkeypatch.setattr("dossier_tools.signing.keys.Path.home", lambda: tmp_path)

        runner = CliRunner()
        result = runner.invoke(
            main, ["publish", str(FIXTURES_DIR / "valid" / "minimal.ds.md"), "--namespace", "myorg/tools"]
        )

        assert result.exit_code == 1
        assert "Not logged in" in result.output

    @respx.mock
    def test_publish_dossier(self, tmp_path, monkeypatch):
        """Should publish valid dossier."""
        monkeypatch.setattr("dossier_tools.signing.keys.Path.home", lambda: tmp_path)
        monkeypatch.setenv("DOSSIER_REGISTRY_URL", "https://registry.test")

        # Create credentials
        dossier_dir = tmp_path / ".dossier"
        dossier_dir.mkdir()
        (dossier_dir / "credentials").write_text('{"token": "my-token", "username": "alice", "orgs": []}')

        # Create dossier with name
        dossier_file = tmp_path / "deploy.ds.md"
        dossier_file.write_text("""---
schema_version: "1.0.0"
title: Deploy
version: "1.0.0"
status: draft
objective: Deploy the app
name: deploy
authors:
  - name: Alice
checksum:
  algorithm: sha256
  hash: 6bb135eeeff94e0e72479e59796ec87ede1be5f425946c882691498957c21568
---

# Deploy
""")

        respx.post("https://registry.test/api/v1/dossiers").mock(
            return_value=Response(
                201,
                json={"name": "myorg/deploy", "version": "1.0.0", "url": "https://registry.test/myorg/deploy"},
            )
        )

        runner = CliRunner()
        result = runner.invoke(main, ["publish", str(dossier_file), "--namespace", "myorg/tools"])

        assert result.exit_code == 0
        assert "Published" in result.output
        assert "myorg/deploy" in result.output

    @respx.mock
    def test_publish_with_changelog(self, tmp_path, monkeypatch):
        """Should include changelog in request."""
        monkeypatch.setattr("dossier_tools.signing.keys.Path.home", lambda: tmp_path)
        monkeypatch.setenv("DOSSIER_REGISTRY_URL", "https://registry.test")

        # Create credentials
        dossier_dir = tmp_path / ".dossier"
        dossier_dir.mkdir()
        (dossier_dir / "credentials").write_text('{"token": "my-token", "username": "alice", "orgs": []}')

        # Create dossier with name
        dossier_file = tmp_path / "deploy.ds.md"
        dossier_file.write_text("""---
schema_version: "1.0.0"
title: Deploy
version: "1.0.0"
status: draft
objective: Deploy the app
name: deploy
authors:
  - name: Alice
checksum:
  algorithm: sha256
  hash: 6bb135eeeff94e0e72479e59796ec87ede1be5f425946c882691498957c21568
---

# Deploy
""")

        route = respx.post("https://registry.test/api/v1/dossiers").mock(
            return_value=Response(201, json={"name": "myorg/deploy", "version": "1.0.0"})
        )

        runner = CliRunner()
        result = runner.invoke(
            main, ["publish", str(dossier_file), "--namespace", "myorg/tools", "--changelog", "Fixed bug"]
        )

        assert result.exit_code == 0
        body = json.loads(route.calls[0].request.content)
        assert body["changelog"] == "Fixed bug"

    @respx.mock
    def test_publish_version_conflict(self, tmp_path, monkeypatch):
        """Should show conflict error on 409."""
        monkeypatch.setattr("dossier_tools.signing.keys.Path.home", lambda: tmp_path)
        monkeypatch.setenv("DOSSIER_REGISTRY_URL", "https://registry.test")

        # Create credentials
        dossier_dir = tmp_path / ".dossier"
        dossier_dir.mkdir()
        (dossier_dir / "credentials").write_text('{"token": "my-token", "username": "alice", "orgs": []}')

        # Create dossier with name
        dossier_file = tmp_path / "deploy.ds.md"
        dossier_file.write_text("""---
schema_version: "1.0.0"
title: Deploy
version: "1.0.0"
status: draft
objective: Deploy the app
name: deploy
authors:
  - name: Alice
checksum:
  algorithm: sha256
  hash: 6bb135eeeff94e0e72479e59796ec87ede1be5f425946c882691498957c21568
---

# Deploy
""")

        respx.post("https://registry.test/api/v1/dossiers").mock(
            return_value=Response(
                409, json={"error": {"code": "VERSION_EXISTS", "message": "Version 1.0.0 already exists"}}
            )
        )

        runner = CliRunner()
        result = runner.invoke(main, ["publish", str(dossier_file), "--namespace", "myorg/tools"])

        assert result.exit_code == 1
        assert "conflict" in result.output.lower()

    def test_publish_invalid_schema(self, tmp_path, monkeypatch):
        """Should error on schema validation failure."""
        monkeypatch.setattr("dossier_tools.signing.keys.Path.home", lambda: tmp_path)

        # Create credentials
        dossier_dir = tmp_path / ".dossier"
        dossier_dir.mkdir()
        (dossier_dir / "credentials").write_text('{"token": "my-token", "username": "alice", "orgs": []}')

        # Create invalid dossier (missing required fields)
        dossier_file = tmp_path / "invalid.ds.md"
        dossier_file.write_text("""---
schema_version: "1.0.0"
name: invalid
---

# Invalid
""")

        runner = CliRunner()
        result = runner.invoke(main, ["publish", str(dossier_file), "--namespace", "myorg/tools"])

        assert result.exit_code == 1
        assert "Validation errors" in result.output

    def test_publish_invalid_checksum(self, tmp_path, monkeypatch):
        """Should error on checksum validation failure."""
        monkeypatch.setattr("dossier_tools.signing.keys.Path.home", lambda: tmp_path)

        # Create credentials
        dossier_dir = tmp_path / ".dossier"
        dossier_dir.mkdir()
        (dossier_dir / "credentials").write_text('{"token": "my-token", "username": "alice", "orgs": []}')

        # Create dossier with wrong checksum (valid format but wrong value)
        dossier_file = tmp_path / "bad-checksum.ds.md"
        dossier_file.write_text("""---
schema_version: "1.0.0"
title: Bad Checksum
version: "1.0.0"
status: draft
objective: Test invalid checksum
name: bad
authors:
  - name: Alice
checksum:
  algorithm: sha256
  hash: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
---

# Bad Checksum
""")

        runner = CliRunner()
        result = runner.invoke(main, ["publish", str(dossier_file), "--namespace", "myorg/tools"])

        assert result.exit_code == 1
        assert "Checksum error" in result.output

    @respx.mock
    def test_publish_unauthorized(self, tmp_path, monkeypatch):
        """Should show session expired on 401."""
        monkeypatch.setattr("dossier_tools.signing.keys.Path.home", lambda: tmp_path)
        monkeypatch.setenv("DOSSIER_REGISTRY_URL", "https://registry.test")

        # Create credentials
        dossier_dir = tmp_path / ".dossier"
        dossier_dir.mkdir()
        (dossier_dir / "credentials").write_text('{"token": "my-token", "username": "alice", "orgs": []}')

        # Create valid dossier
        dossier_file = tmp_path / "deploy.ds.md"
        dossier_file.write_text("""---
schema_version: "1.0.0"
title: Deploy
version: "1.0.0"
status: draft
objective: Deploy the app
name: deploy
authors:
  - name: Alice
checksum:
  algorithm: sha256
  hash: 6bb135eeeff94e0e72479e59796ec87ede1be5f425946c882691498957c21568
---

# Deploy
""")

        respx.post("https://registry.test/api/v1/dossiers").mock(
            return_value=Response(401, json={"error": {"code": "UNAUTHORIZED", "message": "Invalid token"}})
        )

        runner = CliRunner()
        result = runner.invoke(main, ["publish", str(dossier_file), "--namespace", "myorg/tools"])

        assert result.exit_code == 1
        assert "expired" in result.output.lower()

    @respx.mock
    def test_publish_forbidden(self, tmp_path, monkeypatch):
        """Should show permission denied on 403."""
        monkeypatch.setattr("dossier_tools.signing.keys.Path.home", lambda: tmp_path)
        monkeypatch.setenv("DOSSIER_REGISTRY_URL", "https://registry.test")

        # Create credentials
        dossier_dir = tmp_path / ".dossier"
        dossier_dir.mkdir()
        (dossier_dir / "credentials").write_text('{"token": "my-token", "username": "alice", "orgs": []}')

        # Create valid dossier
        dossier_file = tmp_path / "deploy.ds.md"
        dossier_file.write_text("""---
schema_version: "1.0.0"
title: Deploy
version: "1.0.0"
status: draft
objective: Deploy the app
name: forbidden-deploy
authors:
  - name: Alice
checksum:
  algorithm: sha256
  hash: 6bb135eeeff94e0e72479e59796ec87ede1be5f425946c882691498957c21568
---

# Deploy
""")

        respx.post("https://registry.test/api/v1/dossiers").mock(
            return_value=Response(403, json={"error": {"code": "FORBIDDEN", "message": "Not authorized"}})
        )

        runner = CliRunner()
        result = runner.invoke(main, ["publish", str(dossier_file), "--namespace", "myorg/tools"])

        assert result.exit_code == 1
        assert "Permission denied" in result.output
