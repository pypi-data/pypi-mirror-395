# anifetch-rs

A terminal-based animated video player that displays videos as ASCII art alongside system information from fastfetch or neofetch.

## Features

- **Video to ASCII conversion** using Chafa with customizable character sets and colors
- **Smart caching system** - rendered frames are cached based on resolution and settings
- **Parallel frame processing** using Rayon for faster rendering
- **Audio playback support** via ffplay
- **System info integration** with fastfetch or neofetch
- **Smooth playback** with configurable framerates
- **Terminal UI** with resize handling and keyboard controls

## Requirements

- **Rust** (for building)
- **Python** 3.7+ (for the CLI wrapper)
- **ffmpeg** and **ffplay** (for video/audio processing)
- **chafa** (for image to ASCII conversion)
- **fastfetch** or **neofetch** (for system information)

### Installing Dependencies

#### Arch Linux / Manjaro
```bash
sudo pacman -S ffmpeg chafa fastfetch
```

#### Ubuntu / Debian
```bash
sudo apt install ffmpeg chafa neofetch
# For fastfetch, see: https://github.com/fastfetch-cli/fastfetch
```

#### macOS
```bash
brew install ffmpeg chafa fastfetch
```

## Installation

### From PyPI

```bash
pip install anifetch-rs
```

### From Source

1. Clone the repository:
```bash
git clone https://github.com/LinearJet/anifetch-rs.git
cd anifetch-rs
```

2. Create a Python virtual environment (recommended):
```bash
python3.11 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install maturin and build:
```bash
pip install maturin
maturin develop --release
```

### As a Rust Binary (No Python)

If you prefer to use it as a standalone Rust binary:

```bash
cargo build --release
./target/release/anifetch-bin --help
```

## Usage

Basic usage:
```bash
anifetch-rs video.mp4
```

### Options

```
Options:
  -W, --width <WIDTH>              Frame width in characters [default: 40]
  -H, --height <HEIGHT>            Frame height in characters [default: 20]
  -r, --framerate <FRAMERATE>      Playback framerate [default: 10]
  -s, --sound <SOUND>              Custom audio file path
  -f, --fast-fetch                 Use fastfetch instead of neofetch
  -c, --chafa <CHAFA_ARGS>         Custom chafa arguments [default: "--symbols ascii --fg-only"]
  -l, --loops <LOOPS>              Number of times to loop (0 = infinite) [default: 0]
      --force-render               Force re-rendering even if cache exists
      --no-buffer                  Disable alternate screen buffer
  -h, --help                       Print help
  -V, --version                    Print version
```

### Examples

High resolution ASCII with color:
```bash
anifetch -W 80 -H 40 -c "--symbols ascii --colors full" video.mp4
```

Fast playback with custom audio:
```bash
anifetch -r 30 -s music.mp3 animation.mp4
```

Loop 3 times with fastfetch:
```bash
anifetch --loops 3 --fast-fetch video.mp4
```

Force re-render with new settings:
```bash
anifetch --force-render -W 100 -H 50 video.mp4
```

### Keyboard Controls

- `q` or `ESC` - Quit
- `Ctrl+C` - Quit

## How It Works

1. **Video Processing**: Extracts frames from the video using ffmpeg at the specified framerate
2. **ASCII Conversion**: Converts each frame to ASCII art using Chafa with parallel processing
3. **Caching**: Stores rendered frames and audio in `~/.local/share/anifetch-rs/` (on Linux)
4. **Playback**: Displays frames alongside system info with synchronized audio

The cache is indexed by a hash of the video file, dimensions, framerate, and Chafa arguments. This means you only render once for each unique configuration.

## Project Structure

```
anifetch-rs/
├── src/
│   ├── app/
│   │   ├── cache.rs      # Caching system
│   │   ├── cli.rs        # Command-line argument parsing
│   │   ├── core.rs       # Main rendering logic
│   │   ├── external.rs   # External tool wrappers (ffmpeg, chafa, etc.)
│   │   └── renderer.rs   # Terminal UI and playback
│   ├── lib.rs            # Python bindings
│   └── main.rs           # Rust binary entry point
├── python/
│   └── anifetch/
│       └── __init__.py   # Python wrapper
├── Cargo.toml            # Rust dependencies
└── pyproject.toml        # Python package metadata
```

## Performance Tips

- Lower resolution (`-W` and `-H`) renders faster
- Lower framerates (`-r`) reduce processing time
- Use `--fast-fetch` for faster system info generation
- The first run will be slow (rendering), subsequent runs use cache
- ASCII-only mode (`--symbols ascii`) is faster than full color

## Troubleshooting

**"Cache miss or forced render" every time:**
- Check that your cache directory is writable: `~/.local/share/anifetch-rs/`

**"Failed to execute ffmpeg":**
- Install ffmpeg: `sudo apt install ffmpeg` (or equivalent for your OS)

**"Failed to run chafa":**
- Install chafa: `sudo apt install chafa`

**Audio doesn't play:**
- Install ffplay (part of ffmpeg)
- Check that your video has an audio track

**Python 3.14 compatibility issues:**
- Use Python 3.11 or 3.12 for building
- Or update PyO3 to version 0.22+ in Cargo.toml

## Credits

- Original concept inspired by [Notenlish's anifetch](https://github.com/Notenlish/anifetch)
- Built with [Chafa](https://hpjansson.org/chafa/) for ASCII art conversion
- Uses [Ratatui](https://github.com/ratatui-org/ratatui ) for terminal UI


## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.