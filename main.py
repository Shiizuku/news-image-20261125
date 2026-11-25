#!/usr/bin/env python3
"""Copy the pre-rendered broadsheet (entry.png) to the harness output dir.

Stdlib only. The image is drawn by draw_image.py; this program only copies
it, so the two harness runs write byte-identical output.
"""
import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    os.makedirs(out_dir, exist_ok=True)
    with open(src, "rb") as f:
        digest = hashlib.sha256(f.read()).hexdigest()
    shutil.copyfile(src, dst)
    with open(dst, "rb") as f:
        if hashlib.sha256(f.read()).hexdigest() != digest:
            print("output hash mismatch", file=sys.stderr)
            return 1
    print("entry.png written to", dst, "sha256", digest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
