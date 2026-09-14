import json
import os
import struct
import zlib

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site")
os.makedirs(OUT, exist_ok=True)

# ---------- shared stylesheet ----------
CSS = '''
:root{
  --paper:#1B1915; --paper-deep:#141210; --line:#38352C;
  --ink:#EDE7D8; --ink-soft:#A69C87;
  --blue:#8CA3D6; --blue-soft:#6C82AD;
  --red:#E2766A; --green:#7BB496;
  --surface:rgba(255,255,255,.045); --tint:rgba(140,163,214,.08);
  --max:700px;
  color-scheme:dark;
}
*{box-sizing:border-box;}
html{scroll-behavior:smooth;}
body{
  margin:0;
  background:
    radial-gradient(var(--line) 1px, transparent 1.4px) 0 0/22px 22px,
    var(--paper);
  color:var(--ink);
  font-family:'Work Sans', -apple-system, sans-serif;
  font-size:17px; line-height:1.62; -webkit-font-smoothing:antialiased;
}
@media (prefers-reduced-motion: reduce){ *{animation:none !important; transition:none !important;} }
a{color:var(--blue); text-decoration-thickness:1px; text-underline-offset:2px;}
a:hover{color:var(--red);}

/* site header / breadcrumb nav on every page */
.sitebar{
  max-width:var(--max); margin:0 auto; padding:26px 24px 0;
  display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:10px 14px;
  font-size:14px; color:var(--ink-soft);
}
@media (max-width:480px){
  .auth-control{width:100%; justify-content:flex-end;}
}
.sitebar a.home{
  display:flex; align-items:center; gap:8px; color:var(--ink); font-weight:600;
  text-decoration:none;
}
.sitebar a.home svg{width:18px; height:18px;}
.sitebar .pos{color:var(--ink-soft);}

.wrap{max-width:var(--max); margin:0 auto; padding:20px 24px 90px;}

header.masthead{max-width:var(--max); margin:0 auto; padding:40px 24px 8px;}
.kicker{
  font-size:14px; color:var(--ink-soft); display:flex; align-items:center; gap:10px;
  margin-bottom:18px;
}
.kicker svg{width:20px; height:20px; flex:none;}
h1{
  font-family:'Fraunces', serif; font-weight:600;
  font-size:clamp(34px, 7vw, 50px); line-height:1.06; letter-spacing:-0.01em;
  margin:0 0 6px;
}
h1 em{font-style:italic; font-weight:500; color:var(--blue);}
.subhead{font-size:19px; color:var(--ink-soft); max-width:520px; margin:18px 0 28px;}
.underline{width:180px; height:14px; margin-bottom:8px;}
.underline path{
  fill:none; stroke:var(--red); stroke-width:3; stroke-linecap:round;
}
.meta-row{
  display:flex; flex-wrap:wrap; gap:10px 22px; margin-top:26px; font-size:14px;
  color:var(--ink-soft); border-top:1px solid var(--line); padding-top:18px;
}
.meta-row div{display:flex; flex-direction:column; gap:2px;}
.meta-row b{color:var(--ink); font-weight:600; font-size:15px;}

section{max-width:var(--max); margin:0 auto; padding:0 24px;}

.page-head{display:flex; align-items:center; gap:14px; margin:18px 0 4px;}
.page-head svg.icon{width:36px; height:36px; flex:0 0 36px; color:var(--blue);}
h2{
  font-family:'Fraunces', serif; font-weight:600; font-size:30px;
  letter-spacing:-.005em; margin:0; display:flex; align-items:baseline; gap:12px;
}
h2 .no{font-family:'Fraunces', serif; font-style:italic; font-weight:500; color:var(--blue-soft); font-size:22px;}
.duration{
  display:inline-block; font-size:13.5px; color:var(--ink-soft);
  border-left:2px solid var(--line); padding-left:10px; margin:14px 0 26px;
}
h3{font-family:'Fraunces', serif; font-weight:600; font-size:19px; margin:30px 0 10px;}
p{margin:0 0 16px;}
ul,ol{margin:0 0 16px; padding-left:22px;}
li{margin-bottom:7px;}
strong{font-weight:600;}

.callout{
  border-left:3px solid var(--line); padding:12px 16px; margin:16px 0;
  border-radius:2px; background:var(--surface); font-size:15.5px;
}
.callout.do{border-color:var(--green);}
.callout.skip{border-color:var(--red);}
.callout .tag{font-weight:700; font-size:11.5px; margin-bottom:5px; display:block;}
.callout.do .tag{color:var(--green);}
.callout.skip .tag{color:var(--red);}

.tldr{
  background:var(--tint); border:1px solid var(--line); border-radius:6px;
  padding:24px 26px; margin:30px 0;
}
.tldr h3{margin-top:0;}

.findings{list-style:none; margin:24px 0; padding:0;}
.findings li{display:flex; gap:16px; padding:18px 0; border-top:1px solid var(--line);}
.findings li:last-child{border-bottom:1px solid var(--line);}
.findings .fn{
  font-family:'Fraunces', serif; font-style:italic; font-weight:500;
  color:var(--blue-soft); font-size:26px; flex:none; width:34px;
}

blockquote{
  margin:18px 0; padding:2px 0 2px 18px; border-left:2px solid var(--blue-soft);
  font-family:'Fraunces', serif; font-style:italic; font-size:17.5px; color:var(--blue);
}

.supply-grid{display:grid; grid-template-columns:1fr 1fr; gap:10px 24px; margin:18px 0; font-size:15px;}
@media (max-width:520px){.supply-grid{grid-template-columns:1fr;}}

.caveat-box{background:var(--paper-deep); border-radius:6px; padding:22px 26px; font-size:15px; color:var(--ink-soft);}
.caveat-box li{margin-bottom:10px;}
.caveat-box strong{color:var(--ink);}

/* table of contents on index */
.toc{list-style:none; margin:30px 0; padding:0;}
.toc li{border-top:1px solid var(--line);}
.toc li:last-child{border-bottom:1px solid var(--line);}
.toc a{
  display:flex; align-items:center; gap:16px; padding:18px 4px; text-decoration:none;
  color:var(--ink);
}
.toc a:hover{color:var(--blue);}
.toc a:hover .toc-title{color:var(--blue);}
.toc svg.icon{width:30px; height:30px; flex:0 0 30px; color:var(--blue-soft);}
.toc .no{
  font-family:'Fraunces', serif; font-style:italic; color:var(--blue-soft); font-size:20px; width:26px; flex:none;
}
.toc-body{flex:1; min-width:0;}
.toc-title{font-family:'Fraunces', serif; font-weight:600; font-size:19px; display:block;}
.toc-sub{font-size:13.5px; color:var(--ink-soft); margin-top:2px;}
.toc-arrow{color:var(--ink-soft); flex:none;}

/* prev / next footer nav */
nav.pn{
  max-width:var(--max); margin:50px auto 0; padding:22px 24px 0;
  border-top:1px solid var(--line);
  display:flex; justify-content:space-between; gap:16px; font-size:14.5px;
}
nav.pn a{text-decoration:none; max-width:46%;}
nav.pn .lbl{display:block; font-size:12px; color:var(--ink-soft); margin-bottom:3px;}
nav.pn .to-next{margin-left:auto; text-align:right;}

footer.site{
  max-width:var(--max); margin:40px auto 0; padding:24px 24px 40px;
  font-size:13px; color:var(--ink-soft);
}

/* auth control in sitebar */
.auth-control{display:flex; align-items:center; gap:10px; font-size:13px;}
.auth-btn{
  border:1px solid var(--line); background:var(--surface); color:var(--ink);
  padding:6px 13px; border-radius:16px; font-size:12.5px; cursor:pointer;
  font-family:inherit; white-space:nowrap;
}
.auth-btn:hover{border-color:var(--blue); color:var(--blue);}
.auth-btn.primary{background:var(--blue); color:var(--paper); border-color:var(--blue);}
.auth-btn.primary:hover{opacity:.88; color:var(--paper);}
.auth-user{font-weight:600; color:var(--ink);}
.progress-pill{
  font-size:12px; color:var(--ink-soft); border:1px solid var(--line);
  padding:4px 10px; border-radius:12px; white-space:nowrap;
}

/* overall progress bar (index page) */
.overall-bar{max-width:var(--max); margin:22px auto 0; padding:0 24px;}
.bar-track{height:8px; background:var(--paper-deep); border-radius:4px; overflow:hidden; border:1px solid var(--line);}
.bar-fill{height:100%; width:0%; background:var(--green); transition:width .5s ease;}
.bar-label{font-size:12.5px; color:var(--ink-soft); margin-top:7px;}

/* "continue where you left off" card (index page) */
.continue-card{max-width:var(--max); margin:18px auto 0; padding:0 24px;}
.continue-card .continue-label{
  font-size:12px; color:var(--ink-soft); margin-bottom:6px;
  text-transform:uppercase; letter-spacing:.04em;
}
.continue-link{
  display:flex; align-items:center; justify-content:space-between; gap:14px;
  background:rgba(63,107,79,.08); border:1px solid var(--green); border-radius:6px;
  padding:16px 20px; text-decoration:none; color:var(--ink);
}
.continue-link:hover{background:rgba(63,107,79,.14);}
.continue-link:hover .continue-title{color:var(--ink);}
.continue-title{font-family:'Fraunces', serif; font-weight:600; font-size:18px;}
.continue-arrow{color:var(--green); flex:none; font-size:20px;}

/* per-section progress pill in the table of contents */
.toc-progress{
  font-size:12px; color:var(--ink-soft); border:1px solid var(--line);
  padding:3px 9px; border-radius:10px; flex:none; margin-left:2px;
}
.toc-progress.complete{color:var(--green); border-color:var(--green);}

/* progress tracker checklist box on each phase page */
.tracker-box{
  margin:34px 0 6px; border:1px solid var(--line); border-radius:6px;
  padding:22px 24px; background:var(--surface);
}
.tracker-box h3{margin-top:0;}
.track-section{
  font-weight:600; font-size:13px; text-transform:uppercase; letter-spacing:.03em;
  color:var(--ink-soft); margin:18px 0 2px; padding-top:12px; border-top:1px solid var(--line);
}
.track-section:first-child{margin-top:0; padding-top:0; border-top:none;}
.track-section a{font-weight:500; text-transform:none; letter-spacing:0; margin-left:4px;}
.track-item{
  display:grid; grid-template-columns:22px 1fr; column-gap:12px; row-gap:6px;
  align-items:start; padding:12px 0; font-size:15px;
  border-top:1px solid var(--line);
}
.track-item:first-of-type{border-top:none; padding-top:3px;}
/* Native checkboxes render at different sizes/positions across mobile
   browsers, which is what made them look misaligned with the label text.
   Drawing the box ourselves keeps it pixel-identical everywhere. */
.track-item input[type=checkbox]{
  appearance:none; -webkit-appearance:none; -moz-appearance:none;
  margin:0; width:20px; height:20px; grid-column:1; grid-row:1;
  border:1.5px solid var(--ink-soft); border-radius:5px; background:var(--paper-deep);
  position:relative; top:2px; cursor:pointer;
}
.track-item input[type=checkbox]:checked{background:var(--green); border-color:var(--green);}
.track-item input[type=checkbox]:checked::after{
  content:""; position:absolute; left:6px; top:2px; width:5px; height:10px;
  border:solid var(--paper-deep); border-width:0 2px 2px 0; transform:rotate(45deg);
}
.track-item input[type=checkbox]:focus-visible{outline:2px solid var(--blue); outline-offset:2px;}
.track-item input[type=checkbox]:disabled{cursor:not-allowed; opacity:.45;}
.track-item label{grid-column:2; grid-row:1; cursor:pointer; overflow-wrap:break-word;}
.item-links{
  grid-column:2; grid-row:2; display:flex; flex-direction:column; gap:2px;
  font-size:12px; color:var(--ink-soft);
}
.item-links a{color:var(--ink-soft);}
.item-links a:hover{color:var(--green);}
.item-links b{font-weight:600; color:var(--ink);}
.tracker-note{font-size:13px; color:var(--ink-soft); margin:12px 0 0;}

@media print{
  .sitebar, nav.pn, .tracker-box, .overall-bar, .continue-card{display:none;}
  a{color:var(--ink); text-decoration:none;}
}
'''

with open(f"{OUT}/style.css", "w") as f:
    f.write(CSS)

# ---------- favicon / home-screen icons ----------
# Generated directly with stdlib zlib+struct (no Pillow/cairosvg available in
# this environment) so the icons stay a single source of truth alongside the
# rest of the site, reusing the same three-panel mark as the "comics" nav
# icon and the site's own paper/ink colors.
def _hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

_ICON_BG = _hex_to_rgb("1B1915")
_ICON_FG = _hex_to_rgb("EDE7D8")

def _write_png(path, size, pixel_fn):
    raw = bytearray()
    for y in range(size):
        raw.append(0)  # filter: none
        for x in range(size):
            raw += bytes(pixel_fn(x, y))
    compressed = zlib.compress(bytes(raw), 9)
    def chunk(tag, data):
        c = tag + data
        return struct.pack("!I", len(data)) + c + struct.pack("!I", zlib.crc32(c) & 0xffffffff)
    png = (b"\x89PNG\r\n\x1a\n"
           + chunk(b"IHDR", struct.pack("!IIBBBBB", size, size, 8, 2, 0, 0, 0))
           + chunk(b"IDAT", compressed)
           + chunk(b"IEND", b""))
    with open(path, "wb") as f:
        f.write(png)
    return png

def _in_rounded_rect(px, py, x0, y0, x1, y1, r):
    if px < x0 or px > x1 or py < y0 or py > y1:
        return False
    if px < x0 + r and py < y0 + r:
        return (px - (x0 + r)) ** 2 + (py - (y0 + r)) ** 2 <= r * r
    if px > x1 - r and py < y0 + r:
        return (px - (x1 - r)) ** 2 + (py - (y0 + r)) ** 2 <= r * r
    if px < x0 + r and py > y1 - r:
        return (px - (x0 + r)) ** 2 + (py - (y1 - r)) ** 2 <= r * r
    if px > x1 - r and py > y1 - r:
        return (px - (x1 - r)) ** 2 + (py - (y1 - r)) ** 2 <= r * r
    return True

# Same three-panel layout as the "comics" nav icon's 24x24 viewBox, scaled
# in toward the center for the maskable variant so it survives Android's
# circular safe-zone crop.
def _panel_shapes(scale):
    cx = cy = 12.0
    raw = [(2, 2, 11.5, 11, 1.2), (12.5, 2, 22, 11, 1.2), (2, 12, 22, 22, 1.2)]
    return [
        (cx + (x0 - cx) * scale, cy + (y0 - cy) * scale,
         cx + (x1 - cx) * scale, cy + (y1 - cy) * scale, r * scale)
        for x0, y0, x1, y1, r in raw
    ]

def _render_icon_png(path, size, scale=1.0, ss=4):
    unit = size / 24.0
    shapes = [(x0 * unit, y0 * unit, x1 * unit, y1 * unit, r * unit) for x0, y0, x1, y1, r in _panel_shapes(scale)]
    def pixel(x, y):
        hits = 0
        for dy in range(ss):
            for dx in range(ss):
                px, py = x + (dx + 0.5) / ss, y + (dy + 0.5) / ss
                if any(_in_rounded_rect(px, py, *s) for s in shapes):
                    hits += 1
        t = hits / (ss * ss)
        return tuple(round(_ICON_BG[i] * (1 - t) + _ICON_FG[i] * t) for i in range(3))
    return _write_png(path, size, pixel)

def _write_ico(path, entries):
    n = len(entries)
    offset = 6 + 16 * n
    header = struct.pack("<HHH", 0, 1, n)
    dir_entries = b""
    data = b""
    for size, png in entries:
        dir_entries += struct.pack("<BBBBHHII", size, size, 0, 0, 1, 32, len(png), offset)
        data += png
        offset += len(png)
    with open(path, "wb") as f:
        f.write(header + dir_entries + data)

_png16 = _render_icon_png(f"{OUT}/icon-16.png", 16, ss=6)
_png32 = _render_icon_png(f"{OUT}/icon-32.png", 32, ss=6)
_render_icon_png(f"{OUT}/apple-touch-icon.png", 180, ss=3)
_render_icon_png(f"{OUT}/icon-192.png", 192, ss=3)
_render_icon_png(f"{OUT}/icon-512.png", 512, ss=2)
_render_icon_png(f"{OUT}/icon-512-maskable.png", 512, scale=0.65, ss=2)
_write_ico(f"{OUT}/favicon.ico", [(16, _png16), (32, _png32)])

MANIFEST = {
    "name": "Draw Your Own Comics",
    "short_name": "Draw Comics",
    "description": "A curated, human-made curriculum for drawing your own comics.",
    "start_url": "index.html",
    "scope": ".",
    "display": "standalone",
    "background_color": "#1B1915",
    "theme_color": "#1B1915",
    "icons": [
        {"src": "icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
        {"src": "icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
        {"src": "icon-512-maskable.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
    ],
}
with open(f"{OUT}/manifest.webmanifest", "w") as f:
    json.dump(MANIFEST, f, indent=2)

FONT_LINKS = '''<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600;0,9..144,700;1,9..144,500&family=Work+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">'''

FAVICON_LINKS = '''<link rel="icon" href="favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="16x16" href="icon-16.png">
<link rel="icon" type="image/png" sizes="32x32" href="icon-32.png">
<link rel="apple-touch-icon" sizes="180x180" href="apple-touch-icon.png">
<link rel="manifest" href="manifest.webmanifest">
<meta name="theme-color" content="#1B1915">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Draw Comics">'''

ICONS = {
    "rhythm": '<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2" stroke-linecap="round"/></svg>',
    "lines": '<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M3 17c3-8 6-11 9-11s5 5 9 5" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "construction": '<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M4 8l8-4 8 4-8 4-8-4zM4 8v8l8 4 8-4V8M12 12v8" stroke-linejoin="round"/></svg>',
    "perspective": '<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M12 3 4 20h16L12 3z"/><path d="M8 14h8" stroke-linecap="round"/></svg>',
    "gesture": '<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><circle cx="12" cy="5" r="2"/><path d="M12 7v6M12 13l-5 6M12 13l5 6M7 10l5 3 5-3" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "character": '<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><circle cx="12" cy="12" r="8"/><circle cx="9" cy="10" r="1" fill="currentColor" stroke="none"/><circle cx="15" cy="10" r="1" fill="currentColor" stroke="none"/><path d="M8.5 15c1.5 1.4 5.5 1.4 7 0" stroke-linecap="round"/></svg>',
    "comics": '<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><rect x="3" y="4" width="8" height="7" rx="1"/><rect x="13" y="4" width="8" height="7" rx="1"/><rect x="3" y="13" width="18" height="7" rx="1"/></svg>',
    "digital": '<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><rect x="4" y="3" width="16" height="18" rx="2"/><circle cx="12" cy="18" r="1" fill="currentColor" stroke="none"/></svg>',
    "recs": '<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M5 13l4 4L19 7" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "caveats": '<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M12 3 2 20h20L12 3z"/><path d="M12 10v4M12 17h.01" stroke-linecap="round"/></svg>',
    "about": '<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M4 5c2-1 5-1 8 1 3-2 6-2 8-1v13c-2-1-5-1-8 1-3-2-6-2-8-1V5z" stroke-linejoin="round" stroke-linecap="round"/><path d="M12 6v13" stroke-linecap="round"/></svg>',
}

HOME_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M4 11l8-7 8 7M6 10v9h12v-9" stroke-linecap="round" stroke-linejoin="round"/></svg>'

PAGES = []  # filled below, list of dicts: id, file, title, kicker, icon, duration, body

def add(id, file, title, icon, duration, body):
    PAGES.append(dict(id=id, file=file, title=title, icon=icon, duration=duration, body=body))

add("rhythm", "01-rhythm.html", "Weekly rhythm &amp; supplies", "rhythm", None, '''
<p>Progress here comes from consistency, not intensity. Structure it like this:</p>
<ul>
  <li><strong>Two sessions of 45&ndash;90 minutes a week</strong> (or one longer weekend block plus small doodling on the side).</li>
  <li><strong>Split every session roughly 50/50</strong> &mdash; structured exercise from your current phase, then free &ldquo;play&rdquo;: doodle your own characters, copy cartoons you love, sketch from shows.</li>
  <li><strong>Don&rsquo;t chase finished pieces early.</strong> The reps are the point, not the polish.</li>
  <li><strong>Expect each phase to take months.</strong> That&rsquo;s normal, and it&rsquo;s what makes this sustainable for five years instead of five weeks.</li>
</ul>
<h3>Supplies &mdash; keep it cheap</h3>
<div class="supply-grid">
  <div>&#9998; HB pencil + a softer 2B/3B</div>
  <div>&#9998; Vinyl or kneaded eraser</div>
  <div>&#9998; Canson XL or Strathmore sketchbook</div>
  <div>&#9998; Staedtler Mars Lumograph pencils</div>
  <div>&#9998; A pack of fineliners (for ink line drills &mdash; no erasing)</div>
  <div>&#9998; Printer paper is fine to start</div>
</div>
<h3>Four books worth buying (~$110 total, one-time)</h3>
<p>Everything else in this course is free, but four real, proven, expert-designed texts are worth
paying for instead of us improvising an equivalent from YouTube:</p>
<div class="supply-grid">
  <div>&#128214; Scott Robertson &amp; Thomas Bertling, <a href="https://designstudiopress.com/products/how-to-draw" target="_blank" rel="noopener"><em>How to Draw</em></a> (~$40)</div>
  <div>&#128214; Ivan Brunetti, <a href="https://yalebooks.yale.edu/book/9780300170993/cartooning/" target="_blank" rel="noopener"><em>Cartooning: Philosophy and Practice</em></a> (~$20)</div>
  <div>&#128214; Lynda Barry, <a href="https://drawnandquarterly.com/books/making-comics/" target="_blank" rel="noopener"><em>Making Comics</em></a> (~$25)</div>
  <div>&#128214; Marcos Mateu-Mestre, <a href="https://www.amazon.com/Framed-Ink-Drawing-Composition-Storytellers/dp/1933492953" target="_blank" rel="noopener"><em>Framed Ink</em></a> (~$25)</div>
</div>
<p><strong>Order <em>How to Draw</em> first</strong> &mdash; it&rsquo;s the very next module. Brunetti&rsquo;s
escalating drills, Barry&rsquo;s teaching approach, and Mateu-Mestre&rsquo;s panel-staging system don&rsquo;t
come into play until the comics module, but all four are real, classroom-tested courses in book
form, worth ordering now while shipping catches up.</p>
<h3>Start this now: the 4-minute diary</h3>
<p>Before any fundamentals, start a habit you&rsquo;ll keep for the whole course &mdash; Lynda Barry&rsquo;s
<a href="https://www.openculture.com/2021/09/cartoonist-lynda-barry-teaches-you-how-to-make-a-visual-daily-diary.html" target="_blank" rel="noopener">4-minute diary</a>.
Split a page into four boxes: 7 things you did (2 min), 7 things you saw (2 min), one thing you
overheard (30 sec), and one quick sketch from the day (30 sec).</p>
<div class="callout do"><span class="tag">why it matters</span>
It takes zero drawing skill to start, and it builds the observation and finishing habits that
storytelling actually depends on &mdash; running in parallel with the hand-control drills in the next
module, not after them. Do it a few times a week from here on, for the whole course.</div>
''')

add("lines", "02-marks-and-lines.html", "Marks, lines &amp; confidence", "lines",
    'Scott Robertson &amp; Thomas Bertling, <a href="https://designstudiopress.com/products/how-to-draw" target="_blank" rel="noopener"><em>How to Draw</em></a> (Ch. 1 &amp; 5) &middot; roughly 3&ndash;6 weeks', '''
<p>Work Chapter 1 of <a href="https://designstudiopress.com/products/how-to-draw" target="_blank" rel="noopener"><em>How to Draw</em></a> for confident, unbroken line work and proper
markmaking, then jump ahead to Chapter 5, &ldquo;Ellipses and Rotations,&rdquo; for ellipse control.
Robertson and Bertling both taught for years at Art Center College of Design, and the book
explains the reasoning behind each drill instead of just assigning it.</p>
<div class="callout do"><span class="tag">why it matters</span>
This trains the single most transferable cartooning skill: a confident line and a clean shape
drawn from the shoulder, not a scratchy, hesitant one.</div>
<p>Keep it light &mdash; a page or two per session as your structured half, then go draw cartoons for the rest.</p>
''')

add("construction", "03-construction.html", "Basic construction &amp; 3D forms", "construction",
    '<em>How to Draw</em> (Ch. 2&ndash;4 &amp; 6) &middot; roughly 4&ndash;10 weeks', '''
<p>Work Chapters 2 through 4 of <em>How to Draw</em> &mdash; perspective terminology, technique, and
building your first perspective grids &mdash; then Chapter 6, &ldquo;Working with Volume,&rdquo; for
constructing solid 3D forms inside those grids. Understanding how simple volumes fit together in
space is the backbone of &ldquo;built from shapes&rdquo; cartooning (a head as a rounded box, a body
as a blob).</p>
<div class="callout do"><span class="tag">pace it</span>
This is the densest material in the book. Go slowly and work small &mdash; a page of simple boxes
and cylinders sitting in a grid is plenty per session &mdash; and skip the book&rsquo;s later
vehicle/product-design chapters entirely. A loose cartoonist fakes and stylizes perspective for
expression; you don&rsquo;t need that level of measured precision.</div>
''')

add("perspective", "04-perspective.html", "Just enough perspective", "perspective",
    'Marshall Vandruff&rsquo;s <a href="https://marshallart.gumroad.com/l/wbwxz" target="_blank" rel="noopener">Perspective Drawing Series</a> ($12) &middot; roughly 3&ndash;6 weeks', '''
<p>Learn enough 1- and 2-point perspective to place a character in a room and draw a believable
box, building, or prop. That&rsquo;s the whole goal here.</p>
<h3>The best perspective teacher most people never hear of</h3>
<p>Marshall Vandruff&rsquo;s <a href="https://marshallart.gumroad.com/l/wbwxz" target="_blank" rel="noopener">1994 Perspective Drawing Series</a> &mdash; twelve one-hour lectures recorded
live at Fullerton College &mdash; is widely considered some of the clearest perspective teaching ever
put on video, and it&rsquo;s $12 for the whole series. It explains the <em>why</em> behind the
grid-building you just practiced in the construction module, taught as an actual lecture instead
of a wall of procedural text. Preview his teaching style for free on his
<a href="https://www.youtube.com/@MarshallVandruffVideos" target="_blank" rel="noopener">YouTube channel</a> before buying.</p>
<div class="callout skip"><span class="tag">skip / deprioritize</span>
Lectures 10&ndash;12 (Depth Measuring Systems and Plan Projection) are aimed at technical/product-design
precision &mdash; measuring exact real-world distances into a drawing. Skip them; a cartoonist fakes
and stylizes perspective for expression, not measured accuracy.</div>
<div class="callout do"><span class="tag">free alternatives</span>
<a href="https://www.youtube.com/moderndayjames" target="_blank" rel="noopener">ModernDayJames</a> covers the same 1/2/3-point basics for free on YouTube in a looser,
cartoon-friendly way, and Ernest Norling&rsquo;s classic <a href="https://archive.org/details/perspective-made-easy-by-ernest-r.-norling" target="_blank" rel="noopener"><em>Perspective Made Easy</em></a> (free and legal,
Internet Archive) is a good plain-English companion if you&rsquo;d rather read than watch or pay.</div>
''')

add("gesture", "05-gesture.html", "Gesture &amp; simplified anatomy", "gesture",
    '<a href="https://www.proko.com" target="_blank" rel="noopener">Proko</a>, <a href="https://www.lovelifedrawing.com" target="_blank" rel="noopener">Love Life Drawing</a>, Loomis&rsquo; <a href="https://archive.org/details/andrew-loomis-fun-with-a-pencil" target="_blank" rel="noopener"><em>Fun With a Pencil</em></a> &middot; roughly 8&ndash;12 weeks, then ongoing', '''
<p>This is the pivot away from pure fundamentals drilling and toward cartooning proper.</p>
<ul>
  <li><strong><a href="https://www.youtube.com/playlist?list=PLtG4P3lq8RHEQ1kiN_Nub1vXR8fQQLjDF" target="_blank" rel="noopener">Proko</a></strong> &mdash; free gesture and figure-drawing videos on YouTube. Gesture is the
  single most important skill for expressive cartooning; it&rsquo;s what keeps drawings from looking stiff.</li>
  <li><strong><a href="https://www.lovelifedrawing.com" target="_blank" rel="noopener">Love Life Drawing</a></strong> &mdash; beginner-friendly figure/gesture on YouTube.</li>
  <li><strong><a href="https://line-of-action.com" target="_blank" rel="noopener">Line of Action</a> / <a href="https://www.quickposes.com/en" target="_blank" rel="noopener">Quickposes</a></strong> &mdash; free timed-reference websites. Note: both include nude reference photos by default alongside clothed ones &mdash; both let you filter this in their settings.</li>
  <li><strong>Andrew Loomis, <a href="https://archive.org/details/andrew-loomis-fun-with-a-pencil" target="_blank" rel="noopener"><em>Fun With a Pencil</em></a></strong> &mdash; free and legal on the Internet
  Archive. The first ~30 pages teach cartoon heads and figures via ball-and-plane construction,
  the perfect bridge from fundamentals to cartoon character.</li>
</ul>
<h3>Make it a weekly habit, not a single session</h3>
<p>Gesture doesn&rsquo;t come from one good session &mdash; it comes from a repeated cycle, which is exactly
how it was actually taught. For twenty years, Disney animator Walt Stanchfield ran weekly gesture
classes for the studio&rsquo;s own animators (his students include Glen Keane, Brad Bird, and John
Lasseter): draw from a model, get critiqued, repeat, week after week. His own class handouts are
freely shared online with his family&rsquo;s blessing at
<a href="https://www.thinkinganimation.com/walt-stanchfield-handouts" target="_blank" rel="noopener">Thinking Animation</a> &mdash; read a few alongside your own weekly sessions; they&rsquo;re as much
about attitude as technique.</p>
<div class="callout do"><span class="tag">how to practice</span>
Short timed gestures (30 seconds&ndash;2 minutes), then &ldquo;mannequinize&rdquo; into simple shapes.
Chase flow and exaggeration, not accuracy &mdash; and keep it weekly for the whole course, not just this phase.</div>
<div class="callout skip"><span class="tag">skip / deprioritize</span>
Rigorous &eacute;corch&eacute;/muscle anatomy, &ldquo;100 heads / 100 hands&rdquo; realism challenges, and the
Solo Art Curriculum&rsquo;s multi-term anatomy sequence. You need enough anatomy to caricature it,
not medical accuracy.</div>
''')

add("character", "06-character-design.html", "Character design &amp; stylization", "character",
    '<a href="https://theetheringtonbrothers.blogspot.com/p/every-how-to-think-when-you-draw.html" target="_blank" rel="noopener">Etherington Brothers</a>, <a href="https://www.youtube.com/tonikopantoja" target="_blank" rel="noopener">Toniko Pantoja</a>, <a href="https://www.youtube.com/channel/UC5dyu9y0EV0cSvGtbBtHw_w" target="_blank" rel="noopener">Sycra</a> &middot; ongoing, months', '''
<ul>
  <li><strong>Etherington Brothers, <a href="https://theetheringtonbrothers.blogspot.com/p/every-how-to-think-when-you-draw.html" target="_blank" rel="noopener">&ldquo;How to THINK When You Draw&rdquo;</a></strong> &mdash; 300+ free tutorials,
  including &ldquo;How to draw CHARACTERS (3-Shapes)&rdquo; and &ldquo;(Flipped-Shapes).&rdquo; The richest free
  cartoonist library on the web, made by two working comic artists (Robin &amp; Lorenzo Etherington,
  <em>The Phoenix</em> comic).</li>
  <li><strong><a href="https://www.youtube.com/tonikopantoja" target="_blank" rel="noopener">Toniko Pantoja</a></strong> (YouTube) &mdash; story/animation artist (How to Train Your
  Dragon 3, Trolls, Croods 2); excellent free videos on appealing shape language.</li>
  <li><strong><a href="https://www.youtube.com/channel/UC5dyu9y0EV0cSvGtbBtHw_w" target="_blank" rel="noopener">Sycra</a></strong> (YouTube) &mdash; &ldquo;iterative drawing&rdquo; and shape-design; great for
  developing your own voice through variation rather than copying.</li>
  <li><strong>Study your north stars directly.</strong> Copy frames from Adventure Time,
  Invader Zim, and similar cartoons. Break each character into its underlying simple shapes &mdash;
  Finn is a rounded box, Jake is a fluid blob.</li>
</ul>
<h3>A real, repeatable design drill &mdash; not a one-off</h3>
<p>The Etherington Brothers&rsquo; <a href="https://theetheringtonbrothers.blogspot.com/2018/01/how-to-think-when-you-draw-3-shape.html" target="_blank" rel="noopener">3-Shape Characters</a>
method is built to be run over and over, not done once: split a body into three sections, then
randomly pick each section&rsquo;s height (short/medium/tall) and width (narrow/medium/wide). Every
combination produces a different, usable silhouette. Run it weekly with a fresh random combination
&mdash; it&rsquo;s how the Etheringtons themselves teach building a personal library of shapes fast.</p>
<div class="callout do"><span class="tag">exercises</span>
Run the 3-Shape drill weekly, then draw an expression sheet (and eventually a full turnaround model
sheet) for whichever result you liked best that week &mdash; exactly where your Phase 1&ndash;2 construction
work pays off.</div>
''')

add("comics", "07-comics.html", "Comics: paneling &amp; storytelling", "comics",
    'Brunetti&rsquo;s <em>Cartooning: Philosophy and Practice</em>, <a href="https://www.scottmccloud.com" target="_blank" rel="noopener">Scott McCloud</a>, <a href="https://theetheringtonbrothers.blogspot.com/2020/02/what-free-50-page-how-to-think-when-you.html" target="_blank" rel="noopener">Etherington Brothers</a> &middot; ongoing', '''
<p>This is where everything else pays off &mdash; and where a course stitched from free links alone
falls apart. It can teach panel grammar, but not how to actually finish something. This module
borrows its structure from Ivan Brunetti&rsquo;s <em>Cartooning: Philosophy and Practice</em> (the
book from module 01): a real, classroom-tested escalation from a doodle to a finished short comic,
instead of jumping straight from theory to &ldquo;draw a minicomic.&rdquo;</p>

<h3>Learn the grammar</h3>
<ul>
  <li><strong><a href="https://www.scottmccloud.com" target="_blank" rel="noopener">Scott McCloud</a>, <em>Making Comics</em> &amp; <em>Understanding Comics</em></strong>
  &mdash; the standard texts on panel transitions, gutters, pacing, and expressive acting (library, not free).</li>
  <li><strong>Etherington Brothers&rsquo;</strong> free <a href="https://theetheringtonbrothers.blogspot.com/2020/02/what-free-50-page-how-to-think-when-you.html" target="_blank" rel="noopener">&ldquo;How to THINK when you draw JUNIOR &mdash; How
  to draw COMICS&rdquo;</a> &mdash; a free 50-page ebook walking through a full comic project in short daily sessions.</li>
</ul>

<h3>Script it before you draw it</h3>
<p>A comic is written before it&rsquo;s drawn. Learn the basics of a <a href="https://boords.com/blog/writing-a-comic-book-script-101-expert-storytelling-tips" target="_blank" rel="noopener">comic script</a>:
panel-by-panel descriptions, keeping dialogue to roughly 25 words a balloon, and controlling pace
with panel count &mdash; many small panels reads as fast and urgent, a few big ones slows a moment
down. Then write one full page yourself before pencilling anything.</p>

<h3>Thumbnail before you commit</h3>
<p>Working cartoonists redraw a page&rsquo;s layout several small, rough ways before picking one &mdash;
it&rsquo;s a real, teachable skill, not something that just happens. Frank Santoro&rsquo;s free
<a href="http://www.tcj.com/layout-workbook/frank/" target="_blank" rel="noopener">Layout Workbook</a> column breaks down how professional page compositions actually work.</p>

<h3>Stage each panel, not just the page</h3>
<p>Santoro&rsquo;s workbook is about the whole page; staging is about each individual panel &mdash; where
you put the camera, what&rsquo;s in the foreground, how a silhouette reads at a glance. Marcos
Mateu-Mestre&rsquo;s <a href="https://www.amazon.com/Framed-Ink-Drawing-Composition-Storytellers/dp/1933492953" target="_blank" rel="noopener"><em>Framed Ink</em></a> (~$25, the book from module 01) is the standard
reference working storyboard and comic artists use for exactly this &mdash; shot choice, staging, and
visual clarity, one panel at a time.</p>

<h3>Letter it</h3>
<p>Lettering and balloon placement are their own skill, not an afterthought &mdash; a badly placed
balloon breaks a reader&rsquo;s flow no matter how good the art is. The Center for Cartoon Studies&rsquo;
free <a href="https://www.cartoonstudies.org/wp-content/uploads/2014/06/24.pdf" target="_blank" rel="noopener">Expressive Lettering and Balloons</a> handout is a real classroom exercise, not something we invented.</p>

<h3>Build the ladder</h3>
<p>Instead of one big, scary &ldquo;draw a minicomic&rdquo; leap, finish a series of small things, each
one all the way through &mdash; pencils, inks, letters &mdash; before moving up. This is Brunetti&rsquo;s own
structure:</p>
<blockquote>&ldquo;If you can draw a smiley face and a stick figure, you can start drawing comics.&rdquo;</blockquote>
<div class="callout do"><span class="tag">the ladder</span>
One single-panel gag &rarr; one 4-panel strip &rarr; one full page &rarr; a 4-page minicomic &rarr; an 8-page
minicomic. Finish each rung before climbing &mdash; the finishing habit matters more than the page count.</div>

<h3>Study the real thing</h3>
<p>All three shows had real comic-book runs published by BOOM! Studios&rsquo; all-ages KaBOOM!
imprint, drawn by identifiable people whose process is documented:</p>
<ul>
  <li><strong>Adventure Time</strong> &mdash; <a href="https://comicsalliance.com/adventure-time-25-shelli-paroline-braden-lamb-interview/" target="_blank" rel="noopener">Shelli Paroline &amp; Braden Lamb</a>, the
  Eisner-winning art team, describe splitting script &rarr; layout &rarr; pencils &rarr; inks &rarr; color
  between two people.</li>
  <li><strong>Bravest Warriors</strong> &mdash; <a href="https://www.popoptiq.com/interview-with-bravest-warriors-artist-ian-mcginty/" target="_blank" rel="noopener">Ian McGinty</a> drew the series for about a
  year alongside writer Kate Leth.</li>
  <li><strong>Regular Show</strong> &mdash; <a href="https://comicsalliance.com/allison-strejlau-art/" target="_blank" rel="noopener">Allison Strejlau</a> was the series artist, alongside writer KC Green.</li>
</ul>
<p>Read a few actual issues and copy a page panel-for-panel to see how someone working in exactly
this style solves layout and acting problems.</p>

<h3>Get feedback</h3>
<p>Practice without feedback plateaus. Post one finished piece somewhere real people will critique
it &mdash; <a href="https://www.reddit.com/r/ArtCrit/" target="_blank" rel="noopener">r/ArtCrit</a> or a comics-specific Discord &mdash; instead of only judging your own work. Be honest with
yourself that this is the weakest link in a free curriculum: a genuinely consistent feedback loop
is mostly gated behind a paid critique tier &mdash; a pattern across almost every free-to-start art
platform. Free communities are worth using anyway &mdash; they&rsquo;re just less reliable than that.</p>
''')

add("digital", "08-digital.html", "Transition to digital", "digital",
    '<a href="https://www.youtube.com/playlist?list=PLlpSQCrjuGkriILjGVhAMxaroOgpGDbvl" target="_blank" rel="noopener">Procreate&rsquo;s official Beginners Series</a> &middot; when you&rsquo;re ready', '''
<p><strong>When:</strong> only once you can construct and pose a character from imagination on
paper &mdash; roughly the end of Phase 4, into Phase 5. Digital drawing is a separate motor and
software skill; layering it on too early spends hours you don&rsquo;t have to spare.</p>
<ul>
  <li><strong>Procreate&rsquo;s official <a href="https://www.youtube.com/playlist?list=PLlpSQCrjuGkriILjGVhAMxaroOgpGDbvl" target="_blank" rel="noopener">&ldquo;Beginners Series&rdquo;</a></strong> &mdash; free, four-part, on Procreate&rsquo;s
  own YouTube channel: brushes, layers, gestures, painting and editing tools.</li>
  <li>Free beginner Procreate playlists from creators like <a href="https://www.youtube.com/c/BardotBrush" target="_blank" rel="noopener">Lisa Bardot</a>.</li>
  <li>Free alternatives if you&rsquo;d rather not buy software yet: <strong><a href="https://krita.org" target="_blank" rel="noopener">Krita</a></strong> (desktop) or
  <strong><a href="https://ibispaint.com" target="_blank" rel="noopener">Ibis Paint</a> / <a href="https://medibangpaint.com" target="_blank" rel="noopener">Medibang</a></strong> (tablet).</li>
</ul>
<div class="callout do"><span class="tag">first steps</span>
Re-do a few Phase 1 line/ellipse drills digitally to calibrate to the screen, learn layers
(sketch &rarr; ink &rarr; color), and settle on two or three brushes you like. Don&rsquo;t chase advanced rendering.</div>
<h3>Color it: flatting basics</h3>
<p>Once your layer workflow is comfortable, learn <strong>flatting</strong> &mdash; filling each area of
your linework with a flat, solid color on its own layer before any shading. It&rsquo;s the standard
first step in digital comic coloring, and the difference between a coloring session that takes
20 minutes and one that takes 3: <a href="https://www.youtube.com/watch?v=s55gkBwZRU8" target="_blank" rel="noopener">this Procreate walkthrough</a> shows the selection-and-fill method.</p>
<div class="callout do"><span class="tag">keep it simple</span>
Pick 3&ndash;5 colors total for your first colored page. A limited palette forces decisions that
actually read, and it&rsquo;s far more forgiving than choosing from millions of colors with no plan.</div>
<h3>Choosing a palette, not just filling it in</h3>
<p>Flatting is mechanical; picking colors that actually read is a separate skill most free
&ldquo;how to color&rdquo; tutorials skip. Working comic colorist
<a href="https://www.comiccolor.com" target="_blank" rel="noopener">K. Michael Russell</a> teaches color theory alongside flatting for free on his own site and
YouTube &mdash; the same lessons he sells in his paid courses, offered as free trials. The Sequential
Artists Workshop&rsquo;s free <a href="https://www.sequentialartistsworkshop.org/blog/color-in-comics" target="_blank" rel="noopener">&ldquo;How To Color Your Comics&rdquo;</a> is a shorter, practical companion: get
your <em>values</em> right before worrying about which exact hue you picked &mdash; readable line art
beats a pretty palette every time.</p>
''')

add("recs", "09-recommendations.html", "Putting it together", "recs", None, '''
<h3>Start this week</h3>
<ul>
  <li>Order <em>How to Draw</em> by Scott Robertson &amp; Thomas Bertling today &mdash; it&rsquo;s the very
  next module. Buy a fineliner pen and cheap paper while you wait for it to ship.</li>
  <li>Begin Phase 1 at two short sessions a week, always splitting time with fun cartoon doodling.</li>
  <li>Order Brunetti&rsquo;s <em>Cartooning: Philosophy and Practice</em>, Barry&rsquo;s <em>Making
  Comics</em>, and Mateu-Mestre&rsquo;s <em>Framed Ink</em> now (~$70 total) &mdash; you won&rsquo;t open them
  for a while, but shipping takes time.</li>
  <li>Start Lynda Barry&rsquo;s 4-minute diary this week &mdash; it needs no drawing skill and runs
  alongside everything else, for the whole course.</li>
</ul>
<h3>How you&rsquo;ll know it&rsquo;s time to move on</h3>
<ul>
  <li><strong>Past Phase 1&ndash;2</strong> &mdash; your lines are noticeably more confident and a box or
  cylinder &ldquo;sits&rdquo; believably in 3D. Don&rsquo;t wait for perfection.</li>
  <li><strong>Don&rsquo;t try to master every grid-construction method in <em>How to Draw</em>.</strong>
  Once basic one- and two-point boxes click, move to the perspective module and start applying it
  loosely &mdash; precision grids are a means, not the goal, for a cartoonist.</li>
  <li><strong>Spend the bulk of your years in Phases 4&ndash;6</strong> &mdash; gesture, character design,
  comics. This is what actually makes a cartoonist.</li>
</ul>
<h3>Adjust as you go</h3>
<ul>
  <li>Dreading practice? Increase the play half, drop the most tedious exercise, draw more of
  your own characters.</li>
  <li>Figures feel stiff or floaty? Double down on gesture (Phase 4) &mdash; the highest-leverage fix.</li>
  <li>Already drawing confident shapes? Compress Phases 1&ndash;3 and jump toward gesture and
  character design faster.</li>
</ul>
''')

add("caveats", "10-caveats.html", "Caveats worth remembering", "caveats", None, '''
<div class="caveat-box">
<ul style="margin:0; padding-left:20px;">
  <li><strong>Swapping out Drawabox is a real trade-off, not a consensus call.</strong> It&rsquo;s
  free, thorough, and plenty of successful artists swear by it &mdash; this course dropped it as the
  default path because its dense, procedural writing style was a genuine dealbreaker for the
  person this course was built for, not because the underlying drills are bad. If Drawabox is
  working for you, there&rsquo;s no reason to switch.</li>
  <li><strong>Free-book legality varies by title and country.</strong> Treat the <a href="https://archive.org" target="_blank" rel="noopener">Internet
  Archive</a> as the safest free reading source for Loomis and Norling; buy in print if you want certainty.
  McCloud&rsquo;s books are in copyright &mdash; use a library.</li>
  <li><strong>Some &ldquo;free&rdquo; resources have paid upsells &mdash; and some good resources were
  never free.</strong> <a href="https://www.proko.com" target="_blank" rel="noopener">Proko</a> and the Solo Art
  Curriculum surface a lot of free content but also sell premium courses. Marshall Vandruff&rsquo;s
  perspective lectures are $12, not free, and there&rsquo;s no legitimate free copy of Scott
  Robertson&rsquo;s <em>How to Draw</em> &mdash; ignore any &ldquo;free PDF&rdquo; scan you find online; it&rsquo;s
  still in print and in copyright.</li>
  <li><strong>Links and channels change.</strong> If a specific video or playlist has moved,
  search the creator&rsquo;s name directly &mdash; the recommendation still stands even when the URL doesn&rsquo;t.</li>
  <li><strong>This course asks you to spend about $120, deliberately.</strong> Scott Robertson
  &amp; Thomas Bertling&rsquo;s <em>How to Draw</em> (~$40) and Marshall Vandruff&rsquo;s perspective
  lectures ($12) replace what used to be a fully free path through this material &mdash; a
  deliberate trade for teaching quality, not a cost added lightly. Brunetti&rsquo;s
  <em>Cartooning: Philosophy and Practice</em>, Barry&rsquo;s <em>Making Comics</em>, and
  Mateu-Mestre&rsquo;s <em>Framed Ink</em> add another ~$70 for the comics-craft half, chosen
  instead of assembling an equivalent from free YouTube links, which doesn&rsquo;t really exist for
  that material. We looked at pricier structured alternatives too &mdash;
  Proko&rsquo;s Marvel-branded storytelling course ($249) and Frank Santoro&rsquo;s mentored correspondence
  course ($500) &mdash; and skipped both: good programs, but priced for someone making comics a career,
  and the Proko course leans mainstream-superhero rather than the loose cartoon style this course
  targets.</li>
  <li>This is a synthesis of what free resources, a couple of inexpensive books, and their
  communities recommend, not a guarantee of outcomes. Progress depends almost entirely on
  consistent, enjoyable practice sustained over years.</li>
</ul>
</div>
''')

add("about", "11-about.html", "About this course &amp; sources", "about", None, '''
<h3>How this came to be</h3>
<p>This course started from a simple complaint: most &ldquo;learn to draw&rdquo; roadmaps are a pile of
disconnected links, and a single one-off exercise (&ldquo;do a sketch&rdquo;) doesn&rsquo;t actually teach
anything by itself. It was built through an extended back-and-forth between one person who wants to
draw comics in a specific tradition &mdash; the all-ages, cartoon-style comics that ran alongside
shows like <em>Adventure Time</em>, <em>Bravest Warriors</em>, and <em>Regular Show</em> &mdash; and
Claude, an AI assistant, doing the research and drafting.</p>
<p>That means every claim in this course was checked, not invented: real book titles and prices,
Scott Robertson&rsquo;s own published table of contents and Marshall Vandruff&rsquo;s own published
lecture list, real published interviews with the actual artists who drew these comics, and real
class materials from real institutions. Where something couldn&rsquo;t
be verified &mdash; a resource with no identifiable author, a vague &ldquo;there&rsquo;s probably a Discord
for that&rdquo; &mdash; it was either left out or flagged honestly as unverified, rather than presented
as settled fact.</p>

<h3>What we optimized for</h3>
<ul>
  <li><strong>Recurring practice over one-off exercises.</strong> Wherever this course names a
  drill, it tries to name the real, named person or institution who taught it as a repeated habit
  &mdash; Walt Stanchfield&rsquo;s weekly Disney gesture classes, the Etherington Brothers&rsquo; repeatable
  3-Shape method, Lynda Barry&rsquo;s daily 4-minute diary &mdash; instead of a single &ldquo;go draw
  something&rdquo; checkbox.</li>
  <li><strong>Built for one specific style, not a generic artist.</strong> This isn&rsquo;t a
  general concept-art or superhero-comics roadmap with the serial numbers filed off; it&rsquo;s aimed
  at loose, expressive, all-ages cartoon comics, and skips or deprioritizes the fundamentals
  (rigorous anatomy, measured perspective, realistic rendering) that style doesn&rsquo;t need.</li>
  <li><strong>Real, credentialed sources only.</strong> Every named resource traces back to an
  identifiable working artist, a published book, or an established institution &mdash; not an
  anonymous blog or an assembled mixtape of whatever ranked well in a search.</li>
  <li><strong>Free by default, paid when it&rsquo;s actually worth it.</strong> Most of this course
  costs nothing. A small number of real, classroom-tested books and one cheap video series (about
  $120 total across the whole course) were added deliberately where no free equivalent taught as
  well &mdash; while pricier options ($249, $500) were looked at and explicitly turned down as
  overkill for a hobbyist goal.</li>
  <li><strong>Honest about the weak spots.</strong> The &ldquo;skip / contested&rdquo; callouts, the
  caveats page, and the note in the comics module admitting that free critique loops are genuinely
  hard to come by are all here on purpose &mdash; a curriculum that hides its own tradeoffs isn&rsquo;t
  trustworthy. So is swapping a resource out entirely, like dropping Drawabox for a
  clearer-taught (if no longer free) alternative, when it stops working for the person actually
  using this course.</li>
</ul>

<h3>Disclaimers</h3>
<div class="caveat-box">
<ul style="margin:0; padding-left:20px;">
  <li><strong>This is not an accredited program or a single expert&rsquo;s designed course.</strong>
  It&rsquo;s a synthesis, assembled with AI research assistance and cross-checked against real sources,
  built around one person&rsquo;s specific goal &mdash; not a substitute for a mentor, a degree, or a
  paid program if that&rsquo;s what you eventually want.</li>
  <li><strong>Nobody named below endorsed this course.</strong> Creators, authors, and platforms are
  credited because their published work or teaching directly informed a section of this course, not
  because they reviewed, approved, or are affiliated with it.</li>
  <li><strong>Prices, links, and availability change.</strong> Everything was checked at the time
  it was written, but a publisher can raise a price or a channel can move. If something&rsquo;s wrong,
  the recommendation still stands even when the exact URL doesn&rsquo;t.</li>
</ul>
</div>

<h3>Full list of sources &amp; thanks</h3>
<p><strong>Foundations</strong></p>
<ul>
  <li>Scott Robertson &amp; Thomas Bertling, <a href="https://designstudiopress.com/products/how-to-draw" target="_blank" rel="noopener"><em>How to Draw</em></a> (Design Studio Press)</li>
  <li>Marshall Vandruff, <a href="https://marshallart.gumroad.com/l/wbwxz" target="_blank" rel="noopener">1994 Perspective Drawing Series</a></li>
  <li>Andrew Loomis, <em>Fun With a Pencil</em>, via the <a href="https://archive.org/details/andrew-loomis-fun-with-a-pencil" target="_blank" rel="noopener">Internet Archive</a></li>
  <li>Ernest Norling, <em>Perspective Made Easy</em>, via the <a href="https://archive.org/details/perspective-made-easy-by-ernest-r.-norling" target="_blank" rel="noopener">Internet Archive</a></li>
  <li><a href="https://www.youtube.com/moderndayjames" target="_blank" rel="noopener">ModernDayJames</a> (YouTube)</li>
</ul>
<p><strong>Gesture &amp; anatomy</strong></p>
<ul>
  <li>Walt Stanchfield&rsquo;s Disney class notes, freely shared at <a href="https://www.thinkinganimation.com/walt-stanchfield-handouts" target="_blank" rel="noopener">Thinking Animation</a></li>
  <li><a href="https://www.proko.com" target="_blank" rel="noopener">Proko</a></li>
  <li><a href="https://www.lovelifedrawing.com" target="_blank" rel="noopener">Love Life Drawing</a></li>
  <li><a href="https://line-of-action.com" target="_blank" rel="noopener">Line of Action</a> and <a href="https://www.quickposes.com/en" target="_blank" rel="noopener">Quickposes</a></li>
</ul>
<p><strong>Character design &amp; style</strong></p>
<ul>
  <li>Robin &amp; Lorenzo Etherington, <a href="https://theetheringtonbrothers.blogspot.com/p/every-how-to-think-when-you-draw.html" target="_blank" rel="noopener">&ldquo;How to THINK When You Draw&rdquo;</a></li>
  <li><a href="https://www.youtube.com/tonikopantoja" target="_blank" rel="noopener">Toniko Pantoja</a></li>
  <li><a href="https://www.youtube.com/channel/UC5dyu9y0EV0cSvGtbBtHw_w" target="_blank" rel="noopener">Sycra</a></li>
</ul>
<p><strong>Comics craft</strong></p>
<ul>
  <li>Scott McCloud, <a href="https://www.scottmccloud.com" target="_blank" rel="noopener"><em>Making Comics</em> &amp; <em>Understanding Comics</em></a></li>
  <li>Ivan Brunetti, <a href="https://yalebooks.yale.edu/book/9780300170993/cartooning/" target="_blank" rel="noopener"><em>Cartooning: Philosophy and Practice</em></a> (Yale University Press)</li>
  <li>Lynda Barry, <a href="https://drawnandquarterly.com/books/making-comics/" target="_blank" rel="noopener"><em>Making Comics</em></a> (Drawn &amp; Quarterly), and her <a href="https://www.openculture.com/2021/09/cartoonist-lynda-barry-teaches-you-how-to-make-a-visual-daily-diary.html" target="_blank" rel="noopener">4-minute diary</a> as documented by Open Culture</li>
  <li>Marcos Mateu-Mestre, <a href="https://www.amazon.com/Framed-Ink-Drawing-Composition-Storytellers/dp/1933492953" target="_blank" rel="noopener"><em>Framed Ink</em></a> (Design Studio Press)</li>
  <li>Frank Santoro&rsquo;s free <a href="http://www.tcj.com/layout-workbook/frank/" target="_blank" rel="noopener">Layout Workbook</a> column on The Comics Journal</li>
  <li>The Center for Cartoon Studies&rsquo; free <a href="https://www.cartoonstudies.org/wp-content/uploads/2014/06/24.pdf" target="_blank" rel="noopener">Expressive Lettering and Balloons</a> handout</li>
  <li><a href="https://boords.com/blog/writing-a-comic-book-script-101-expert-storytelling-tips" target="_blank" rel="noopener">Boords</a>&rsquo; comic-script-writing guide</li>
</ul>
<p><strong>Studying the target style (BOOM! Studios&rsquo; KaBOOM! imprint)</strong></p>
<ul>
  <li>Shelli Paroline &amp; Braden Lamb, <em>Adventure Time</em> (<a href="https://comicsalliance.com/adventure-time-25-shelli-paroline-braden-lamb-interview/" target="_blank" rel="noopener">interview</a>)</li>
  <li>Ian McGinty, <em>Bravest Warriors</em> (<a href="https://www.popoptiq.com/interview-with-bravest-warriors-artist-ian-mcginty/" target="_blank" rel="noopener">interview</a>)</li>
  <li>Allison Strejlau, <em>Regular Show</em> (<a href="https://comicsalliance.com/allison-strejlau-art/" target="_blank" rel="noopener">interview</a>)</li>
</ul>
<p><strong>Digital &amp; color</strong></p>
<ul>
  <li>Procreate&rsquo;s official <a href="https://www.youtube.com/playlist?list=PLlpSQCrjuGkriILjGVhAMxaroOgpGDbvl" target="_blank" rel="noopener">Beginners Series</a></li>
  <li><a href="https://www.youtube.com/c/BardotBrush" target="_blank" rel="noopener">Lisa Bardot</a></li>
  <li><a href="https://krita.org" target="_blank" rel="noopener">Krita</a>, <a href="https://ibispaint.com" target="_blank" rel="noopener">Ibis Paint</a>, and <a href="https://medibangpaint.com" target="_blank" rel="noopener">Medibang</a> as free alternatives</li>
  <li><a href="https://www.comiccolor.com" target="_blank" rel="noopener">K. Michael Russell</a>, working comic colorist</li>
  <li><a href="https://www.sequentialartistsworkshop.org/blog/color-in-comics" target="_blank" rel="noopener">Sequential Artists Workshop</a></li>
</ul>
<p><strong>Feedback</strong></p>
<ul>
  <li><a href="https://www.reddit.com/r/ArtCrit/" target="_blank" rel="noopener">r/ArtCrit</a></li>
</ul>
<p><strong>Looked at, and deliberately not centered here</strong> &mdash; credited because comparing
against them shaped what this course chose to include:</p>
<ul>
  <li>The <a href="https://www.soloartcurriculum.com/" target="_blank" rel="noopener">Solo Art Curriculum</a> &mdash; excellent, but built for a concept-art/realism artist, not a cartoonist</li>
  <li><a href="https://drawabox.com" target="_blank" rel="noopener">Drawabox</a> (Uncomfortable) &mdash; free, thorough, and it works well for plenty of people; dropped from the main path here because its dense, procedural writing style was a genuine dealbreaker for the person this course was built for, not because the drills themselves are bad</li>
  <li>Proko&rsquo;s Marvel-branded &ldquo;The Art of Storytelling&rdquo; course ($249)</li>
  <li>Frank Santoro&rsquo;s mentored correspondence course ($500)</li>
</ul>
''')

# ---------- progress-tracking checklists ----------
# Each page id maps to a list of entries: (item_id, label) is a checkable
# action; a Section is a non-checkable heading that mirrors a table-of-
# contents group (used to reproduce a source site's own outline exactly).
class Section:
    __slots__ = ("label", "url", "videos")
    def __init__(self, label, url=None, videos=None):
        self.label = label
        self.url = url
        self.videos = videos or []

CHECKLISTS = {
    "rhythm": [
        ("supplies", "Got a fineliner pen, an HB pencil, and cheap paper"),
        ("schedule", "Picked your two weekly session slots"),
        ("diaryhabit", "Started the 4-minute diary habit (keep it going a few times a week)"),
    ],
    "lines": [
        ("ch1read", "Read How to Draw Chapter 1 (materials &amp; markmaking)"),
        ("linedrill", "Practice confident, unbroken line strokes drawn from the shoulder, not the wrist"),
        ("ch5read", "Read How to Draw Chapter 5, &ldquo;Ellipses and Rotations&rdquo;"),
        ("ellipsedrill", "Fill a page with ellipses in a range of degrees and rotations"),
    ],
    "construction": [
        ("ch2read", "Read How to Draw Chapter 2 (perspective terminology)"),
        ("ch3read", "Read How to Draw Chapter 3 (perspective drawing technique)"),
        ("ch4read", "Read How to Draw Chapter 4 and build your first perspective grid"),
        ("ch6read", "Read How to Draw Chapter 6, &ldquo;Working with Volume&rdquo;"),
        ("formdrill", "Draw a page of simple boxes and cylinders sitting inside a perspective grid"),
    ],
    "perspective": [
        ("lecture1", "Lecture 1: Intro to Perspective"),
        ("lecture2", "Lecture 2: Right Angles, Part 1"),
        ("lecture3", "Lecture 3: Right Angles, Part 2"),
        ("lecture4", "Lecture 4: Right Angles, Part 3"),
        ("lecture5", "Lecture 5: Circles &amp; Ellipses, Part 1"),
        ("lecture6", "Lecture 6: Circles &amp; Ellipses, Part 2"),
        ("lecture7", "Lecture 7: Circles &amp; Ellipses, Part 3"),
        ("lecture8", "Lecture 8: Right Angles &amp; Circles Combined"),
        ("lecture9", "Lecture 9: Inclined Planes &amp; The Vanishing Trace"),
        ("roomsketch", "Sketch a character standing in a simple room"),
    ],
    "gesture": [
        ("gesturesession", "Started weekly timed-gesture sessions (Stanchfield&rsquo;s own Disney classes ran the same draw-critique-repeat cycle) &mdash; keep it going"),
        ("prokovideo", "Watch a Proko gesture fundamentals video"),
        ("loomispages", "Read the first ~30 pages of <em>Fun With a Pencil</em>"),
        ("mannequin", "Mannequinize 10 gesture sketches into simple shapes"),
    ],
    "character": [
        ("etherington", "Browse the Etherington Brothers&rsquo; character-shape tutorials"),
        ("shapedrill", "Run the 3-Shape design drill (repeat weekly with a new random combination)"),
        ("expressionsheet", "Draw an expression sheet for your favorite result each week"),
    ],
    "comics": [
        Section("Learn the grammar"),
        ("mccloudread", "Read/skim McCloud on panel transitions"),
        ("comicsebook", "Download the Etherington Brothers&rsquo; free comics ebook"),
        Section("Script it before you draw it"),
        ("scriptbasics", "Learn comic-script basics: panel descriptions &amp; dialogue economy"),
        ("writeonepage", "Write one full page of script before pencilling anything"),
        Section("Thumbnail before you commit"),
        ("thumbnaildrill", "Redraw one page&rsquo;s layout 4&ndash;5 rough ways before picking one"),
        Section("Letter it"),
        ("letteringdrill", "Practice hand-lettering &amp; balloon placement"),
        Section("Build the ladder &mdash; finish each rung: pencils, inks, letters"),
        ("gagpanel", "Finish one single-panel gag"),
        ("fourpanelstrip", "Finish one 4-panel strip"),
        ("onepagecomic", "Finish one full page"),
        ("fourpagemini", "Finish a 4-page minicomic"),
        ("eightpagemini", "Finish an 8-page minicomic"),
        Section("Study the real thing"),
        ("kaboomstudy", "Read a few Adventure Time / Bravest Warriors / Regular Show issues and copy a page"),
        Section("Get feedback"),
        ("getfeedback", "Post one finished piece to a critique community"),
    ],
    "digital": [
        ("procreatepart1", "Watch Procreate Beginners Series, Part One"),
        ("digitaldrill", "Redo a line/ellipse drill digitally"),
        ("layerworkflow", "Set up a sketch &rarr; ink &rarr; color layer workflow"),
        ("brushpicks", "Pick your 2&ndash;3 go-to brushes"),
        ("flattingdrill", "Practice flatting a page: solid color fills before any shading"),
        ("limitedpalette", "Pick a 3&ndash;5 color limited palette for your first colored page"),
        ("colortheory", "Read a real color-theory lesson before picking your palette"),
    ],
}

# Optional per-item external reference links (a lesson page, a video, or both),
# keyed by (page_id, item_id). Filled in module by module.
# A "videos" entry is a dict {"label", "lesson" (optional), "video" (optional)}
# pairing one named exercise/part with its own confirmed reading page and/or
# video.
ITEM_LINKS = {
    ("rhythm", "diaryhabit"): {
        "lesson": "https://www.openculture.com/2021/09/cartoonist-lynda-barry-teaches-you-how-to-make-a-visual-daily-diary.html",
    },
    ("lines", "ch1read"): {
        "lesson": "https://designstudiopress.com/products/how-to-draw",
    },
    ("lines", "ch5read"): {
        "lesson": "https://designstudiopress.com/products/how-to-draw",
    },
    ("construction", "ch2read"): {
        "lesson": "https://designstudiopress.com/products/how-to-draw",
    },
    # The 1994 series is one $12 bundle, not individually-linkable lectures --
    # every checklist item points at the same real, official purchase page.
    ("perspective", "lecture1"): {
        "lesson": "https://marshallart.gumroad.com/l/wbwxz",
    },
    # These two already have real, verified sources named in this page's own
    # prose (a Proko YouTube playlist and the archive.org Loomis scan) -- no
    # need to guess a single specific video out of a whole playlist.
    ("gesture", "gesturesession"): {
        "lesson": "https://www.thinkinganimation.com/walt-stanchfield-handouts",
    },
    ("gesture", "prokovideo"): {
        "video": "https://www.youtube.com/playlist?list=PLtG4P3lq8RHEQ1kiN_Nub1vXR8fQQLjDF",
    },
    ("gesture", "loomispages"): {
        "lesson": "https://archive.org/details/andrew-loomis-fun-with-a-pencil",
    },
    ("character", "etherington"): {
        "lesson": "https://theetheringtonbrothers.blogspot.com/p/every-how-to-think-when-you-draw.html",
    },
    ("character", "shapedrill"): {
        "lesson": "https://theetheringtonbrothers.blogspot.com/2018/01/how-to-think-when-you-draw-3-shape.html",
    },
    ("comics", "mccloudread"): {
        "lesson": "https://www.scottmccloud.com",
    },
    ("comics", "comicsebook"): {
        "lesson": "https://theetheringtonbrothers.blogspot.com/2020/02/what-free-50-page-how-to-think-when-you.html",
    },
    ("comics", "scriptbasics"): {
        "lesson": "https://boords.com/blog/writing-a-comic-book-script-101-expert-storytelling-tips",
    },
    ("comics", "thumbnaildrill"): {
        "lesson": "http://www.tcj.com/layout-workbook/frank/",
    },
    ("comics", "letteringdrill"): {
        "lesson": "https://www.cartoonstudies.org/wp-content/uploads/2014/06/24.pdf",
    },
    ("comics", "kaboomstudy"): {
        "videos": [
            {"label": "Adventure Time &mdash; Shelli Paroline &amp; Braden Lamb", "lesson": "https://comicsalliance.com/adventure-time-25-shelli-paroline-braden-lamb-interview/"},
            {"label": "Bravest Warriors &mdash; Ian McGinty", "lesson": "https://www.popoptiq.com/interview-with-bravest-warriors-artist-ian-mcginty/"},
            {"label": "Regular Show &mdash; Allison Strejlau", "lesson": "https://comicsalliance.com/allison-strejlau-art/"},
        ],
    },
    ("comics", "getfeedback"): {
        "lesson": "https://www.reddit.com/r/ArtCrit/",
    },
    ("digital", "procreatepart1"): {
        "video": "https://www.youtube.com/playlist?list=PLlpSQCrjuGkriILjGVhAMxaroOgpGDbvl",
    },
    ("digital", "flattingdrill"): {
        "video": "https://www.youtube.com/watch?v=s55gkBwZRU8",
    },
    ("digital", "colortheory"): {
        "videos": [
            {"label": "K. Michael Russell &mdash; free color &amp; flatting tutorials", "lesson": "https://www.comiccolor.com/resources"},
            {"label": "Sequential Artists Workshop &mdash; How To Color Your Comics", "lesson": "https://www.sequentialartistsworkshop.org/blog/color-in-comics"},
        ],
    },
}

def tracker_box(page_id):
    items = CHECKLISTS.get(page_id)
    if not items:
        return ""
    rows = ""
    for entry in items:
        if isinstance(entry, Section):
            open_link = f' &middot; <a href="{entry.url}" target="_blank" rel="noopener">Open</a>' if entry.url else ""
            video_links = "".join(
                f' &middot; <a href="{vurl}" target="_blank" rel="noopener">Video: {vlabel}</a>'
                for vlabel, vurl in entry.videos
            )
            rows += f'<div class="track-section">{entry.label}{open_link}{video_links}</div>\n'
            continue
        item_id, label = entry
        cb_id = f"{page_id}-{item_id}"
        links = ITEM_LINKS.get((page_id, item_id))
        links_html = ""
        if links:
            lines = []
            base_parts = []
            if links.get("lesson"):
                base_parts.append(f'<a href="{links["lesson"]}" target="_blank" rel="noopener">Lesson</a>')
            if links.get("video"):
                base_parts.append(f'<a href="{links["video"]}" target="_blank" rel="noopener">Video</a>')
            if base_parts:
                lines.append(" &middot; ".join(base_parts))
            for ex in links.get("videos", []):
                ex_parts = []
                if ex.get("lesson"):
                    ex_parts.append(f'<a href="{ex["lesson"]}" target="_blank" rel="noopener">Lesson</a>')
                if ex.get("video"):
                    ex_parts.append(f'<a href="{ex["video"]}" target="_blank" rel="noopener">Video</a>')
                if ex_parts:
                    lines.append(f'<b>{ex["label"]}:</b> ' + " &middot; ".join(ex_parts))
            if lines:
                joined = "".join(f'<span class="link-line">{l}</span>' for l in lines)
                links_html = f'\n      <span class="item-links">{joined}</span>'
        rows += f'''<div class="track-item">
      <input type="checkbox" id="{cb_id}" data-id="{item_id}" disabled>
      <label for="{cb_id}">{label}</label>{links_html}
    </div>
'''
    return f'''<div class="tracker-box">
    <h3>Track your progress</h3>
    {rows}
    <p class="tracker-note" id="tracker-note">Sign in above to save your progress and sync it across devices.</p>
  </div>'''

TOC_SUBS = {
    "rhythm": "How to structure 1&ndash;3 hours a week, and what to buy",
    "lines": "Confident lines and ellipse control, from a real perspective-drawing textbook",
    "construction": "3D forms and perspective grids, from the same book",
    "perspective": "Just enough 1- and 2-point perspective",
    "gesture": "Movement, flow, and simplified cartoon anatomy",
    "character": "Shape language, expression, and your own style",
    "comics": "Scripting, layout, lettering, and finishing a real minicomic",
    "digital": "Moving from paper to an iPad, when you&rsquo;re ready",
    "recs": "Where to start and how to know it&rsquo;s time to move on",
    "caveats": "What&rsquo;s contested, what changes, what to double-check",
    "about": "How this course was built, the theory behind it, and every source credited",
}

def shell(title, body, page_id=""):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} &mdash; Draw Your Own Comics</title>
{FAVICON_LINKS}
{FONT_LINKS}
<link rel="stylesheet" href="style.css">
</head>
<body data-page-id="{page_id}">
{body}
<script src="progress-schema.js"></script>
<script src="firebase-config.js"></script>
<script src="https://accounts.google.com/gsi/client"></script>
<script type="module" src="app.js"></script>
</body>
</html>
'''

def auth_control():
    # signin-btn is a plain container now, not a button: Google Identity
    # Services renders its own real "Sign in with Google" button (a
    # cross-origin iframe) inside it -- see the note in APP_JS for why.
    return '''<div class="auth-control" id="auth-control">
    <span class="progress-pill" id="header-progress" style="display:none"></span>
    <span id="signin-btn"></span>
    <span class="auth-user" id="auth-user" style="display:none"></span>
    <button class="auth-btn" id="signout-btn" style="display:none">Sign out</button>
  </div>'''

def sitebar():
    return f'''<div class="sitebar">
  <a class="home" href="index.html">{HOME_ICON}Draw Your Own Comics</a>
  {auth_control()}
</div>'''

# ---------- build index.html ----------
toc_items = ""
for i, p in enumerate(PAGES):
    progress_pill = f'<span class="toc-progress" data-progress-for="{p["id"]}"></span>' if p['id'] in CHECKLISTS else ""
    toc_items += f'''<li><a href="{p['file']}">
    <span class="no">{i+1:02d}</span>
    {ICONS[p['icon']]}
    <span class="toc-body">
      <span class="toc-title">{p['title']}</span>
      <span class="toc-sub">{TOC_SUBS[p['id']]}</span>
    </span>
    {progress_pill}
    <span class="toc-arrow">&rarr;</span>
  </a></li>
'''

index_body = f'''
{sitebar()}
<header class="masthead">
  <div class="kicker">
    <svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M8 12h8M12 8v8" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
    A curated, human-made resource curriculum
  </div>
  <h1>Draw your own comics,<br><em>one page at a time.</em></h1>
  <svg class="underline" viewBox="0 0 180 14"><path d="M3 9 C 40 2, 90 14, 130 6 S 175 4, 177 9"/></svg>
  <p class="subhead">
    A sustainable, mostly-free curriculum built from resources other artists actually recommend &mdash;
    tuned for a busy beginner with 1&ndash;3 hours a week whose goal is loose, expressive, stylized comics,
    not photorealism.
  </p>
  <div class="meta-row">
    <div><b>Starting point</b>Complete beginner, pencil &amp; paper</div>
    <div><b>Time budget</b>1&ndash;3 hrs / week</div>
    <div><b>Style range</b>Pendleton Ward &rarr; Dilworth &rarr; Invader Zim</div>
    <div><b>Format</b>11 sections, self-paced, years not weeks</div>
  </div>
</header>

<div class="overall-bar" id="overall-progress">
  <div class="bar-track"><div class="bar-fill"></div></div>
  <div class="bar-label">Sign in above to start tracking your progress.</div>
</div>

<div class="continue-card" id="continue-card" style="display:none">
  <div class="continue-label">Continue where you left off</div>
  <a class="continue-link" id="continue-link" href="#">
    <span class="continue-title"></span>
    <span class="continue-arrow">&rarr;</span>
  </a>
</div>

<div class="wrap">
<section>
  <div class="tldr">
    <h3>The short version</h3>
    <p>You do not need to finish the <a href="https://www.soloartcurriculum.com/" target="_blank" rel="noopener">Solo Art Curriculum</a> &mdash; it&rsquo;s built to
    produce a generalist realism artist over a year or more of near-daily work. Work through Scott
    Robertson &amp; Thomas Bertling&rsquo;s <em>How to Draw</em> for spatial fundamentals, then
    deliberately pivot toward cartooning: Loomis, Proko, the Etherington Brothers, and Scott
    McCloud on comics craft.</p>
    <p>At 1&ndash;3 hrs a week, this is a multi-year hobby, not a bootcamp. Split every session
    roughly 50/50 between structured practice and free drawing from day one, stay on paper through
    character design, and add an iPad only once you can build a character from imagination.</p>
  </div>

  <h3 style="margin-top:40px;">Key findings from the research</h3>
  <ul class="findings">
    <li><span class="fn">1</span><span><strong>A clearly-taught fundamentals book beats a free but
    confusing one.</strong> <em>How to Draw</em>&rsquo;s early chapters transfer to any style; its
    later vehicle and product-design chapters are precision-heavy repetition most cartoonists
    don&rsquo;t need.</span></li>
    <li><span class="fn">2</span><span><strong>The Solo Art Curriculum is excellent, but built for a
    different artist.</strong> Its figure-drawing and character-design units are worth borrowing;
    its anatomy and painting sequence targets concept artists, not cartoonists.</span></li>
    <li><span class="fn">3</span><span><strong>Dedicated cartooning resources already exist and are
    free.</strong> Loomis, the Etherington Brothers, Proko, and McCloud cover exactly the ground a
    comic artist needs.</span></li>
  </ul>

  <h3 style="margin-top:44px;">The eleven sections</h3>
  <ul class="toc">
    {toc_items}
  </ul>
</section>

<footer class="site">
  <p>Compiled from web research into free, community-recommended drawing resources &mdash; September 2026.
  Not a professional curriculum; a personal roadmap built for one specific goal: making comics you&rsquo;re proud of.</p>
</footer>
</div>
'''

with open(f"{OUT}/index.html", "w") as f:
    f.write(shell("Contents", index_body))

# ---------- build each section page ----------
for i, p in enumerate(PAGES):
    prev_p = PAGES[i-1] if i > 0 else None
    next_p = PAGES[i+1] if i < len(PAGES)-1 else None

    pn = '<nav class="pn">'
    if prev_p:
        pn += f'<a href="{prev_p["file"]}"><span class="lbl">&larr; Previous</span>{prev_p["title"]}</a>'
    else:
        pn += '<span></span>'
    if next_p:
        pn += f'<a class="to-next" href="{next_p["file"]}"><span class="lbl">Next &rarr;</span>{next_p["title"]}</a>'
    pn += '</nav>'

    duration_html = f'<div class="duration">{p["duration"]}</div>' if p["duration"] else ''

    body = f'''
{sitebar()}
<div class="wrap">
<section>
  <div class="page-head">
    {ICONS[p['icon']]}
    <h2><span class="no">{i+1:02d}</span>{p['title']}</h2>
  </div>
  {duration_html}
  {p['body']}
  {tracker_box(p['id'])}
</section>
{pn}
<footer class="site"><p><a href="index.html">&larr; Back to the table of contents</a></p></footer>
</div>
'''
    with open(f"{OUT}/{p['file']}", "w") as f:
        f.write(shell(p['title'].replace('&amp;','&'), body, page_id=p['id']))

# ---------- progress-schema.js (single source of truth for counts + page order) ----------
import json
schema_obj = {
    pid: [entry[0] for entry in items if not isinstance(entry, Section)]
    for pid, items in CHECKLISTS.items()
}
page_info = [{"id": p["id"], "file": p["file"], "title": p["title"]} for p in PAGES if p["id"] in CHECKLISTS]
with open(f"{OUT}/progress-schema.js", "w") as f:
    f.write("window.PROGRESS_SCHEMA = " + json.dumps(schema_obj, indent=2) + ";\n")
    f.write("window.PAGE_INFO = " + json.dumps(page_info, indent=2) + ";\n")

# ---------- firebase-config.js (placeholder — edit with your own project's config) ----------
FIREBASE_CONFIG_JS = '''// Paste your Firebase project's web config here.
// Firebase Console > Project settings > General > Your apps > SDK setup and configuration.
// Until apiKey below is filled in, the site works fine but progress tracking stays off.
window.FIREBASE_CONFIG = {
  apiKey: "PASTE_YOUR_API_KEY",
  authDomain: "PASTE_YOUR_PROJECT_ID.firebaseapp.com",
  projectId: "PASTE_YOUR_PROJECT_ID",
  storageBucket: "PASTE_YOUR_PROJECT_ID.appspot.com",
  messagingSenderId: "PASTE_YOUR_SENDER_ID",
  appId: "PASTE_YOUR_APP_ID",
  // Firebase Console > Authentication > Sign-in method > Google > click it
  // > "Web SDK configuration" > Web client ID. Used to sign in via Google
  // Identity Services directly instead of Firebase's own popup/redirect,
  // which silently fails on mobile browsers that block third-party
  // storage between this site's domain and the authDomain above.
  googleClientId: "PASTE_YOUR_GOOGLE_OAUTH_WEB_CLIENT_ID"
};
'''
with open(f"{OUT}/firebase-config.js", "w") as f:
    f.write(FIREBASE_CONFIG_JS)

# ---------- app.js (tracking logic) ----------
APP_JS = '''import { initializeApp } from "https://www.gstatic.com/firebasejs/12.17.1/firebase-app.js";
import {
  getAuth, GoogleAuthProvider, signInWithCredential, signOut, onAuthStateChanged
} from "https://www.gstatic.com/firebasejs/12.17.1/firebase-auth.js";
import {
  getFirestore, doc, setDoc, onSnapshot
} from "https://www.gstatic.com/firebasejs/12.17.1/firebase-firestore.js";

var schema = window.PROGRESS_SCHEMA || {};
var pageId = document.body.getAttribute("data-page-id") || null;

var signinBtn = document.getElementById("signin-btn");
var signoutBtn = document.getElementById("signout-btn");
var authUserEl = document.getElementById("auth-user");
var headerProgressEl = document.getElementById("header-progress");
var trackerNote = document.getElementById("tracker-note");

function totalForPage(pid){ return (schema[pid] || []).length; }
function doneForPage(pid, data){
  var items = (data && data[pid]) || {};
  var n = 0;
  for (var k in items) { if (items[k]) n++; }
  return n;
}
function totalAll(){
  var t = 0;
  for (var pid in schema) t += schema[pid].length;
  return t;
}
function doneAll(data){
  var d = 0;
  for (var pid in schema) d += doneForPage(pid, data);
  return d;
}

function renderChecklist(data){
  if (!pageId) return;
  var items = (data && data[pageId]) || {};
  var boxes = document.querySelectorAll(".track-item input[type=checkbox]");
  for (var i = 0; i < boxes.length; i++){
    var cb = boxes[i];
    cb.checked = !!items[cb.getAttribute("data-id")];
  }
}

function renderProgress(data){
  var total = totalAll(), done = doneAll(data || {});
  if (headerProgressEl){
    headerProgressEl.textContent = total ? (done + "/" + total + " tracked") : "";
    headerProgressEl.style.display = total ? "inline-block" : "none";
  }
  var bar = document.getElementById("overall-progress");
  if (bar){
    var pct = total ? Math.round((done / total) * 100) : 0;
    bar.querySelector(".bar-fill").style.width = pct + "%";
    bar.querySelector(".bar-label").textContent = done + "/" + total + " exercises tracked (" + pct + "%)";
  }
  var pills = document.querySelectorAll("[data-progress-for]");
  for (var i = 0; i < pills.length; i++){
    var node = pills[i];
    var pid = node.getAttribute("data-progress-for");
    var t = totalForPage(pid), d = doneForPage(pid, data || {});
    node.textContent = t ? (d + "/" + t) : "";
    node.classList.toggle("complete", t > 0 && d === t);
  }
}

function renderContinue(data, signedIn){
  var card = document.getElementById("continue-card");
  if (!card) return;
  var pages = window.PAGE_INFO || [];
  if (!signedIn || doneAll(data || {}) === 0){
    card.style.display = "none";
    return;
  }
  var target = null;
  for (var i = 0; i < pages.length; i++){
    var p = pages[i];
    if (doneForPage(p.id, data || {}) < totalForPage(p.id)){ target = p; break; }
  }
  if (!target){
    card.style.display = "none";
    return;
  }
  var link = document.getElementById("continue-link");
  var titleEl = link.querySelector(".continue-title");
  titleEl.innerHTML = target.title;
  link.setAttribute("href", target.file);
  card.style.display = "";
}

function setSignedInUI(user){
  if (user){
    if (signinBtn) signinBtn.style.display = "none";
    if (signoutBtn) signoutBtn.style.display = "";
    if (authUserEl){
      authUserEl.style.display = "";
      authUserEl.textContent = user.displayName ? user.displayName.split(" ")[0] : "Signed in";
    }
  } else {
    if (signinBtn) signinBtn.style.display = "";
    if (signoutBtn) signoutBtn.style.display = "none";
    if (authUserEl) authUserEl.style.display = "none";
  }
  var boxes = document.querySelectorAll(".track-item input[type=checkbox]");
  for (var i = 0; i < boxes.length; i++) boxes[i].disabled = !user;
  if (trackerNote) trackerNote.style.display = user ? "none" : "";
}

var cfg = window.FIREBASE_CONFIG;
var configured = cfg && cfg.apiKey && cfg.apiKey.indexOf("PASTE") === -1;

if (!configured){
  setSignedInUI(null);
  renderProgress({});
  renderContinue({}, false);
  if (signinBtn) signinBtn.textContent = "Tracking not set up yet";
  if (trackerNote) trackerNote.textContent = "Progress tracking isn\\u2019t connected yet \\u2014 see the setup steps to enable it.";
} else {
  var app = initializeApp(cfg);
  var auth = getAuth(app);
  var db = getFirestore(app);
  var unsub = null;

  // Firebase's own popup/redirect sign-in depends on a storage/iframe relay
  // between this site's own domain and the Firebase authDomain (a
  // different origin) to complete. Modern mobile browsers increasingly
  // block that relay as third-party tracking protection (Safari's ITP,
  // Firefox's Total Cookie Protection, etc.), so it fails silently: it
  // looks like it worked, but the result never comes back. Google Identity
  // Services talks to accounts.google.com directly instead (first-party,
  // no relay needed) and hands back an ID token, which we exchange for a
  // Firebase session in one direct call.
  function handleGoogleCredential(response){
    var cred = GoogleAuthProvider.credential(response.credential);
    signInWithCredential(auth, cred).catch(function(e){
      console.error("sign-in failed:", e);
      if (trackerNote){
        trackerNote.style.display = "";
        trackerNote.textContent = "Sign-in didn\\u2019t go through (" + e.code + "). Please try again.";
      }
    });
  }

  var gsi = window.google && window.google.accounts && window.google.accounts.id;
  if (signinBtn && gsi && cfg.googleClientId && cfg.googleClientId.indexOf("PASTE") === -1){
    gsi.initialize({
      client_id: cfg.googleClientId,
      callback: handleGoogleCredential,
      auto_select: false
    });
    gsi.renderButton(signinBtn, { theme: "filled_black", shape: "pill", size: "medium", text: "signin_with" });
  }

  if (signoutBtn) signoutBtn.addEventListener("click", function(){
    signOut(auth);
    if (gsi) gsi.disableAutoSelect();
  });

  var boxes = document.querySelectorAll(".track-item input[type=checkbox]");
  for (var i = 0; i < boxes.length; i++){
    (function(cb){
      cb.addEventListener("change", function(){
        if (!auth.currentUser || !pageId) return;
        var id = cb.getAttribute("data-id");
        var field = pageId + "." + id;
        var payload = {};
        payload[pageId] = {};
        payload[pageId][id] = cb.checked;
        payload.updatedAt = Date.now();
        setDoc(doc(db, "progress", auth.currentUser.uid), payload, { mergeFields: [field, "updatedAt"] })
          .catch(function(e){ console.error("write failed:", e); cb.checked = !cb.checked; });
      });
    })(boxes[i]);
  }

  onAuthStateChanged(auth, function(user){
    setSignedInUI(user);
    if (unsub){ unsub(); unsub = null; }
    if (user){
      unsub = onSnapshot(doc(db, "progress", user.uid), function(snap){
        var data = snap.data() || {};
        renderChecklist(data);
        renderProgress(data);
        renderContinue(data, true);
      });
    } else {
      renderChecklist({});
      renderProgress({});
      renderContinue({}, false);
    }
  });
}
'''
with open(f"{OUT}/app.js", "w") as f:
    f.write(APP_JS)

print("Built", len(PAGES) + 1, "pages + progress-schema.js + firebase-config.js + app.js")
print(os.listdir(OUT))
