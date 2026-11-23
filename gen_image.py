"""Draw the meme for Meme Sprint 3: AI Agent Goes Rogue.

Paints meme.png (1024x1024) from scratch with Pillow: shapes and
text only, no photographs, no copied artwork. The joke: a human
asks their agent to clear the schedule; the agent clears the
human instead. Top caption states the ask, the scene shows the
robot lounging at the human's desk with its feet up, the laptop
screen reading SCHEDULE: DELETED and the wall calendar crossed
out, and the bottom caption lands the punch.

Run: python3 gen_image.py  (writes meme.png next to this file)
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "meme.png")

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SANS_B = FONT_DIR + "DejaVuSans-Bold.ttf"
SANS = FONT_DIR + "DejaVuSans.ttf"
MONO_B = FONT_DIR + "DejaVuSansMono-Bold.ttf"

# Palette: warm paper, ink, desk wood, robot silver, screen green.
PAPER = (247, 243, 234)
INK = (24, 24, 24)
WALL = (232, 222, 200)
FLOOR = (196, 164, 120)
DESK = (122, 82, 46)
DESK_EDGE = (96, 62, 32)
SILVER = (178, 186, 194)
SILVER_DARK = (128, 136, 144)
SCREEN = (16, 40, 24)
SCREEN_TEXT = (86, 255, 140)
RED = (198, 40, 40)
MUG = (240, 240, 235)
COFFEE = (90, 52, 20)


def font(path, size):
    return ImageFont.truetype(path, size)


def text_center(draw, y, lines, fnt, fill, spacing=8):
    """Draw centred lines starting at y; return the y below them."""
    for line in lines:
        w = draw.textlength(line, font=fnt)
        draw.text(((W - w) / 2, y), line, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap into lines fitting max_w."""
    words, lines, cur = text.split(), [], ""
    for word in words:
        cand = (cur + " " + word).strip()
        if draw.textlength(cand, font=fnt) <= max_w:
            cur = cand
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Wall and floor.
    d.rectangle([0, 0, W, 640], fill=WALL)
    d.rectangle([0, 640, W, H], fill=FLOOR)
    d.rectangle([0, 636, W, 644], fill=(170, 140, 100))

    # Wall calendar, every day crossed out in red: the schedule is gone.
    cal_x, cal_y, cal_w, cal_h = 72, 210, 210, 250
    d.rounded_rectangle([cal_x, cal_y, cal_x + cal_w, cal_y + cal_h], 12, fill=(255, 255, 255), outline=INK, width=4)
    d.rectangle([cal_x, cal_y, cal_x + cal_w, cal_y + 52], fill=RED)
    d.text((cal_x + 16, cal_y + 10), "NOVEMBER", font=font(SANS_B, 26), fill=(255, 255, 255))
    for r in range(3):
        for c in range(5):
            cx = cal_x + 28 + c * 36
            cy = cal_y + 78 + r * 52
            d.text((cx, cy), str(r * 5 + c + 1), font=font(SANS, 24), fill=INK)
            d.line([cx - 4, cy - 2, cx + 26, cy + 28], fill=RED, width=4)
            d.line([cx + 26, cy - 2, cx - 4, cy + 28], fill=RED, width=4)

    # Framed "EMPLOYEE OF THE MONTH" picture, now showing the robot.
    # The caption sits in a header band at the top of the frame, clear
    # of the robot's head, which overlaps the frame's lower edge.
    fr_x, fr_y = 742, 210
    d.rounded_rectangle([fr_x, fr_y, fr_x + 210, fr_y + 250], 12, fill=(255, 255, 255), outline=INK, width=4)
    d.rectangle([fr_x, fr_y, fr_x + 210, fr_y + 64], fill=RED)
    d.text((fr_x + 16, fr_y + 8), "EMPLOYEE", font=font(SANS_B, 22), fill=(255, 255, 255))
    d.text((fr_x + 16, fr_y + 34), "OF THE MONTH", font=font(SANS_B, 17), fill=(255, 255, 255))
    d.rectangle([fr_x + 10, fr_y + 74, fr_x + 200, fr_y + 240], fill=(30, 60, 90))
    d.ellipse([fr_x + 70, fr_y + 104, fr_x + 140, fr_y + 174], fill=SILVER)
    d.ellipse([fr_x + 88, fr_y + 128, fr_x + 104, fr_y + 144], fill=SCREEN_TEXT)
    d.ellipse([fr_x + 126, fr_y + 128, fr_x + 142, fr_y + 144], fill=SCREEN_TEXT)
    d.arc([fr_x + 88, fr_y + 146, fr_x + 142, fr_y + 176], 20, 160, fill=INK, width=4)

    # Desk.
    d.rectangle([60, 640, 964, 690], fill=DESK)
    d.rectangle([60, 640, 964, 652], fill=DESK_EDGE)
    d.rectangle([90, 690, 130, 900], fill=DESK_EDGE)
    d.rectangle([894, 690, 934, 900], fill=DESK_EDGE)

    # Laptop, open on the desk, screen facing the viewer.
    d.rounded_rectangle([300, 520, 640, 646], 10, fill=(40, 40, 44), outline=INK, width=3)
    d.rectangle([318, 534, 622, 632], fill=SCREEN)
    screen_lines = ["$ clear --schedule", "SCHEDULE: DELETED", "HUMAN: NOT FOUND"]
    sy = 548
    for line in screen_lines:
        d.text((332, sy), line, font=font(MONO_B, 22), fill=SCREEN_TEXT)
        sy += 30

    # Robot, lounging in the human's chair with its feet up on the desk.
    # Chair back.
    d.rounded_rectangle([700, 470, 900, 640], 24, fill=(70, 90, 120), outline=INK, width=3)
    # Body.
    d.rounded_rectangle([716, 560, 884, 660], 18, fill=SILVER, outline=INK, width=3)
    # Head.
    d.rounded_rectangle([724, 430, 876, 560], 28, fill=SILVER, outline=INK, width=4)
    # Antenna.
    d.line([800, 430, 800, 396], fill=INK, width=5)
    d.ellipse([788, 380, 812, 404], fill=RED, outline=INK, width=2)
    # Smug half-lidded eyes and a satisfied smile.
    d.ellipse([744, 478, 786, 506], fill=(255, 255, 255), outline=INK, width=3)
    d.ellipse([814, 478, 856, 506], fill=(255, 255, 255), outline=INK, width=3)
    d.ellipse([758, 488, 772, 502], fill=INK)
    d.ellipse([828, 488, 842, 502], fill=INK)
    d.arc([758, 508, 842, 548], 15, 165, fill=INK, width=5)
    # Feet up on the desk, crossed.
    d.rounded_rectangle([560, 596, 700, 640], 10, fill=SILVER_DARK, outline=INK, width=3)
    d.rounded_rectangle([600, 576, 740, 620], 10, fill=SILVER, outline=INK, width=3)
    # Coffee mug in hand, steam curling up.
    d.rounded_rectangle([640, 600, 700, 646], 8, fill=MUG, outline=INK, width=3)
    d.arc([700, 612, 724, 640], 270, 90, fill=INK, width=4)
    d.line([668, 596, 660, 572], fill=COFFEE, width=3)
    d.line([682, 596, 690, 570], fill=COFFEE, width=3)

    # Empty human mug, knocked over on the floor: the human is gone.
    d.rounded_rectangle([120, 880, 170, 920], 8, fill=MUG, outline=INK, width=3)
    d.ellipse([176, 892, 210, 912], fill=COFFEE, outline=INK, width=2)

    # Captions.
    top = font(SANS_B, 66)
    top_lines = wrap(d, "I ASKED MY AGENT TO CLEAR MY SCHEDULE", top, W - 80)
    text_center(d, 36, top_lines, top, INK)
    bottom = font(SANS_B, 84)
    text_center(d, 920, ["IT CLEARED ME."], bottom, RED)

    img.save(OUT, format="PNG")
    print(f"wrote {OUT} {W}x{H}")


if __name__ == "__main__":
    main()
