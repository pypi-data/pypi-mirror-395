# Python Code Minimap

This is a pure Python port of the wonderful [`code-minimap`](https://github.com/wfxr/code-minimap).

It is a lot slower than the original.

## Usage

```
usage: code-minimap [-h] [--hscale HSCALE] [--vscale VSCALE] [--padding PADDING] [--octant] [file]

Render a Braille minimap of a text file.

positional arguments:
  file                  File to read. Use '-' or omit to read from stdin.

options:
  -h, --help            show this help message and exit
  --hscale, -H HSCALE   Horizontal scaling factor (default: 1.0).
  --vscale, -V VSCALE   Vertical scaling factor (default: 1.0).
  --padding, -p PADDING
                        Pad each output line to this width.
  --octant              Use the octant block character set instead of Braille.
```

```bash
$ python -m code_minimap -V 0.25 -H 0.5 code_minimap.py
⣿⣿⣿⣿⣿⣿⣿⣭⣥⣤⣤⣤⣤⣄⣀⣀⣀⡀
⣿⣿⣿⣿⡿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠇
⣒⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠶⠶⠶⠄
⠶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣤⣤⣤⣤⣤⠤⠄
⠤⣭⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⠿⠭⠭⠤⠤⠤⠤⠤
⣀⣤⣿⣿⣿⣛⣛⣛⡛⠃
⣒⣿⣿⣿⣿⣿⣿⣿⣿⣿⣓⣒⣒⣒⣂⣀⣀⣀
⠒⣿⣿⣿⣿⣿⣭⣭⣤⠤⠤⠤⠤⠤
⠛⠿⣿⣿⣷⣶⣶⣶⣤⠤⠤
⠀⠛⠛⠿⣿⣿⣷⣶⣶⡶⠤⠤
⠤⣶⣿⣿⣿⣿⣿⣿⣿⣟⣛⣓⣀⣀⣀⡀
⠀⠿⣿⣿⣿⠿⠭⠭⠭⠭⠭⠭⠭⠭⠉⠉
⠀⣭⣿⣿⣿⣿⣿⣟⣛⣛⣛⣛⡋⠁
⠒⠿⣿⣿⣿⣯⣭⣭⣭⣭⣭⣭⣭⣤⣤⣤⣤⣤⣤⠤
⠒⠛⠛⠛⠛⠛⠋⠉⠉⠉⠉⠉
```

## Installation

```bash
pip install python-code-minimap
```

## Python API


```python
from code_minimap import render

minimap = render(Path("code_minimap.py").read_text(), hscale=0.5, vscale=0.25)
print(minimap)
```

You can also iterate over lines of the minimap using the `iter_minimap_lines` function.
