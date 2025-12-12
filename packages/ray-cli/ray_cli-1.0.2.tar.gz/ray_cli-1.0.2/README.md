# Ray CLI

![](https://img.shields.io/pypi/v/ray-cli.svg)
![](https://img.shields.io/pypi/l/ray-cli.svg)
[![GitHub last commit](https://img.shields.io/github/last-commit/nobbmaestro/ray-cli/development)](github-last-commit)
[![GitHub commits since](https://img.shields.io/github/commits-since/nobbmaestro/ray-cli/v1.0.2/development)](githut-commits-since)
![](https://img.shields.io/pypi/pyversions/ray-cli.svg)
![CI](https://github.com/nobbmaestro/ray-cli/actions/workflows/tests.yml/badge.svg)

Ray CLI is a command-line engineering utility for generating and broadcasting DMX data over sACN and Art-Net.

## Installation

Install `ray-cli` from [PyPi](https://pypi.org/project/ray-cli/):

```sh
# With pip.
pip install ray-cli
```

```sh
# With pipx.
pipx install ray-cli
```

```sh
# Or uv.
uv tool install ray-cli
```

Or, directly from GitHub:

> **Note**: The GitHub installation requires [uv](https://github.com/astral-sh/uv) to be installed!

```sh
git clone git@github.com:nobbmaestro/ray-cli.git
cd ray-cli
make install
```

## Usage

### Basic Example

To broadcast a ramp DMX signal to a specific IP address:

```sh
ray-cli sacn            \
    --dst 192.168.86.67 \
    --mode chase        \
    --universes 1 2     \
    --channels 24       \
    --fps 50            \
    --duration 60
```

### Available Modes

| Mode        | Description                           |
| ----------- | ------------------------------------- |
| `chase`     | Light chases across the channel range |
| `ramp`      | Linear ramp up **_and_** down         |
| `ramp-up`   | Gradually increases intensity         |
| `ramp-down` | Gradually decreases intensity         |
| `sine`      | Sine wave modulation                  |
| `square`    | Binary high/low intensity             |
| `static`    | Static intensity output               |

### Complete List of Command-Line Options

```sh
usage: ray-cli sacn [-m MODE] [-c CHANNELS] [-i INTENSITY] [-I INTENSITY_MIN]
                    [-f FREQUENCY] [-u UNIVERSES [UNIVERSES ...]] [-p PRIORITY]
                    [--src SRC] [--dst DST] [-w WORKERS] [-P PACKETS | -d DURATION]
                    [--fps FPS] [-v | -q] [--dry] [--purge] [--purge-on-exit] [-h] [-V]

options:
  -m, --mode MODE                            DMX signal shape mode (choices: chase, ramp,
                                             ramp-down, ramp-up, sine, square, static,
                                             default: ramp)
  -c, --channels CHANNELS                    DMX channels at universe to send to (range:
                                             1-512, default: 24)
  -i, --intensity INTENSITY                  DMX channels output intensity (range: 1-255,
                                             default: 10)
  -I, --intensity-min INTENSITY_MIN          DMX channels minimum output intensity (range:
                                             0-254, default: 0)
  -f, --frequency FREQUENCY                  frequency of the generated signal (range:
                                             0.001-unlimited, default: 1.0)
  -u, --universes UNIVERSES [UNIVERSES ...]  sACN universe(s) to send to (range: 1-63999,
                                             default: [1])
  -p, --priority PRIORITY                    DMX source priority (range: 0-200, default:
                                             100)

network group:
  --src SRC                                  IP address of the DMX source (default:
                                             0.0.0.0)
  --dst DST                                  IP address of the DMX destination (default:
                                             MULTICAST)

runtime group:
  -w, --workers WORKERS                      number of sender workers per universe (range:
                                             1-100, default: 1)
  -P, --packets PACKETS                      number of packets to send per universe per
                                             worker (range: 1-unlimited)
  -d, --duration DURATION                    broadcast duration in seconds (range:
                                             0.001-unlimited)
  --fps FPS                                  frames per second per universe (range:
                                             0.001-unlimited, default: 10)

display options:
  -v, --verbose                              run in verbose mode
  -q, --quiet                                run in quiet mode

operational options:
  --dry                                      simulate outputs without broadcast
  --purge                                    send zero-data on all channels and exit
  --purge-on-exit                            send zero-data on all channels upon
                                             completion

query options:
  -h, --help                                 print help and exit
  -V, --version                              show program's version number and exit
```
