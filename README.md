# ArchDrawer

<p align="center">
  <img src="https://img.shields.io/badge/Diagrams-Auto-FF6B6B?style=for-the-badge&logo=diagram&logoColor=white" alt="Architecture">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
</p>

> 🏗️ **Architecture Diagram Generator** - Generates C4, UML diagrams from code analysis. Reverse engineers legacy systems.

## ✨ Features

### Diagram Types
- 📊 **C4 Model** - Context, Container, Component, Code
- 🔧 **UML Class** - Class diagrams
- 🔄 **UML Sequence** - API call flows
- 🗺️ **Component** - System architecture
- 🔗 **ER Diagrams** - Database schemas

### Analysis
- 💻 **Code Parsing** - AST-based analysis
- 🔌 **Dependency Graph** - Import/export relationships
- 🗄️ **Database** - Schema extraction
- 🌐 **API Endpoints** - Route mapping
- 📨 **Events** - Event/logging patterns

### Output
- 📑 **Mermaid** - Text-based diagrams
- 🖼️ **SVG/PNG** - Image export
- 📝 **PlantUML** - Text to diagram
- 📂 **draw.io** - XML format

## 📦 Installation

```bash
pip install archdrawer
archdrawer init
```

## 🚀 Usage

```bash
# Generate C4 diagram
archdrawer generate --type c4 --path ./src --output architecture.png

# Generate ER diagram
archdrawer generate --type er --db postgresql://localhost/mydb

# Generate sequence diagram
archdrawer generate --type sequence --path ./src/services/api.py
```

## 📄 License

MIT License
