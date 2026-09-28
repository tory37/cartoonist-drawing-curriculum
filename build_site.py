import hashlib
import json
import os
import shutil

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site")
os.makedirs(OUT, exist_ok=True)

# Cache-busting query string appended to this site's own CSS/JS asset
# links. Derived from this script's own source, so it changes on every
# content edit -- forcing browsers and GitHub Pages' CDN to fetch fresh
# assets instead of serving a stale cached copy after a deploy.
with open(os.path.abspath(__file__), "rb") as _f:
    BUILD_VERSION = hashlib.sha256(_f.read()).hexdigest()[:10]

# ---------- shared stylesheet ----------
CSS = '''
:root{
  --max:700px;
  color-scheme:dark;
}
*{box-sizing:border-box;}
html{scroll-behavior:smooth;}
body{
  margin:0;
  background:
    radial-gradient(var(--dj-border) 1px, transparent 1.4px) 0 0/22px 22px,
    var(--dj-bg);
  color:var(--dj-text);
  font-family:var(--dj-font-body);
  font-size:17px; line-height:var(--dj-leading-body); -webkit-font-smoothing:antialiased;
}
@media (prefers-reduced-motion: reduce){ *{animation:none !important; transition:none !important;} }
a{color:var(--dj-accent); text-decoration-thickness:1px; text-underline-offset:2px;}
a:hover{color:var(--dj-accent-hi);}

/* small, unlinked brand credit -- see BRANDING.md; the site keeps its own
   name and content, Djaunt just supplies the visual system plus this line */
.dj-credit{
  max-width:var(--max); margin:0 auto; padding:0 24px 28px;
  display:flex; align-items:center; gap:7px;
  font-family:var(--dj-font-mono); font-size:11px; letter-spacing:.08em; text-transform:uppercase;
  color:var(--dj-text-muted); opacity:.7;
}
.dj-credit img{width:14px; height:14px; display:block; opacity:.9;}

/* site header / breadcrumb nav on every page */
.sitebar{
  max-width:var(--max); margin:0 auto; padding:26px 24px 0;
  display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:10px 14px;
  font-size:14px; color:var(--dj-text-muted);
}
.sitebar-links{display:flex; align-items:center; gap:18px; flex-wrap:wrap;}
.sitebar a.home{
  display:flex; align-items:center; gap:8px; color:var(--dj-text); font-weight:600;
  text-decoration:none;
}
.sitebar a.home svg{width:18px; height:18px;}
.sitebar .pos{color:var(--dj-text-muted);}
.nav-link{
  display:flex; align-items:center; gap:6px; color:var(--dj-text-muted); font-weight:500;
  text-decoration:none;
}
.nav-link:hover{color:var(--dj-accent);}

.wrap{max-width:var(--max); margin:0 auto; padding:20px 24px 90px;}

/* .dj-hero / .dj-hero-mark / .dj-hero-lede come from djaunt-branding's
   components/hero/hero.css, linked in shell(). */
.dj-hero{max-width:var(--max); margin:0 auto; padding:40px 24px 8px;}
.dj-hero-mark{
  top:-10%; right:-6%; width:42%; max-width:380px; aspect-ratio:1;
  background-color:var(--dj-accent);
  -webkit-mask:url('djaunt-icon-radiant.svg') no-repeat center / contain;
          mask:url('djaunt-icon-radiant.svg') no-repeat center / contain;
  transform:none;
}
.kicker{
  font-family:var(--dj-font-mono); font-size:var(--dj-text-xs); text-transform:uppercase;
  letter-spacing:var(--dj-tracking-label); color:var(--dj-text-muted);
  display:flex; align-items:center; gap:10px; margin-bottom:18px;
}
.kicker svg{width:20px; height:20px; flex:none;}
h1{
  font-family:var(--dj-font-display); font-weight:700; letter-spacing:var(--dj-tracking-display);
  font-size:clamp(34px, 7vw, 50px); line-height:var(--dj-leading-tight);
  margin:0 0 6px;
}
h1 em{font-style:italic; font-weight:600; color:var(--dj-accent);}
.dj-hero-lede{font-size:19px; max-width:520px; margin:18px 0 28px;}
.underline{width:180px; height:14px; margin-bottom:8px;}
.underline path{
  fill:none; stroke:var(--dj-accent); stroke-width:3; stroke-linecap:round;
}
.meta-row{
  display:flex; flex-wrap:wrap; gap:10px 22px; margin-top:26px; font-size:14px;
  color:var(--dj-text-muted); border-top:1px solid var(--dj-border); padding-top:18px;
}
.meta-row div{display:flex; flex-direction:column; gap:2px;}
.meta-row b{color:var(--dj-text); font-weight:600; font-size:15px;}

section{max-width:var(--max); margin:0 auto; padding:0 24px;}

.page-head{display:flex; align-items:center; gap:14px; margin:18px 0 4px;}
.page-head svg.icon{width:36px; height:36px; flex:0 0 36px; color:var(--dj-accent);}
h2{
  font-family:var(--dj-font-display); font-weight:700; font-size:30px;
  letter-spacing:var(--dj-tracking-display); margin:0; display:flex; align-items:baseline; gap:12px;
}
h2 .no{
  font-family:var(--dj-font-mono); font-weight:500; letter-spacing:.05em;
  color:var(--dj-accent); font-size:16px;
}
.duration{
  display:inline-block; font-size:13.5px; color:var(--dj-text-muted);
  border-left:2px solid var(--dj-border); padding-left:10px; margin:14px 0 26px;
}
h3{font-family:var(--dj-font-display); font-weight:600; letter-spacing:var(--dj-tracking-display); font-size:19px; margin:30px 0 10px;}
p{margin:0 0 16px;}
ul,ol{margin:0 0 16px; padding-left:22px;}
li{margin-bottom:7px;}
strong{font-weight:600;}

/* .dj-callout/.dj-callout-success/.dj-callout-danger/.dj-callout-tag come
   from djaunt-branding's components/callout/callout.css, linked in shell(). */

.tldr{
  background:color-mix(in srgb, var(--dj-accent) 8%, transparent);
  border:1px solid var(--dj-border); border-radius:var(--dj-radius-lg);
  padding:24px 26px; margin:30px 0;
}
.tldr h3{margin-top:0;}

/* .findings uses djaunt-branding's components/divided-list/divided-list.css
   (dj-divided-list dj-divided-list-marked), linked in shell(); this residual
   keeps its framed top+bottom border and wider numbered marker. */
.findings{margin:24px 0;}
.findings .dj-divided-item{
  padding:18px 0; border-top:1px solid var(--dj-border); border-bottom:none;
}
.findings .dj-divided-item:last-child{border-bottom:1px solid var(--dj-border);}
.findings .dj-divided-item-marker{
  font-weight:500; color:var(--dj-accent); font-size:20px; width:34px; min-width:34px;
}

blockquote{
  margin:18px 0; padding:2px 0 2px 18px; border-left:2px solid var(--dj-accent);
  font-size:17.5px; color:var(--dj-text);
}

.supply-grid{display:grid; grid-template-columns:1fr 1fr; gap:10px 24px; margin:18px 0; font-size:15px;}
@media (max-width:520px){.supply-grid{grid-template-columns:1fr;}}

.caveat-box{background:var(--dj-ink-900); border-radius:var(--dj-radius-lg); padding:22px 26px; font-size:15px; color:var(--dj-text-muted);}
.caveat-box li{margin-bottom:10px;}
.caveat-box strong{color:var(--dj-text);}

/* table of contents on index */
.toc{list-style:none; margin:30px 0; padding:0;}
.toc li{border-top:1px solid var(--dj-border);}
.toc li:last-child{border-bottom:1px solid var(--dj-border);}
.toc a{
  display:flex; flex-direction:column; gap:10px; padding:20px 4px; text-decoration:none;
  color:var(--dj-text);
}
.toc a:hover{color:var(--dj-accent);}
.toc a:hover .toc-title{color:var(--dj-accent);}
.toc-head{display:flex; align-items:center; justify-content:space-between; gap:12px;}
.toc-marker{display:flex; align-items:center; gap:8px;}
.toc svg.icon{width:19px; height:19px; flex:none; color:var(--dj-accent);}
.toc .no{
  font-family:var(--dj-font-mono); font-weight:500; color:var(--dj-accent); font-size:14px; flex:none;
}
.toc-status{display:flex; align-items:center; gap:10px;}
.toc-title{font-family:var(--dj-font-display); font-weight:700; font-size:21px; line-height:1.22; letter-spacing:var(--dj-tracking-display); display:block;}
.toc-sub{font-size:14.5px; color:var(--dj-text-muted); line-height:1.5;}
.toc-arrow{color:var(--dj-text-muted); flex:none; display:flex;}

/* prev / next footer nav */
nav.pn{
  max-width:var(--max); margin:50px auto 0; padding:22px 24px 0;
  border-top:1px solid var(--dj-border);
  display:flex; justify-content:space-between; gap:16px; font-size:14.5px;
}
nav.pn a{text-decoration:none; max-width:46%;}
nav.pn .lbl{display:block; font-size:12px; color:var(--dj-text-muted); margin-bottom:3px;}
nav.pn .to-next{margin-left:auto; text-align:right;}

footer.site{
  max-width:var(--max); margin:40px auto 0; padding:24px 24px 40px;
  font-size:13px; color:var(--dj-text-muted);
}

/* "start here" card (index page) */
.continue-card{max-width:var(--max); margin:18px auto 0; padding:0 24px;}
.continue-card .continue-label{
  font-size:12px; color:var(--dj-text-muted); margin-bottom:6px;
  text-transform:uppercase; letter-spacing:.04em;
}
.continue-link{
  display:flex; align-items:center; justify-content:space-between; gap:14px;
  background:color-mix(in srgb, var(--dj-success) 10%, transparent);
  border:1px solid var(--dj-success); border-radius:var(--dj-radius-md);
  padding:16px 20px; text-decoration:none; color:var(--dj-text);
}
.continue-link:hover{background:color-mix(in srgb, var(--dj-success) 16%, transparent);}
.continue-link:hover .continue-title{color:var(--dj-text);}
.continue-title{font-family:var(--dj-font-display); font-weight:600; font-size:18px;}
.continue-arrow{color:var(--dj-success); flex:none; font-size:20px;}

/* current module in the table of contents */
.toc-now .toc-title{color:var(--dj-success);}

/* "not started yet" note at the top of modules not reached yet */
.upcoming-note{margin:4px 0 26px;}
.page-badge{margin:0 0 0 auto; align-self:center;}

/* steps list on each module (plain list, no tracking) */
.steps-box{
  margin:34px 0 6px; border:1px solid var(--dj-border); border-radius:var(--dj-radius-lg);
  padding:22px 24px; background:var(--dj-surface);
}
.steps-box h3{margin-top:0;}
.steps-box ul{margin:0; padding-left:20px; font-size:15px;}
.steps-box li{margin-bottom:10px;}
.steps-box li:last-child{margin-bottom:0;}
.step-section{
  list-style:none; margin-left:-20px; font-weight:600; font-size:13px; text-transform:uppercase;
  letter-spacing:.03em; color:var(--dj-text-muted); padding-top:12px; margin-top:6px;
  border-top:1px solid var(--dj-border);
}
.step-section:first-child{padding-top:0; margin-top:0; border-top:none;}
.item-links{display:flex; flex-direction:column; gap:2px; margin-top:3px; font-size:12px; color:var(--dj-text-muted);}
.item-links a{color:var(--dj-text-muted);}
.item-links a:hover{color:var(--dj-success);}
.item-links b{font-weight:600; color:var(--dj-text);}

/* playlist cards on the current-phase page */
.track-card{
  border:1px solid var(--dj-border); border-radius:var(--dj-radius-lg); background:var(--dj-surface);
  padding:20px 22px; margin:16px 0;
}
.track-card h3{margin-top:0;}
.track-card p:last-child{margin-bottom:0;}

@media print{
  .sitebar, nav.pn, .continue-card, .dj-credit{display:none;}
  a{color:var(--dj-text); text-decoration:none;}
}
'''

with open(f"{OUT}/style.css", "w") as f:
    f.write(CSS)

# ---------- favicon / home-screen icons ----------
# These are the real Djaunt dragon mark (github.com/tory37/djaunt-branding),
# not something a script can derive procedurally the way a simple placeholder
# shape could be. They're pre-rendered once from that repo's
# brand/favicon/{favicon,maskable}.svg via headless Chromium (no image
# libraries are available in this environment) and checked into this repo as
# static files, then just copied into the build output here -- the same
# "real asset lives outside the generator" pattern firebase-config.js uses.
# If the brand assets ever change, re-render and re-commit these; nothing
# below regenerates them.
_ICON_FILES = [
    "favicon.ico", "favicon.svg", "icon-16.png", "icon-32.png",
    "icon-192.png", "icon-512.png", "icon-512-maskable.png",
    "apple-touch-icon.png", "djaunt-icon-radiant.svg",
]
_ROOT = os.path.dirname(os.path.abspath(__file__))
for _name in _ICON_FILES:
    shutil.copy2(os.path.join(_ROOT, _name), os.path.join(OUT, _name))

MANIFEST = {
    "name": "Draw Your Own Comics",
    "short_name": "Draw Comics",
    "description": "A curated, human-made curriculum for drawing your own comics.",
    "start_url": "index.html",
    "scope": ".",
    "display": "standalone",
    "background_color": "#12100A",
    "theme_color": "#12100A",
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
<link href="https://fonts.googleapis.com/css2?family=Archivo:ital,wght@0,600;0,700;1,600&family=IBM+Plex+Sans:wght@400;500&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">'''

FAVICON_LINKS = '''<link rel="icon" type="image/svg+xml" href="favicon.svg">
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="16x16" href="icon-16.png">
<link rel="icon" type="image/png" sizes="32x32" href="icon-32.png">
<link rel="apple-touch-icon" sizes="180x180" href="apple-touch-icon.png">
<link rel="manifest" href="manifest.webmanifest">
<meta name="theme-color" content="#12100A">
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
PAGES = []  # filled below, list of dicts: id, file, title, icon, duration, body, status

# This plan is edited live as it gets worked through: modules that were done
# describe what actually happened, and later modules get kept, changed, or
# swapped out when they're reached. status is one of:
#   "done"     -- worked through.
#   "current"  -- being worked through now (the "Continue" link points here).
#   "upcoming" -- not reached yet; the plan as it stands, open to change.
#   None       -- not a module (recommendations / caveats / about).
def add(id, file, title, icon, duration, body, status="upcoming"):
    PAGES.append(dict(id=id, file=file, title=title, icon=icon, duration=duration, body=body, status=status))

DRAWABOX_URL = "https://drawabox.com"
DLAS_URL = "https://youtube.com/playlist?list=PL0V_JTTg_6baV8tBE4Qm1O8Vhxy59GTah"
PETER_HAN_URL = "https://youtube.com/playlist?list=PLqR-aNpyEIVd91GCwsyOS3oRn6eoRhyio"
HOW_TO_DRAW_URL = "https://designstudiopress.com/products/how-to-draw"

def ext(url, text):
    return f'<a href="{url}" target="_blank" rel="noopener">{text}</a>'

add("rhythm", "01-rhythm.html", "Getting set up", "rhythm",
    f'The start of {ext(DRAWABOX_URL, "Drawabox")} &middot; a week or two', f'''
<h3>The very beginning of Drawabox</h3>
<p>Read the opening material of {ext(DRAWABOX_URL, "Drawabox")}: materials, how to hold the pen, and
drawing from your shoulder instead of your wrist. That&rsquo;s all you need from it &mdash; the setup
basics and some ideas about arm movement. You don&rsquo;t need to go further into its lessons or do
the 250 box challenge.</p>

<h3>Fitting it in</h3>
<p>There&rsquo;s no schedule to keep. Draw as much as you can, wherever you can fit it in.</p>
<ul>
  <li><strong>Small sessions count.</strong> Ten minutes with a pen between other things is real
  practice. Something is always better than nothing, and a lot of small sessions add up.</li>
  <li><strong>Take the long sessions when you get them</strong>, but don&rsquo;t wait for one to start.</li>
  <li><strong>Missed a few days? Just pick it back up.</strong> There&rsquo;s nothing to catch up on.</li>
  <li><strong>When there&rsquo;s time, split it roughly 50/50</strong> &mdash; structured practice from your current module, then free &ldquo;play&rdquo;: doodle your own characters, copy cartoons you love, sketch from shows.</li>
  <li><strong>Don&rsquo;t chase finished pieces early.</strong> The reps are the point, not the polish.</li>
  <li><strong>Expect each module to take months.</strong> That&rsquo;s normal, and it&rsquo;s what makes this sustainable for five years instead of five weeks.</li>
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

<h3>Books worth having</h3>
<div class="supply-grid">
  <div>&#128214; Scott Robertson &amp; Thomas Bertling, {ext(HOW_TO_DRAW_URL, "<em>How to Draw</em>")} (~$40)</div>
  <div>&#128214; Ivan Brunetti, <a href="https://yalebooks.yale.edu/book/9780300170993/cartooning/" target="_blank" rel="noopener"><em>Cartooning: Philosophy and Practice</em></a> (~$20)</div>
  <div>&#128214; Lynda Barry, <a href="https://drawnandquarterly.com/books/making-comics/" target="_blank" rel="noopener"><em>Making Comics</em></a> (~$25)</div>
  <div>&#128214; Marcos Mateu-Mestre, <a href="https://www.amazon.com/Framed-Ink-Drawing-Composition-Storytellers/dp/1933492953" target="_blank" rel="noopener"><em>Framed Ink</em></a> (~$25)</div>
</div>
<p><strong><em>How to Draw</em></strong> is a respected perspective and form textbook &mdash; Robertson and
Bertling both taught for years at Art Center College of Design. It&rsquo;s recommended, but as a
reference to dip into, not the main path: it gets dry fast for a beginner, and the playlists in the
next module turned out to be a better way in. Brunetti, Barry, and Mateu-Mestre don&rsquo;t come into
play until the comics module.</p>

<h3>Worth considering: the 4-minute diary</h3>
<p>Lynda Barry&rsquo;s
<a href="https://www.openculture.com/2021/09/cartoonist-lynda-barry-teaches-you-how-to-make-a-visual-daily-diary.html" target="_blank" rel="noopener">4-minute diary</a>:
split a page into four boxes &mdash; 7 things you did (2 min), 7 things you saw (2 min), one thing you
overheard (30 sec), and one quick sketch from the day (30 sec).</p>
<div class="dj-callout dj-callout-success"><span class="dj-callout-tag">why it&rsquo;s here</span>
It takes zero drawing skill, and it builds the observation and finishing habits that storytelling
depends on. It isn&rsquo;t required to move on &mdash; keep it on the list and pick it up whenever it
fits, a few times a week.</div>
''', status="done")

add("learn", "02-learning-to-draw.html", "Learning to draw", "lines",
    f'{ext(DLAS_URL, "Draw Like a Sir")} + {ext(PETER_HAN_URL, "Peter Han")} &middot; as long as it takes', f'''
<p>The big, general &ldquo;learn to draw&rdquo; module &mdash; lines, shapes, form, and space, before
anything specific to comics or cartooning. It&rsquo;s built on two YouTube playlists worked through side
by side.</p>

<div class="track-card">
  <h3>{ext(DLAS_URL, "Draw Like a Sir")}</h3>
  <p>An excellent, very well produced guide to the concepts. Each video lays out what to work on, but
  it isn&rsquo;t a homework channel &mdash; it assumes you&rsquo;ll go find your own practice material for
  the ideas it introduces.</p>
</div>
<div class="track-card">
  <h3>{ext(PETER_HAN_URL, "Peter Han&rsquo;s course")}</h3>
  <p>More focused on direct instruction and homework: concrete exercises to practice. Lean on it for
  structured practice.</p>
</div>

<h3>How to work through them</h3>
<div class="dj-callout dj-callout-success"><span class="dj-callout-tag">the loop</span>
Watch both playlists in order. Take the next video (or so) from each, then stop and practice what it
covered. Don&rsquo;t move on until you have some real proficiency with it &mdash; not mastery, just the
feeling that you can do it on purpose. That might take one week, two weeks, or longer. Then watch the
next video in each and repeat.</div>
<ul>
  <li><strong>Proficiency, not mastery.</strong> You&rsquo;ll keep coming back to every one of these
  ideas for years. The bar for moving on is &ldquo;I get it and can do it reasonably,&rdquo; not
  &ldquo;it&rsquo;s perfect.&rdquo;</li>
  <li><strong>Solo research is the key skill here.</strong> Neither playlist hands you everything you
  need to practice, Draw Like a Sir especially. When a concept doesn&rsquo;t click, or you run out of
  things to draw, go look it up: other tutorials on the same topic, drills and worksheets, reference
  photos, other artists&rsquo; takes. Finding your own practice material is part of the work.</li>
  <li><strong>Build your own warm-up toolkit.</strong> This plan gives you the bones; the specifics
  are yours. When you find a drill worth coming back to, write it down somewhere you&rsquo;ll see it
  and use it to warm up. Your list will look different from anyone else&rsquo;s, and that&rsquo;s the point.</li>
  <li><strong>Mix drills and play.</strong> Drill the concept, then use it in drawings you actually
  want to make.</li>
</ul>

<h3>Companion reading</h3>
<p>{ext(HOW_TO_DRAW_URL, "<em>How to Draw</em>")} covers much of the same ground &mdash; confident lines,
ellipses, perspective boxes &mdash; with the reasoning behind each drill. This module originally started
with its Chapters 1 and 5, but the book is dry as a starting point, so the playlists took over as the
main path. Keep it around to look things up or go deeper when a topic grabs you.</p>
''', status="current")

add("construction", "03-construction.html", "Basic construction &amp; 3D forms", "construction",
    '<a href="https://www.youtube.com/channel/UC5dyu9y0EV0cSvGtbBtHw_w" target="_blank" rel="noopener">Sycra</a> (YouTube, free) &middot; roughly 3&ndash;6 weeks', '''
<p>Watch Sycra&rsquo;s <a href="https://www.youtube.com/watch?v=j2KVnOfyAIE" target="_blank" rel="noopener">&ldquo;The Importance of Construction in Drawing&rdquo;</a> &mdash; free, and it teaches
exactly the &ldquo;built from shapes&rdquo; thinking cartooning actually needs: run a simple line of
action through a form, then wrap simple solids (spheres, cylinders, boxes) around it. No
vanishing-point math required.</p>
<div class="dj-callout dj-callout-success"><span class="dj-callout-tag">why it matters</span>
This is the mental model behind every cartoon character in this style: a head is a rounded box, a
body is a blob or a sausage, a prop is two or three overlapping simple solids. Once this clicks,
gesture and character design (the next two modules) get dramatically easier.</div>
<p>Practice on ordinary objects around you before jumping to characters &mdash; a mug, a shoe, a
lamp. Simple, everyday subjects make the &ldquo;shapes stacked in space&rdquo; logic obvious.</p>
''')

add("perspective", "04-perspective.html", "Just enough perspective", "perspective",
    'The Etherington Brothers&rsquo; free perspective tutorials &middot; roughly 2&ndash;4 weeks', '''
<p>Learn enough 1- and 2-point perspective to place a character in a room and draw a believable
box, building, or prop. That&rsquo;s the whole goal here.</p>
<p>The Etherington Brothers &mdash; already your character-design resource later in this course &mdash;
have their own free, cartoon-native perspective tutorials: <a href="http://theetheringtonbrothers.blogspot.com/2019/09/how-to-think-when-you-draw-1-point.html" target="_blank" rel="noopener">1-point perspective</a>
(<a href="http://theetheringtonbrothers.blogspot.com/2019/09/how-to-think-when-you-draw-1-point_8.html" target="_blank" rel="noopener">part two</a>), <a href="http://theetheringtonbrothers.blogspot.com/2022/12/how-to-think-when-you-draw-2-point.html" target="_blank" rel="noopener">2-point perspective</a>, and
<a href="http://theetheringtonbrothers.blogspot.com/2021/11/how-to-think-when-you-draw-perspective.html" target="_blank" rel="noopener">perspective boxes</a>. Visual, practical, and built for exactly this
style &mdash; no textbook or lecture series required.</p>
<div class="dj-callout dj-callout-success"><span class="dj-callout-tag">free alternatives</span>
<a href="https://www.youtube.com/moderndayjames" target="_blank" rel="noopener">ModernDayJames</a> covers the same ground for free on YouTube in a looser way, and Ernest
Norling&rsquo;s classic <a href="https://archive.org/details/perspective-made-easy-by-ernest-r.-norling" target="_blank" rel="noopener"><em>Perspective Made Easy</em></a> (free and legal, Internet Archive) is a
good plain-English companion if you&rsquo;d rather read than watch.</div>
<div class="dj-callout dj-callout-danger"><span class="dj-callout-tag">optional deep dive</span>
If perspective genuinely clicks for you and you want to go further, Marshall Vandruff&rsquo;s
<a href="https://marshallart.gumroad.com/l/wbwxz" target="_blank" rel="noopener">1994 Perspective Drawing Series</a> ($12, 12 lectures) is some of the clearest, most in-depth
perspective teaching ever recorded &mdash; but it&rsquo;s well past what a cartoonist strictly needs,
so treat it as optional, not required.</div>
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
<a href="https://www.thinkinganimation.com/walt-stanchfield-handouts" target="_blank" rel="noopener">Thinking Animation</a> &mdash; read a few alongside your own gesture practice; they&rsquo;re as much
about attitude as technique.</p>
<div class="dj-callout dj-callout-success"><span class="dj-callout-tag">how to practice</span>
Short timed gestures (30 seconds&ndash;2 minutes), then &ldquo;mannequinize&rdquo; into simple shapes.
Chase flow and exaggeration, not accuracy &mdash; and keep it weekly for the whole course, not just this phase.</div>
<div class="dj-callout dj-callout-danger"><span class="dj-callout-tag">skip / deprioritize</span>
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
<div class="dj-callout dj-callout-success"><span class="dj-callout-tag">exercises</span>
Run the 3-Shape drill weekly, then draw an expression sheet (and eventually a full turnaround model
sheet) for whichever result you liked best that week &mdash; exactly where your module 02&ndash;03 construction
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
<div class="dj-callout dj-callout-success"><span class="dj-callout-tag">the ladder</span>
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
paper &mdash; roughly the end of module 05, into module 06. Digital drawing is a separate motor and
software skill; layering it on too early spends hours you don&rsquo;t have to spare.</p>
<ul>
  <li><strong>Procreate&rsquo;s official <a href="https://www.youtube.com/playlist?list=PLlpSQCrjuGkriILjGVhAMxaroOgpGDbvl" target="_blank" rel="noopener">&ldquo;Beginners Series&rdquo;</a></strong> &mdash; free, four-part, on Procreate&rsquo;s
  own YouTube channel: brushes, layers, gestures, painting and editing tools.</li>
  <li>Free beginner Procreate playlists from creators like <a href="https://www.youtube.com/c/BardotBrush" target="_blank" rel="noopener">Lisa Bardot</a>.</li>
  <li>Free alternatives if you&rsquo;d rather not buy software yet: <strong><a href="https://krita.org" target="_blank" rel="noopener">Krita</a></strong> (desktop) or
  <strong><a href="https://ibispaint.com" target="_blank" rel="noopener">Ibis Paint</a> / <a href="https://medibangpaint.com" target="_blank" rel="noopener">Medibang</a></strong> (tablet).</li>
</ul>
<div class="dj-callout dj-callout-success"><span class="dj-callout-tag">first steps</span>
Re-do a few of your own line/ellipse warm-ups digitally to calibrate to the screen, learn layers
(sketch &rarr; ink &rarr; color), and settle on two or three brushes you like. Don&rsquo;t chase advanced rendering.</div>
<h3>Color it: flatting basics</h3>
<p>Once your layer workflow is comfortable, learn <strong>flatting</strong> &mdash; filling each area of
your linework with a flat, solid color on its own layer before any shading. It&rsquo;s the standard
first step in digital comic coloring, and the difference between a coloring session that takes
20 minutes and one that takes 3: <a href="https://www.youtube.com/watch?v=s55gkBwZRU8" target="_blank" rel="noopener">this Procreate walkthrough</a> shows the selection-and-fill method.</p>
<div class="dj-callout dj-callout-success"><span class="dj-callout-tag">keep it simple</span>
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

add("recs", "09-recommendations.html", "Putting it together", "recs", None, status=None, body='''
<h3>Start this week</h3>
<ul>
  <li>Grab a fineliner pen and cheap paper, and read the opening of Drawabox (module 01).</li>
  <li>Start the Draw Like a Sir and Peter Han playlists (module 02), drawing whenever you can fit it
  in &mdash; even short sessions count &mdash; and mixing in fun cartoon doodling.</li>
  <li>Consider Lynda Barry&rsquo;s 4-minute diary &mdash; it needs no drawing skill and can run
  alongside everything else.</li>
</ul>
<h3>How you&rsquo;ll know it&rsquo;s time to move on</h3>
<ul>
  <li><strong>Past modules 02&ndash;03</strong> &mdash; your lines are noticeably more confident and a box or
  cylinder &ldquo;sits&rdquo; believably in 3D. Don&rsquo;t wait for perfection.</li>
  <li><strong>Don&rsquo;t chase perfect construction before moving on.</strong> Once a simple object
  built from a couple of overlapping shapes reads believably, move to the perspective module and
  start applying it loosely &mdash; precision is a means, not the goal, for a cartoonist.</li>
  <li><strong>Spend the bulk of your years in modules 05&ndash;07</strong> &mdash; gesture, character design,
  comics. This is what actually makes a cartoonist.</li>
</ul>
<h3>Adjust as you go</h3>
<ul>
  <li>This plan gets edited as it&rsquo;s worked through. If a resource isn&rsquo;t working, look for a
  better one and swap it in &mdash; that&rsquo;s how module 02 came to be built on two YouTube playlists
  instead of a textbook.</li>
  <li>Dreading practice? Increase the play half, drop the most tedious exercise, draw more of
  your own characters.</li>
  <li>Figures feel stiff or floaty? Double down on gesture (module 05) &mdash; the highest-leverage fix.</li>
  <li>Already drawing confident shapes? Compress modules 02&ndash;04 and jump toward gesture and
  character design faster.</li>
</ul>
''')

add("caveats", "10-caveats.html", "Caveats worth remembering", "caveats", None, status=None, body='''
<div class="caveat-box">
<ul style="margin:0; padding-left:20px;">
  <li><strong>Only using the start of Drawabox is a real trade-off, not a consensus call.</strong>
  It&rsquo;s free, thorough, and plenty of successful artists swear by it. Its opening material
  (materials, pen grip, drawing from the shoulder) was genuinely useful here; the rest of the course
  wasn&rsquo;t the right fit for the person this site is built for, which isn&rsquo;t a judgment on the
  drills themselves. If Drawabox is working for you, there&rsquo;s no reason to switch.</li>
  <li><strong>Modules you haven&rsquo;t reached yet are the plan as it stands.</strong> They come from
  research, not experience, and real learning rarely follows a plan made in advance &mdash; expect
  them to change, get skipped, or get replaced once you actually get there.</li>
  <li><strong>Free-book legality varies by title and country.</strong> Treat the <a href="https://archive.org" target="_blank" rel="noopener">Internet
  Archive</a> as the safest free reading source for Loomis and Norling; buy in print if you want certainty.
  McCloud&rsquo;s books are in copyright &mdash; use a library.</li>
  <li><strong>Some &ldquo;free&rdquo; resources have paid upsells &mdash; and some good resources were
  never free.</strong> <a href="https://www.proko.com" target="_blank" rel="noopener">Proko</a> and the Solo Art
  Curriculum surface a lot of free content but also sell premium courses. There&rsquo;s no legitimate
  free copy of Scott Robertson&rsquo;s <em>How to Draw</em> &mdash; ignore any &ldquo;free PDF&rdquo; scan
  you find online; it&rsquo;s still in print and in copyright. Marshall Vandruff&rsquo;s perspective
  lectures, mentioned as an optional deep dive, are $12 &mdash; nothing in the required path costs
  money except the books below.</li>
  <li><strong>Links and channels change.</strong> If a specific video or playlist has moved,
  search the creator&rsquo;s name directly &mdash; the recommendation still stands even when the URL doesn&rsquo;t.</li>
  <li><strong>The books are the only real cost.</strong> Scott Robertson &amp; Thomas
  Bertling&rsquo;s <em>How to Draw</em> (~$40) is recommended as a companion reference rather than
  required &mdash; the main drawing path is free YouTube. Brunetti&rsquo;s
  <em>Cartooning: Philosophy and Practice</em>, Barry&rsquo;s <em>Making Comics</em>, and
  Mateu-Mestre&rsquo;s <em>Framed Ink</em> (~$70 together) cover the comics-craft half, chosen
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

add("about", "11-about.html", "About this course &amp; sources", "about", None, status=None, body='''
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
<p>It&rsquo;s also a living plan, edited as it&rsquo;s worked through. No plan made in advance fully
matches how someone actually learns, so modules that have been done describe what actually worked
&mdash; keeping course where the plan held up, and swapping in a better resource where it didn&rsquo;t
&mdash; while modules not yet reached stay open to change.</p>

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
  costs nothing. A small number of real, classroom-tested books (about $70 for the comics half, plus an
  optional ~$40 drawing reference) were added deliberately where no free equivalent taught as well &mdash; while pricier
  options ($249, $500, and even a cheap $12 video series) were looked at and explicitly kept
  optional rather than required.</li>
  <li><strong>Honest about the weak spots.</strong> The &ldquo;skip / contested&rdquo; callouts, the
  caveats page, and the note in the comics module admitting that free critique loops are genuinely
  hard to come by are all here on purpose &mdash; a curriculum that hides its own tradeoffs isn&rsquo;t
  trustworthy. So is swapping a resource out when it stops working for the person actually using this
  course &mdash; keeping only the start of Drawabox, then moving <em>How to Draw</em> from the main path
  to a companion reference when it proved too dry, in favor of two YouTube playlists.</li>
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
<p><strong>Current phase</strong></p>
<ul>
  <li><a href="https://drawabox.com" target="_blank" rel="noopener">Drawabox</a> (Uncomfortable) &mdash; the opening lessons only: materials, pen grip, drawing from the shoulder</li>
  <li><a href="https://youtube.com/playlist?list=PL0V_JTTg_6baV8tBE4Qm1O8Vhxy59GTah" target="_blank" rel="noopener">Draw Like a Sir</a>&rsquo;s tutorial series (YouTube)</li>
  <li><a href="https://youtube.com/playlist?list=PLqR-aNpyEIVd91GCwsyOS3oRn6eoRhyio" target="_blank" rel="noopener">Peter Han</a>&rsquo;s course (YouTube)</li>
</ul>
<p><strong>Foundations</strong></p>
<ul>
  <li>Scott Robertson &amp; Thomas Bertling, <a href="https://designstudiopress.com/products/how-to-draw" target="_blank" rel="noopener"><em>How to Draw</em></a> (Design Studio Press)</li>
  <li><a href="https://www.youtube.com/channel/UC5dyu9y0EV0cSvGtbBtHw_w" target="_blank" rel="noopener">Sycra</a> (YouTube) &mdash; free construction teaching</li>
  <li>Robin &amp; Lorenzo Etherington&rsquo;s free <a href="http://theetheringtonbrothers.blogspot.com/2019/09/how-to-think-when-you-draw-1-point.html" target="_blank" rel="noopener">perspective tutorials</a></li>
  <li>Andrew Loomis, <em>Fun With a Pencil</em>, via the <a href="https://archive.org/details/andrew-loomis-fun-with-a-pencil" target="_blank" rel="noopener">Internet Archive</a></li>
  <li>Ernest Norling, <em>Perspective Made Easy</em>, via the <a href="https://archive.org/details/perspective-made-easy-by-ernest-r.-norling" target="_blank" rel="noopener">Internet Archive</a></li>
  <li><a href="https://www.youtube.com/moderndayjames" target="_blank" rel="noopener">ModernDayJames</a> (YouTube)</li>
  <li>Marshall Vandruff&rsquo;s <a href="https://marshallart.gumroad.com/l/wbwxz" target="_blank" rel="noopener">1994 Perspective Drawing Series</a> &mdash; optional deep dive, $12</li>
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
  <li>Proko&rsquo;s Marvel-branded &ldquo;The Art of Storytelling&rdquo; course ($249)</li>
  <li>Frank Santoro&rsquo;s mentored correspondence course ($500)</li>
</ul>
''')

# ---------- suggested steps for later modules ----------
# Each page id maps to a list of entries: (item_id, label) is one suggested
# step; a Section is a sub-heading grouping the steps below it. These used to
# be sign-in-synced progress checkboxes; tracking was removed (it may come
# back), so they now render as a plain list. item_id is kept so per-item
# links in ITEM_LINKS still resolve, and so tracking can be re-added later.
class Section:
    __slots__ = ("label", "url", "videos")
    def __init__(self, label, url=None, videos=None):
        self.label = label
        self.url = url
        self.videos = videos or []

CHECKLISTS = {
    "rhythm": [
        ("drawabox", "Read the opening of Drawabox: materials, pen grip, drawing from the shoulder"),
        ("supplies", "Get a fineliner pen, an HB pencil, and cheap paper"),
        ("schedule", "Start drawing whenever you can fit it in &mdash; even a few minutes counts"),
        ("diaryhabit", "Optional: try the 4-minute diary a few times a week"),
    ],
    "learn": [
        ("loop", "Watch the next video (or so) from each playlist, in order"),
        ("practice", "Practice what it covered until you can do it on purpose &mdash; researching extra drills and material as needed"),
        ("warmups", "Write down the drills worth keeping as your own warm-up list"),
        ("repeat", "Repeat until both playlists are done"),
    ],
    "construction": [
        ("constructionvideo", "Watch Sycra&rsquo;s &ldquo;How to Draw Anything with Construction&rdquo;"),
        ("arrowdrill", "Practice building a form around a single &ldquo;arrow&rdquo; line of action"),
        ("simpleforms", "Draw a page of everyday objects built from 2&ndash;3 overlapping simple solids (sphere, cylinder, box)"),
    ],
    "perspective": [
        ("onepoint1", "Etherington Brothers: 1-Point Perspective, Part 1"),
        ("onepoint2", "Etherington Brothers: 1-Point Perspective, Part 2"),
        ("twopoint", "Etherington Brothers: 2-Point Perspective"),
        ("perspectiveboxes", "Etherington Brothers: Perspective Boxes"),
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
        ("digitaldrill", "Redo a few of your own line/ellipse warm-ups digitally"),
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
# If a link here turns out to be dead or mis-cited, log the fix in
# SOURCES.md (what it was, what it turned out to be, how it was verified)
# before swapping the URL below -- that log is the only record of citations
# that were checked versus ones nobody's ever confirmed.
ITEM_LINKS = {
    ("rhythm", "diaryhabit"): {
        "lesson": "https://www.openculture.com/2021/09/cartoonist-lynda-barry-teaches-you-how-to-make-a-visual-daily-diary.html",
    },
    ("rhythm", "drawabox"): {
        "lesson": "https://drawabox.com",
    },
    ("learn", "loop"): {
        "videos": [
            {"label": "Draw Like a Sir", "video": "https://youtube.com/playlist?list=PL0V_JTTg_6baV8tBE4Qm1O8Vhxy59GTah"},
            {"label": "Peter Han", "video": "https://youtube.com/playlist?list=PLqR-aNpyEIVd91GCwsyOS3oRn6eoRhyio"},
        ],
    },
    ("construction", "constructionvideo"): {
        # Was v=iTey_rv-Trc, mislabeled as Sycra -- that ID is actually Brad
        # Colbow's "Brad's Art School". See SOURCES.md for the fix writeup.
        "video": "https://www.youtube.com/watch?v=j2KVnOfyAIE",
    },
    ("perspective", "onepoint1"): {
        "lesson": "http://theetheringtonbrothers.blogspot.com/2019/09/how-to-think-when-you-draw-1-point.html",
    },
    ("perspective", "onepoint2"): {
        "lesson": "http://theetheringtonbrothers.blogspot.com/2019/09/how-to-think-when-you-draw-1-point_8.html",
    },
    ("perspective", "twopoint"): {
        "lesson": "http://theetheringtonbrothers.blogspot.com/2022/12/how-to-think-when-you-draw-2-point.html",
    },
    ("perspective", "perspectiveboxes"): {
        "lesson": "http://theetheringtonbrothers.blogspot.com/2021/11/how-to-think-when-you-draw-perspective.html",
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

def steps_box(page_id):
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
            rows += f'<li class="step-section">{entry.label}{open_link}{video_links}</li>\n'
            continue
        item_id, label = entry
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
                links_html = f'<span class="item-links">{joined}</span>'
        rows += f'<li>{label}{links_html}</li>\n'
    return f'''<div class="steps-box">
    <h3>Steps</h3>
    <ul>
    {rows}
    </ul>
  </div>'''

STATUS_BADGES = {
    "done": '<span class="dj-badge dj-badge-success">Done</span>',
    "current": '<span class="dj-badge dj-badge-accent">Current</span>',
    "upcoming": '<span class="dj-badge">Not started</span>',
}

UPCOMING_NOTE = '''<div class="dj-callout upcoming-note"><span class="dj-callout-tag">not started yet</span>
This is the plan for this module as it stands. It gets revisited once it&rsquo;s reached &mdash; kept if it
still fits, changed or swapped out if something better turns up along the way.</div>'''

TOC_SUBS = {
    "rhythm": "The opening of Drawabox, fitting drawing into your life, supplies, and books",
    "learn": "Draw Like a Sir + Peter Han, one video at a time, practiced to proficiency",
    "construction": "3D forms built from simple shapes, the free way",
    "perspective": "Just enough 1- and 2-point perspective",
    "gesture": "Movement, flow, and simplified cartoon anatomy",
    "character": "Shape language, expression, and your own style",
    "comics": "Scripting, layout, lettering, and finishing a real minicomic",
    "digital": "Moving from paper to an iPad, when you&rsquo;re ready",
    "recs": "Where to start and how to know it&rsquo;s time to move on",
    "caveats": "What&rsquo;s contested, what changes, what to double-check",
    "about": "How this course was built, the theory behind it, and every source credited",
}

# Draw Your Own Comics keeps its own name and content -- Djaunt supplies the
# visual system (color, type, geometry) plus this one small, unlinked credit
# line on every page, not top billing. See BRANDING.md in djaunt-branding.
DJAUNT_CREDIT = '''<div class="dj-credit"><img src="djaunt-icon-radiant.svg" alt="" width="14" height="14">Part of Djaunt</div>'''

def shell(title, body, page_id=""):
    return f'''<!DOCTYPE html>
<html lang="en" data-dj-theme="radiant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Cartooning Guide &mdash; {title}</title>
{FAVICON_LINKS}
{FONT_LINKS}
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/tory37/djaunt-branding@main/brand/tokens/tokens.css">
<link rel="stylesheet" href="style.css?v={BUILD_VERSION}">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/tory37/djaunt-branding@main/components/callout/callout.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/tory37/djaunt-branding@main/components/badge/badge.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/tory37/djaunt-branding@main/components/hero/hero.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/tory37/djaunt-branding@main/components/divided-list/divided-list.css">
</head>
<body data-page-id="{page_id}">
{body}
{DJAUNT_CREDIT}
</body>
</html>
'''

CURRENT = next(p for p in PAGES if p["status"] == "current")

def sitebar():
    return f'''<div class="sitebar">
  <div class="sitebar-links">
    <a class="home" href="index.html">{HOME_ICON}Draw Your Own Comics</a>
    <a class="nav-link" href="{CURRENT['file']}">Continue &rarr;</a>
  </div>
</div>'''

def page_no(p):
    return f'{PAGES.index(p) + 1:02d}'

# ---------- build index.html ----------
def toc_item(p):
    chip = STATUS_BADGES.get(p["status"], "")
    return f'''<li class="{'toc-now' if p['status'] == 'current' else ''}"><a href="{p['file']}">
    <span class="toc-head">
      <span class="toc-marker">
        {ICONS[p['icon']]}
        <span class="no">{page_no(p)}</span>
      </span>
      <span class="toc-status">
        {chip}
        <span class="toc-arrow">&rarr;</span>
      </span>
    </span>
    <span class="toc-title">{p['title']}</span>
    <span class="toc-sub">{TOC_SUBS[p['id']]}</span>
  </a></li>
'''

toc_items = "".join(toc_item(p) for p in PAGES)

index_body = f'''
{sitebar()}
<header class="dj-hero">
  <div class="dj-hero-mark" aria-hidden="true"></div>
  <div class="kicker">
    <svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M8 12h8M12 8v8" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
    A living plan, edited as it&rsquo;s worked through
  </div>
  <h1>Draw your own comics,<br><em>one page at a time.</em></h1>
  <svg class="underline" viewBox="0 0 180 14"><path d="M3 9 C 40 2, 90 14, 130 6 S 175 4, 177 9"/></svg>
  <p class="dj-hero-lede">
    A mostly-free plan for going from learning to draw to making loose, expressive, stylized comics
    &mdash; the bones of a path, updated as it&rsquo;s actually followed. You fill in the specifics.
  </p>
  <div class="meta-row">
    <div><b>Starting point</b>Complete beginner, pencil &amp; paper</div>
    <div><b>Time budget</b>Whatever you can fit in</div>
    <div><b>Style range</b>Pendleton Ward &rarr; Dilworth &rarr; Invader Zim</div>
    <div><b>Format</b>Self-paced, years not weeks</div>
  </div>
</header>

<div class="continue-card">
  <div class="continue-label">Continue</div>
  <a class="continue-link" href="{CURRENT['file']}">
    <span class="continue-title">{page_no(CURRENT)} &middot; {CURRENT['title']}</span>
    <span class="continue-arrow">&rarr;</span>
  </a>
</div>

<div class="wrap">
<section>
  <div class="tldr">
    <h3>The short version</h3>
    <p>Get set up with the opening of Drawabox &mdash; materials, pen grip, drawing from the
    shoulder. Then learn to draw from two YouTube playlists side by side: Draw Like a Sir for the
    concepts and Peter Han for instruction and homework. Watch a video or so of each, practice until
    you&rsquo;re proficient (not perfect), researching your own practice material as needed, then move on.
    After that: construction, perspective, gesture, character design, and finally comics.</p>
    <p>This plan is edited as it&rsquo;s worked through. Modules marked done describe what actually
    worked; modules not started yet are the plan as it stands, and will change if something better
    turns up. Draw as much as you can, whenever you can &mdash; small sessions count. This is a multi-year hobby,
    not a bootcamp.</p>
  </div>

  <h3 style="margin-top:40px;">Principles behind the plan</h3>
  <ul class="findings dj-divided-list dj-divided-list-marked">
    <li class="dj-divided-item"><span class="dj-divided-item-marker">1</span><span class="dj-divided-item-body"><strong>The best resource is the one you&rsquo;ll actually
    keep using.</strong> A respected textbook that feels dry loses to a well-made video series you look
    forward to &mdash; keep the textbook as a reference, not the main path.</span></li>
    <li class="dj-divided-item"><span class="dj-divided-item-marker">2</span><span class="dj-divided-item-body"><strong>Bones, not specifics.</strong> The plan names
    what to learn and where; finding extra drills, reference, and your own warm-up routine is part of
    the work.</span></li>
    <li class="dj-divided-item"><span class="dj-divided-item-marker">3</span><span class="dj-divided-item-body"><strong>Dedicated cartooning resources already exist and are
    free.</strong> Loomis, the Etherington Brothers, Proko, and McCloud cover exactly the ground a
    comic artist needs, once the general drawing basics are in place.</span></li>
  </ul>

  <h3 style="margin-top:44px;">The plan</h3>
  <ul class="toc">
    {toc_items}
  </ul>
</section>

<footer class="site">
  <p>Compiled from web research into free, community-recommended drawing resources, and revised as
  it&rsquo;s followed &mdash; September 2026. Not a professional curriculum; a personal roadmap built for
  one specific goal: making comics you&rsquo;re proud of.</p>
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
    banner_html = UPCOMING_NOTE if p["status"] == "upcoming" else ''
    badge_html = STATUS_BADGES.get(p["status"], "")

    body = f'''
{sitebar()}
<div class="wrap">
<section>
  <div class="page-head">
    {ICONS[p['icon']]}
    <h2><span class="no">{page_no(p)}</span>{p['title']}</h2>
    <span class="page-badge">{badge_html}</span>
  </div>
  {duration_html}
  {banner_html}
  {p['body']}
  {steps_box(p['id'])}
</section>
{pn}
<footer class="site"><p><a href="index.html">&larr; Back to the table of contents</a></p></footer>
</div>
'''
    with open(f"{OUT}/{p['file']}", "w") as f:
        f.write(shell(p['title'].replace('&amp;','&'), body, page_id=p['id']))

# Progress tracking (Firebase sign-in + synced checkboxes, generated as
# progress-schema.js / firebase-config.js / app.js) was removed -- see git
# history if it comes back.

print("Built", len(PAGES) + 1, "pages")
print(os.listdir(OUT))
