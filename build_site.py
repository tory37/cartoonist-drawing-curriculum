import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site")
os.makedirs(OUT, exist_ok=True)

# ---------- shared stylesheet ----------
CSS = '''
:root{
  --paper:#F2EFE6; --paper-deep:#EBE6D8; --line:#DBD4BF;
  --ink:#221F1B; --ink-soft:#5B5646;
  --blue:#2B3A55; --blue-soft:#4C5D7D;
  --red:#A83B2E; --green:#3F6B4F;
  --max:700px;
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
  display:flex; align-items:center; justify-content:space-between;
  font-size:14px; color:var(--ink-soft);
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
  border-radius:2px; background:rgba(255,255,255,.4); font-size:15.5px;
}
.callout.do{border-color:var(--green);}
.callout.skip{border-color:var(--red);}
.callout .tag{font-weight:700; font-size:11.5px; margin-bottom:5px; display:block;}
.callout.do .tag{color:var(--green);}
.callout.skip .tag{color:var(--red);}

.tldr{
  background:rgba(43,58,85,.05); border:1px solid var(--line); border-radius:6px;
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
  border:1px solid var(--line); background:rgba(255,255,255,.5); color:var(--ink);
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

/* per-section progress pill in the table of contents */
.toc-progress{
  font-size:12px; color:var(--ink-soft); border:1px solid var(--line);
  padding:3px 9px; border-radius:10px; flex:none; margin-left:2px;
}
.toc-progress.complete{color:var(--green); border-color:var(--green);}

/* progress tracker checklist box on each phase page */
.tracker-box{
  margin:34px 0 6px; border:1px solid var(--line); border-radius:6px;
  padding:22px 24px; background:rgba(255,255,255,.35);
}
.tracker-box h3{margin-top:0;}
.track-item{
  display:flex; align-items:flex-start; gap:11px; padding:9px 0; font-size:15px;
  border-top:1px solid var(--line);
}
.track-item:first-of-type{border-top:none; padding-top:2px;}
.track-item input[type=checkbox]{
  margin-top:3px; width:17px; height:17px; accent-color:var(--green);
  flex:none; cursor:pointer;
}
.track-item input[type=checkbox]:disabled{cursor:not-allowed; opacity:.45;}
.track-item label{cursor:pointer;}
.tracker-note{font-size:13px; color:var(--ink-soft); margin:12px 0 0;}

@media print{
  .sitebar, nav.pn, .tracker-box, .overall-bar{display:none;}
  a{color:var(--ink); text-decoration:none;}
}
'''

with open(f"{OUT}/style.css", "w") as f:
    f.write(CSS)

FONT_LINKS = '''<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600;0,9..144,700;1,9..144,500&family=Work+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">'''

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
  <div>&#9998; A pack of fineliners (for Drawabox &mdash; ink only, no erasing)</div>
  <div>&#9998; Printer paper is fine to start</div>
</div>
''')

add("lines", "02-marks-and-lines.html", "Marks, lines &amp; confidence", "lines",
    '<a href="https://drawabox.com/lesson/0" target="_blank" rel="noopener">Drawabox Lesson 0</a>&ndash;<a href="https://drawabox.com/lesson/1" target="_blank" rel="noopener">1</a> &middot; roughly 4&ndash;8 weeks', '''
<p>Read <a href="https://drawabox.com/lesson/0" target="_blank" rel="noopener">Lesson 0</a> for the mindset and the 50% rule, then work <a href="https://drawabox.com/lesson/1" target="_blank" rel="noopener">Lesson 1</a>: superimposed lines,
ghosted lines and planes, tables of ellipses, and the basic perspective/box exercises.</p>
<div class="callout do"><span class="tag">why it matters</span>
This trains the single most transferable cartooning skill: a confident line and a clean shape
drawn from the shoulder, not a scratchy, hesitant one.</div>
<p>Keep it light &mdash; a page or two per session as your structured half, then go draw cartoons for the rest.</p>
''')

add("construction", "03-construction.html", "Basic construction &amp; 3D forms", "construction",
    '<a href="https://drawabox.com/lesson/2" target="_blank" rel="noopener">Drawabox Lesson 2</a> + optional partial <a href="https://drawabox.com/lesson/250boxes" target="_blank" rel="noopener">Box Challenge</a> &middot; roughly 4&ndash;10 weeks', '''
<p>Work <a href="https://drawabox.com/lesson/2" target="_blank" rel="noopener">Lesson 2</a>&rsquo;s form and intersection exercises &mdash; understanding how simple
volumes fit together in space is the backbone of &ldquo;built from shapes&rdquo; cartooning
(a head as a rounded box, a body as a blob).</p>
<div class="callout skip"><span class="tag">contested &mdash; read before skipping</span>
The full <a href="https://drawabox.com/lesson/250boxes" target="_blank" rel="noopener">250 Box Challenge</a> is tedious for many students and a real burnout risk. Others argue
the spatial payoff helps you rotate a character consistently across comic panels. Compromise:
spread 50&ndash;100 boxes across several weeks as warm-ups instead of grinding all 250 in a block.
Skip the deep texture-rendering drills &mdash; a cartoonist rarely needs realistic texture.</div>
''')

add("perspective", "04-perspective.html", "Just enough perspective", "perspective",
    '<a href="https://www.youtube.com/moderndayjames" target="_blank" rel="noopener">ModernDayJames</a> (YouTube), Norling&rsquo;s <a href="https://archive.org/details/perspective-made-easy-by-ernest-r.-norling" target="_blank" rel="noopener"><em>Perspective Made Easy</em></a> &middot; roughly 3&ndash;6 weeks', '''
<p>Learn enough 1- and 2-point perspective to place a character in a room and draw a believable
box, building, or prop. That&rsquo;s the whole goal here.</p>
<div class="callout skip"><span class="tag">skip / deprioritize</span>
Drawabox&rsquo;s Lesson 6 (everyday objects), Lesson 7 (vehicles), the 25 Wheel Challenge, and 250
Cylinder Challenge. These are technical-perspective marathons for concept artists and
industrial designers. A loose cartoonist fakes and stylizes perspective for expression &mdash; you
don&rsquo;t need measured vanishing-point precision.</div>
''')

add("gesture", "05-gesture.html", "Gesture &amp; simplified anatomy", "gesture",
    '<a href="https://www.proko.com" target="_blank" rel="noopener">Proko</a>, <a href="https://www.lovelifedrawing.com" target="_blank" rel="noopener">Love Life Drawing</a>, Loomis&rsquo; <a href="https://archive.org/details/andrew-loomis-fun-with-a-pencil" target="_blank" rel="noopener"><em>Fun With a Pencil</em></a> &middot; roughly 8&ndash;12 weeks, then ongoing', '''
<p>This is the pivot away from Drawabox and toward cartooning proper.</p>
<ul>
  <li><strong><a href="https://www.youtube.com/playlist?list=PLtG4P3lq8RHEQ1kiN_Nub1vXR8fQQLjDF" target="_blank" rel="noopener">Proko</a></strong> &mdash; free gesture and figure-drawing videos on YouTube. Gesture is the
  single most important skill for expressive cartooning; it&rsquo;s what keeps drawings from looking stiff.</li>
  <li><strong><a href="https://www.lovelifedrawing.com" target="_blank" rel="noopener">Love Life Drawing</a></strong> &mdash; beginner-friendly figure/gesture on YouTube.</li>
  <li><strong><a href="https://line-of-action.com" target="_blank" rel="noopener">Line of Action</a> / <a href="https://www.quickposes.com/en" target="_blank" rel="noopener">Quickposes</a></strong> &mdash; free timed-reference websites. Note: both include nude reference photos by default alongside clothed ones &mdash; both let you filter this in their settings.</li>
  <li><strong>Andrew Loomis, <a href="https://archive.org/details/andrew-loomis-fun-with-a-pencil" target="_blank" rel="noopener"><em>Fun With a Pencil</em></a></strong> &mdash; free and legal on the Internet
  Archive. The first ~30 pages teach cartoon heads and figures via ball-and-plane construction,
  the perfect bridge from fundamentals to cartoon character.</li>
</ul>
<div class="callout do"><span class="tag">how to practice</span>
Short timed gestures (30 seconds&ndash;2 minutes), then &ldquo;mannequinize&rdquo; into simple shapes.
Chase flow and exaggeration, not accuracy.</div>
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
  cartoonist library on the web.</li>
  <li><strong><a href="https://www.youtube.com/tonikopantoja" target="_blank" rel="noopener">Toniko Pantoja</a></strong> (YouTube) &mdash; story/animation artist (How to Train Your
  Dragon 3, Trolls, Croods 2); excellent free videos on appealing shape language.</li>
  <li><strong><a href="https://www.youtube.com/channel/UC5dyu9y0EV0cSvGtbBtHw_w" target="_blank" rel="noopener">Sycra</a></strong> (YouTube) &mdash; &ldquo;iterative drawing&rdquo; and shape-design; great for
  developing your own voice through variation rather than copying.</li>
  <li><strong>Study your north stars directly.</strong> Copy frames from Adventure Time,
  Invader Zim, and similar cartoons. Break each character into its underlying simple shapes &mdash;
  Finn is a rounded box, Jake is a fluid blob.</li>
</ul>
<div class="callout do"><span class="tag">exercises</span>
Shape-language studies (design the same character from circles, then squares, then triangles),
expression sheets, and model sheets &mdash; the same character from multiple angles, which is exactly
where your Phase 1&ndash;2 construction work pays off.</div>
''')

add("comics", "07-comics.html", "Comics: paneling &amp; storytelling", "comics",
    '<a href="https://www.scottmccloud.com" target="_blank" rel="noopener">Scott McCloud</a>, <a href="https://theetheringtonbrothers.blogspot.com/2020/02/what-free-50-page-how-to-think-when-you.html" target="_blank" rel="noopener">Etherington Brothers</a> &middot; ongoing', '''
<ul>
  <li><strong><a href="https://www.scottmccloud.com" target="_blank" rel="noopener">Scott McCloud</a>, <em>Making Comics</em> &amp; <em>Understanding Comics</em></strong>
  &mdash; the standard texts on panel transitions, gutters, pacing, and expressive acting (library, not free).</li>
  <li><strong>Etherington Brothers&rsquo;</strong> free <a href="https://theetheringtonbrothers.blogspot.com/2020/02/what-free-50-page-how-to-think-when-you.html" target="_blank" rel="noopener">&ldquo;How to THINK when you draw JUNIOR &mdash; How
  to draw COMICS&rdquo;</a> &mdash; a free 50-page ebook walking through a full comic project: character, world,
  story, page planning, dialogue, finished page, in short daily sessions.</li>
</ul>
<blockquote>&ldquo;If you can draw a smiley face and a stick figure, you can start drawing comics.&rdquo;</blockquote>
<div class="callout do"><span class="tag">just start</span>
Make a short minicomic early &mdash; eight pages is a common, achievable target. Working cartoonists
argue there&rsquo;s no prerequisite skill level to begin; starting reveals exactly what to improve next.</div>
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
''')

add("recs", "09-recommendations.html", "Putting it together", "recs", None, '''
<h3>Start this week</h3>
<ul>
  <li>Read <a href="https://drawabox.com/lesson/0" target="_blank" rel="noopener">Drawabox Lesson 0</a> and adopt the 50% rule. Buy a fineliner pen and cheap paper.</li>
  <li>Begin Phase 1 at two short sessions a week, always splitting time with fun cartoon doodling.</li>
</ul>
<h3>How you&rsquo;ll know it&rsquo;s time to move on</h3>
<ul>
  <li><strong>Past Phase 1&ndash;2</strong> &mdash; your lines are noticeably more confident and a box or
  cylinder &ldquo;sits&rdquo; believably in 3D. Don&rsquo;t wait for perfection.</li>
  <li><strong>Cap your Drawabox investment</strong> at Lessons 0&ndash;2 plus a partial box challenge.
  If boxes are killing your motivation, stop around 50 and move on.</li>
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
  <li><strong>The &ldquo;skip&rdquo; advice is contested, not settled.</strong> Some experienced Drawabox
  students argue the full construction sequence &mdash; including the box challenge &mdash; pays off in
  any style, comics included. Treating it as optional here is a deliberate trade-off for your
  time budget, not a fact everyone agrees on.</li>
  <li><strong>Free-book legality varies by title and country.</strong> Treat the <a href="https://archive.org" target="_blank" rel="noopener">Internet
  Archive</a> as the safest free reading source for Loomis and Norling; buy in print if you want certainty.
  McCloud&rsquo;s books are in copyright &mdash; use a library.</li>
  <li><strong>Some &ldquo;free&rdquo; resources have paid upsells.</strong> <a href="https://www.proko.com" target="_blank" rel="noopener">Proko</a> and the Solo Art
  Curriculum surface a lot of free content but also sell premium courses. <a href="https://drawabox.com" target="_blank" rel="noopener">Drawabox</a> itself is
  fully free, with an optional paid critique tier.</li>
  <li><strong>Links and channels change.</strong> If a specific video or playlist has moved,
  search the creator&rsquo;s name directly &mdash; the recommendation still stands even when the URL doesn&rsquo;t.</li>
  <li>This is a synthesis of what free resources and their communities recommend, not a
  guarantee of outcomes. Progress depends almost entirely on consistent, enjoyable practice
  sustained over years.</li>
</ul>
</div>
''')

# ---------- progress-tracking checklists ----------
# Each page id maps to a list of (item_id, label) checkable actions.
CHECKLISTS = {
    "rhythm": [
        ("supplies", "Got a fineliner pen, an HB pencil, and cheap paper"),
        ("schedule", "Picked your two weekly session slots"),
    ],
    "lines": [
        ("lesson0", "Read Drawabox Lesson 0 (mindset &amp; the 50% rule)"),
        ("superimposed", "Superimposed lines"),
        ("ghosted", "Ghosted lines &amp; planes"),
        ("ellipses", "Tables of ellipses"),
        ("boxes", "Basic perspective / box exercises"),
    ],
    "construction": [
        ("organic", "Lesson 2: organic forms with contour curves"),
        ("texture", "Lesson 2: texture analysis"),
        ("intersect", "Lesson 2: form intersections"),
        ("organicintersect", "Lesson 2: organic intersections"),
        ("boxwarmup", "50&ndash;100 warm-up boxes (partial box challenge)"),
    ],
    "perspective": [
        ("onepoint", "Watch a 1-point perspective video"),
        ("twopoint", "Watch a 2-point perspective video"),
        ("roomsketch", "Sketch a character standing in a simple room"),
    ],
    "gesture": [
        ("gesturesession", "Do one timed gesture session (30s&ndash;2min poses)"),
        ("prokovideo", "Watch a Proko gesture fundamentals video"),
        ("loomispages", "Read the first ~30 pages of <em>Fun With a Pencil</em>"),
        ("mannequin", "Mannequinize 10 gesture sketches into simple shapes"),
    ],
    "character": [
        ("etherington", "Browse the Etherington Brothers&rsquo; character-shape tutorials"),
        ("circleschar", "Design one character built from circles"),
        ("squareschar", "Design the same character built from squares"),
        ("triangleschar", "Design the same character built from triangles"),
        ("expressionsheet", "Draw an expression sheet for one character"),
    ],
    "comics": [
        ("mccloudread", "Read/skim McCloud on panel transitions"),
        ("comicsebook", "Download the Etherington Brothers&rsquo; free comics ebook"),
        ("minicomic", "Draw an 8-page minicomic"),
    ],
    "digital": [
        ("procreatepart1", "Watch Procreate Beginners Series, Part One"),
        ("digitaldrill", "Redo a line/ellipse drill digitally"),
        ("layerworkflow", "Set up a sketch &rarr; ink &rarr; color layer workflow"),
        ("brushpicks", "Pick your 2&ndash;3 go-to brushes"),
    ],
}

def tracker_box(page_id):
    items = CHECKLISTS.get(page_id)
    if not items:
        return ""
    rows = ""
    for item_id, label in items:
        cb_id = f"{page_id}-{item_id}"
        rows += f'''<div class="track-item">
      <input type="checkbox" id="{cb_id}" data-id="{item_id}" disabled>
      <label for="{cb_id}">{label}</label>
    </div>
'''
    return f'''<div class="tracker-box">
    <h3>Track your progress</h3>
    {rows}
    <p class="tracker-note" id="tracker-note">Sign in above to save your progress and sync it across devices.</p>
  </div>'''

TOC_SUBS = {
    "rhythm": "How to structure 1&ndash;3 hours a week, and what to buy",
    "lines": "Confident lines, ellipses, and basic perspective",
    "construction": "3D forms and the (partial) box challenge",
    "perspective": "Just enough 1- and 2-point perspective",
    "gesture": "Movement, flow, and simplified cartoon anatomy",
    "character": "Shape language, expression, and your own style",
    "comics": "Panels, pacing, and making your first minicomic",
    "digital": "Moving from paper to an iPad, when you&rsquo;re ready",
    "recs": "Where to start and how to know it&rsquo;s time to move on",
    "caveats": "What&rsquo;s contested, what changes, what to double-check",
}

def shell(title, body, page_id=""):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} &mdash; Draw Your Own Comics</title>
{FONT_LINKS}
<link rel="stylesheet" href="style.css">
</head>
<body data-page-id="{page_id}">
{body}
<script src="progress-schema.js"></script>
<script src="firebase-config.js"></script>
<script type="module" src="app.js"></script>
</body>
</html>
'''

def auth_control():
    return '''<div class="auth-control" id="auth-control">
    <span class="progress-pill" id="header-progress" style="display:none"></span>
    <button class="auth-btn primary" id="signin-btn">Sign in to track</button>
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
    <div><b>Format</b>10 sections, self-paced, years not weeks</div>
  </div>
</header>

<div class="overall-bar" id="overall-progress">
  <div class="bar-track"><div class="bar-fill"></div></div>
  <div class="bar-label">Sign in above to start tracking your progress.</div>
</div>

<div class="wrap">
<section>
  <div class="tldr">
    <h3>The short version</h3>
    <p>You do not need to finish <a href="https://drawabox.com" target="_blank" rel="noopener">Drawabox</a> or the <a href="https://www.soloartcurriculum.com/" target="_blank" rel="noopener">Solo Art Curriculum</a> &mdash; both are built to
    produce generalist realism artists over a year or more of near-daily work. Take Drawabox&rsquo;s
    Lessons 0&ndash;2 for spatial fundamentals, then deliberately pivot toward cartooning: Loomis,
    Proko, the Etherington Brothers, and Scott McCloud on comics craft.</p>
    <p>At 1&ndash;3 hrs a week, this is a multi-year hobby, not a bootcamp. Adopt Drawabox&rsquo;s own
    <strong>50% rule</strong> from day one, stay on paper through character design, and add an
    iPad only once you can build a character from imagination.</p>
  </div>

  <h3 style="margin-top:40px;">Key findings from the research</h3>
  <ul class="findings">
    <li><span class="fn">1</span><span><strong>Drawabox teaches spatial reasoning, not style.</strong>
    Its early lessons transfer to any style; its later lessons (plants, animals, vehicles) are
    realism-flavored repetition most cartoonists don&rsquo;t need.</span></li>
    <li><span class="fn">2</span><span><strong>The Solo Art Curriculum is excellent, but built for a
    different artist.</strong> Its figure-drawing and character-design units are worth borrowing;
    its anatomy and painting sequence targets concept artists, not cartoonists.</span></li>
    <li><span class="fn">3</span><span><strong>Dedicated cartooning resources already exist and are
    free.</strong> Loomis, the Etherington Brothers, Proko, and McCloud cover exactly the ground a
    comic artist needs.</span></li>
  </ul>

  <h3 style="margin-top:44px;">The ten sections</h3>
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

# ---------- progress-schema.js (single source of truth for counts) ----------
import json
schema_obj = {pid: [item_id for item_id, _ in items] for pid, items in CHECKLISTS.items()}
with open(f"{OUT}/progress-schema.js", "w") as f:
    f.write("window.PROGRESS_SCHEMA = " + json.dumps(schema_obj, indent=2) + ";\n")

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
  appId: "PASTE_YOUR_APP_ID"
};
'''
with open(f"{OUT}/firebase-config.js", "w") as f:
    f.write(FIREBASE_CONFIG_JS)

# ---------- app.js (tracking logic) ----------
APP_JS = '''import { initializeApp } from "https://www.gstatic.com/firebasejs/12.17.1/firebase-app.js";
import {
  getAuth, GoogleAuthProvider, signInWithPopup, signOut, onAuthStateChanged
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
  if (signinBtn){
    signinBtn.textContent = "Tracking not set up yet";
    signinBtn.disabled = true;
  }
  if (trackerNote) trackerNote.textContent = "Progress tracking isn\\u2019t connected yet \\u2014 see the setup steps to enable it.";
} else {
  var app = initializeApp(cfg);
  var auth = getAuth(app);
  var db = getFirestore(app);
  var unsub = null;

  if (signinBtn) signinBtn.addEventListener("click", function(){
    signInWithPopup(auth, new GoogleAuthProvider()).catch(function(e){ console.error(e); });
  });
  if (signoutBtn) signoutBtn.addEventListener("click", function(){ signOut(auth); });

  var boxes = document.querySelectorAll(".track-item input[type=checkbox]");
  for (var i = 0; i < boxes.length; i++){
    (function(cb){
      cb.addEventListener("change", function(){
        if (!auth.currentUser || !pageId) return;
        var id = cb.getAttribute("data-id");
        var field = pageId + "." + id;
        var payload = {};
        payload[field] = cb.checked;
        payload.updatedAt = Date.now();
        setDoc(doc(db, "progress", auth.currentUser.uid), payload, { merge: true })
          .catch(function(e){ console.error(e); cb.checked = !cb.checked; });
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
      });
    } else {
      renderChecklist({});
      renderProgress({});
    }
  });
}
'''
with open(f"{OUT}/app.js", "w") as f:
    f.write(APP_JS)

print("Built", len(PAGES) + 1, "pages + progress-schema.js + firebase-config.js + app.js")
print(os.listdir(OUT))
