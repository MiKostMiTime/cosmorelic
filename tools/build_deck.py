"""Build cosmorelic_deck.pptx — the seven-slide submission deck (PRD §7, SRS §9.9).

BUILD-TIME TOOL ONLY. `python-pptx` is used once to write the deck file; it is
deliberately NOT part of the app. The running application still needs only
gradio, openai, requests and python-dotenv, exactly as SRS §2 says.

Run:  .venv/bin/python tools/build_deck.py
Out:  deck/cosmorelic_deck.pptx

Design rules enforced here:
  - exactly seven slides, count checked before the file is written
  - 16:9, English only
  - no NASA logo, mission patch or flag anywhere
  - no AI-generated imagery; the only photograph is the app screenshot,
    which shows NASA archival hardware photographs, already credited in-app
  - no image of any person
  - Arial, so the file looks identical in PowerPoint, Google Slides and the
    LibreOffice render used to check it (Helvetica Neue falls back to a serif
    on machines that do not have it)
"""

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE, PP_ALIGN
from pptx.util import Emu, Inches, Pt

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "deck"
OUT_FILE = OUT_DIR / "cosmorelic_deck.pptx"
SHOT = ROOT / "screenshots" / "app_hero.png"

# --- the two things only the author can supply ---------------------------------
FILL_TEAM = "TEAM NAME - add your team name and members here"
FILL_LINK = "LIVE DEMO - paste your hosted link here"

# --- design tokens --------------------------------------------------------------
W, H = 13.333, 7.5           # inches, 16:9
MARGIN = 0.85
GUTTER = W - 2 * MARGIN      # 11.633
FONT = "Arial"

BG = RGBColor(0x0B, 0x10, 0x24)     # deep navy
CARD = RGBColor(0x16, 0x1D, 0x38)   # raised panel
INK = RGBColor(0xFF, 0xFF, 0xFF)    # headings
BODY = RGBColor(0xC3, 0xCC, 0xDE)   # body copy
MUTED = RGBColor(0x84, 0x91, 0xAB)  # captions, footers
ACCENT = RGBColor(0x7A, 0x9C, 0xFF)  # the one accent colour

TIER_COLORS = {
    "MEASURED": RGBColor(0x4A, 0xDE, 0x80),
    "EPHEMERIS": RGBColor(0x60, 0xA5, 0xFA),
    "DERIVED": RGBColor(0xFB, 0x92, 0x3C),
    "ARCHIVAL": RGBColor(0x9C, 0xA3, 0xAF),
}


# --- primitives -----------------------------------------------------------------
def blank(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    plate = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Emu(int(W * 914400)), Emu(int(H * 914400)))
    plate.fill.solid()
    plate.fill.fore_color.rgb = BG
    plate.line.fill.background()
    plate.shadow.inherit = False
    return s


def text(slide, l, t, w, h, runs, size=18, color=BODY, bold=False, italic=False,
         align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, space_after=0, line=None):
    """One paragraph of possibly-mixed runs. `runs` is a str or [(text, color, bold, size)]."""
    box = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.vertical_anchor = anchor
    p = tf.paragraphs[0]
    p.alignment = align
    if space_after:
        p.space_after = Pt(space_after)
    if line:
        p.line_spacing = line
    items = [(runs, color, bold, size)] if isinstance(runs, str) else runs
    for txt, col, bd, sz in items:
        r = p.add_run()
        r.text = txt
        r.font.name = FONT
        r.font.size = Pt(sz)
        r.font.bold = bd
        r.font.italic = italic
        r.font.color.rgb = col
    return box


def bullets(slide, l, t, w, h, items, size=18, gap=15, color=BODY, marker="\u2022  "):
    box = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.space_after = Pt(gap)
        m = p.add_run()
        m.text = marker
        m.font.name = FONT
        m.font.size = Pt(size)
        m.font.bold = True
        m.font.color.rgb = ACCENT
        r = p.add_run()
        r.text = item
        r.font.name = FONT
        r.font.size = Pt(size)
        r.font.color.rgb = color
    return box


def rule(slide, l, t, w=1.5, h=0.055, color=ACCENT):
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(l), Inches(t), Inches(w), Inches(h))
    bar.fill.solid()
    bar.fill.fore_color.rgb = color
    bar.line.fill.background()
    bar.shadow.inherit = False
    return bar


def card(slide, l, t, w, h, fill=CARD):
    s = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(l), Inches(t), Inches(w), Inches(h))
    s.adjustments[0] = 0.06
    s.fill.solid()
    s.fill.fore_color.rgb = fill
    s.line.fill.background()
    s.shadow.inherit = False
    s.text_frame.word_wrap = True
    return s


def chrome(slide, index):
    """Wordmark top-left and page number bottom-right. No NASA insignia anywhere."""
    text(slide, MARGIN, 0.42, 4.0, 0.3, "COSMORELIC", size=11, color=ACCENT, bold=True)
    text(slide, W - MARGIN - 2.0, H - 0.58, 2.0, 0.3, f"{index} / 7", size=11, color=MUTED, align=PP_ALIGN.RIGHT)


def heading(slide, title_text, lines=1, size=32):
    """Title plus its accent rule. `lines` must match the number of lines the title
    actually renders as, otherwise the rule strikes through the second line."""
    box_h = (size * 1.22 / 72) * lines
    text(slide, MARGIN, 0.96, GUTTER, box_h, title_text, size=size, color=INK, bold=True, line=1.0)
    ry = 0.96 + box_h + 0.16
    rule(slide, MARGIN, ry)
    return ry + 0.26


def callout(slide, t, lines, title, size=15):
    """A bottom-of-slide panel holding one or two lines of supporting text."""
    h = 0.34 + 0.30 * lines
    body = card(slide, MARGIN, t, GUTTER, h)
    rule(slide, MARGIN + 0.02, t + 0.16, w=0.06, h=h - 0.32, color=ACCENT)
    tf = body.text_frame
    tf.margin_left = Inches(0.34)
    tf.margin_right = Inches(0.3)
    tf.margin_top = Inches(0.12)
    tf.margin_bottom = Inches(0.10)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    for i, row in enumerate(title):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.space_after = Pt(4)
        items = row if isinstance(row, list) else [(row, BODY, False, size)]
        for txt, col, bd, sz in items:
            r = p.add_run()
            r.text = txt
            r.font.name = FONT
            r.font.size = Pt(sz)
            r.font.bold = bd
            r.font.color.rgb = col
    return t + h


# --- content --------------------------------------------------------------------
def slide_1(prs):
    s = blank(prs)
    text(s, MARGIN, 0.42, 6.0, 0.3, "COSMORELIC", size=11, color=ACCENT, bold=True)

    text(s, MARGIN, 1.16, 11.0, 1.35, "CosmoRelic", size=64, color=INK, bold=True, line=0.95)
    text(s, MARGIN, 2.50, 11.0, 0.5, "Abandoned, but not forgotten.", size=25, color=ACCENT)
    text(
        s, MARGIN, 3.16, 10.2, 0.9,
        "Eight machines left behind on the Moon and Mars tell their own story \u2014 "
        "with every number labelled by how we know it.",
        size=17, color=BODY, line=1.25,
    )

    rule(s, MARGIN, 4.34, w=GUTTER, h=0.02, color=RGBColor(0x2A, 0x33, 0x52))

    text(s, MARGIN, 4.60, GUTTER, 0.35,
         "NASA Space Apps Challenge 2026  \u00b7  Challenge 01", size=15, color=INK, bold=True)
    text(
        s, MARGIN, 4.98, 10.8, 0.5,
        "Abandoned but not Forgotten: Storytelling about NASA's Discarded Equipment on the Moon and Mars",
        size=12.5, color=MUTED, italic=True,
    )

    text(s, MARGIN, 6.06, GUTTER, 0.4, FILL_TEAM, size=15, color=ACCENT, bold=True)
    text(s, W - MARGIN - 2.0, H - 0.58, 2.0, 0.3, "1 / 7", size=11, color=MUTED, align=PP_ALIGN.RIGHT)
    return s


def slide_2(prs):
    s = blank(prs)
    chrome(s, 2)
    top = heading(s, "The missions that ended are the ones\nnobody tells them about", lines=2, size=30)
    bullets(
        s, MARGIN, top, 11.3, 3.2,
        [
            "School-age space enthusiasts hear about what is flying now \u2014 Artemis, Perseverance, the James Webb Space Telescope.",
            "The machines that finished are in catalogs, not in classrooms. Almost nothing about them is written for a 12-year-old.",
            "Eight of them are on NASA's own list for this challenge. The history is documented. The voice is missing.",
        ],
        size=18, gap=20,
    )
    callout(s, 5.82, 1, [[("For students aged 10\u201314 ", MUTED, True, 13),
                          ("\u2014 in a classroom, with no account and no setup required.", MUTED, False, 13)]])
    return s


def slide_3(prs):
    s = blank(prs)
    chrome(s, 3)
    top = heading(s, "So we let them speak")
    bullets(
        s, MARGIN, top, 11.3, 1.9,
        [
            "Eight relics. One question each: what happened to you?",
            "All eight map to the 14 resources named in this challenge \u2014 none from outside the list.",
            "No internet, no API key, no sign-up. It runs from archived memory when the network is gone.",
        ],
        size=18, gap=16,
    )

    strip = card(s, MARGIN, 4.14, GUTTER, 1.76)
    tf = strip.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.36)
    tf.margin_right = Inches(0.36)
    tf.margin_top = Inches(0.20)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE

    def row(index, label, value, gap_after):
        p = tf.paragraphs[0] if index == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.space_after = Pt(gap_after)
        a = p.add_run()
        a.text = label
        a.font.name = FONT
        a.font.size = Pt(15)
        a.font.bold = True
        a.font.color.rgb = INK
        b = p.add_run()
        b.text = value
        b.font.name = FONT
        b.font.size = Pt(15)
        b.font.color.rgb = BODY

    row(0, "Moon      ", "Eagle (Apollo 11)  \u00b7  Challenger (Apollo 17)", 10)
    row(1, "Mars       ", "Ingenuity  \u00b7  Viking 1  \u00b7  Sojourner  \u00b7  Spirit  \u00b7  Opportunity  \u00b7  InSight", 10)
    row(2, "Photos    ", "NASA archival photographs, credited exactly as published", 0)
    return s


def slide_4(prs):
    s = blank(prs)
    chrome(s, 4)
    top = heading(s, "Every number says how we know it")

    tiers = [
        ("MEASURED", "Where the machine sits.\nRead from NASA's landing-site records."),
        ("EPHEMERIS", "Live from JPL Horizons.\nNever older than 15 minutes."),
        ("DERIVED", "Arithmetic on a dated fact,\ndone by our own code."),
        ("ARCHIVAL", "Read from a mission record.\nFixed. Never a guess."),
    ]
    cw, gap = 2.72, 0.28
    for i, (name, desc) in enumerate(tiers):
        l = MARGIN + i * (cw + gap)
        card(s, l, top, cw, 2.05)
        rule(s, l + 0.24, top + 0.24, w=0.5, h=0.05, color=TIER_COLORS[name])
        text(s, l + 0.24, top + 0.42, cw - 0.48, 0.3, name, size=12.5, color=TIER_COLORS[name], bold=True)
        text(s, l + 0.24, top + 0.80, cw - 0.48, 1.05, desc, size=12, color=BODY, line=1.2)

    bullets(
        s, MARGIN, top + 2.40, 11.3, 2.0,
        [
            "The AI receives a closed list of numbers and nothing else. It cannot state a number we did not hand it.",
            "\u201cWhat is the temperature there right now?\u201d  \u2192  \u201cI have no working instruments.\u201d",
            "\u201cDid your mole reach five metres?\u201d  \u2192  \u201cIt stopped around 40 cm.\u201d",
        ],
        size=16, gap=14,
    )
    callout(s, 6.12, 1, [[("If a value cannot be labelled, it does not go on the card.", INK, True, 14)]])
    return s


def slide_5(prs):
    s = blank(prs)
    chrome(s, 5)
    top = heading(s, "Ask a machine what happened")

    img_h = 4.46
    img_w = img_h * (1440 / 1550)
    s.shapes.add_picture(str(SHOT), Inches(MARGIN), Inches(top), height=Inches(img_h))
    text(s, MARGIN, top + img_h + 0.14, img_w, 0.3,
         "The running app. Archival photograph credited in the interface.", size=10, color=MUTED)

    lx = MARGIN + img_w + 0.55
    lw = W - MARGIN - lx
    bullets(
        s, lx, top + 0.04, lw, 3.4,
        [
            "The live Earth\u2013Mars distance comes from JPL Horizons and is badged EPHEMERIS.",
            "How long a machine has been silent is DERIVED \u2014 computed from its recorded last-contact date, so it updates itself.",
            "Switch the network off and the live row becomes a clearly labelled ARCHIVAL range. Nothing is invented.",
        ],
        size=15, gap=18,
    )
    text(s, lx, 5.98, lw, 0.4, "Try it:", size=14, color=ACCENT, bold=True)
    text(s, lx, 6.32, lw, 0.7, FILL_LINK, size=14, color=INK, bold=True)
    return s


def slide_6(prs):
    s = blank(prs)
    chrome(s, 6)
    t = heading(s, "Where the data comes from, and where it stops", size=30)

    blocks = [
        ("NASA data used", [
            "NSSDCA Master Catalog and landing-site coordinates",
            "JPL Horizons for the live Earth\u2013Moon and Earth\u2013Mars distance",
            "NASA GISS Mars24 for Mars landing coordinates",
            "NASA Image and Video Library for the archival photographs",
        ]),
        ("Limits we state ourselves", [
            "The voice is an AI storyteller, not the spacecraft, and it says so",
            "Coordinates are landing sites, not the current position of debris",
            "Low-power mode shows an archival range, clearly labelled as such",
        ]),
        ("Disclosure", [
            "gpt-oss-20b on Groq writes the dialogue only, from a closed list of numbers",
            "No AI-generated images: NASA archival photography, credited exactly as published",
            "Not affiliated with or endorsed by NASA",
        ]),
    ]
    for name, items in blocks:
        text(s, MARGIN, t, 5.0, 0.3, name, size=13.5, color=ACCENT, bold=True)
        bullets(s, MARGIN, t + 0.33, 11.2, 0.32 * len(items), items,
                size=13, gap=6, color=BODY, marker="\u2013  ")
        t += 0.33 + 0.30 * len(items) + 0.30
    return s


def slide_7(prs):
    s = blank(prs)
    chrome(s, 7)
    top = heading(s, "Built for a classroom, not a conference")
    bullets(
        s, MARGIN, top, 11.3, 2.6,
        [
            "Free. No login. Nothing for a student to install.",
            "A teacher box is built in \u2014 guided questions, no lesson preparation needed.",
            "Next: the remaining families on the challenge list \u2014 Surveyor, ALSEP, Dawn, NEAR Shoemaker, Pioneer 10/11, Kepler.",
        ],
        size=18, gap=18,
    )

    panel = card(s, MARGIN, 4.72, GUTTER, 1.92)
    tf = panel.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.40)
    tf.margin_top = Inches(0.22)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE

    def r(row_index, run_list):
        p = tf.paragraphs[0] if row_index == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        for txt, col, bd, sz in run_list:
            run = p.add_run()
            run.text = txt
            run.font.name = FONT
            run.font.size = Pt(sz)
            run.font.bold = bd
            run.font.color.rgb = col

    r(0, [("Thank you.", INK, True, 26)])
    tf.paragraphs[0].space_after = Pt(10)
    r(1, [("Try it:  ", ACCENT, True, 14), (FILL_LINK, INK, True, 14)])
    tf.paragraphs[1].space_after = Pt(8)
    r(2, [("CosmoRelic \u2014 NASA Space Apps Challenge 2026, Challenge 01", MUTED, False, 11.5)])
    return s


# --- build ----------------------------------------------------------------------
def build():
    prs = Presentation()
    prs.slide_width = Emu(int(W * 914400))
    prs.slide_height = Emu(int(H * 914400))

    builders = [slide_1, slide_2, slide_3, slide_4, slide_5, slide_6, slide_7]
    for b in builders:
        b(prs)

    count = len(prs.slides._sldIdLst)
    if count != 7:
        raise SystemExit(f"refusing to write: expected exactly 7 slides, built {count}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    prs.save(str(OUT_FILE))

    size_kb = OUT_FILE.stat().st_size / 1024
    print(f"wrote {OUT_FILE.relative_to(ROOT)}  ({count} slides, {size_kb:.0f} KB)")
    print()
    print("two places still need your input (both marked in the deck):")
    print(f"  slide 1        ->  {FILL_TEAM}")
    print(f"  slide 5 and 7  ->  {FILL_LINK}")


if __name__ == "__main__":
    build()
