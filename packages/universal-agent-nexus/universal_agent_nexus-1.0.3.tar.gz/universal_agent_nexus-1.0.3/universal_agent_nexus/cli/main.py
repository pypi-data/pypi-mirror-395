"""
Universal Agent Nexus CLI.

The nexus command provides compilation, translation, and server management
for the Universal Agent Architecture.
"""

import logging
from typing import Optional

import typer

from universal_agent_nexus.cli.compile import app as compile_app

app = typer.Typer(
    name="nexus",
    help="Universal Agent Nexus - Foreign Interface Compiler",
    add_completion=False,
)

# Mount subcommands
app.add_typer(compile_app, name="compile")


@app.command()
def translate(
    source: str = typer.Argument(..., help="Source file to translate"),
    target: str = typer.Option("uaa", "--to", "-t", help="Target format: langgraph, aws, uaa"),
    source_type: str = typer.Option(
        "auto", "--from", "-f", help="Source type: auto, langgraph, aws, yaml"
    ),
    output: Optional[str] = typer.Option(None, "--out", "-o", help="Output file path"),
    optimize: bool = typer.Option(True, "--optimize/--no-optimize", help="Apply optimizations"),
    validate: bool = typer.Option(True, "--validate/--no-validate", help="Apply validations"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
):
    """
    Translate between any supported formats (BIDIRECTIONAL!).

    Uses IR-based compilation for lossless, bidirectional translation.

    Supports:
    - LangGraph (Python) ← → AWS Step Functions (ASL)
    - LangGraph (Python) ← → UAA YAML
    - AWS Step Functions ← → UAA YAML
    - Any → Any!

    Examples:
        # LangGraph → AWS
        nexus translate agent.py --to aws --out state_machine.json

        # AWS → LangGraph (REVERSE!)
        nexus translate state_machine.json --to langgraph --out agent.py

        # Any → UAA YAML (for Fabric enrichment)
        nexus translate agent.py --to uaa --out manifest.yaml

        # Then enrich with Fabric
        fabric enrich manifest.yaml --role researcher.yaml --out production.yaml
    """
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    from universal_agent_nexus.compiler import compile as nexus_compile

    typer.echo(f"[Nexus] Compiling {source} → {target}")

    try:
        result = nexus_compile(
            source,
            target=target,
            source_type=source_type,
            output=output,
            optimize_ir=optimize,
            validate_ir=validate,
        )

        if output:
            typer.echo(f"[OK] Wrote output to {output}")
        else:
            typer.echo("\n--- OUTPUT ---")
            typer.echo(result)

        typer.echo(f"\n[OK] Translation complete: {source} → {target}")

        if target == "uaa":
            typer.echo("\nNext steps:")
            typer.echo(f"  1. Review baseline manifest")
            typer.echo(f"  2. Enrich with Fabric:")
            typer.echo(f"     fabric enrich {output or 'manifest.yaml'} \\")
            typer.echo(f"       --role manifests/roles/researcher.yaml \\")
            typer.echo(f"       --domain ontology/domains/finance.yaml \\")
            typer.echo(f"       --out production_ready.yaml")

    except Exception as e:
        typer.echo(f"[ERROR] Translation failed: {e}", err=True)
        if verbose:
            import traceback
            traceback.print_exc()
        raise typer.Exit(1)


@app.command()
def info():
    """
    Show compiler information.

    Lists available source types, target types, and transformation passes.
    """
    from universal_agent_nexus.compiler import get_compiler_info

    info = get_compiler_info()

    typer.echo("Universal Agent Nexus Compiler")
    typer.echo(f"Version: {info['version']}")
    typer.echo("")
    typer.echo("Source Types (parsers):")
    for st in info["source_types"]:
        typer.echo(f"  - {st}")
    typer.echo("")
    typer.echo("Target Types (generators):")
    for tt in info["target_types"]:
        typer.echo(f"  - {tt}")
    typer.echo("")
    typer.echo("Transformation Passes:")
    for t in info["transforms"]:
        typer.echo(f"  - {t}")


@app.command()
def serve(
    manifest: str = typer.Argument(..., help="Path to UAA manifest YAML"),
    host: str = typer.Option("127.0.0.1", help="Server host"),
    port: int = typer.Option(8000, help="Server port"),
    transport: str = typer.Option(
        "stdio", help="Transport: stdio (default), http"
    ),
):
    """
    Start MCP server exposing UAA graphs as tools.

    The MCP server allows AI clients (Claude, Cursor, VS Code) to invoke
    your agent graphs as callable tools.

    Examples:
        # Start with stdio transport (for Claude Desktop)
        nexus serve manifest.yaml

        # Start with HTTP transport
        nexus serve manifest.yaml --transport http --port 8000
    """
    import asyncio

    typer.echo(f"[Nexus] Starting MCP server for {manifest}")
    typer.echo(f"Transport: {transport}")

    try:
        from universal_agent_nexus.adapters.mcp.server import MCPServerAdapter

        adapter = MCPServerAdapter()
        asyncio.run(adapter.start(manifest, transport=transport))
    except ImportError:
        typer.echo(
            "[ERROR] MCP dependencies not installed. "
            "Install with: pip install 'universal-agent-nexus[mcp]'",
            err=True,
        )
        raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"[ERROR] Server failed: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def validate(
    source: str = typer.Argument(..., help="Source file to validate"),
    source_type: str = typer.Option(
        "auto", "--type", "-t", help="Source type: auto, langgraph, aws, yaml"
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
):
    """
    Validate source file without generating output.

    Parses the source, applies validation passes, and reports any issues.

    Examples:
        nexus validate agent.py
        nexus validate state_machine.json --type aws
        nexus validate manifest.yaml --verbose
    """
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    from universal_agent_nexus.compiler import parse
    from universal_agent_nexus.ir.transforms import create_validation_pipeline

    typer.echo(f"[Nexus] Validating {source}")

    try:
        # Parse
        ir = parse(source, source_type=source_type)
        typer.echo(f"[OK] Parsed: {len(ir.graphs)} graph(s)")

        # Validate IR structure
        errors = ir.validate()
        if errors:
            typer.echo("\n[WARN] IR validation issues:")
            for err in errors:
                typer.echo(f"  - {err}")
        else:
            typer.echo("[OK] IR structure valid")

        # Apply validation transforms
        pipeline = create_validation_pipeline()
        pipeline.apply(ir)

        typer.echo(f"\n[OK] Validation complete for {source}")

    except Exception as e:
        typer.echo(f"[ERROR] Validation failed: {e}", err=True)
        if verbose:
            import traceback
            traceback.print_exc()
        raise typer.Exit(1)


@app.callback()
def main():
    """
    Universal Agent Nexus - Foreign Interface Compiler.

    Nexus translates between Universal Agent definitions and ecosystem-specific
    formats (LangGraph, AWS Step Functions, MCP) using an IR-based compiler.

    Architecture:
        Parser → IR → Transform → Generator

    Commands:
        translate  Bidirectional translation between formats
        validate   Validate source without generating output
        compile    Compile UAA manifest to specific target
        serve      Start MCP server for AI client access
        info       Show compiler information
    """
    pass


if __name__ == "__main__":
    app()
