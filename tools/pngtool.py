#!/usr/bin/env python3
"""Small PNG helpers for tools/render-icons.sh (standard library only).

pngtool.py alpha <on-black.png> <on-white.png> <out.png>
    Recovers a transparent image from two opaque renders of it, one over black and one over
    white: alpha = 1 - (white - black), colour = black / alpha.
pngtool.py ico <out.ico> <png>...
    Packs PNGs (16, 32, 48 px ...) into one .ico, each entry stored as PNG.
"""
import struct
import sys
import zlib


def read_png(path):
    data = open(path, "rb").read()
    assert data[:8] == b"\x89PNG\r\n\x1a\n", path
    pos, idat = 8, b""
    while pos < len(data):
        n, kind = struct.unpack(">I4s", data[pos:pos + 8])
        body = data[pos + 8:pos + 8 + n]
        if kind == b"IHDR":
            w, h, depth, ctype, _, _, interlace = struct.unpack(">IIBBBBB", body)
            assert depth == 8 and ctype in (2, 6) and interlace == 0, (path, depth, ctype)
        elif kind == b"IDAT":
            idat += body
        pos += 12 + n
    bpp = 4 if ctype == 6 else 3
    raw, stride = zlib.decompress(idat), w * bpp
    rows, prev = [], bytearray(stride)
    for y in range(h):
        f = raw[y * (stride + 1)]
        line = bytearray(raw[y * (stride + 1) + 1:(y + 1) * (stride + 1)])
        for i in range(stride):
            a = line[i - bpp] if i >= bpp else 0
            b = prev[i]
            c = prev[i - bpp] if i >= bpp else 0
            if f == 1:
                line[i] = (line[i] + a) & 255
            elif f == 2:
                line[i] = (line[i] + b) & 255
            elif f == 3:
                line[i] = (line[i] + (a + b) // 2) & 255
            elif f == 4:
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                pr = a if pa <= pb and pa <= pc else (b if pb <= pc else c)
                line[i] = (line[i] + pr) & 255
        rows.append(line)
        prev = line
    px = [[tuple(r[x * bpp:x * bpp + 3]) for x in range(w)] for r in rows]
    return w, h, px


def write_png(path, w, h, rgba_rows):
    raw = b"".join(b"\x00" + bytes(r) for r in rgba_rows)

    def chunk(kind, body):
        return struct.pack(">I", len(body)) + kind + body + struct.pack(">I", zlib.crc32(kind + body))

    with open(path, "wb") as out:
        out.write(b"\x89PNG\r\n\x1a\n")
        out.write(chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0)))
        out.write(chunk(b"IDAT", zlib.compress(raw, 9)))
        out.write(chunk(b"IEND", b""))


def alpha(black, white, out):
    w, h, b = read_png(black)
    w2, h2, wh = read_png(white)
    assert (w, h) == (w2, h2)
    rows = []
    for y in range(h):
        row = bytearray()
        for x in range(w):
            bp, wp = b[y][x], wh[y][x]
            a = 255 - round(sum(wp[i] - bp[i] for i in range(3)) / 3)
            a = max(0, min(255, a))
            rgb = [min(255, round(bp[i] * 255 / a)) if a else 0 for i in range(3)]
            row += bytes(rgb + [a])
        rows.append(row)
    write_png(out, w, h, rows)


def ico(out, pngs):
    entries, blobs = [], []
    offset = 6 + 16 * len(pngs)
    for p in pngs:
        data = open(p, "rb").read()
        w, h = struct.unpack(">II", data[16:24])
        entries.append(struct.pack("<BBBBHHII", w % 256, h % 256, 0, 0, 1, 32, len(data), offset))
        blobs.append(data)
        offset += len(data)
    with open(out, "wb") as f:
        f.write(struct.pack("<HHH", 0, 1, len(pngs)) + b"".join(entries) + b"".join(blobs))


if __name__ == "__main__":
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == "alpha":
        alpha(*args)
    elif cmd == "ico":
        ico(args[0], args[1:])
    else:
        sys.exit(__doc__)
