# MarkDeck 🎬

A lightweight, markdown-based presentation tool that runs locally.

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Features

- **📝 Markdown-based**: Write presentations in plain text using familiar Markdown syntax
- **🚀 Fast & Lightweight**: No heavy frameworks, just clean HTML/CSS/JS
- **🔥 Hot Reload**: Automatically refreshes when you edit your markdown file (with `--watch`)
- **🎨 Beautiful Design**: Modern, distraction-free presentation interface
- **⌨️ Keyboard Shortcuts**: Navigate efficiently with keyboard controls
- **💬 Speaker Notes**: Hidden notes visible in speaker view
- **🎯 Syntax Highlighting**: Beautiful code blocks powered by highlight.js
- **📱 Responsive**: Works on different screen sizes
- **🔧 Easy Setup**: Simple CLI interface, no complex configuration

## 🚀 Quick Start

### Installation

#### Install from GitHub (Recommended)

```bash
# Install directly from GitHub using uv
uv pip install git+https://github.com/orangewise/markdeck.git

# Install from a specific branch
uv pip install git+https://github.com/orangewise/markdeck.git@claude/init-markdeck-project-01DJeHxbuthmNtDFjgxToFrP

# Then run it
markdeck present examples/demo.md
```

#### Install from Local Clone

```bash
# Clone the repository
git clone https://github.com/orangewise/markdeck.git
cd markdeck

# Using uv (recommended)
uv pip install -e .

# Or using pip
pip install -e .
```

### Run Without Installing

You can run MarkDeck directly without permanent installation:

```bash
# Create a test presentation
echo "# Hello MarkDeck

---

## Your First Slide

- Quick
- Easy
- Beautiful

---

## That's It!

Start creating your own presentations!" > test.md

# Run directly from GitHub (no installation needed)
uvx --from git+https://github.com/orangewise/markdeck.git@claude/init-markdeck-project-01DJeHxbuthmNtDFjgxToFrP markdeck present test.md

# Or use the main branch
uvx --from git+https://github.com/orangewise/markdeck.git markdeck present test.md
```

### Create Your First Presentation

```bash
# Create a new presentation from template
markdeck init my-presentation.md

# Start presenting
markdeck present my-presentation.md
```

Your browser will automatically open to `http://127.0.0.1:8000` with your presentation ready!

## 📖 Usage

### Basic Commands

```bash
# Present a markdown file
markdeck present slides.md

# Present with hot reload (auto-refresh on file changes)
markdeck present slides.md --watch

# Present on a custom port
markdeck present slides.md --port 3000

# Present without auto-opening browser
markdeck present slides.md --no-browser

# Combine options
markdeck present slides.md --watch --port 3000

# Create a new presentation
markdeck init my-talk.md

# Create with custom title
markdeck init my-talk.md --title "My Awesome Talk"

# Validate a presentation file
markdeck validate slides.md

# Show version
markdeck --version
```

### Markdown Syntax

Create slides by separating content with `---` on its own line:

```markdown
# My First Slide

This is the content of the first slide.

---

# Second Slide

- Bullet point 1
- Bullet point 2
- Bullet point 3

---

# Code Example

```python
def hello_markdeck():
    print("Hello from MarkDeck!")
```

---

# Slide with Speaker Notes

This content is visible to the audience.

<!--NOTES:
These are speaker notes.
Press 'S' to toggle speaker notes view.
-->
```

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `→` / `Space` / `PageDown` | Next slide |
| `←` / `PageUp` | Previous slide |
| `Home` | First slide |
| `End` | Last slide |
| `F` | Toggle fullscreen |
| `S` | Toggle speaker notes |
| `?` | Show help |
| `Esc` | Exit fullscreen/help |

## 📁 Project Structure

```
markdeck/
├── markdeck/          # Main package
│   ├── __init__.py
│   ├── __main__.py     # Entry point
│   ├── cli.py          # CLI interface
│   ├── server.py       # FastAPI server
│   ├── parser.py       # Markdown parser
│   └── static/         # Frontend files
│       ├── index.html
│       ├── style.css
│       └── slides.js
├── tests/              # Unit tests
├── examples/           # Example presentations
│   ├── demo.md
│   ├── features.md
│   └── code-examples.md
└── pyproject.toml      # Project configuration
```

## 🎨 Features in Detail

### Markdown Support

MarkDeck supports standard Markdown features:

- **Headings**: `#` through `######`
- **Bold**: `**bold**` or `__bold__`
- **Italic**: `*italic*` or `_italic_`
- **Code**: `` `inline code` ``
- **Links**: `[text](url)`
- **Images**: `![alt](url)`
- **Lists**: Unordered (`-`, `*`, `+`) and ordered (`1.`, `2.`)
- **Tables**: GitHub-flavored markdown tables
- **Blockquotes**: `> quote`
- **Code blocks**: Fenced with ` ``` `

### Code Syntax Highlighting

MarkDeck includes syntax highlighting for many languages:

```python
# Python
def fibonacci(n):
    return n if n <= 1 else fibonacci(n-1) + fibonacci(n-2)
```

```javascript
// JavaScript
const greet = (name) => console.log(`Hello, ${name}!`);
```

```rust
// Rust
fn main() {
    println!("Hello, MarkDeck!");
}
```

### Speaker Notes

Add speaker notes that are hidden from the main view:

```markdown
# My Slide

Visible content here.

<!--NOTES:
These notes are only visible when you press 'S'
- Remember to mention X
- Don't forget Y
- Time: 2 minutes
-->
```

### Hot Reload

MarkDeck includes hot reload functionality for a seamless development experience:

```bash
# Start with watch mode enabled
markdeck present my-slides.md --watch
```

**What happens:**
- MarkDeck monitors your markdown file for changes
- When you save edits, the presentation automatically refreshes in your browser
- You stay on the current slide (or closest available slide if slides were removed)
- A brief "Presentation reloaded" notification appears

**Perfect for:**
- Iterating on your presentation content
- Live editing during practice sessions
- Quick feedback on formatting and layout changes

## 🛠️ Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/markdeck.git
cd markdeck

# Install with development dependencies
uv pip install -e ".[dev]"

# Run tests
python -m unittest discover tests/

# Run linter
ruff check .

# Format code
ruff format .
```

### Running Tests

```bash
# Run all tests
python -m unittest discover tests/

# Run with verbose output
python -m unittest discover tests/ -v

# Run specific test file
python -m unittest tests.test_parser
```

### Project Commands

```bash
# Run the server in development mode
python -m markdeck present examples/demo.md

# Run linting
ruff check markdeck/ tests/

# Format code
ruff format markdeck/ tests/
```

## 📚 Examples

Check out the `examples/` directory for sample presentations:

- **demo.md**: Basic introduction to MarkDeck
- **features.md**: Comprehensive feature showcase
- **code-examples.md**: Syntax highlighting demo

Try them out:

```bash
markdeck present examples/demo.md
markdeck present examples/features.md
markdeck present examples/code-examples.md
```

## 🗺️ Roadmap

### Phase 2 - Enhanced Features

- [x] Hot reload (watch file for changes) ✓
- [ ] Multiple themes (dark/light mode toggle)
- [ ] Slide overview/grid view
- [ ] Slide transitions
- [ ] Two-column layouts
- [ ] Media embedding improvements

### Phase 3 - Polish & Distribution (Planned)

- [ ] Export to PDF
- [ ] Export to standalone HTML
- [ ] Configuration file support
- [ ] Custom themes
- [ ] PyPI distribution
- [ ] Plugin system

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new features
5. Run tests and linting
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

Please ensure:
- Code follows PEP 8 style guide
- All tests pass
- New features include tests
- Documentation is updated

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [marked.js](https://marked.js.org/) - Markdown parser
- [highlight.js](https://highlightjs.org/) - Syntax highlighting
- [Python-Markdown](https://python-markdown.github.io/) - Server-side markdown parsing

## 📞 Support

- 🐛 [Report bugs](https://github.com/YOUR_USERNAME/markdeck/issues)
- 💡 [Request features](https://github.com/YOUR_USERNAME/markdeck/issues)
- 📖 [Documentation](https://github.com/YOUR_USERNAME/markdeck)

## ⭐ Show Your Support

If you find MarkDeck useful, please consider giving it a star on GitHub!

---

**Made with ❤️ by the MarkDeck community**
