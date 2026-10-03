# Ikona AI (ex «Миллениум») - session notes and handoff

Last updated: 2026-10-01 (museum pivot). Read this file first in a new session, then `README.md` and `docs/DESIGN-cosmos.md`.

## Start a fresh session

Open Claude Code in `~/Desktop/photo-bureau` and paste:

> Read notes/STATUS.md, README.md and docs/DESIGN-cosmos.md in this repo. This is the «Миллениум» photo-zone site. Continue from the "Next steps" section of notes/STATUS.md. Reply in Russian.

## What the project is

- Static Russian site for «Миллениум»: photo zones for museums and parks, shoots in kindergartens and schools (albums), image presets library.
- Live: https://photo-bureau.vercel.app (Vercel project `photo-bureau`, account eugenazxa).
- Repo: `git@github.com:EugenAzxa/-1.git`, branch `main`. Local: `~/Desktop/photo-bureau`.
- Pages: `index`, `museums`, `worlds`, `schools`, `presets`, `contacts`, `lab` (noindex test page).

## Rules the client insists on

- Russian copy. Short dash `-` only, never em dashes. No emoji, use SVG icons.
- Contact by phone only: Андрей, +7 (921) 406-33-84. No forms anywhere.
- No mentions of AI on public pages (the presets page is the exception).
- Design must look literally like cosmos.so (Cosmos design system): linen `#f7f5f3`, ink `#0d0d0d`, Playfair Display + Manrope, radius 16, flat.
- If the client says they see a defect in their browser, it is real. Do not blame the test tool.
- Report honestly what was and was not checked.

## Build, check, deploy

```sh
cd ~/Desktop/photo-bureau
python3 build.py                      # src/pages + src/partials -> *.html in root
python3 -m http.server 8080           # http://localhost:8080
git push   # Vercel auto-deploys main (CLI deploy also possible: npx vercel@latest deploy --prod)
git add -A
git -c user.email="Eugen@azxa.io" -c user.name="EugenAzxa" commit -m "..."
GIT_SSH_COMMAND="ssh -o BatchMode=yes -o ConnectTimeout=20" git push
```

- Edit `src/pages/*.html` and `src/partials/*.html`, never the built root HTML.
- `build.py` holds `CONFIG` (brand, phone, manager), the layout, recursive `{{include:name}}` (5 levels), and `stamp_assets` which adds `?v=<md5>` to every image/css/js.
- `.vercelignore` keeps `src/`, `build.py`, `notes/` and docs off the server.

## Current design state (all deployed and committed)

- **Hero ring** (`src/partials/ring.html`, finale uses `ring-b.html`): 36 unique tiles each, 22 outer + 14 inner (`tile--in`). Tiles move on a fixed ellipse via `@property --ph` (0 to 360deg over 70 s) and `cos()/sin()`; `.collage{container-type:size}`, `--RX:43.5cqw --RY:40cqh` (mobile `37cqw / 41cqh`). Tiles fade whole via `--fade`.
  - Do NOT go back to rotating the container (ellipse smears) or radial masks (they slice tiles). The client noticed both.
- **Film reveal** after hero: `.film__frame` grows with scroll (`--p` set in `assets/js/main.js`).
- **Finale** (`src/partials/finale.html`): second ring, lead line, big phone button, giant brand wordmark in footer.
- **Glass lens menu**: JS spring (K=420, D=30, zoom 1.1), magnified copy of the links inside, glass 12 px wider than the item, follows finger on mobile, keeps position across pages via sessionStorage `aib-glass`.
  - `.nav-links` is `position:fixed` on mobile. Any global `position` rule on it breaks the mobile menu; desktop rule is scoped to `min-width:1081px`.
- **View Transitions** between pages (`@view-transition{navigation:auto}`).
- Light theme default, dark toggle in header (`aib-theme` in localStorage).

## Photos

- Real photos live in `assets/img/works/` (name table in `assets/img/works/README.md`). Cards load through `data-src`; if a file is missing the card shows a brand fill.
- Ring tiles: `assets/img/ring/` (r26 excluded - it is a schematic; r15 was a duplicate).
- Home «Образы» grid now uses `works/racer-speed.jpg` (Гонщик) and `works/lab.jpg` (Врач и учёный).
- Spare portraits cut from the client collages: `scientist, ballet, detective, dancer, cellist, cowboy, artist, retro`.
- Crop images with a canvas in Chrome, not `sips --cropOffset` (it crops from the center).

## Rename 2026-10-03: brand is now «Ikona AI»

- CONFIG brand «Ikona AI»; logo = navy arch #1A2F6E with gold inner line and sparkle #C79C40 and a white person (inline SVG in LAYOUT header/footer, `assets/favicon.svg`); header word «Ikona» navy + «AI» gold (`.brand__word`), footer wordmark the same.
- Home: «Шесть направлений» block `src/partials/directions.html` (also on worlds.html) - 6 venue types x family + individual shot, images `assets/img/dir/d1..d6-{family,ind}.jpg` (9 generated in GPT Image 2.5, 3 reused). Venue names are generic on purpose (Гранд Макет / РЖД / Maza Park not named).
- Home: «Примеры фотографий» gallery (client photos `assets/img/examples/{alchemy,magician,library}.jpg`) before the FAQ.
- Higgsfield jobs: run ONE at a time with `--json`; parallel jobs often fail with «API request failed».

## Pivot 2026-10-01: museums of Saint Petersburg only

- Site is now strictly about photo zones for museums in Saint Petersburg. Schools/kindergartens page, albums and all kids-in-costume portraits removed (`/schools` redirects to `/museums` in `vercel.json`).
- Copy and family photos come from the client deck `~/Downloads/КП объекты 2.pdf` (extracted to `assets/img/kp/`). Families with kids at the booth are fine; costumed kid portraits are not.
- Do not name specific museums (no Эрмитаж, РЖД etc.) - themes only. Railway theme uses the client's photo `kp/family-railway.jpg`.
- Manager: «Андрей Михалев - звоните по всем вопросам».
- New home block `src/partials/tour.html` (+ CSS `.tour*`, JS `[data-tour]`): sticky background of museum halls changing on scroll, guest card per step. t-1,3,5 are real SPb halls (Wikimedia); t-2 railway depot and t-4 dinosaur hall generated in Higgsfield.
- Wikimedia sources in `assets/img/spb/` (+ credits.json, kept off the server by .vercelignore). Every one used (rings s01-s18, tour) is credited in `src/partials/credits.html` on the contacts page - regenerate credits if the set changes.
- Hero is now an animated SCENE (`src/partials/hero-scene.html`, CSS `.scene*`, JS `[data-scene]` in main.js): photographer cutout `assets/img/gen/photographer.webp` (GPT Image, transparent bg) on the right, viewfinder corners + focus box hunt/lock, shutter flash from the speedlight (x 36 %, y 5 % of the cutout), a polaroid develops with the theme portrait (`assets/img/gen/pola-*.jpg`) and flies to a pile, then the hall changes. 6 hall/portrait pairs, ~5.4 s per cycle; pauses off-screen and in hidden tabs; static under reduced motion. Finale still uses the crossfade `museums-bg-b`.
- Hero and finale rings REMOVED at the client's request (2026-10-01): replaced by crossfading SPb museum halls `src/partials/museums-bg.html` / `museums-bg-b.html` (CSS `.mbg`, 7 images `assets/img/halls/h1..h7.jpg`, 6 s each, pure CSS). Ring partials still exist but are unused (lab.html too uses the new hero).
- Home: statement «Музею не нужен разговор про технологии» removed; «Пять шагов по созданию зоны притяжения» restored on home.
- (old) Rings rebuilt from 15 museum-safe images `assets/img/ring/m01..m15.jpg` (360 px).
- Open questions to the client: use the word «ИИ» like the deck does (currently avoided)? Confirm «0 ₽ вложений от музея».

## Next steps

1. DEPLOYED 2026-10-01 (commit 350f8b7). The Vercel project is connected to GitHub: `git push` to main auto-deploys in ~20 s. `vercel deploy --prod` from the CLI kept failing with «fetch failed» mid-upload (flaky network from the session sandbox) - just push instead. Verify with `curl -s https://photo-bureau.vercel.app/ | grep -o 'main.js?v=[0-9a-f]*'`.
2. Higgsfield is logged in (workspace Private, ultra). Model `gpt_image_2_5`, `--resolution 2k --quality high --wait`; run at most 2 jobs at once (7 parallel jobs failed with «API request failed»). Generated so far: halls railway/naval/dino (hero h5-h7, tour t-2/t-4) and family portraits `assets/img/gen/fam-{ball,naval,curio,whitenights}.jpg` (themes tiles, tour step 1). Client wants it to look EXPENSIVE (premium editorial light).
3. Wikimedia photos in use: only hero h1-h4 and tour t-1/t-3/t-5 (4 files); credits in `src/partials/credits.html` on contacts - update it whenever the set of used Wikimedia files changes.
4. Screenshot all pages at 1440 and 390 after the real tour images land.

## Testing notes (Chrome over CDP)

- Chrome was run with `--remote-debugging-port=9333` and a separate profile; helper scripts (audit, orbit check, slicer) were in the session scratchpad and are gone - rewrite if needed.
- For rAF animations in a background tab: `Page.bringToFront` + `Emulation.setFocusEmulationEnabled`. Use `Network.setCacheDisabled` to avoid stale CSS.
- Nudge window size before screenshots (old paint lingers); screenshots with `clip` can drop hover state.
- View Transitions do not fire under device emulation or with cache disabled.
- After string-replace edits to CSS, check brace balance and that no stray markup ended up in `<body>` - this broke twice.

## Rollback points

Git tags `v1-first-release`, `v2-before-cosmos`. Recent commits:

- `c1913c2` Два новых портрета в сетке образов на главной
- `d5c5fec` Кольцо по эллипсу без срезов, линза шире текста
- `07f502e` Стеклянная линза в меню, кольца - настоящие окружности с разными кадрами
- `96f7ae3` Движение по образцу Cosmos: объёмное кольцо, большая картинка, финал
