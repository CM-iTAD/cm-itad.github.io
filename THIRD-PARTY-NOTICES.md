# Third-party notices

This site redistributes or loads the components below. They are **not** covered
by [`LICENSE`](LICENSE) — each is used under its own terms, reproduced here.

---

## 1. `<model-viewer>` — redistributed in this repository

**File:** `assets/js/vendor/model-viewer.min.js` (v4.1.0, ~979 KB)
**Copyright:** © 2019 Google LLC
**Licence:** BSD-3-Clause (`SPDX-License-Identifier: BSD-3-Clause`)
**Upstream:** https://github.com/google/model-viewer

This file is **vendored**, i.e. a copy is served from this repository rather
than loaded from a CDN (see `HANDOFF.md` §3a for why). Redistribution triggers
the licence's retention condition, so the `@license` header **must stay intact
in the minified file** — do not strip comments from it during any future
minification or build step.

```
Copyright 2019 Google LLC. All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

  1. Redistributions of source code must retain the above copyright notice,
     this list of conditions and the following disclaimer.

  2. Redistributions in binary form must reproduce the above copyright notice,
     this list of conditions and the following disclaimer in the documentation
     and/or other materials provided with the distribution.

  3. Neither the name of the copyright holder nor the names of its contributors
     may be used to endorse or promote products derived from this software
     without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```

---

## 2. IBM Plex Sans / Mono / Serif — loaded, not redistributed

**Copyright:** © 2017 IBM Corp.
**Licence:** SIL Open Font License 1.1 — https://openfontlicense.org
**Upstream:** https://github.com/IBM/plex

Served at runtime from Google Fonts (`<link>` in each page's `<head>`); no font
file is stored in this repository, so no redistribution obligation arises. If a
future change self-hosts the `.woff2` files, the OFL text must be included
alongside them and this notice updated.

---

## 3. Design foundation

The structural layer of the design system (type scale, hairline grids, mono
eyebrows, squared corners) derives from the **Frahan StonePack** design system,
as recorded in `DESIGN.md` §1. Only the structure was adopted; the palette is
CM-iTAD's own. No StonePack code or asset is redistributed here — the tokens in
`assets/css/site.css` are written out rather than imported.

---

## 4. Partner logos

The logos on the About page are the property of their respective owners and are
reproduced to indicate collaboration. They are not licensed under `LICENSE` and
carry no implication that those organisations endorse its terms.

---

*Additions: if you vendor another dependency, add it here in the same shape —
what the file is, who owns it, the licence, and whether redistribution applies.*
