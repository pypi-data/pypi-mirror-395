"""
universal_agent_nexus.cli.compile

Command line tool to target different ecosystems.
Usage:
    nexus compile --target aws --manifest agent.yaml --out agent.asl.json
"""

from pathlib import Path
from typing import Annotated, Optional
import json

import typer
import yaml

from universal_agent.manifests.loader import ManifestLoader
from universal_agent_nexus.adapters.aws.step_functions import AWSStepFunctionsCompiler
from universal_agent_nexus.adapters.langgraph.compiler import LangGraphCompiler

app = typer.Typer()


@app.command()
def compile(
    target: Annotated[str, typer.Option(help="Target ecosystem: aws, langgraph, mcp")],
    manifest: Annotated[Path, typer.Option(help="Path to input manifest.yaml")],
    out: Annotated[Optional[Path], typer.Option(help="Output file path")] = None,
    graph: Annotated[str, typer.Option(help="Name of the graph to compile")] = "main",
) -> None:
    """
    Compile a Universal Agent Manifest into a target ecosystem artifact.
    """
    # 1. Load Manifest
    try:
        agent_manifest = ManifestLoader.load_from_path(manifest)
    except Exception as exc:  # pragma: no cover - simple CLI error path
        typer.echo(f"Error loading manifest: {exc}", err=True)
        raise typer.Exit(code=1) from exc

    result = None
    output_format = "json"

    # 2. Select Adapter
    if target == "aws":
        compiler = AWSStepFunctionsCompiler()
        result = compiler.compile(agent_manifest, graph)
    elif target == "langgraph":
        typer.echo(
            "LangGraph compilation generates a Python object, not a file. Running dry-run..."
        )
        compiler = LangGraphCompiler()
        compiler.compile(agent_manifest, graph)
        typer.echo("✅ Graph compiled to LangGraph StateGraph successfully.")
        return
    else:
        typer.echo(f"Unknown target: {target}", err=True)
        raise typer.Exit(code=1)

    # 3. Output
    if result is not None:
        serialized = (
            json.dumps(result, indent=2) if output_format == "json" else str(result)
        )

        if out:
            out.write_text(serialized)
            typer.echo(f"✅ Compiled to {out}")
        else:
            typer.echo(serialized)


if __name__ == "__main__":
    app()

