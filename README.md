# Soccer Tactics Board

An interactive soccer/football tactics board built with Streamlit and an HTML5 Canvas component.

## Features

- Drag-and-drop players and ball on a realistic FIFA pitch
- 9 formation presets (4-4-2, 4-3-3, 3-5-2, 4-2-3-1, and more)
- Draw tactical arrows
- Undo/redo support
- Save/load tactics as JSON
- Export board as PNG
- Customizable team colors
- Edit player names and numbers
- Mobile touch support

## Installation

```bash
pip install soccer-tactics
```

## Usage

```bash
soccer-tactics
```

Or run as a Python module:

```bash
python -m soccer_tactics
```

The app will launch in your default browser.

### Options

```
--port INTEGER  Port to run the Streamlit server on (default: 8501)
```

## Development

```bash
git clone https://github.com/yourusername/Soccer-Tactics.git
cd Soccer-Tactics
pip install -e .
pytest
```

## License

MIT
