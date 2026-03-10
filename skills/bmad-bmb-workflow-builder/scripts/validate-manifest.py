#!/usr/bin/env python3
"""Validate BMad manifest.yaml against the schema.

This script validates a manifest.yaml file against the BMad manifest schema.
It follows PEP 723 for inline script metadata and supports structured JSON output.
"""

# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "jsonschema>=4.0.0",
#     "pyyaml>=6.0",
# ]
# ///

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("Error: pyyaml is required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

try:
    from jsonschema import Draft7Validator
except ImportError:
    print("Error: jsonschema is required. Install with: pip install jsonschema", file=sys.stderr)
    sys.exit(2)


def load_schema(schema_path: Path) -> dict[str, Any]:
    """Load the JSON schema file."""
    if not schema_path.exists():
        print(f"Error: Schema file not found: {schema_path}", file=sys.stderr)
        sys.exit(2)
    with schema_path.open() as f:
        return json.load(f)


def load_manifest(manifest_path: Path) -> dict[str, Any]:
    """Load the manifest.yaml file."""
    if not manifest_path.exists():
        print(f"Error: Manifest file not found: {manifest_path}", file=sys.stderr)
        sys.exit(2)
    with manifest_path.open() as f:
        content = f.read()
    # Strip comment lines that start with # before the YAML content
    # (YAML supports comments natively, but we parse anyway)
    try:
        data = yaml.safe_load(content)
    except yaml.YAMLError as e:
        print(f"Error: Invalid YAML in {manifest_path}: {e}", file=sys.stderr)
        sys.exit(2)
    if data is None:
        return {}
    return data


def validate_manifest(manifest: dict[str, Any], schema: dict[str, Any]) -> list[dict[str, Any]]:
    """Validate manifest against schema and return list of errors."""
    validator = Draft7Validator(schema)
    errors = []

    for error in validator.iter_errors(manifest):
        errors.append({
            "path": ".".join(str(p) for p in error.path) if error.path else "root",
            "message": error.message,
            "type": error.validator,
        })

    return errors


def validate_workflow_fields(manifest: dict[str, Any]) -> list[str]:
    """Validate workflow-specific fields."""
    warnings = []
    bmad_type = manifest.get("bmad-type", "")

    if bmad_type in ("bmad-workflow", "bmad-skill"):
        # Check for required workflow fields
        if "bmad-creates" not in manifest:
            warnings.append("Missing 'bmad-creates' field — what does this workflow produce?")
        if "bmad-output-location-variable" not in manifest:
            warnings.append("Missing 'bmad-output-location-variable' field — use 'none' if not applicable")

    if bmad_type == "bmad-workflow":
        # Module workflows should have module info
        if "bmad-module-code" not in manifest and "replaces" not in manifest:
            warnings.append("Workflow missing 'bmad-module-code' — is this standalone or module-based?")

    # Check dependency arrays are lists
    for field in ("bmad-requires", "bmad-prefer-after", "bmad-prefer-before"):
        val = manifest.get(field)
        if val is not None and not isinstance(val, list):
            warnings.append(f"'{field}' should be a list, got {type(val).__name__}")

    return warnings


def print_results(errors: list[dict[str, Any]], warnings: list[str], json_output: bool) -> None:
    """Print validation results."""
    result = {
        "valid": len(errors) == 0,
        "error_count": len(errors),
        "warning_count": len(warnings),
        "errors": errors,
        "warnings": warnings,
    }

    if json_output:
        print(json.dumps(result, indent=2))
    else:
        if result["valid"]:
            print("✓ Manifest is valid")
        else:
            print(f"✗ Manifest validation failed with {result['error_count']} error(s)", file=sys.stderr)

        if warnings:
            print(f"\nWarnings ({len(warnings)}):", file=sys.stderr)
            for warning in warnings:
                print(f"  - {warning}", file=sys.stderr)

        if errors:
            print("\nErrors:", file=sys.stderr)
            for error in errors:
                print(f"  [{error['path']}] {error['message']}", file=sys.stderr)

    sys.exit(0 if result["valid"] else 1)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate BMad manifest.yaml against schema",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "manifest",
        type=Path,
        help="Path to manifest.yaml file to validate",
    )
    parser.add_argument(
        "--schema",
        type=Path,
        default=Path(__file__).parent / "manifest-schema.json",
        help="Path to manifest schema JSON (default: ./manifest-schema.json)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON",
    )
    parser.add_argument(
        "--skill-path",
        type=Path,
        help="Path to skill directory for auto-discovery of manifest.yaml",
    )
    args = parser.parse_args()

    # Auto-discover manifest if --skill-path provided
    manifest_path = args.manifest
    if args.skill_path:
        candidate = args.skill_path / "resources" / "manifest.yaml"
        if candidate.exists():
            manifest_path = candidate

    # Load schema and manifest
    schema = load_schema(args.schema)
    manifest = load_manifest(manifest_path)

    # Validate against schema
    errors = validate_manifest(manifest, schema)

    # Additional workflow field validation
    warnings = validate_workflow_fields(manifest)

    # Print results
    print_results(errors, warnings, args.json)
    return 0


if __name__ == "__main__":
    main()
