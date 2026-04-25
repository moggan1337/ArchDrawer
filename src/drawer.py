"""Architecture Diagram Generator.

Supports multiple output formats: Mermaid, PlantUML, and DOT/Graphviz.
Supports multiple diagram types: component, deployment, sequence, and flow.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class DiagramType(Enum):
    """Supported diagram types."""

    COMPONENT = "component"
    DEPLOYMENT = "deployment"
    SEQUENCE = "sequence"
    FLOW = "flow"


class OutputFormat(Enum):
    """Supported output formats."""

    MERMAID = "mermaid"
    PLANTUML = "plantuml"
    DOT = "dot"


@dataclass
class Node:
    """Represents a node/component in the architecture."""

    id: str
    label: str
    description: str = ""
    technology: str = ""
    parent: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "label": self.label,
            "description": self.description,
            "technology": self.technology,
            "parent": self.parent,
        }


@dataclass
class Connection:
    """Represents a connection/relationship between nodes."""

    source: str
    target: str
    label: str = ""
    style: str = "solid"
    bidirectional: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "target": self.target,
            "label": self.label,
            "style": self.style,
            "bidirectional": self.bidirectional,
        }


@dataclass
class ArchitectureDescription:
    """Description of an architecture for diagram generation."""

    title: str = "Architecture Diagram"
    description: str = ""
    nodes: list[Node] = field(default_factory=list)
    connections: list[Connection] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def add_node(
        self,
        id: str,
        label: str,
        description: str = "",
        technology: str = "",
        parent: str = "",
    ) -> "ArchitectureDescription":
        """Add a node to the architecture."""
        self.nodes.append(
            Node(id=id, label=label, description=description, technology=technology, parent=parent)
        )
        return self

    def add_connection(
        self,
        source: str,
        target: str,
        label: str = "",
        style: str = "solid",
        bidirectional: bool = False,
    ) -> "ArchitectureDescription":
        """Add a connection between two nodes."""
        self.connections.append(
            Connection(source=source, target=target, label=label, style=style, bidirectional=bidirectional)
        )
        return self


class MermaidGenerator:
    """Generates diagrams in Mermaid format."""

    def generate(self, arch: ArchitectureDescription, diagram_type: DiagramType) -> str:
        """Generate Mermaid diagram."""
        if diagram_type == DiagramType.COMPONENT:
            return self._generate_component(arch)
        elif diagram_type == DiagramType.DEPLOYMENT:
            return self._generate_deployment(arch)
        elif diagram_type == DiagramType.SEQUENCE:
            return self._generate_sequence(arch)
        elif diagram_type == DiagramType.FLOW:
            return self._generate_flow(arch)
        raise ValueError(f"Unsupported diagram type: {diagram_type}")

    def _generate_component(self, arch: ArchitectureDescription) -> str:
        lines = ["```mermaid", "graph LR"]
        for node in arch.nodes:
            tech = f" [{node.technology}]" if node.technology else ""
            lines.append(f'    {node.id}["{node.label}{tech}"]')
        for conn in arch.connections:
            arrow = "<-->" if conn.bidirectional else "-->"
            label = f"|{conn.label}|" if conn.label else ""
            lines.append(f"    {conn.source} {arrow} {label} {conn.target}")
        lines.append("```")
        return "\n".join(lines)

    def _generate_deployment(self, arch: ArchitectureDescription) -> str:
        lines = ["```mermaid", "graph TB"]
        # Group nodes by parent
        parents: dict[str, list[Node]] = {}
        for node in arch.nodes:
            if node.parent:
                parents.setdefault(node.parent, []).append(node)
            else:
                lines.append(f'    {node.id}["{node.label}"]')
        for parent, child_nodes in parents.items():
            lines.append(f"    subgraph {parent}")
            for child in child_nodes:
                lines.append(f'        {child.id}["{child.label}"]')
            lines.append("    end")
        for conn in arch.connections:
            arrow = "<-->" if conn.bidirectional else "-->"
            label = f"|{conn.label}|" if conn.label else ""
            lines.append(f"    {conn.source} {arrow} {label} {conn.target}")
        lines.append("```")
        return "\n".join(lines)

    def _generate_sequence(self, arch: ArchitectureDescription) -> str:
        lines = ["```mermaid", "sequenceDiagram"]
        # Add participants
        for node in arch.nodes:
            lines.append(f"    participant {node.id} as {node.label}")
        # Add connections as interactions
        for conn in arch.connections:
            label = conn.label or "interacts"
            lines.append(f"    {conn.source}->>+{conn.target}: {label}")
            if conn.bidirectional:
                lines.append(f"    {conn.target}->>+{conn.source}: response")
        lines.append("```")
        return "\n".join(lines)

    def _generate_flow(self, arch: ArchitectureDescription) -> str:
        lines = ["```mermaid", "flowchart TD"]
        for node in arch.nodes:
            shape = "{" if "decision" in node.label.lower() else "("
            shape_close = "}" if "decision" in node.label.lower() else ")"
            lines.append(f'    {node.id}{shape}"{node.label}"{shape_close}')
        for conn in arch.connections:
            arrow = "<-->" if conn.bidirectional else "-->"
            label = f"|{conn.label}|" if conn.label else ""
            lines.append(f"    {conn.source} {arrow} {label} {conn.target}")
        lines.append("```")
        return "\n".join(lines)


class PlantUMLGenerator:
    """Generates diagrams in PlantUML format."""

    def generate(self, arch: ArchitectureDescription, diagram_type: DiagramType) -> str:
        """Generate PlantUML diagram."""
        if diagram_type == DiagramType.COMPONENT:
            return self._generate_component(arch)
        elif diagram_type == DiagramType.DEPLOYMENT:
            return self._generate_deployment(arch)
        elif diagram_type == DiagramType.SEQUENCE:
            return self._generate_sequence(arch)
        elif diagram_type == DiagramType.FLOW:
            return self._generate_flow(arch)
        raise ValueError(f"Unsupported diagram type: {diagram_type}")

    def _generate_component(self, arch: ArchitectureDescription) -> str:
        lines = ["@startuml", "!theme plain"]
        for node in arch.nodes:
            if node.technology:
                lines.append(f'component "{node.label}" as {node.id} [[tech:{node.technology}]]')
            else:
                lines.append(f'component "{node.label}" as {node.id}')
        for conn in arch.connections:
            arrow = "<-->" if conn.bidirectional else "-->"
            label = f" : {conn.label}" if conn.label else ""
            lines.append(f"{conn.source} {arrow}{label} {conn.target}")
        lines.append("@enduml")
        return "\n".join(lines)

    def _generate_deployment(self, arch: ArchitectureDescription) -> str:
        lines = ["@startuml", "!theme plain"]
        # Group nodes by parent
        parents: dict[str, list[Node]] = {}
        for node in arch.nodes:
            if node.parent:
                parents.setdefault(node.parent, []).append(node)
            else:
                lines.append(f'node "{node.label}" as {node.id}')
        for parent, child_nodes in parents.items():
            lines.append(f'node "{parent}" {{')
            for child in child_nodes:
                lines.append(f'    node "{child.label}" as {child.id}')
            lines.append("}")
        for conn in arch.connections:
            arrow = "<-->" if conn.bidirectional else "-->"
            label = f" : {conn.label}" if conn.label else ""
            lines.append(f"{conn.source} {arrow}{label} {conn.target}")
        lines.append("@enduml")
        return "\n".join(lines)

    def _generate_sequence(self, arch: ArchitectureDescription) -> str:
        lines = ["@startuml", "skinparam backgroundColor #FEFEFE"]
        # Add participants
        for node in arch.nodes:
            lines.append(f"participant {node.id} as \"{node.label}\"")
        # Add sequence
        for conn in arch.connections:
            label = conn.label or "calls"
            lines.append(f"{conn.source} -> {conn.target} : {label}")
            if conn.bidirectional:
                lines.append(f"{conn.target} --> {conn.source} : response")
        lines.append("@enduml")
        return "\n".join(lines)

    def _generate_flow(self, arch: ArchitectureDescription) -> str:
        lines = ["@startuml", "!theme plain"]
        for node in arch.nodes:
            if "decision" in node.label.lower():
                lines.append(f'circle "{node.label[0]}\" as {node.id}')
            else:
                lines.append(f'rectangle "{node.label}" as {node.id}')
        for conn in arch.connections:
            arrow = "<-->" if conn.bidirectional else "->"
            label = f" : {conn.label}" if conn.label else ""
            lines.append(f"{conn.source} {arrow}{label} {conn.target}")
        lines.append("@enduml")
        return "\n".join(lines)


class DOTGenerator:
    """Generates diagrams in DOT/Graphviz format."""

    def generate(self, arch: ArchitectureDescription, diagram_type: DiagramType) -> str:
        """Generate DOT diagram."""
        if diagram_type == DiagramType.COMPONENT:
            return self._generate_component(arch)
        elif diagram_type == DiagramType.DEPLOYMENT:
            return self._generate_deployment(arch)
        elif diagram_type == DiagramType.SEQUENCE:
            return self._generate_sequence(arch)
        elif diagram_type == DiagramType.FLOW:
            return self._generate_flow(arch)
        raise ValueError(f"Unsupported diagram type: {diagram_type}")

    def _generate_component(self, arch: ArchitectureDescription) -> str:
        lines = ["digraph architecture {", '    rankdir="LR";', "    node [shape=box];"]
        for node in arch.nodes:
            tech = f"\\n({node.technology})" if node.technology else ""
            desc = f"\\n{node.description}" if node.description else ""
            label = f'"{node.label}{tech}{desc}"'
            lines.append(f'    {node.id} [label={label}];')
        for conn in arch.connections:
            arrow = " -> " if not conn.bidirectional else " -> "
            style = " [style=dashed];" if conn.style == "dashed" else ";"
            label = f' [label="{conn.label}"];' if conn.label else style
            lines.append(f"    {conn.source}{arrow}{conn.target}{label}")
        lines.append("}")
        return "\n".join(lines)

    def _generate_deployment(self, arch: ArchitectureDescription) -> str:
        lines = ["digraph deployment {", '    rankdir="TB";', "    node [shape=box];"]
        # Group nodes by parent using subgraphs
        parents: dict[str, list[Node]] = {}
        for node in arch.nodes:
            if node.parent:
                parents.setdefault(node.parent, []).append(node)
            else:
                lines.append(f'    {node.id} [label="{node.label}"];')
        for idx, (parent, child_nodes) in enumerate(parents.items(), 1):
            lines.append(f'    subgraph cluster_{idx} {{')
            lines.append(f'        label="{parent}";')
            for child in child_nodes:
                lines.append(f'        {child.id} [label="{child.label}"];')
            lines.append("    }")
        for conn in arch.connections:
            arrow = " -> "
            label = f' [label="{conn.label}"];' if conn.label else ";"
            lines.append(f"    {conn.source}{arrow}{conn.target}{label}")
        lines.append("}")
        return "\n".join(lines)

    def _generate_sequence(self, arch: ArchitectureDescription) -> str:
        lines = ["digraph sequence {", '    rankdir="LR";', "    node [shape=box];", "    edge [arrowhead=normal];"]
        for node in arch.nodes:
            lines.append(f'    {node.id} [label="{node.label}"];')
        # Create invisible nodes for ordering
        for i, conn in enumerate(arch.connections, 1):
            label = conn.label or "interacts"
            lines.append(f'    edge{i} [shape=point, width=0];')
            lines.append(f"    {conn.source} -> edge{i} [style=invis];")
            lines.append(f"    edge{i} -> {conn.target} [label=\"{label}\"];")
        lines.append("}")
        return "\n".join(lines)

    def _generate_flow(self, arch: ArchitectureDescription) -> str:
        lines = ["digraph flowchart {", '    rankdir="TB";']
        for node in arch.nodes:
            if "decision" in node.label.lower():
                lines.append(f'    {node.id} [shape=diamond, label="{node.label}"];')
            else:
                lines.append(f'    {node.id} [shape=box, label="{node.label}"];')
        for conn in arch.connections:
            arrow = " -> "
            label = f' [label="{conn.label}"];' if conn.label else ";"
            lines.append(f"    {conn.source}{arrow}{conn.target}{label}")
        lines.append("}")
        return "\n".join(lines)


class ArchitectureDrawer:
    """Main class for generating architecture diagrams.

    Supports multiple output formats:
    - Mermaid (markdown compatible)
    - PlantUML (text-based UML)
    - DOT/Graphviz (graph visualization)

    Supports multiple diagram types:
    - Component diagrams
    - Deployment diagrams
    - Sequence diagrams
    - Flow diagrams
    """

    def __init__(self):
        """Initialize the ArchitectureDrawer."""
        self.mermaid = MermaidGenerator()
        self.plantuml = PlantUMLGenerator()
        self.dot = DOTGenerator()

    def generate_diagram(
        self,
        architecture: ArchitectureDescription | dict[str, Any],
        output_format: OutputFormat | str = OutputFormat.MERMAID,
        diagram_type: DiagramType | str = DiagramType.COMPONENT,
    ) -> str:
        """Generate a diagram from an architecture description.

        Args:
            architecture: Either an ArchitectureDescription object or a dict
                         with keys: title, nodes, connections
            output_format: The output format (mermaid, plantuml, dot)
            diagram_type: The type of diagram to generate

        Returns:
            The generated diagram as a string
        """
        # Convert dict to ArchitectureDescription if needed
        if isinstance(architecture, dict):
            arch = self._dict_to_architecture(architecture)
        else:
            arch = architecture

        # Normalize enums to strings
        if isinstance(output_format, OutputFormat):
            output_format_str = output_format.value
        else:
            output_format_str = output_format

        if isinstance(diagram_type, DiagramType):
            diagram_type_enum = diagram_type
        else:
            diagram_type_enum = DiagramType(diagram_type)

        # Generate based on format
        if output_format_str == OutputFormat.MERMAID.value:
            return self.mermaid.generate(arch, diagram_type_enum)
        elif output_format_str == OutputFormat.PLANTUML.value:
            return self.plantuml.generate(arch, diagram_type_enum)
        elif output_format_str == OutputFormat.DOT.value:
            return self.dot.generate(arch, diagram_type_enum)
        else:
            raise ValueError(f"Unsupported output format: {output_format}")

    def render_to_file(
        self,
        architecture: ArchitectureDescription | dict[str, Any],
        output_path: str,
        output_format: OutputFormat | str = OutputFormat.MERMAID,
        diagram_type: DiagramType | str = DiagramType.COMPONENT,
    ) -> None:
        """Generate a diagram and write it to a file.

        Args:
            architecture: The architecture description
            output_path: Path to the output file
            output_format: The output format
            diagram_type: The type of diagram to generate
        """
        diagram = self.generate_diagram(architecture, output_format, diagram_type)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(diagram)

    def _dict_to_architecture(self, data: dict[str, Any]) -> ArchitectureDescription:
        """Convert a dictionary to an ArchitectureDescription."""
        arch = ArchitectureDescription(
            title=data.get("title", "Architecture Diagram"),
            description=data.get("description", ""),
            metadata=data.get("metadata", {}),
        )

        # Convert nodes
        for node_data in data.get("nodes", []):
            if isinstance(node_data, dict):
                arch.add_node(
                    id=node_data["id"],
                    label=node_data["label"],
                    description=node_data.get("description", ""),
                    technology=node_data.get("technology", ""),
                    parent=node_data.get("parent", ""),
                )

        # Convert connections
        for conn_data in data.get("connections", []):
            if isinstance(conn_data, dict):
                arch.add_connection(
                    source=conn_data["source"],
                    target=conn_data["target"],
                    label=conn_data.get("label", ""),
                    style=conn_data.get("style", "solid"),
                    bidirectional=conn_data.get("bidirectional", False),
                )

        return arch

    def create_from_yaml_like(
        self,
        title: str,
        nodes: list[dict[str, str]],
        connections: list[dict[str, str]],
    ) -> ArchitectureDescription:
        """Create an ArchitectureDescription from simplified input.

        Args:
            title: The diagram title
            nodes: List of node dicts with id, label, and optional fields
            connections: List of connection dicts with source, target, and optional fields

        Returns:
            An ArchitectureDescription object
        """
        arch = ArchitectureDescription(title=title)
        for node in nodes:
            arch.add_node(
                id=node["id"],
                label=node["label"],
                description=node.get("description", ""),
                technology=node.get("technology", ""),
                parent=node.get("parent", ""),
            )
        for conn in connections:
            arch.add_connection(
                source=conn["source"],
                target=conn["target"],
                label=conn.get("label", ""),
                style=conn.get("style", "solid"),
                bidirectional=conn.get("bidirectional", False),
            )
        return arch
