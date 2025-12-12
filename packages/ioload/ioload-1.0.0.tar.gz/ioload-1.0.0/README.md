# ioload

[![CI](https://github.com/guntanis/ioload/workflows/CI/badge.svg)](https://github.com/guntanis/ioload/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![PyPI version](https://badge.fury.io/py/ioload.svg)](https://badge.fury.io/py/ioload)

A wrapper for `iostat` that displays I/O statistics in a real-time chart format similar to `nload`, with the ability to switch between devices using keyboard navigation.

## 🎯 Features

- **Real-time visualization** - Live I/O statistics with smooth updates
- **Multiple chart views** - IOPS, Throughput, Utilization, and Wait Times
- **Keyboard navigation** - Switch devices and views with arrow keys
- **Color-coded charts** - Easy-to-read terminal charts with color support
- **Cross-platform** - Works on Linux and macOS (Unix-like systems)
- **Lightweight** - Minimal dependencies, fast startup

## Features

- Real-time I/O statistics visualization
- Multiple charts showing:
  - Read/Write IOPS (requests per second)
  - Read/Write Throughput (KB/s)
  - Device Utilization (%)
  - Average wait times
- Switch between devices using `<` (previous) and `>` (next) keys
- Clean, terminal-based interface using curses

## Used by

- Ring.cr

## Sponsored by

- Ring.cr

## Requirements

- Python 3.6+
- `iostat` command (part of `sysstat` package)
  - On macOS: `brew install sysstat`
  - On Linux: Usually pre-installed or available via package manager
- `asciichartpy` Python library for chart rendering
  - Install with: `pip install asciichartpy`

## Installation

### Quick Install (Recommended)

```bash
curl -fsSL https://raw.githubusercontent.com/guntanis/ioload/main/scripts/install.sh | bash
```

### Manual Installation

See [docs/INSTALL.md](docs/INSTALL.md) for detailed manual installation instructions.

## Usage

```bash
./ioload.py
```

Or:

```bash
python3 ioload.py
```

You can specify a custom refresh interval (in seconds):

```bash
./ioload.py -i 0.5  # Refresh every 0.5 seconds
./ioload.py --interval 2.0  # Refresh every 2 seconds
```

## Controls

- `Left Arrow` or `<`: Switch to previous device
- `Right Arrow` or `>`: Switch to next device
- `Up Arrow`: Switch to previous chart view
- `Down Arrow`: Switch to next chart view
- `Q`: Quit the application

## How it works

The tool continuously runs `iostat -x` in the background to collect I/O statistics for all block devices. It maintains a rolling history of the last 60 data points and displays them as ASCII charts in real-time.

The charts show:
- **Read/Write IOPS**: Combined visualization of read and write requests per second
- **Read/Write Throughput**: Combined visualization of read and write data transfer rates
- **Utilization**: Device utilization percentage over time

## 📸 Screenshots

*(Add screenshots or animated GIFs here showing ioload in action)*

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by `nload` and `htop`
- Uses `asciichartpy` for beautiful terminal charts
- Built with Python's `curses` library

## 📁 Project Structure

```
ioload/
├── docs/          # Additional documentation
├── scripts/       # Installation scripts
├── tests/         # Test files
└── ioload.py      # Main application
```

See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for details.

## 📚 Related Projects

- [nload](https://github.com/rolandriegel/nload) - Network traffic monitor
- [htop](https://github.com/htop-dev/htop) - Interactive process viewer
- [iotop](https://github.com/Tomas-M/iotop) - I/O monitoring tool

## ⭐ Star History

If you find this project useful, please consider giving it a star on GitHub!

---

**Made with ❤️ by the ioload contributors**

