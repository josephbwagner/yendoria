# Yendoria Distribution Guide

## 🎮 Sharing Your Roguelike Game

### Quick Start for Players

#### Option 1: Direct Installation (Recommended)
```bash
pip install git+https://github.com/josephbwagner/yendoria.git@v0.1.1
python -m yendoria
```

#### Option 2: Download and Run
```bash
# Download latest release
wget https://github.com/josephbwagner/yendoria/archive/v0.1.1.tar.gz
tar -xzf v0.1.1.tar.gz
cd yendoria-0.1.1

# Install and play
pip install poetry
poetry install
poetry run python -m yendoria
```

#### Option 3: Developer Setup
```bash
git clone https://github.com/josephbwagner/yendoria.git
cd yendoria
poetry install
poetry run python -m yendoria
```

### System Requirements
- **Python**: 3.10 or higher
- **Operating System**: Linux, macOS, Windows
- **Dependencies**: Automatically installed via pip/poetry
- **Terminal**: ANSI color support recommended

### Game Features (v0.1.1)
- Traditional roguelike gameplay
- Procedural dungeon generation
- Turn-based combat system
- Field of view mechanics
- Multiple input schemes (arrows, WASD, vim keys, numpad)
- ASCII graphics with libtcod

### Controls
- **Movement**: Arrow keys, WASD, hjkl (vim), or numpad
- **Quit**: ESC or Q
- **Look**: L + direction keys

### For Developers
- **Source Code**: Available on GitHub
- **Documentation**: Sphinx-generated docs
- **Testing**: Full test suite with coverage
- **CI/CD**: Automated builds and releases
- **Architecture**: Entity Component System (ECS)

### Community
- **Report Issues**: GitHub Issues
- **Contribute**: Pull requests welcome
- **Discussion**: GitHub Discussions
- **License**: MIT (open source)

### Version History
- **v0.1.1**: Bug fixes and workflow improvements
- **v0.1.0**: Initial release

---

*Built with ❤️ using Python, libtcod, and modern development practices*
