import csv
import struct
import zlib
from pathlib import Path

from config import DATA_PROCESSED, OUTPUTS_FIGURES


STATUS_COLORS = {
    "Likely usable": (33, 131, 104),
    "Marginal": (213, 142, 53),
    "Below threshold": (181, 72, 66),
}
BG = (248, 250, 252)
INK = (28, 40, 51)
MUTED = (105, 118, 132)


FONT = {
    "0": ["111", "101", "101", "101", "111"], "1": ["010", "110", "010", "010", "111"],
    "2": ["111", "001", "111", "100", "111"], "3": ["111", "001", "111", "001", "111"],
    "4": ["101", "101", "111", "001", "001"], "5": ["111", "100", "111", "001", "111"],
    "6": ["111", "100", "111", "101", "111"], "7": ["111", "001", "010", "010", "010"],
    "8": ["111", "101", "111", "101", "111"], "9": ["111", "101", "111", "001", "111"],
    "-": ["000", "000", "111", "000", "000"], ".": ["000", "000", "000", "000", "010"],
    " ": ["000", "000", "000", "000", "000"], "A": ["010", "101", "111", "101", "101"],
    "B": ["110", "101", "110", "101", "110"], "C": ["111", "100", "100", "100", "111"],
    "D": ["110", "101", "101", "101", "110"], "E": ["111", "100", "110", "100", "111"],
    "F": ["111", "100", "110", "100", "100"], "G": ["111", "100", "101", "101", "111"],
    "H": ["101", "101", "111", "101", "101"], "I": ["111", "010", "010", "010", "111"],
    "J": ["001", "001", "001", "101", "111"], "K": ["101", "101", "110", "101", "101"],
    "L": ["100", "100", "100", "100", "111"], "M": ["101", "111", "111", "101", "101"],
    "N": ["101", "111", "111", "111", "101"], "O": ["111", "101", "101", "101", "111"],
    "P": ["111", "101", "111", "100", "100"], "Q": ["111", "101", "101", "111", "001"],
    "R": ["111", "101", "111", "110", "101"], "S": ["111", "100", "111", "001", "111"],
    "T": ["111", "010", "010", "010", "010"], "U": ["101", "101", "101", "101", "111"],
    "V": ["101", "101", "101", "101", "010"], "W": ["101", "101", "111", "111", "101"],
    "X": ["101", "101", "010", "101", "101"], "Y": ["101", "101", "010", "010", "010"],
    "Z": ["111", "001", "010", "100", "111"],
}


def read_rows() -> list[dict]:
    with (DATA_PROCESSED / "launch_status.csv").open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def rect(pixels, width, height, x0, y0, x1, y1, color):
    for y in range(max(0, y0), min(height, y1)):
        for x in range(max(0, x0), min(width, x1)):
            pixels[y * width + x] = color


def text(pixels, width, height, x, y, value, color=INK, scale=2):
    cx = x
    for char in value.upper():
        pattern = FONT.get(char, FONT[" "])
        for row_idx, row in enumerate(pattern):
            for col_idx, bit in enumerate(row):
                if bit == "1":
                    rect(pixels, width, height, cx + col_idx * scale, y + row_idx * scale, cx + (col_idx + 1) * scale, y + (row_idx + 1) * scale, color)
        cx += 4 * scale


def save_png(path: Path, width: int, height: int, pixels: list[tuple[int, int, int]]) -> None:
    raw = bytearray()
    for y in range(height):
        raw.append(0)
        for x in range(width):
            raw.extend(pixels[y * width + x])

    def chunk(kind, data):
        body = kind + data
        return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += chunk(b"IEND", b"")
    path.write_bytes(png)


def main() -> Path:
    rows = read_rows()
    width, height = 1400, 820
    pixels = [BG] * (width * height)
    text(pixels, width, height, 48, 36, "Lake Roosevelt launch margin ft", INK, 4)
    text(pixels, width, height, 50, 92, "Positive margin means lake elevation is above NPS threshold", MUTED, 2)
    zero_x = 1030
    top = 140
    bar_h = 22
    gap = 12
    max_abs = max(abs(float(row["margin_ft"])) for row in rows) or 1
    scale = 620 / max_abs
    rect(pixels, width, height, zero_x - 1, top - 20, zero_x + 1, height - 62, (180, 190, 200))
    for idx, row in enumerate(rows):
        y = top + idx * (bar_h + gap)
        margin = float(row["margin_ft"])
        text(pixels, width, height, 52, y + 4, row["launch_name"][:24], INK, 2)
        color = STATUS_COLORS[row["status"]]
        if margin >= 0:
            rect(pixels, width, height, zero_x, y, zero_x + int(margin * scale), y + bar_h, color)
        else:
            rect(pixels, width, height, zero_x + int(margin * scale), y, zero_x, y + bar_h, color)
        text(pixels, width, height, 1080, y + 4, f"{margin:.1f}", INK, 2)
        text(pixels, width, height, 1180, y + 4, row["status"][:14], color, 2)
    OUTPUTS_FIGURES.mkdir(parents=True, exist_ok=True)
    path = OUTPUTS_FIGURES / "launch_status_chart.png"
    save_png(path, width, height, pixels)
    return path


if __name__ == "__main__":
    print(f"Wrote {main()}")

