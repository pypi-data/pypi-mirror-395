# **edhelper**

A command-line deck builder, analyzer, and management tool for *Magic: The Gathering* — focused on the Commander (EDH) format.

`edhelper` allows you to create, modify, validate, analyze, import, export, and manage Commander decks entirely from the terminal, shell, or web editor.

---

## **📦 Installation**

### Full Installation

```bash
pip install edhelper
```

or with **pipx**:

```bash
pipx install edhelper
```

### Modular Installation

You can install only the components you need:

```bash
# Only shell (interactive REPL)
pip install edhelper[shell]

# Only GUI editor
pip install edhelper[editor]

# Full installation (CLI + Shell + Editor)
pip install edhelper[all]
```

---

## **🚀 Quick Start**

### Using the CLI

```bash
# Create or open a deck
edhelper deck create MyDeck

# Add cards to a deck
edhelper deck add MyDeck "Lightning Bolt" 1

# List all decks
edhelper deck list

# Search for cards
edhelper card search "lightning"

# Get top commanders
edhelper card top-commanders
```

### Using the Shell (Interactive REPL)

```bash
# Start interactive shell
edhelper shell

# In the shell:
[ 1 ] > select MyDeck
[ 2 ] : [ MyDeck ] > add "Lightning Bolt" 1
[ 3 ] : [ MyDeck ] > list
```

### Using the Web Editor

```bash
# Start the web editor
edhelper start-editor

# Opens browser at http://0.0.0.0:3839
```

---

## **📖 Features**

### Deck Management
- Create, delete, rename, and copy decks
- Import decks from `.txt` files
- Export decks to `.txt`, `.csv`, or `.json`
- Set and manage commanders

### Card Operations
- Search cards by name or partial match
- Get top 100 commanders
- Get meta cards for commanders from EDHREC
- View card details and statistics

### Interactive Shell
- Full-featured REPL with autocomplete
- Context-aware commands (root vs deck mode)
- Command history and suggestions

### Web Editor
- Modern web interface for deck building
- RESTful API backend
- Real-time updates

---

## **📚 Documentation**

For detailed documentation on each component:

- **[CLI Commands](cli/README.md)** - Complete CLI command reference
- **[Shell Guide](shell/README.md)** - Interactive shell usage
- **[Editor Guide](editor/README.md)** - Web editor documentation

---

## **🔧 Configuration**

### Authentication

Before using the tool, you need to authenticate:

```bash
edhelper --get-key
```

This will prompt you for your API key and client ID.

### Version and Info

```bash
# Show version
edhelper --version

# Show metadata
edhelper --info
```

---

## **🧰 Examples**

### Create a deck with commander

```bash
edhelper deck create Atraxa "Atraxa, Praetors' Voice"
```

### Import deck from file

```bash
edhelper deck import-txt decklist.txt MyDeck
```

### Get meta cards for a commander

```bash
edhelper deck meta "Atraxa, Praetors' Voice" "Top Cards"
```

### Export deck

```bash
edhelper export txt MyDeck /path/to/export/
```

### Search and add cards

```bash
# Search for cards
edhelper card search "lightning"

# Add to deck
edhelper deck add MyDeck "Lightning Bolt" 1
```

---

## **🏗️ Architecture**

The project is organized into modular components:

- **`cli/`** - CLI commands (can be installed separately)
- **`shell/`** - Interactive REPL shell
- **`editor/`** - Web editor (frontend + backend)
- **`domain/`** - Business logic and services
- **`commom/`** - Shared utilities and commands
- **`external/`** - External API integrations

---

## **📝 License**

[Add your license here]

---

## **🤝 Contributing**

[Add contributing guidelines here]

---

## **📧 Support**

[Add support information here]

