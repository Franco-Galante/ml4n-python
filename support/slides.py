"""Reusable slide furniture.

Kept out of the lecture files because edtrace shows the traced module's source
in the viewer, and this markup would drown the lecture itself.

Everything here is presentation only: no lecture-specific content, no heavy
dependencies.  Copy this file into your own course and edit the palette at the
top; the lectures that import it need no change.
"""

import ast
import hashlib
import html
import inspect
import os
import re
import struct
import textwrap

from edtrace import image, text, video

# ---------------------------------------------------------------- palette --
# One accent blue, one ink, one muted grey, one hairline, one stripe.  Every
# style below is built out of these five, so recolouring the deck is a
# five-line edit rather than a search-and-replace.
ACCENT = "#2563eb"
INK = "#1f3550"
MUTED = "#5b6b7f"
HAIRLINE = "#dbe4ee"
STRIPE = "#f5f9fd"

# ----------------------------------------------------------------- rhythm --
# The viewer's stylesheet sets line-height 1.5 on :root and zeroes the margins
# of every heading, which reads as one dense column on a projector.  A lecture
# calls theme() once from its first function to override that from the course
# side: patching the vendored frontend would be undone by the next submodule
# update, and a per-call style cannot reach the many text() calls that pass no
# style dict.  The rendering is an invisible <style> element, so the line it
# sits on shows nothing - it must not be @hide-d, because the viewer drops the
# renderings of hidden lines along with the line.
THEME_CSS = """
.line { line-height: 1.85; font-size: 17px; }
/* Fluid, not fixed: the viewer ships an 800px column sized to fit an A4 page.
   A wider fixed width is clipped by the PDF exporter, so the column grows with
   the window up to max-width and shrinks to the printable width on paper.
   The panel's own 1000px min-width has to go, or it forces the overflow back. */
/* One row = [line number][content]. Laying it out as flex lets the content
   fill the column instead of shrinking to fit, so prose, figures, tables, code
   blocks and callouts all share the same left and right edges.  The indent
   spacer in front of a rendering is dropped: as a block it would otherwise
   push every rendering onto the line below its own line number. */
.line { display: flex; align-items: flex-start; }
.line > span:last-child { flex: 1 1 auto; min-width: 0; }
.line-number { flex: 0 0 auto; }
.code-container:has(+ .renderings) { display: none; }
.renderings { line-height: 1.85; display: block; width: auto; max-width: 1080px; }
.lines-panel { min-width: 0; }
/* The variable panel: the viewer draws values in the bare `monospace` font,
   which browsers render at ~13px whatever the page size.  A real font stack
   lifts that quirk; the panel may grow wider so longer values wrap less. */
.env { font-size: 19px; min-width: 0; max-width: 720px; }
.env .code-container { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 1em; }
/* Numpy arrays reach the panel as <table class="matrix">: monospace and right
   aligned, so the columns line up the way an array printout does. */
.env .matrix > tbody > tr > td { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; text-align: right; padding: 3px 8px; border-color: #dbe4ee; }
/* The panel sizes to its content (up to max-width): no stretched gaps between a name, "=" and its value. */
.env > tbody > tr > td:nth-child(-n+2) { white-space: nowrap; padding-right: 0.5em; }
/* The lecture's own executed lines: the same tinted box as a code_block, so
   every piece of code reads alike.  Consecutive lines join into one band; a
   blank source line breaks it, which is how a demo separates from the next.
   Only the code column is painted: the line number stays outside it, and the
   indent spacer of a rendering line is already display:none. */
/* A code line is one whose code span is the *last* child: in a rendering line
   that span is only the indent spacer, followed by the rendering itself.
   (:has cannot be nested inside :has, so this is the signal to key off.) */
.line > span:last-child > .code-container:last-child:not(:empty) { display: block; background: #f5f9fd; border-left: 3px solid #dbe4ee; padding: 1px 0 1px 14px; }
/* The yellow cursor must stay on top of the band, not under it. */
.line.current-line > span:last-child > .code-container:last-child { background: #FFFFCC; }
/* Breathing room around a run of code lines: after the last line of the run,
   and before the first one - written as space under the prose line above it,
   because CSS cannot look at a previous sibling. */
.line:has(> span:last-child > .code-container:last-child:not(:empty)):has(+ .line .renderings) { margin-bottom: 22px; }
.line:has(.renderings):has(+ .line > span:last-child > .code-container:last-child:not(:empty)) { margin-bottom: 18px; }
/* Inline code (`backticks` in text) as a tinted chip, like GitHub's markdown.
   Semi-transparent, so it still stands out inside the light-blue callouts. */
.markdown code { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 0.88em; color: #1f3550; background: rgba(110, 130, 155, 0.14); border: 1px solid rgba(110, 130, 155, 0.22); border-radius: 5px; padding: 0.06em 0.38em; text-transform: none; letter-spacing: normal; -webkit-box-decoration-break: clone; box-decoration-break: clone; }
.markdown h1 { margin-top: 38px; margin-bottom: 10px; }
.markdown h2 { margin-top: 8px; margin-bottom: 8px; }
.notes { line-height: 1.6; margin-top: 8px; margin-bottom: 8px; }
"""


# Keeping the current step near the middle of the window.  The viewer scrolls
# only once the current line has left the window, so the text sits still and
# then jumps.  A <style> cannot scroll and the viewer is a submodule we do not
# patch, so the page installs a small observer instead: a <script> inserted as
# innerHTML never runs, but an inline event handler does, so it rides on the
# onload of a 1x1 transparent GIF.  It recentres after each re-render, and only
# when the line has drifted, so stepping inside one screenful stays calm.
_BLANK_GIF = "data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=="

def _centre_script(drift: int) -> str:
    """The inline handler, built by concatenation: its JavaScript is full of braces."""
    return (
        "if(!window.__edtraceCentre){window.__edtraceCentre=1;let q=false;"
        "const c=()=>{q=false;const e=document.querySelector('.current-line');if(!e)return;"
        "const r=e.getBoundingClientRect();"
        "if(Math.abs((r.top+r.bottom)/2-innerHeight/2)>" + str(drift) + ")e.scrollIntoView({block:'center',behavior:'auto'});};"
        "const s=()=>{if(!q){q=true;requestAnimationFrame(c);}};"
        "new MutationObserver(s).observe(document.body,{subtree:true,childList:true,attributes:true,attributeFilter:['class']});s();}"
    )


def _python_repr_script() -> str:
    """Show a string on the panel the way Python writes it, not the way JSON does.

    The viewer renders anything it has no special case for with
    JSON.stringify, so `He said "yes"` arrives on the panel as an escaped
    `He said \"yes\"`.  Patching the vendored viewer would be undone by the
    next submodule update, so the page repairs the cell itself, on the same
    MutationObserver idea as the centring above: a string whose only awkward
    character is the double quote is re-quoted with single quotes, which is
    exactly how its literal was written in the lecture.  A string carrying a
    backslash or a control character (`skip\n`) is left alone, because there
    the escaping is the information.

    The JavaScript never contains a double quote of its own (the character is
    built with String.fromCharCode), so it survives inside the onload="..."
    attribute untouched.
    """
    return (
        "if(!window.__edtracePyRepr){window.__edtracePyRepr=1;let p=false;"
        "const Q=String.fromCharCode(34),A=String.fromCharCode(39);"
        "const f=()=>{p=false;document.querySelectorAll('table.env td').forEach(d=>{"
        "if(d.children.length)return;const t=d.textContent;"
        "if(t.length<2||t[0]!==Q||t[t.length-1]!==Q)return;"
        "let v;try{v=JSON.parse(t);}catch(e){return;}"
        "if(typeof v!=='string'||v.indexOf(Q)<0||v.indexOf(A)>=0)return;"
        "if(v.indexOf(String.fromCharCode(92))>=0||/[\\x00-\\x1f]/.test(v))return;"
        "d.textContent=A+v+A;});};"
        "const o=()=>{if(!p){p=true;requestAnimationFrame(f);}};"
        "new MutationObserver(o).observe(document.body,{subtree:true,childList:true,characterData:true});o();}"
    )


def _panel_order_script() -> str:
    """List the variables on the panel in the order they were put there.

    The viewer merges the env of every earlier step of the current function
    with Object.assign, and Object.assign keeps a key where it was *first*
    seen - so a name that was used, cleared and used again in the same section
    keeps its original slot and floats above the variables it is built from.
    The page fixes the order itself: a name that is on the panel gets a
    sequence number the first time it appears, loses it when it leaves the
    panel (i.e. when @clear removes it), and takes a fresh one when it comes
    back.  Sorting the rows by that number gives the order of the code.

    Stepping forward is what the numbers are built from, so a reload in the
    middle of a lecture simply falls back to the viewer's own order.
    """
    return (
        "if(!window.__edtracePanelOrder){window.__edtracePanelOrder=1;"
        "let n=0,rank=new Map(),w=false;"
        "const f=()=>{w=false;const b=document.querySelector('table.env > tbody');"
        "if(!b){rank.clear();return;}"
        "const rows=Array.from(b.children);"
        "const name=r=>r.children[0]?r.children[0].textContent:'';"
        "const live=new Set(rows.map(name));"
        "Array.from(rank.keys()).forEach(k=>{if(!live.has(k))rank.delete(k);});"
        "rows.forEach(r=>{const k=name(r);if(!rank.has(k))rank.set(k,n++);});"
        "const sorted=rows.slice().sort((x,y)=>rank.get(name(x))-rank.get(name(y)));"
        "for(let i=0;i<sorted.length;i++){if(sorted[i]!==rows[i]){sorted.forEach(r=>b.appendChild(r));break;}}};"
        "const o=()=>{if(!w){w=true;requestAnimationFrame(f);}};"
        "new MutationObserver(o).observe(document.body,{subtree:true,childList:true,characterData:true});o();}"
    )


def theme(css: str = THEME_CSS, centre_current_line: bool = True, drift: int = 60) -> None:
    """Set the vertical rhythm of the whole page. Call once, early in the lecture.

    Also switches the code band off on the lecture's structural lines - the
    module docstring, the imports, the `def` headers and main()'s list of
    sections - so a boxed line means "code presented to the class".

    With `centre_current_line`, the current step is kept around the middle of
    the window while stepping; `drift` is how far (in pixels) it may wander
    from the centre before the page scrolls again.
    """
    scripts = (_centre_script(drift) if centre_current_line else "") + _python_repr_script() + _panel_order_script()
    centre = f'<img src="{_BLANK_GIF}" alt="" style="display:none" onload="{scripts}">'
    # The call renders nothing visible, so its own line would show as a blank
    # row under `def title():`.  It cannot be @hide-d (the viewer drops the
    # renderings of hidden lines with the line, and the style is the point), so
    # the line is collapsed from the inside: the marker below is what the rule
    # in _THEME_LINE_CSS matches.  The <style> keeps working and the 1x1 GIF
    # still fires its onload, because height:0 does not stop either of them.
    text(f"<style>{css}{_plain_line_rules(inspect.stack()[1].filename)}{_THEME_LINE_CSS}</style>{centre}<span class=\"theme-line\"></span>")


_THEME_LINE_CSS = ".line:has(.theme-line){height:0;overflow:hidden;}"


def _plain_line_rules(path: str) -> str:
    """CSS switching the code band off on a lecture's scaffolding lines.

    The viewer has no idea what a line means, and CSS cannot match on text, so
    the lines are found here with `ast` and addressed by position.  The viewer
    renders the trimmed file and skips @hide-den lines, so line numbers are
    mapped to the positions that actually reach the DOM; the rules are rebuilt
    at every run, hence they follow the file as it is edited.
    """
    try:
        with open(path, encoding="utf-8") as handle:
            source = handle.read()
        tree = ast.parse(source)
    except (OSError, SyntaxError):
        return ""

    plain: set[int] = set()
    for node in tree.body:
        start = min([node.lineno] + [decorator.lineno for decorator in getattr(node, "decorator_list", [])])
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            plain.update(range(start, node.body[0].lineno))  # the def header only...
            if node.name == "main":
                plain.update(range(start, node.end_lineno + 1))  # ...but all of main()
        else:
            plain.update(range(start, node.end_lineno + 1))  # docstring, imports, constants

    lines = source.split("\n")
    leading = 0
    while leading < len(lines) and not lines[leading].strip():
        leading += 1  # the viewer trims the file before splitting it

    position, selectors = 0, []
    for number, line in enumerate(lines[leading:], start=leading + 1):
        if re.search(r"#.*@hide", line):
            continue  # hidden lines never reach the DOM
        position += 1
        if number in plain:
            # Mirrors the band selector exactly, plus :nth-child, so it is the
            # more specific of the two and wins.
            selectors.append(f".line:nth-child({position}) > span:last-child > .code-container:last-child:not(:empty)")
    return f"{','.join(selectors)}{{background:none;border-left:0;padding-left:0;}}" if selectors else ""


# Figures: capped width so a tall diagram does not dominate the slide, centred
# with a soft frame so it reads as a figure rather than an inline screenshot.
FIGURE = {
    "display": "block",
    "width": "620px",
    "maxWidth": "100%",
    "margin": "18px auto 4px auto",
    "borderRadius": "12px",
    "border": f"1px solid {HAIRLINE}",
    "boxShadow": "0 2px 12px rgba(15, 40, 80, 0.10)",
}

# The figure frame spans the content column; the media inside it is centred and
# capped, so every figure has the same left and right edges as the prose.
FIGURE_FRAME = {
    "display": "block",
    "width": "100%",
    "boxSizing": "border-box",
    "margin": "18px 0 4px 0",
    "padding": "12px",
    "background": "#ffffff",
    "borderRadius": "12px",
    "border": f"1px solid {HAIRLINE}",
    "boxShadow": "0 2px 12px rgba(15, 40, 80, 0.10)",
}

MEDIA = {"display": "block", "margin": "0 auto", "height": "auto"}

# Space between a figure (or its caption) and whatever follows it.
FIGURE_GAP_AFTER = "30px"

CAPTION = {
    "display": "block",
    "textAlign": "center",
    "fontSize": "15px",
    "color": MUTED,
    "margin": "0 auto 18px auto",
    "maxWidth": "100%",
    "lineHeight": "1.45",
}

# Callout box for the take-away line: light blue panel with an accent rail,
# matching the blue used by the plots.
CALLOUT = {
    "display": "block",
    "background": "#eaf2fb",
    "borderLeft": f"5px solid {ACCENT}",
    "borderRadius": "10px",
    "padding": "18px 22px",
    "margin": "26px 0 12px 0",
    "lineHeight": "1.7",
    "boxShadow": "0 1px 3px rgba(15, 40, 80, 0.08)",
}

# "Your turn": the moment the class stops watching and starts typing.  Amber,
# the colour already used for the name tags on the screenshots, so an exercise
# can never be mistaken for a blue take-away callout.
EXERCISE = {
    "display": "block",
    "background": "#fdf4dd",
    "borderLeft": "5px solid #f5b300",
    "borderRadius": "10px",
    "padding": "18px 22px",
    "margin": "26px 0 12px 0",
    "lineHeight": "1.7",
    "boxShadow": "0 1px 3px rgba(15, 40, 80, 0.08)",
}

# Extensions figure() hands to edtrace's video() instead of image().  The
# viewer renders those with `controls`, which is the whole point: an animation
# you can stop on the frame you are talking about.
MOVIE_SUFFIXES = (".mp4", ".webm", ".mov", ".m4v")

# Markdown has no nested-list syntax that survives one-rendering-per-line, so
# indentation is done with a margin instead.  See the comment on _divider().
SUBLIST = {"display": "block", "marginLeft": "2em"}
SUBSUBLIST = {"display": "block", "marginLeft": "4em"}


def figure(path: str, caption: str | None = None, width: str = "100%", caption_width: str | None = None, poster: str | None = None) -> None:
    """Show a framed figure, with an optional caption underneath.

    The frame always spans the content column, so a figure lines up with the
    text, the tables, the code blocks and the callouts around it.  `width` caps
    the *media inside* the frame and defaults to filling it: vector diagrams
    scale cleanly, while a screenshot is capped at its natural size, because
    upscaling a picture of text blurs it.  A narrower medium is centred in the
    frame, so the outer edges stay aligned either way.

    Emitted as raw HTML rather than through edtrace's image(): the frame and
    the media need separate widths, and image() writes a single style onto the
    <img> itself.  That means the path is checked here, as figure_row does.

    A video path (see MOVIE_SUFFIXES) gets the browser's native controls, so an
    animation can be **paused, resumed and scrubbed** while commenting it -
    which a GIF cannot do.  Frame, width and caption are identical either way.
    """
    if not os.path.exists(path):  # image()/video() check this for us; raw HTML does not
        raise ValueError(f"Figure not found: {path}")

    # Reserve the media's box before it loads.  The viewer rebuilds a line's
    # HTML at every step, and a fresh <video> has no height until its metadata
    # arrives: the viewer then measures the next line as already on screen,
    # skips its auto-scroll, and the presentation looks stuck on the figure.
    is_movie = path.lower().endswith(MOVIE_SUFFIXES)
    size = _media_size(poster if is_movie and poster else path)
    ratio = {"aspectRatio": f"{size[0]} / {size[1]}"} if size else {}
    media_style = css({**MEDIA, **ratio, "width": f"min(100%, {width})"})
    if is_movie:
        # The poster is what shows before playback starts, and what the PDF
        # exporter prints: Playwright's bundled Chromium cannot decode H.264,
        # so without one an .mp4 comes out of the handout as an empty box.
        if poster and not os.path.exists(poster):
            raise ValueError(f"Poster not found: {poster}")
        poster_attr = f' poster="{poster}"' if poster else ""
        media = f'<video controls preload="metadata"{poster_attr} style="{media_style}"><source src="{path}" type="video/mp4"></video>'
    else:
        media = f'<img src="{path}" style="{media_style}">'
    # The gap after a figure is the same whether or not it has a caption: the
    # frame hugs its caption, and whichever of the two comes last carries it.
    frame = {**FIGURE_FRAME, "marginBottom": "4px" if caption else FIGURE_GAP_AFTER}
    text(f'<div style="{css(frame)}">{media}</div>')
    if caption:
        text(caption, style={**CAPTION, "maxWidth": caption_width or "100%", "marginBottom": FIGURE_GAP_AFTER})


# Name tags written on top of a screenshot.  Amber reads on both light and
# dark screenshots.  Sizes are in `cqw` (percent of the image's width), so the
# tags scale with the image: the same proportions on a projector and on A4.
LABEL = {
    "position": "absolute",
    "display": "inline-flex",
    "alignItems": "center",
    "gap": "0.4em",
    "whiteSpace": "nowrap",
    "padding": "0.22em 0.7em",
    "borderRadius": "999px",
    "background": "#f5b300",
    "color": "#1f1a0a",
    "border": "1px solid rgba(255, 255, 255, 0.9)",
    "boxShadow": "0 1px 5px rgba(0, 0, 0, 0.45)",
    "fontSize": "max(9px, 1.25cqw)",
    "fontWeight": "700",
    "lineHeight": "1.3",
}

LABEL_NUMBER = {
    "display": "inline-block",
    "minWidth": "1.4em",
    "height": "1.4em",
    "lineHeight": "1.4em",
    "borderRadius": "50%",
    "background": INK,
    "color": "#ffffff",
    "textAlign": "center",
    "fontSize": "0.85em",
}

# Where the tag sits relative to its point, and the arrow that points back.
_LABEL_PLACES = {
    "right-of": ("translate(0.4em, -50%)", "◂ {}"),
    "left-of": ("translate(calc(-100% - 0.4em), -50%)", "{} ▸"),
    "above": ("translate(-50%, calc(-100% - 0.4em))", "{} ▾"),
    "above-left": ("translate(calc(-100% + 1.1em), calc(-100% - 0.4em))", "{} ▾"),
    "below": ("translate(-50%, 0.4em)", "▴ {}"),
    "center": ("translate(-50%, -50%)", "{}"),
}


# Step-by-step descriptions on an annotated screenshot.  Each explain() call is
# its own source line, hence its own step; the card on the figure is visible
# only while that line is the current one, so the next arrow press hides it
# and shows the following card.  On screen the explain() lines collapse to
# nothing; tools/export-pdf.mjs does the reverse, hiding the cards and printing
# those lines as a numbered legend, because a handout has no current step.
REVEAL_CARD = {
    "position": "absolute",
    "width": "27cqw",
    "padding": "0.55em 0.85em",
    "borderRadius": "8px",
    "background": "rgba(255, 255, 255, 0.97)",
    "borderLeft": "4px solid #f5b300",
    "boxShadow": "0 3px 14px rgba(0, 0, 0, 0.5)",
    "color": INK,
    "fontSize": "max(9px, 1.3cqw)",
    "lineHeight": "1.4",
    "whiteSpace": "normal",
    "textAlign": "left",
    "zIndex": "2",
}

_REVEAL_BASE_CSS = ".line:has(.reveal-legend){height:0;overflow:hidden;}.reveal-card{opacity:0;visibility:hidden;transition:opacity .15s;}.reveal-card .reveal-text::first-letter{text-transform:uppercase;}"


def annotated_figure(path: str, labels: list[dict], caption: str | None = None, width: str = "100%") -> None:
    """A screenshot with the names of its parts written on it.

    Each label is a dict: `x` and `y` in percent of the image (the point to
    name), `text`, optional `number` (a badge matching a numbered list), and
    `place`: where the tag sits relative to the point - "right-of",
    "left-of", "above", "above-left" (for points near the right edge),
    "below" or "center".  Framed, sized and captioned like figure().

    A numbered label can also carry a `description`, an optional `title`
    (defaults to `text`) and a `note` dict with its own `x`, `y` and `place`:
    that is the card explain(labels, number) reveals on the figure.
    """
    if not os.path.exists(path):
        raise ValueError(f"Figure not found: {path}")
    size = _media_size(path)
    ratio = f" aspect-ratio:{size[0]} / {size[1]};" if size else ""
    tags = "".join(_label_html(label) for label in labels)
    described = [label for label in labels if label.get("description") and label.get("number") is not None]
    cards, style, anchor = "", "", ""
    if described:
        key = _labels_key(labels)
        cards = "".join(_card_html(label, key) for label in described)
        shown = "".join(f'.lines-panel:has(.current-line [data-reveal="{key}-{label["number"]}"]) [data-describe="{key}-{label["number"]}"]{{opacity:1;visibility:visible;}}' for label in described)
        # Pin the (invisible) explain() lines to the middle of the image.  The
        # viewer scrolls whenever the current line is near the edge of the
        # window; left below the caption, those lines made it scroll the top of
        # the screenshot - and its cards - out of view on short screens.  With
        # CSS anchor positioning the steps sit mid-image: no scroll while the
        # image is on screen, and the image centred when it is not.  Browsers
        # without anchor support ignore the rule and keep the old behaviour.
        anchor = f" anchor-name:--{key};"
        pinned = f'.line:has([data-reveal^="{key}-"]){{position:absolute;left:0;right:0;top:anchor(--{key} center);}}'
        style = f"<style>{_REVEAL_BASE_CSS}{shown}{pinned}</style>"
    image = f'<img src="{path}" style="display:block; width:100%; height:auto;{ratio}">'
    box = f'<div style="position:relative; width:min(100%, {width}); margin:0 auto; container-type:inline-size;{anchor}">{style}{image}{tags}{cards}</div>'
    frame = {**FIGURE_FRAME, "marginBottom": "4px" if caption else FIGURE_GAP_AFTER}
    text(f'<div style="{css(frame)}">{box}</div>')
    if caption:
        text(caption, style={**CAPTION, "maxWidth": "100%", "marginBottom": FIGURE_GAP_AFTER})


def explain(labels: list[dict], number: int) -> None:
    """One step of a walkthrough over an annotated_figure: reveals the card of label `number`.

    Call it on its own line, once per numbered label, right after the figure.
    """
    label = next((item for item in labels if item.get("number") == number), None)
    if label is None or not label.get("description"):
        raise ValueError(f"No label numbered {number} with a description")
    key = _labels_key(labels)
    title = inline(label.get("title", label["text"]))
    text(f'<div class="reveal-legend" data-reveal="{key}-{number}" style="display:block; margin-left:2em;">{number}. <b>{title}</b>: {inline(label["description"])}</div>')


def _labels_key(labels: list[dict]) -> str:
    """A short, stable id for a set of labels, shared by the figure and its explain() steps."""
    return "ann-" + hashlib.sha1(repr(labels).encode("utf-8")).hexdigest()[:8]


def _card_html(label: dict, key: str) -> str:
    note = label.get("note", {})
    place = note.get("place", "center")
    if place not in _LABEL_PLACES:
        raise ValueError(f"Unknown note place {place!r}: use one of {list(_LABEL_PLACES)}")
    transform = _LABEL_PLACES[place][0]
    style = css({**REVEAL_CARD, "left": f"{note.get('x', label['x'])}%", "top": f"{note.get('y', label['y'])}%", "transform": transform})
    badge = f'<span style="{css({**LABEL_NUMBER, "marginRight": "0.45em"})}">{label["number"]}</span>'
    title = inline(label.get("title", label["text"]))
    return f'<div class="reveal-card" data-describe="{key}-{label["number"]}" style="{style}"><div style="font-weight:700; margin-bottom:0.2em;">{badge}{title}</div><div class="reveal-text">{inline(label["description"])}</div></div>'


def _label_html(label: dict) -> str:
    place = label.get("place", "center")
    if place not in _LABEL_PLACES:
        raise ValueError(f"Unknown label place {place!r}: use one of {list(_LABEL_PLACES)}")
    transform, template = _LABEL_PLACES[place]
    number = label.get("number")
    badge = f'<span style="{css(LABEL_NUMBER)}">{number}</span>' if number is not None else ""
    body = template.format(f"{badge}<span>{inline(label['text'])}</span>")
    style = css({**LABEL, "left": f"{label['x']}%", "top": f"{label['y']}%", "transform": transform})
    return f'<span style="{style}">{body}</span>'


def _media_size(path: str) -> tuple[float, float] | None:
    """Width and height of a PNG, JPEG or SVG file, read from its header; None if unknown."""
    lower = path.lower()
    try:
        if lower.endswith(".png"):
            with open(path, "rb") as f:
                head = f.read(24)
            return struct.unpack(">II", head[16:24])
        if lower.endswith((".jpg", ".jpeg")):
            with open(path, "rb") as f:
                data = f.read()
            i = 2
            while i + 9 < len(data):
                if data[i] != 0xFF:
                    i += 1
                    continue
                marker = data[i + 1]
                length = struct.unpack(">H", data[i + 2 : i + 4])[0]
                if marker in (0xC0, 0xC1, 0xC2):  # start of frame: height, then width
                    height, width = struct.unpack(">HH", data[i + 5 : i + 9])
                    return width, height
                i += 2 + length
        if lower.endswith(".svg"):
            with open(path, encoding="utf-8") as f:
                head = f.read(4000)
            match = re.search(r'viewBox="\s*[-\d.]+[\s,]+[-\d.]+[\s,]+([\d.]+)[\s,]+([\d.]+)\s*"', head)
            if match:
                return float(match.group(1)), float(match.group(2))
    except (OSError, struct.error, IndexError, UnicodeDecodeError):
        return None
    return None


def figure_row(paths: list[str], caption: str | None = None, width: str = "340px", gap: str = "14px") -> None:
    """Several figures side by side, centred, under one shared caption.

    Emitted as one raw-HTML flex row rather than as separate image() renderings:
    those are laid out inline inside a fixed-width container, so any leftover
    space piles up on the right instead of splitting evenly.
    """
    for path in paths:
        if not os.path.exists(path):  # image() checks this for us; raw HTML does not
            raise ValueError(f"Image not found: {path}")

    img_style = css(dict(FIGURE, display="block", width=width, margin="0"))
    imgs = "".join(f'<img src="{path}" style="{img_style}">' for path in paths)
    text(f'<div style="display:flex; justify-content:center; align-items:flex-start; gap:{gap}; margin:18px 0 4px 0;">{imgs}</div>')
    if caption:
        text(caption, style={**CAPTION, "maxWidth": "100%"})


# Section dividers.  Numbering restarts on its own whenever a different lecture
# function starts calling them, so reordering sections never needs a renumber.
_SECTION_COUNTERS: dict[str, int] = {}

SECTION_ACCENT = "#8494a8"  # reading
DEMO_ACCENT = ACCENT  # running code


def section(label: str) -> None:
    """A numbered divider: grey chip, label, hairline rule."""
    _divider(label, SECTION_ACCENT)


def demo(label: str) -> None:
    """Same divider in accent blue: the audience should watch the code panel."""
    _divider(label, DEMO_ACCENT)


def _divider(label: str, accent: str) -> None:
    # stack()[2] is the lecture function, because stack()[1] is section()/demo().
    caller = inspect.stack()[2].function
    number = _SECTION_COUNTERS.get(caller, 0) + 1
    _SECTION_COUNTERS[caller] = number
    chip = f'<span style="background:{accent}; color:#fff; font-size:13.5px; font-weight:700; border-radius:999px; padding:2px 10px;">{number}</span>'
    name = f'<span style="font-size:17.5px; font-weight:600; color:{INK};">{label}</span>'
    rule = f'<span style="flex:1; height:1px; background:{HAIRLINE};"></span>'
    text(f'<div style="display:flex; align-items:center; gap:10px; margin:44px 0 16px 0;">{chip}{name}{rule}</div>')


# Tables: no table styling ships with the viewer's markdown CSS, so the whole
# thing is emitted as inline-styled HTML, in the same palette as the figures
# and callouts above.
TABLE = {
    "display": "table",
    "width": "100%",
    "borderCollapse": "collapse",
    "tableLayout": "fixed",
    "fontSize": "15px",
    "lineHeight": "1.45",
    "margin": "16px 0 4px 0",
}

TABLE_HEAD = {
    "textAlign": "left",
    "padding": "7px 10px",
    "fontSize": "12.5px",
    "fontWeight": "700",
    "letterSpacing": "0.05em",
    "textTransform": "uppercase",
    "color": MUTED,
    "borderBottom": f"2px solid {ACCENT}",
}

TABLE_CELL = {
    "padding": "9px 10px",
    "verticalAlign": "top",
    "borderBottom": f"1px solid {HAIRLINE}",
    "color": INK,
}

# First column names the trend, last column carries the punchline: both get a
# little weight so the eye lands on them before reading the numbers.
TABLE_FIRST = {"fontWeight": "600"}
TABLE_LAST = {"color": "#1b4b91", "fontWeight": "600"}

TABLE_STRIPE = STRIPE


def table(headers: list[str], rows: list[list[str]], widths: list[str] | None = None, caption: str | None = None) -> None:
    """A comparison table, zebra-striped, with the last column as the take-away.

    Cells take the same inline markup as text() (`**bold**`, `[text](url)`):
    markdown is not parsed inside a raw-HTML block, so it is converted here.
    `widths` is one CSS length per column ("26%", "180px", ...).
    """
    for row in rows:
        if len(row) != len(headers):
            raise ValueError(f"Row has {len(row)} cells but there are {len(headers)} headers: {row}")

    cols = "".join(f'<col style="width:{width}">' for width in widths) if widths else ""
    head = "".join(f'<th style="{css(TABLE_HEAD)}">{inline(header)}</th>' for header in headers)

    body = ""
    for index, row in enumerate(rows):
        cells = ""
        for column, cell in enumerate(row):
            style = dict(TABLE_CELL)
            if column == 0:
                style.update(TABLE_FIRST)
            if column == len(row) - 1:
                style.update(TABLE_LAST)
            cells += f'<td style="{css(style)}">{inline(cell)}</td>'
        background = TABLE_STRIPE if index % 2 else "transparent"
        body += f'<tr style="background:{background};">{cells}</tr>'

    text(
        f'<table style="{css(TABLE)}">{cols}' f"<thead><tr>{head}</tr></thead>" f"<tbody>{body}</tbody></table>",
        style={"display": "block"},
    )
    if caption:
        text(caption, style={**CAPTION, "maxWidth": "100%", "textAlign": "left", "fontSize": "14px"})


def table_all(spec: dict) -> None:
    """A whole table in one step, straight from a `*_content.py` spec.

    The revealed form below (`table_head` + one `table_row` per line) is for a
    table you comment row by row; this one is for a table the class reads at a
    glance.
    """
    table(spec["headers"], spec["rows"], spec.get("widths"), spec.get("caption"))


# Revealed tables: same look as table(), but emitted one fragment per *source
# line*, because the viewer keeps a single set of renderings per line (a loop
# would overwrite itself) and highlights the current line.  One row per line
# therefore means one highlighted row at a time.  Every fragment is a table of
# its own with the same <col> widths, so the columns stay aligned; the row
# background is left transparent so the viewer's yellow cursor shows through.
TABLE_FRAGMENT = {**TABLE, "margin": "0"}


def table_head(spec: dict) -> None:
    """Open a revealed table: the header row, nothing else."""
    cols = "".join(f'<col style="width:{width}">' for width in spec.get("widths") or [])
    cells = "".join(f'<th style="{css(TABLE_HEAD)}">{inline(header)}</th>' for header in spec["headers"])
    text(f'<table style="{css(TABLE_FRAGMENT)}">{cols}<thead><tr>{cells}</tr></thead></table>', style={"display": "block"})


def table_row(spec: dict, key: str) -> None:
    """One row of a revealed table, found by the text of its first cell."""
    # Prefix first, so "A **word**" picks its own row rather than also matching
    # "**Embedding** of a **word**"; substring second, so a key can skip a leading emoji.
    matches = [row for row in spec["rows"] if row[0].lower().startswith(key.lower())]
    matches = matches or [row for row in spec["rows"] if key.lower() in row[0].lower()]
    if len(matches) != 1:  # fail while tracing, not in front of the class
        raise ValueError(f"{key!r} matches {len(matches)} rows: {[row[0] for row in matches]}")
    row = matches[0]

    cols = "".join(f'<col style="width:{width}">' for width in spec.get("widths") or [])
    cells = ""
    for column, cell in enumerate(row):
        style = dict(TABLE_CELL)
        if column == 0:
            style.update(TABLE_FIRST)
        if column == len(row) - 1:
            style.update(TABLE_LAST)
        cells += f'<td style="{css(style)}">{inline(cell)}</td>'
    text(f'<table style="{css(TABLE_FRAGMENT)}">{cols}<tbody><tr>{cells}</tr></tbody></table>', style={"display": "block"})


def table_caption(spec: dict) -> None:
    """Close a revealed table with its caption."""
    text(spec["caption"], style={**CAPTION, "maxWidth": "100%", "textAlign": "left", "fontSize": "14px"})


# Code the class reads rather than runs: a snippet in another language, a
# terminal session, a disassembly.  text(..., verbatim=True) hands each line to
# markdown on its own, which turns `**` into bold and a four-space indent into
# a code block, so the snippet is emitted as one escaped <pre> instead.  An
# empty line would close the surrounding HTML block, hence the &#160;.
# Same look as the lecture's own code lines (see THEME_CSS): tinted band with
# a left rule, so a shown-not-run snippet and an executed line read alike.
CODE = {
    "margin": "0",
    "padding": "8px 0 8px 14px",
    "background": STRIPE,
    "borderLeft": f"3px solid {HAIRLINE}",
    "fontFamily": "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace",
    "fontSize": "15px",
    "lineHeight": "1.5",
    "color": INK,
    "whiteSpace": "pre",
    "overflowX": "auto",
}

CODE_TITLE = {
    "fontSize": "12.5px",
    "fontWeight": "700",
    "letterSpacing": "0.05em",
    "textTransform": "uppercase",
    "color": MUTED,
    "margin": "0 0 5px 2px",
}


# Python colouring for code that is shown, not executed: the viewer highlights
# the lecture's own source, but a code_block is plain HTML.  Opt-in per block
# (`language="python"`), so a Java or PowerShell snippet is left alone.
_PY_COLORS = {"comment": "#6a737d", "string": "#b26a00", "number": "#1b4b91", "keyword": "#c2185b", "builtin": "#6f42c1"}

_PY_TOKENS = re.compile(
    r"(?P<comment>#[^\n]*)"
    r"|(?P<string>'(?:[^'\\\n]|\\.)*'|\"(?:[^\"\\\n]|\\.)*\")"
    r"|(?P<keyword>\b(?:and|as|assert|break|class|continue|def|del|elif|else|except|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield|True|False|None)\b)"
    r"|(?P<builtin>\b(?:print|len|range|list|dict|set|tuple|str|int|float|bool|open|type|id|sorted|sum|min|max|zip|enumerate|filter|map)\b)"
    r"|(?P<number>\b\d+(?:\.\d+)?\b)"
)


def _highlight_python(escaped: str) -> str:
    """Colour an already-escaped Python snippet (quotes left unescaped so strings match)."""

    def paint(match: re.Match) -> str:
        kind = match.lastgroup
        return f'<span style="color:{_PY_COLORS[kind]};{" font-style:italic;" if kind == "comment" else ""}">{match.group()}</span>'

    return _PY_TOKENS.sub(paint, escaped)


def code_block(source: str, title: str | None = None, language: str | None = None) -> None:
    """One framed snippet that is shown, not executed, with an optional small title.

    `language="python"` colours it like a fenced ```python block.
    """
    code_row([(title, source)], language=language)


def code_row(blocks: list[tuple], gap: str = "16px", language: str | None = None) -> None:
    """Snippets side by side, e.g. the same loop in two languages.

    `blocks` is a list of (title, source) pairs, or (title, source, language)
    when the columns are in different languages - a Python snippet next to the
    shell commands that run it.  A title may be None; `language` is the default
    for blocks that do not name one.
    """
    columns = "".join(_code_column(block[0], block[1], block[2] if len(block) > 2 else language) for block in blocks)
    text(f'<div style="display:flex; flex-wrap:wrap; align-items:flex-start; gap:{gap}; margin:22px 0 26px 0;">{columns}</div>')


def _code_column(title: str | None, source: str, language: str | None = None) -> str:
    # quote=False: the quotes stay as they are, so the highlighter can find strings.
    escaped = html.escape(textwrap.dedent(source).strip("\n"), quote=False)
    if language == "python":
        escaped = _highlight_python(escaped)
    body = "\n".join(line if line.strip() else "&#160;" for line in escaped.split("\n"))
    head = f'<div style="{css(CODE_TITLE)}">{inline(title)}</div>' if title else ""
    return f'<div style="flex:1 1 0; min-width:260px;">{head}<pre style="{css(CODE)}">{body}</pre></div>'


# A cited *book*: cover on the left, bibliographic line and a note on the right.
# A portrait cover centred with figure() would push the bullets that follow it
# off the screen, and a book is not a figure anyway: it is a citation the
# audience should recognise on sight.
BOOK_CARD = {
    "display": "flex",
    "alignItems": "center",
    "gap": "22px",
    "background": STRIPE,
    "border": f"1px solid {HAIRLINE}",
    "borderRadius": "12px",
    "padding": "16px 22px",
    "margin": "18px 0 6px 0",
    "maxWidth": "700px",
    "boxShadow": "0 1px 3px rgba(15, 40, 80, 0.08)",
}

BOOK_COVER = {
    "display": "block",
    "width": "118px",
    "flexShrink": "0",
    "borderRadius": "5px",
    "boxShadow": "0 3px 12px rgba(15, 40, 80, 0.22)",
}


def book_card(cover: str, title: str, byline: str, note: str, source: str | None = None) -> None:
    """Cite a book the way the deck cites a person: with its face.

    `note` takes the same inline markup as text() and carries the reason the
    book is on the slide; `source` is the small print underneath.
    """
    if not os.path.exists(cover):  # image() checks this for us; raw HTML does not
        raise ValueError(f"Cover not found: {cover}")

    small = f'<div style="font-size:11.5px; color:{MUTED}; margin-top:9px;">{inline(source)}</div>' if source else ""
    # Dedent before interpolating, and join without blank lines: a blank line
    # would close the raw-HTML block and let markdown wrap the rest in <p>.
    card = textwrap.dedent("""
    <div style="{card}">
        <img src="{cover}" style="{image}">
        <div>
            <div style="font-size:17px; font-weight:700; color:{ink};">{title}</div>
            <div style="font-size:13px; color:{muted}; margin:3px 0 11px 0;">{byline}</div>
            <div style="font-size:14px; color:{ink}; line-height:1.5; border-left:3px solid {accent}; padding-left:12px;">{note}</div>
            {small}
        </div>
    </div>
    """)
    text(card.format(card=css(BOOK_CARD), cover=cover, image=css(BOOK_COVER), title=inline(title), byline=inline(byline), note=inline(note), small=small, ink=INK, muted=MUTED, accent=ACCENT).strip())


# People cards for the title slide.  `people` is a list of dicts with the keys
# used below; `focus` is a CSS object-position, so a full-body portrait can be
# cropped up to the face without touching the file.
PERSON_PLACEHOLDER = {"name": "", "affiliation": "", "image": "", "focus": "50% 50%", "url": "#", "role": ""}


def people_row(people: list[dict], gap: str = "48px", justify: str = "center", photo: str = "120px", name_size: str = "14px") -> None:
    """A row of portrait cards: photo, name, affiliation, role.

    `justify` is any CSS justify-content value: "center" for a row of authors,
    "flex-start" to line a single portrait up with the text above it.

    `photo` is the diameter of the portrait and `name_size` the size of the
    name under it; the card, the initials disc and the affiliation line scale
    with them, so one presenter can be shown larger than a row of five.
    """
    # Join without blank lines: a blank line would end the raw-HTML block and
    # let the markdown renderer wrap the rest in <p> tags.
    cards = "\n".join(_person_card({**PERSON_PLACEHOLDER, **person}, photo, name_size).strip() for person in people)
    # Dedent the template *before* interpolating, otherwise the flush-left card
    # HTML makes the common indent 0 and the wrapper stays indented (which
    # markdown reads as a code block).
    row = textwrap.dedent("""
    <div style="
        display:flex;
        justify-content:{justify};
        align-items:flex-start;
        gap:{gap};
    ">
    {cards}
    </div>
    """)
    text(row.format(cards=cards, gap=gap, justify=justify))


def _person_card(person: dict, photo: str = "120px", name_size: str = "14px") -> str:
    if person["image"] and not os.path.exists(person["image"]):
        raise ValueError(f"Portrait not found: {person['image']}")

    # No portrait yet: an initials disc, so the title slide is presentable
    # before anyone has collected the photos.
    if person["image"]:
        face = f'<img src="{person["image"]}" style="width:{photo}; height:{photo}; object-fit:cover; object-position:{person["focus"]}; border-radius:50%; margin-bottom:10px;">'
    else:
        initials = "".join(word[0] for word in person["name"].split()[:2]).upper()
        face = f'<div style="width:{photo}; height:{photo}; border-radius:50%; margin:0 auto 10px auto; background:{STRIPE}; border:1px solid {HAIRLINE}; color:{ACCENT}; font-size:calc({photo} * 0.28); font-weight:700; line-height:{photo};">{initials}</div>'

    return textwrap.dedent(f"""
    <div style="width:calc({photo} + 30px); text-align:center; font-size:{name_size};">
        <a href="{person["url"]}" target="_blank" style="text-decoration:none; color:inherit;">
            {face}
            <div>{person["name"]}</div>
        </a>
        <div style="font-size:calc({name_size} * 0.85); opacity:0.75;">{person["affiliation"]}</div>
        <div>{inline(person["role"])}</div>
    </div>
    """)


def inline(markup: str) -> str:
    """`**bold**`, `*italic*`, `` `code` `` and `[text](url)` to HTML; anything else passes through."""
    html = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2" target="_blank">\1</a>', markup)
    html = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", html)
    html = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", html)
    html = re.sub(r"`([^`]+)`", r'<code style="font-family:ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size:0.88em; color:#1f3550; background:rgba(110, 130, 155, 0.14); border:1px solid rgba(110, 130, 155, 0.22); border-radius:5px; padding:0.06em 0.38em; text-transform:none; letter-spacing:normal;">\1</code>', html)
    return html


def css(style: dict) -> str:
    """Turn a React-style dict into an inline CSS string."""

    def dashed(key: str) -> str:
        return "".join("-" + c.lower() if c.isupper() else c for c in key)

    return ";".join(f"{dashed(key)}:{value}" for key, value in style.items())
