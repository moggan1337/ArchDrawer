"""Tests for ArchitectureDrawer."""

import pytest

from src.drawer import (
    ArchitectureDescription,
    ArchitectureDrawer,
    DiagramType,
    OutputFormat,
)


class TestArchitectureDescription:
    """Tests for ArchitectureDescription class."""

    def test_create_empty_architecture(self):
        """Test creating an empty architecture description."""
        arch = ArchitectureDescription(title="Test Architecture")
        assert arch.title == "Test Architecture"
        assert arch.nodes == []
        assert arch.connections == []

    def test_add_node(self):
        """Test adding a node to architecture."""
        arch = ArchitectureDescription(title="Test")
        arch.add_node(id="web", label="Web App", technology="React")
        assert len(arch.nodes) == 1
        assert arch.nodes[0].id == "web"
        assert arch.nodes[0].label == "Web App"
        assert arch.nodes[0].technology == "React"

    def test_add_connection(self):
        """Test adding a connection between nodes."""
        arch = ArchitectureDescription(title="Test")
        arch.add_node(id="web", label="Web App")
        arch.add_node(id="api", label="API Server")
        arch.add_connection(source="web", target="api", label="REST API")
        assert len(arch.connections) == 1
        assert arch.connections[0].source == "web"
        assert arch.connections[0].target == "api"
        assert arch.connections[0].label == "REST API"

    def test_add_bidirectional_connection(self):
        """Test adding a bidirectional connection."""
        arch = ArchitectureDescription(title="Test")
        arch.add_node(id="client", label="Client")
        arch.add_node(id="server", label="Server")
        arch.add_connection(source="client", target="server", bidirectional=True)
        assert arch.connections[0].bidirectional is True


class TestMermaidGenerator:
    """Tests for Mermaid diagram generation."""

    @pytest.fixture
    def drawer(self):
        return ArchitectureDrawer()

    @pytest.fixture
    def simple_arch(self):
        arch = ArchitectureDescription(title="Simple Architecture")
        arch.add_node(id="client", label="Client App", technology="React")
        arch.add_node(id="server", label="API Server", technology="Python")
        arch.add_connection(source="client", target="server", label="HTTP")
        return arch

    def test_generate_mermaid_component(self, drawer, simple_arch):
        """Test generating Mermaid component diagram."""
        result = drawer.generate_diagram(
            simple_arch,
            output_format=OutputFormat.MERMAID,
            diagram_type=DiagramType.COMPONENT,
        )
        assert "```mermaid" in result
        assert "graph LR" in result
        assert 'client["Client App' in result
        assert 'server["API Server' in result
        assert "client -->" in result

    def test_generate_mermaid_with_technology(self, drawer, simple_arch):
        """Test that technology info appears in Mermaid diagram."""
        result = drawer.generate_diagram(
            simple_arch,
            output_format=OutputFormat.MERMAID,
            diagram_type=DiagramType.COMPONENT,
        )
        assert "[React]" in result

    def test_generate_mermaid_sequence(self, drawer, simple_arch):
        """Test generating Mermaid sequence diagram."""
        result = drawer.generate_diagram(
            simple_arch,
            output_format=OutputFormat.MERMAID,
            diagram_type=DiagramType.SEQUENCE,
        )
        assert "```mermaid" in result
        assert "sequenceDiagram" in result
        assert "participant client as Client App" in result

    def test_generate_mermaid_flow(self, drawer, simple_arch):
        """Test generating Mermaid flowchart."""
        result = drawer.generate_diagram(
            simple_arch,
            output_format=OutputFormat.MERMAID,
            diagram_type=DiagramType.FLOW,
        )
        assert "```mermaid" in result
        assert "flowchart TD" in result


class TestPlantUMLGenerator:
    """Tests for PlantUML diagram generation."""

    @pytest.fixture
    def drawer(self):
        return ArchitectureDrawer()

    @pytest.fixture
    def simple_arch(self):
        arch = ArchitectureDescription(title="Simple Architecture")
        arch.add_node(id="client", label="Client App", technology="React")
        arch.add_node(id="server", label="API Server", technology="Python")
        arch.add_connection(source="client", target="server", label="HTTP")
        return arch

    def test_generate_plantuml_component(self, drawer, simple_arch):
        """Test generating PlantUML component diagram."""
        result = drawer.generate_diagram(
            simple_arch,
            output_format=OutputFormat.PLANTUML,
            diagram_type=DiagramType.COMPONENT,
        )
        assert "@startuml" in result
        assert "@enduml" in result
        assert 'component "Client App" as client' in result
        assert 'component "API Server" as server' in result

    def test_generate_plantuml_sequence(self, drawer, simple_arch):
        """Test generating PlantUML sequence diagram."""
        result = drawer.generate_diagram(
            simple_arch,
            output_format=OutputFormat.PLANTUML,
            diagram_type=DiagramType.SEQUENCE,
        )
        assert "@startuml" in result
        assert "sequenceDiagram" in result or "participant" in result


class TestDOTGenerator:
    """Tests for DOT/Graphviz diagram generation."""

    @pytest.fixture
    def drawer(self):
        return ArchitectureDrawer()

    @pytest.fixture
    def simple_arch(self):
        arch = ArchitectureDescription(title="Simple Architecture")
        arch.add_node(id="client", label="Client App", technology="React")
        arch.add_node(id="server", label="API Server", technology="Python")
        arch.add_connection(source="client", target="server", label="HTTP")
        return arch

    def test_generate_dot_component(self, drawer, simple_arch):
        """Test generating DOT component diagram."""
        result = drawer.generate_diagram(
            simple_arch,
            output_format=OutputFormat.DOT,
            diagram_type=DiagramType.COMPONENT,
        )
        assert "digraph" in result
        assert "rankdir=" in result
        assert "Client App" in result
        assert "client -> server" in result

    def test_generate_dot_deployment(self, drawer, simple_arch):
        """Test generating DOT deployment diagram."""
        result = drawer.generate_diagram(
            simple_arch,
            output_format=OutputFormat.DOT,
            diagram_type=DiagramType.DEPLOYMENT,
        )
        assert "digraph" in result
        assert "Client App" in result


class TestArchitectureDrawer:
    """Tests for ArchitectureDrawer main class."""

    def test_init(self):
        """Test drawer initialization."""
        drawer = ArchitectureDrawer()
        assert drawer.mermaid is not None
        assert drawer.plantuml is not None
        assert drawer.dot is not None

    def test_create_from_yaml_like(self):
        """Test creating architecture from simplified input."""
        drawer = ArchitectureDrawer()
        nodes = [
            {"id": "web", "label": "Web App", "technology": "React"},
            {"id": "api", "label": "API", "technology": "Node.js"},
        ]
        connections = [{"source": "web", "target": "api", "label": "REST"}]

        arch = drawer.create_from_yaml_like("Test Architecture", nodes, connections)
        assert arch.title == "Test Architecture"
        assert len(arch.nodes) == 2
        assert len(arch.connections) == 1

    def test_generate_from_dict(self):
        """Test generating diagram from dictionary input."""
        drawer = ArchitectureDrawer()
        data = {
            "title": "Dict Architecture",
            "nodes": [
                {"id": "a", "label": "Node A", "technology": "Python"},
                {"id": "b", "label": "Node B"},
            ],
            "connections": [{"source": "a", "target": "b", "label": "connects"}],
        }

        result = drawer.generate_diagram(
            data,
            output_format=OutputFormat.MERMAID,
            diagram_type=DiagramType.COMPONENT,
        )
        assert "Dict Architecture" in result or "a" in result

    def test_render_to_file(self, tmp_path):
        """Test rendering diagram to file."""
        drawer = ArchitectureDrawer()
        arch = ArchitectureDescription(title="Test")
        arch.add_node(id="test", label="Test Node")

        output_path = tmp_path / "test_diagram.md"
        drawer.render_to_file(
            arch,
            str(output_path),
            output_format=OutputFormat.MERMAID,
            diagram_type=DiagramType.COMPONENT,
        )

        assert output_path.exists()
        content = output_path.read_text()
        assert "```mermaid" in content
        assert "Test Node" in content

    def test_invalid_format_raises_error(self):
        """Test that invalid format raises ValueError."""
        drawer = ArchitectureDrawer()
        arch = ArchitectureDescription(title="Test")
        arch.add_node(id="a", label="A")

        with pytest.raises(ValueError, match="Unsupported output format"):
            drawer.generate_diagram(arch, output_format="invalid")

    def test_invalid_diagram_type_raises_error(self):
        """Test that invalid diagram type raises ValueError."""
        drawer = ArchitectureDrawer()
        arch = ArchitectureDescription(title="Test")
        arch.add_node(id="a", label="A")

        with pytest.raises(ValueError):
            drawer.generate_diagram(
                arch,
                output_format=OutputFormat.MERMAID,
                diagram_type="invalid",
            )


class TestDeploymentDiagram:
    """Tests for deployment diagram with parent grouping."""

    @pytest.fixture
    def drawer(self):
        return ArchitectureDrawer()

    @pytest.fixture
    def deployment_arch(self):
        arch = ArchitectureDescription(title="Deployment Architecture")
        arch.add_node(id="web", label="Web Server", parent="AWS")
        arch.add_node(id="db", label="Database", parent="AWS")
        arch.add_node(id="client", label="Client", parent="Browser")
        arch.add_connection(source="client", target="web", label="HTTPS")
        arch.add_connection(source="web", target="db", label="SQL")
        return arch

    def test_mermaid_deployment_with_parents(self, drawer, deployment_arch):
        """Test Mermaid deployment diagram with parent groups."""
        result = drawer.generate_diagram(
            deployment_arch,
            output_format=OutputFormat.MERMAID,
            diagram_type=DiagramType.DEPLOYMENT,
        )
        assert "subgraph AWS" in result
        assert "subgraph Browser" in result


class TestBidirectionalConnections:
    """Tests for bidirectional connections."""

    @pytest.fixture
    def drawer(self):
        return ArchitectureDrawer()

    def test_mermaid_bidirectional(self, drawer):
        """Test bidirectional connection in Mermaid."""
        arch = ArchitectureDescription(title="Test")
        arch.add_node(id="a", label="Node A")
        arch.add_node(id="b", label="Node B")
        arch.add_connection(source="a", target="b", bidirectional=True)

        result = drawer.generate_diagram(
            arch,
            output_format=OutputFormat.MERMAID,
            diagram_type=DiagramType.COMPONENT,
        )
        assert "a <-->" in result


class TestDiagramTypes:
    """Tests for all diagram types."""

    @pytest.fixture
    def drawer(self):
        return ArchitectureDrawer()

    @pytest.fixture
    def arch(self):
        arch = ArchitectureDescription(title="Test")
        arch.add_node(id="start", label="Start")
        arch.add_node(id="process", label="Process Data")
        arch.add_node(id="decision", label="Is Valid?")
        arch.add_node(id="end", label="End")
        arch.add_connection(source="start", target="process")
        arch.add_connection(source="process", target="decision")
        arch.add_connection(source="decision", target="end", label="Yes")
        return arch

    def test_component_diagram(self, drawer, arch):
        """Test component diagram generation."""
        result = drawer.generate_diagram(
            arch,
            output_format=OutputFormat.MERMAID,
            diagram_type=DiagramType.COMPONENT,
        )
        assert "graph LR" in result

    def test_deployment_diagram(self, drawer, arch):
        """Test deployment diagram generation."""
        result = drawer.generate_diagram(
            arch,
            output_format=OutputFormat.MERMAID,
            diagram_type=DiagramType.DEPLOYMENT,
        )
        assert "graph TB" in result

    def test_sequence_diagram(self, drawer, arch):
        """Test sequence diagram generation."""
        result = drawer.generate_diagram(
            arch,
            output_format=OutputFormat.MERMAID,
            diagram_type=DiagramType.SEQUENCE,
        )
        assert "sequenceDiagram" in result

    def test_flow_diagram(self, drawer, arch):
        """Test flowchart diagram generation."""
        result = drawer.generate_diagram(
            arch,
            output_format=OutputFormat.MERMAID,
            diagram_type=DiagramType.FLOW,
        )
        assert "flowchart TD" in result
