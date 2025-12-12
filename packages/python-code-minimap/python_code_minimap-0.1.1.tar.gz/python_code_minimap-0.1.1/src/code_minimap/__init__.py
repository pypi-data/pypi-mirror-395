#!/usr/bin/env python3
"""Generate a textual minimap representation of source files."""

from __future__ import annotations

from itertools import islice
from pathlib import Path
from typing import TYPE_CHECKING, Iterable, Iterator, TextIO

if TYPE_CHECKING:
    import argparse

__all__ = ["render", "iter_minimap_lines", "BRAILLE", "OCTANTS"]

Span = tuple[int, int] | None

BRAILLE = (
    "⠀⠁⠂⠃⠄⠅⠆⠇⡀⡁⡂⡃⡄⡅⡆⡇⠈⠉⠊⠋⠌⠍⠎⠏⡈⡉⡊⡋⡌⡍⡎⡏⠐⠑⠒⠓⠔⠕⠖⠗⡐⡑⡒⡓⡔⡕⡖⡗⠘⠙⠚⠛⠜⠝⠞⠟⡘⡙⡚⡛⡜⡝⡞⡟"
    "⠠⠡⠢⠣⠤⠥⠦⠧⡠⡡⡢⡣⡤⡥⡦⡧⠨⠩⠪⠫⠬⠭⠮⠯⡨⡩⡪⡫⡬⡭⡮⡯⠰⠱⠲⠳⠴⠵⠶⠷⡰⡱⡲⡳⡴⡵⡶⡷⠸⠹⠺⠻⠼⠽⠾⠿⡸⡹⡺⡻⡼⡽⡾⡿"
    "⢀⢁⢂⢃⢄⢅⢆⢇⣀⣁⣂⣃⣄⣅⣆⣇⢈⢉⢊⢋⢌⢍⢎⢏⣈⣉⣊⣋⣌⣍⣎⣏⢐⢑⢒⢓⢔⢕⢖⢗⣐⣑⣒⣓⣔⣕⣖⣗⢘⢙⢚⢛⢜⢝⢞⢟⣘⣙⣚⣛⣜⣝⣞⣟"
    "⢠⢡⢢⢣⢤⢥⢦⢧⣠⣡⣢⣣⣤⣥⣦⣧⢨⢩⢪⢫⢬⢭⢮⢯⣨⣩⣪⣫⣬⣭⣮⣯⢰⢱⢲⢳⢴⢵⢶⢷⣰⣱⣲⣳⣴⣵⣶⣷⢸⢹⢺⢻⢼⢽⢾⢿⣸⣹⣺⣻⣼⣽⣾⣿"
)

OCTANTS = (
    "⠀𜺨𜴀▘𜴉𜴊🯦𜴍𜺣𜴶𜴹𜴺▖𜵅𜵈▌𜺫🮂𜴁𜴂𜴋𜴌𜴎𜴏𜴷𜴸𜴻𜴼𜵆𜵇𜵉𜵊𜴃𜴄𜴆𜴇𜴐𜴑𜴔𜴕𜴽𜴾𜵁𜵂𜵋𜵌𜵎𜵏▝𜴅𜴈▀𜴒𜴓𜴖𜴗𜴿𜵀𜵃𜵄▞𜵍𜵐▛"
    "𜴘𜴙𜴜𜴝𜴧𜴨𜴫𜴬𜵑𜵒𜵕𜵖𜵡𜵢𜵥𜵦𜴚𜴛𜴞𜴟𜴩𜴪𜴭𜴮𜵓𜵔𜵗𜵘𜵣𜵤𜵧𜵨🯧𜴠𜴣𜴤𜴯𜴰𜴳𜴴𜵙𜵚𜵝𜵞𜵩𜵪𜵭𜵮𜴡𜴢𜴥𜴦𜴱𜴲𜴵🮅𜵛𜵜𜵟𜵠𜵫𜵬𜵯𜵰"
    "𜺠𜵱𜵴𜵵𜶀𜶁𜶄𜶅▂𜶬𜶯𜶰𜶻𜶼𜶿𜷀𜵲𜵳𜵶𜵷𜶂𜶃𜶆𜶇𜶭𜶮𜶱𜶲𜶽𜶾𜷁𜷂𜵸𜵹𜵼𜵽𜶈𜶉𜶌𜶍𜶳𜶴𜶷𜶸𜷃𜷄𜷇𜷈𜵺𜵻𜵾𜵿𜶊𜶋𜶎𜶏𜶵𜶶𜶹𜶺𜷅𜷆𜷉𜷊"
    "▗𜶐𜶓▚𜶜𜶝𜶠𜶡𜷋𜷌𜷏𜷐▄𜷛𜷞▙𜶑𜶒𜶔𜶕𜶞𜶟𜶢𜶣𜷍𜷎𜷑𜷒𜷜𜷝𜷟𜷠𜶖𜶗𜶙𜶚𜶤𜶥𜶨𜶩𜷓𜷔𜷗𜷘𜷡𜷢▆𜷤▐𜶘𜶛▜𜶦𜶧𜶪𜶫𜷕𜷖𜷙𜷚▟𜷣𜷥█"
)

FRAME_HEIGHT = 4


def render(
    reader: str | bytes | Iterable[str] | TextIO,
    hscale: float,
    vscale: float,
    padding: int | None = None,
    charset: str = BRAILLE,
) -> str:
    """Render a minimap into a single string."""
    return "\n".join(iter_minimap_lines(reader, hscale, vscale, padding, charset))


def iter_minimap_lines(
    reader: str | bytes | Iterable[str] | TextIO,
    hscale: float,
    vscale: float,
    padding: int | None = None,
    charset: str = BRAILLE,
) -> Iterator[str]:
    """Yield minimap lines (without trailing newline) for the supplied reader."""
    groups = _iter_scaled_groups(_iter_lines(reader), vscale)

    for chunk in _batched(groups, FRAME_HEIGHT):
        frame = [_collapse_group(group) for group in chunk]
        frame.extend([(0, 0)] * (FRAME_HEIGHT - len(frame)))
        scaled = [_scale_span(span, hscale) for span in frame]
        yield _frame_to_line(scaled, padding, charset)


def _iter_lines(reader: str | bytes | Iterable[str] | TextIO) -> Iterator[str]:
    """Yield normalized lines of text from the reader."""
    if isinstance(reader, (bytes, bytearray)):
        yield from reader.decode("utf-8", errors="replace").splitlines()
        return
    if isinstance(reader, str):
        yield from reader.splitlines()
        return

    source = reader if hasattr(reader, "read") else iter(reader)
    for line in source:
        if isinstance(line, bytes):
            line = line.decode("utf-8", errors="replace")
        yield line.rstrip("\r\n")


def _iter_scaled_groups(lines: Iterable[str], vscale: float) -> Iterator[list[Span]]:
    """Group lines according to the vertical scale factor."""
    current_bucket = None
    bucket: list[Span] = []

    for index, line in enumerate(lines):
        bucket_id = int(index * vscale)
        if current_bucket is None:
            current_bucket = bucket_id

        if bucket_id != current_bucket:
            yield bucket
            bucket = []
            current_bucket = bucket_id

        bucket.append(_line_span(line))

    if bucket:
        yield bucket


def _line_span(line: str) -> Span:
    """Determine the start and stop columns of non-whitespace text in a line."""
    if not line.strip():
        return None
    start = len(line) - len(line.lstrip())
    stop = len(line.rstrip())
    return start, stop


def _collapse_group(group: list[Span]) -> tuple[int, int]:
    """Combine spans within a vertical group into a single span."""
    spans = [span for span in group if span is not None]
    if not spans:
        return (0, 0)

    starts = [span[0] for span in spans]
    stops = [span[1] for span in spans]
    return min(starts), max(stops)


def _scale_span(span: tuple[int, int], factor: float) -> tuple[int, int]:
    """Apply horizontal scaling to a span."""
    start = int(span[0] * factor)
    stop = int(span[1] * factor)
    if start >= stop:
        return (0, 0)
    return start, stop


def _batched(iterable, n):
    """Yield successive n-length tuples from iterable."""
    if n <= 0:
        raise ValueError("n must be a positive integer")
    it = iter(iterable)
    while True:
        chunk = tuple(islice(it, n))
        if not chunk:
            return
        yield chunk


def _frame_to_line(
    frame: list[tuple[int, int]],
    padding: int | None,
    charset: str,
) -> str:
    """Convert a frame of spans into a single rendered line."""
    bounds: list[tuple[int, int] | None] = []
    max_stop = 0

    for start, stop in frame:
        if start >= stop:
            bounds.append(None)
            continue
        bounds.append((start, stop))
        if stop > max_stop:
            max_stop = stop

    if max_stop == 0:
        line = ""
    else:
        chars: list[str] = []
        for col in range(0, max_stop, 2):
            mask = 0
            col_next = col + 1
            for row, bound in enumerate(bounds):
                if bound is None:
                    continue
                start, stop = bound
                if start <= col < stop:
                    mask |= 1 << row
                if start <= col_next < stop:
                    mask |= 1 << (row + 4)
            chars.append(charset[mask])
        line = "".join(chars)

    if padding is not None:
        return line.ljust(padding)
    return line


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for the minimap renderer."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Render a Braille minimap of a text file."
    )
    parser.add_argument(
        "file",
        nargs="?",
        help="File to read. Use '-' or omit to read from stdin.",
    )
    parser.add_argument(
        "--hscale",
        "-H",
        type=float,
        default=1.0,
        help="Horizontal scaling factor (default: 1.0).",
    )
    parser.add_argument(
        "--vscale",
        "-V",
        type=float,
        default=1.0,
        help="Vertical scaling factor (default: 1.0).",
    )
    parser.add_argument(
        "--padding",
        "-p",
        type=int,
        default=None,
        help="Pad each output line to this width.",
    )
    parser.add_argument(
        "--octant",
        action="store_true",
        help="Use the octant block character set instead of Braille.",
    )

    args = parser.parse_args()

    if args.hscale < 0:
        parser.error("hscale must be non-negative")
    if args.vscale < 0:
        parser.error("vscale must be non-negative")
    if args.padding is not None and args.padding < 0:
        parser.error("padding must be non-negative")

    return args


def main() -> None:
    """Execute the command-line interface for minimap rendering."""
    import sys

    args = parse_args()
    charset = OCTANTS if args.octant else BRAILLE
    try:
        if args.file is None or args.file == "-":
            output = render(sys.stdin, args.hscale, args.vscale, args.padding, charset)
        else:
            with Path(args.file).open("r", encoding="utf-8", errors="replace") as fh:
                output = render(fh, args.hscale, args.vscale, args.padding, charset)
        print(output)
    except OSError as exc:
        print(f"minimap: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
