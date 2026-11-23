"""Meme Sprint 3: AI Agent Goes Rogue — entry for make.fun's
u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6.

Writes one image meme to the harness output directory as
entry.png: a robot lounging at its human's desk, feet up, coffee
in hand, the laptop screen reading SCHEDULE: DELETED. The image
is painted at build time by gen_image.py (Pillow, shapes and
text only, no photographs) and shipped as meme.png; main.py
checks it against the competition's caps (a whole PNG, at most
1 MiB, at most 1024x1024 pixels) and copies it to the output.
The image is a fixed file, so two runs produce identical bytes.
"""

import hashlib
import os
import shutil

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "meme.png")

MAX_BYTES = 1024 * 1024
MAX_DIM = 1024


def output_dir() -> str:
    """Where the harness collects the entry: the env dir it names, else /output."""
    return (
        os.environ.get("MAKEFUN_OUTPUT_DIR")
        or os.environ.get("MAKEFUN_OUTPUT")
        or "/output"
    )


def main() -> None:
    from PIL import Image

    with Image.open(SRC) as im:
        im.verify()
    with Image.open(SRC) as im:
        assert im.format == "PNG", f"meme must be PNG, got {im.format}"
        w, h = im.size
        assert w <= MAX_DIM and h <= MAX_DIM, f"meme is {w}x{h}, over the {MAX_DIM}x{MAX_DIM} cap"
    size = os.path.getsize(SRC)
    assert size <= MAX_BYTES, f"meme is {size} bytes, over the 1 MiB cap"
    out = os.path.join(output_dir(), "entry.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    shutil.copyfile(SRC, out)
    # The copy must be the file that was checked: same bytes, no surprises.
    src_sha = hashlib.sha256(open(SRC, "rb").read()).hexdigest()
    out_sha = hashlib.sha256(open(out, "rb").read()).hexdigest()
    assert src_sha == out_sha, "entry.png differs from the checked meme.png"
    print(f"wrote {w}x{h} PNG ({size} bytes) to {out}")


if __name__ == "__main__":
    main()
