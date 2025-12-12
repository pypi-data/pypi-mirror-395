"""
universal_agent.runtime.cli

Command Line Interface for the Universal Agent.
"""

from __future__ import annotations

import os

import typer
import uvicorn

from universal_agent.manifests.loader import ManifestLoader
from universal_agent.manifests.validator import ManifestValidator

app = typer.Typer()


@app.command()
def validate(manifest_path: str = "manifest.yaml") -> None:
    """Validate a manifest file."""
    try:
        manifest = ManifestLoader.load_from_path(manifest_path)
        validator = ManifestValidator(manifest)
        validator.validate()
        typer.echo(f"✅ Manifest '{manifest_path}' is valid.")
    except Exception as exc:  # pragma: no cover - CLI feedback
        typer.echo(f"❌ Validation failed: {exc}", err=True)
        raise typer.Exit(code=1)


@app.command()
def serve(
    host: str = "0.0.0.0",
    port: int = 8000,
    manifest: str = "manifest.yaml",
    reload: bool = False,
) -> None:
    """Start the Agent API server."""
    validate(manifest)
    os.environ["AGENT_MANIFEST_PATH"] = manifest
    typer.echo(f"🚀 Starting Universal Agent on {host}:{port}")
    uvicorn.run("universal_agent.runtime.api:app", host=host, port=port, reload=reload)


if __name__ == "__main__":
    app()

