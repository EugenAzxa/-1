# Миллениум - session notes and handoff

Last updated: 2026-10-01. Read this file first in a new session, then `README.md` and `docs/DESIGN-cosmos.md`.

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
npx --yes vercel@latest deploy --prod --yes   # retry once if "Not authorized"
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

## Next steps (unfinished when this session ended)

1. **Worlds page «Профессии» row** - the client asked to swap photos there.
   - `assets/img/works/chef-girl.jpg` is already cut (girl in chef hat, from the kids collage) and committed but NOT used yet.
   - In `src/pages/worlds.html` line ~96: change `works/chef.jpg` to `works/chef-girl.jpg`, alt «Девочка в поварском колпаке на кухне».
   - Line ~112 («Скорость и спорт», Гонщик): change `works/racer.jpg` (Red Bull boy) to `works/racer-speed.jpg`; adjust alt/caption from «за рулём болида» to helmet/track wording.
   - Then build, screenshot both rows at 1440 and 390, deploy, commit, push, update `assets/img/works/README.md`.
2. Tell the client honestly: there are no other photos for Пожарный, Пилот, Врач. Offer either new profession cards from the spare portraits (художник, виолончелист, сыщик, ковбой, ретро, диско) or new generated shots.
3. `src/pages/schools.html` line ~93 «Профессии» card still uses `chef.jpg` (boy) - ask if it should also change.

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
