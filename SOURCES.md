# Source verification log

`build_site.py` links out to a lot of third-party lessons and videos (see
`ITEM_LINKS` and the per-module `add(...)` calls). Nobody had been checking
those links after they were written, so citations could go stale or turn out
to be wrong from the start with no record of it. This file is that record:
every time a citation is found broken or mis-attributed and gets fixed, log
it here — what it was, what it turned out to be, how it was checked, and how
confident the fix is. Skip logging a plain link-rot swap (same real source,
new URL because the old one 404s) unless the correct replacement was hard to
pin down; this file is for cases worth a future double-check, not routine
maintenance.

## 2026-09-17 — Lesson 3 (construction) video citation was a different creator entirely

- **Was:** `https://www.youtube.com/watch?v=iTey_rv-Trc`, credited on the site as
  Sycra's "How to Draw Anything with Construction" (used in both the
  `03-construction.html` module intro and the `constructionvideo` toolkit
  item).
- **Found:** That video ID belongs to Brad Colbow's "Brad's Art School"
  channel, not Sycra — confirmed by the user clicking through and landing on
  a Brad's Art School video, and independently by web search (bradsartschool.com,
  `youtube.com/@BradsArtSchool`). YouTube never reassigns a video ID after
  deletion, so this wasn't a real Sycra video that later disappeared — the
  citation was wrong from the moment it was written, likely a hallucinated
  title/ID pairing from whatever produced the original curriculum content.
- **Replaced with:** `https://www.youtube.com/watch?v=j2KVnOfyAIE` — Sycra's
  "The Importance of Construction in Drawing" (TS Archive reupload). Sycra's
  original channel was hacked and suspended around December 2018; he gave
  fans permission to mirror his catalog while it was down, which is why this
  title shows up consistently across several independent reuploads (TS
  Archive, a channel literally named "Sycra reupload," and what looks like
  the original 2015 upload). Content-wise it matches the lesson's framing
  much better too: it's Sycra explaining *why* construction/built-from-shapes
  thinking matters, which is exactly what the module intro paraphrases.
- **Confidence: medium.** Matched by title, topic, and cross-channel
  provenance from multiple independent search hits — not by watching the
  video, since this sandbox's network egress blocks youtube.com entirely (no
  WebFetch, no oembed proxies). Worth a human spot-check that the content
  still matches once it's live.
