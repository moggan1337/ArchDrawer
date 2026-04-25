# ArchDrawer

**Architecture Diagram Generator** - Generate beautiful architecture diagrams from simple descriptions.

## Features

- 🚀 **Multiple Output Formats**: Mermaid, PlantUML, and DOT/Graphviz
- 📊 **Multiple Diagram Types**: Component, Deployment, Sequence, and Flow diagrams
- 💻 **Interactive CLI**: Easy-to-use command-line interface with interactive mode
- 🔧 **Flexible Input**: Use dict/YAML/JSON or interactive prompts

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

### Interactive Mode

```bash
python -m src.cli generate --interactive
```

### Command Line Mode

```bash
# Generate a Mermaid component diagram
echo '{"nodes": [{"id": "web", "label": "Web App"}], "connections": []}' > arch.json
python -m src.cli render arch.json -f mermaid -t component

# Generate a PlantUML deployment diagram
python -m src.cli generate -f plantuml -t deployment -o diagram.puml
```

## Usage

### CLI Commands

```bash
# Generate a diagram (interactive)
archdrawer generate --interactive

# Generate a diagram (simple mode)
archdrawer generate --format mermaid --type component

# Render from file
archdrawer render architecture.yaml --format plantuml --output diagram.puml

# List supported formats
archdrawer list-formats
```

### Python API

```python
from src.drawer import ArchitectureDrawer, DiagramType, OutputFormat

# Create drawer
drawer = ArchitectureDrawer()

# Create architecture description
arch = ArchitectureDrawer().create_from_yaml_like(
    title="My Architecture",
    nodes=[
        {"id": "web", "label": "Web App", "technology": "React"},
        {"id": "api", "label": "API Server", "technology": "Python"},
        {"id": "db", "label": "Database", "technology": "PostgreSQL"},
    ],
    connections=[
        {"source": "web", "target": "api", "label": "REST API"},
        {"source": "api", "target": "db", "label": "SQL"},
    ]
)

# Generate diagram
diagram = drawer.generate_diagram(
    arch,
    output_format=OutputFormat.MERMAID,
    diagram_type=DiagramType.COMPONENT
)

# Save to file
drawer.render_to_file(arch, "diagram.md", OutputFormat.MERMAID, DiagramType.COMPONENT)
```

## Supported Formats

| Format | Description | Use Case |
|--------|-------------|----------|
| `mermaid` | Markdown-compatible diagrams | Documentation, README files |
| `plantuml` | Text-based UML diagrams | Technical documentation |
| `dot` | Graphviz DOT language | Complex visualizations |

## Supported Diagram Types

| Type | Description |
|------|-------------|
| `component` | Show components and their relationships |
| `deployment` | Show deployment topology with parent groups |
| `sequence` | Show interaction sequence between components |
| `flow` | Show flowcharts and decision trees |

## Examples

### Mermaid Component Diagram

````markdown
```mermaid
graph LR
    web["Web App [React]"]
    api["API Server [Python]"]
    db["Database [PostgreSQL]"]
    web --> |REST API| api
    api --> |SQL| db
```
````

### Architecture Description (YAML)

```yaml
title: Microservices Architecture
nodes:
  - id: gateway
    label: API Gateway
    technology: Kong
    parent: Infrastructure
  - id: user-service
    label: User Service
    technology: Node.js
    parent: Services
  - id: order-service
    label: Order Service
    technology: Python
    parent: Services
connections:
  - source: gateway
    target: user-service
    label: gRPC
  - source: gateway
    target: order-service
    label: gRPC
```

## Development

### Run Tests

```bash
pytest tests/ -v
```

### Project Structure

```
ArchDrawer/
├── src/
│   ├── __init__.py
│   ├── drawer.py       # Core diagram generation logic
│   └── cli.py          # Command-line interface
├── tests/
│   ├── __init__.py
│   └── test_drawer.py  # Unit tests
├── requirements.txt
└── README.md
```

## License

MIT License - See LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
