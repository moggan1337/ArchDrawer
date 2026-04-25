"""Command-line interface for ArchDrawer."""

import sys
from typing import Optional

import click

from src.drawer import (
    ArchitectureDescription,
    ArchitectureDrawer,
    DiagramType,
    OutputFormat,
)


@click.group()
@click.version_option(version="0.1.0", prog_name="archdrawer")
def cli() -> None:
    """ArchDrawer - Architecture Diagram Generator.

    Generate architecture diagrams from simple descriptions.
    Supports Mermaid, PlantUML, and DOT/Graphviz formats.
    """
    pass


@cli.command()
@click.option(
    "--format",
    "-f",
    "output_format",
    type=click.Choice(["mermaid", "plantuml", "dot"], case_sensitive=False),
    default="mermaid",
    help="Output format for the diagram",
)
@click.option(
    "--type",
    "-t",
    "diagram_type",
    type=click.Choice(["component", "deployment", "sequence", "flow"], case_sensitive=False),
    default="component",
    help="Type of diagram to generate",
)
@click.option(
    "--output",
    "-o",
    "output_file",
    type=click.Path(),
    help="Output file path (prints to stdout if not specified)",
)
@click.option(
    "--interactive",
    "-i",
    is_flag=True,
    help="Interactive mode for entering architecture description",
)
def generate(
    output_format: str,
    diagram_type: str,
    output_file: Optional[str],
    interactive: bool,
) -> None:
    """Generate an architecture diagram.

    Examples:
        archdrawer generate --format mermaid --type component
        archdrawer generate -f plantuml -t deployment -o diagram.puml
        archdrawer generate -i
    """
    drawer = ArchitectureDrawer()

    if interactive:
        architecture = _interactive_input()
    else:
        architecture = _simple_input()

    diagram = drawer.generate_diagram(
        architecture,
        output_format=OutputFormat(output_format),
        diagram_type=DiagramType(diagram_type),
    )

    if output_file:
        drawer.render_to_file(
            architecture,
            output_file,
            output_format=OutputFormat(output_format),
            diagram_type=DiagramType(diagram_type),
        )
        click.echo(f"Diagram written to {output_file}")
    else:
        click.echo(diagram)


@cli.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option(
    "--format",
    "-f",
    "output_format",
    type=click.Choice(["mermaid", "plantuml", "dot"], case_sensitive=False),
    default="mermaid",
    help="Output format for the diagram",
)
@click.option(
    "--type",
    "-t",
    "diagram_type",
    type=click.Choice(["component", "deployment", "sequence", "flow"], case_sensitive=False),
    default="component",
    help="Type of diagram to generate",
)
@click.option(
    "--output",
    "-o",
    "output_file",
    type=click.Path(),
    help="Output file path (prints to stdout if not specified)",
)
def render(
    input_file: str,
    output_format: str,
    diagram_type: str,
    output_file: Optional[str],
) -> None:
    """Render a diagram from a YAML/JSON architecture description file.

    Examples:
        archdrawer render architecture.yaml
        archdrawer render arch.json -f plantuml -o diagram.puml
    """
    import json

    import yaml

    drawer = ArchitectureDrawer()

    # Load the architecture description
    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Try to parse as YAML or JSON
    try:
        architecture_data = yaml.safe_load(content)
    except yaml.YAMLError:
        try:
            architecture_data = json.loads(content)
        except json.JSONDecodeError as e:
            click.echo(f"Error: Could not parse input file as YAML or JSON: {e}", err=True)
            sys.exit(1)

    diagram = drawer.generate_diagram(
        architecture_data,
        output_format=OutputFormat(output_format),
        diagram_type=DiagramType(diagram_type),
    )

    if output_file:
        drawer.render_to_file(
            architecture_data,
            output_file,
            output_format=OutputFormat(output_format),
            diagram_type=DiagramType(diagram_type),
        )
        click.echo(f"Diagram written to {output_file}")
    else:
        click.echo(diagram)


def _simple_input() -> ArchitectureDescription:
    """Get architecture from simple command-line prompts."""
    click.echo("\n=== Simple Architecture Input ===\n")

    title = click.prompt("Diagram title", default="Architecture Diagram")

    arch = ArchitectureDescription(title=title)

    click.echo("\n--- Add Nodes ---")
    click.echo("Enter node details (press Enter with empty id to finish)\n")

    while True:
        node_id = click.prompt("Node ID", default="")
        if not node_id:
            break
        label = click.prompt("  Label", default=node_id)
        tech = click.prompt("  Technology (optional)", default="")
        desc = click.prompt("  Description (optional)", default="")
        parent = click.prompt("  Parent group (optional)", default="")

        arch.add_node(
            node_id=node_id,
            label=label,
            technology=tech,
            description=desc,
            parent=parent,
        )
        click.echo(f"  Added node: {node_id}\n")

    click.echo("\n--- Add Connections ---")
    click.echo("Enter connection details (press Enter with empty source to finish)\n")

    while True:
        source = click.prompt("Source node ID", default="")
        if not source:
            break
        target = click.prompt("  Target node ID", default="")
        label = click.prompt("  Label (optional)", default="")
        is_bidirectional = click.confirm("  Bidirectional?", default=False)

        arch.add_connection(
            source=source,
            target=target,
            label=label,
            bidirectional=is_bidirectional,
        )
        click.echo(f"  Added connection: {source} -> {target}\n")

    return arch


def _interactive_input() -> ArchitectureDescription:
    """Get architecture from interactive mode with guided prompts."""
    click.echo("\n" + "=" * 50)
    click.echo("  ArchDrawer - Interactive Mode")
    click.echo("=" * 50)

    # Title and description
    click.echo("\n[Step 1/4] Diagram Details")
    title = click.prompt("  Title", default="My Architecture")
    description = click.prompt("  Description (optional)", default="")

    arch = ArchitectureDescription(title=title, description=description)

    # Nodes
    click.echo("\n[Step 2/4] Define Components/Services")
    click.echo("  Add the nodes in your architecture.\n")

    nodes: list[tuple[str, str, str, str]] = []

    while True:
        click.echo("  Node #{}".format(len(nodes) + 1))
        node_id = click.prompt("    ID (e.g., api-server)", default="")
        if not node_id:
            if nodes:
                click.echo("  Finished adding nodes.\n")
            break

        label = click.prompt("    Label", default=node_id.replace("-", " ").replace("_", " ").title())
        tech = click.prompt("    Technology (e.g., Python, React)", default="")
        parent = click.prompt("    Parent group (e.g., AWS, On-Premise)", default="")

        nodes.append((node_id, label, tech, parent))
        arch.add_node(node_id, label, tech, parent=parent)
        click.echo("")

    # Connections
    click.echo("\n[Step 3/4] Define Connections")
    click.echo("  Define how components communicate.\n")

    connections: list[tuple[str, str, str, bool]] = []

    while True:
        click.echo("  Connection #{}".format(len(connections) + 1))

        # Show available nodes
        if nodes:
            click.echo("    Available nodes: {}".format(", ".join(n[0] for n in nodes)))

        source = click.prompt("    Source node ID", default="")
        if not source:
            if connections:
                click.echo("  Finished adding connections.\n")
            break

        target = click.prompt("    Target node ID", default="")
        label = click.prompt("    Connection label (e.g., REST API, gRPC)", default="")
        bidirectional = click.confirm("    Bidirectional?", default=False)

        connections.append((source, target, label, bidirectional))
        arch.add_connection(source, target, label, bidirectional=bidirectional)
        click.echo("")

    # Metadata
    click.echo("\n[Step 4/4] Additional Metadata (optional)")
    click.echo("  Add key-value pairs for metadata (empty key to finish).\n")

    while True:
        key = click.prompt("  Key", default="")
        if not key:
            break
        value = click.prompt(f"  Value for '{key}'", default="")
        arch.metadata[key] = value

    # Summary
    click.echo("\n" + "=" * 50)
    click.echo("  Summary")
    click.echo("=" * 50)
    click.echo(f"  Title: {arch.title}")
    if arch.description:
        click.echo(f"  Description: {arch.description}")
    click.echo(f"  Nodes: {len(arch.nodes)}")
    for node in arch.nodes:
        tech_str = f" ({node.technology})" if node.technology else ""
        click.echo(f"    - {node.id}: {node.label}{tech_str}")
    click.echo(f"  Connections: {len(arch.connections)}")
    for conn in arch.connections:
        arrow = "<->" if conn.bidirectional else "->"
        label_str = f" ({conn.label})" if conn.label else ""
        click.echo(f"    - {conn.source} {arrow} {conn.target}{label_str}")
    click.echo("=" * 50 + "\n")

    return arch


@cli.command()
def list_formats() -> None:
    """List all supported output formats and diagram types."""
    click.echo("Supported Output Formats:")
    for fmt in OutputFormat:
        click.echo(f"  - {fmt.value}")

    click.echo("\nSupported Diagram Types:")
    for dtype in DiagramType:
        click.echo(f"  - {dtype.value}")


if __name__ == "__main__":
    cli()
