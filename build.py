#!/usr/bin/env python3
"""
Сборка статического сайта AI BUREAU.

Запуск:  python3 build.py
Результат: готовые .html в корне репозитория (их и деплоим).

Всё, что меняется чаще всего - контакты, имя бренда, пункты меню -
лежит в CONFIG ниже. Правим в одном месте, пересобираем, пушим.
"""
import html
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).parent
PAGES = ROOT / "src" / "pages"

CONFIG = {
    "brand": "AI BUREAU",
    "brand_sub": "photo experience",
    "phone": "+7 (995) 000-00-00",
    "phone_href": "+79950000000",
    "email": "hello@aibureau.studio",
    "telegram": "aibureau",
    "city": "Москва и область, выезд по России",
    "domain": "https://aibureau.studio",
}

NAV = [
    ("index.html", "Главная"),
    ("museums.html", "Музеям и паркам"),
    ("schools.html", "Сады и школы"),
    ("worlds.html", "AI-образы"),
    ("contacts.html", "Контакты"),
]

LAYOUT = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{domain}/assets/img/station-hall.jpg">
<meta property="og:locale" content="ru_RU">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
<header class="site-header">
  <div class="wrap nav">
    <a class="brand" href="index.html" aria-label="{brand}, на главную">
      <svg width="30" height="30" viewBox="0 0 30 30" fill="none" aria-hidden="true">
        <rect x="1" y="6.5" width="28" height="19" rx="5" stroke="#e8a33d" stroke-width="1.6"/>
        <circle cx="15" cy="16" r="6" stroke="#f3f5f9" stroke-width="1.6"/>
        <circle cx="15" cy="16" r="2.2" fill="#5b8cff"/>
        <path d="M10.5 6.5l1.8-3.2h5.4l1.8 3.2" stroke="#e8a33d" stroke-width="1.6" stroke-linejoin="round"/>
      </svg>
      <span>{brand}<small>{brand_sub}</small></span>
    </a>
    <button class="burger" type="button" aria-label="Меню" aria-expanded="false"><span></span></button>
    <nav class="nav-links">
      {nav}
      <a class="btn btn--primary btn--sm nav-cta" href="contacts.html">Обсудить проект</a>
    </nav>
  </div>
</header>

<main>
{body}
</main>

<footer class="site-footer">
  <div class="wrap">
    <div class="footer-top">
      <div>
        <a class="brand" href="index.html" style="margin-bottom:16px">
          <svg width="30" height="30" viewBox="0 0 30 30" fill="none" aria-hidden="true">
            <rect x="1" y="6.5" width="28" height="19" rx="5" stroke="#e8a33d" stroke-width="1.6"/>
            <circle cx="15" cy="16" r="6" stroke="#f3f5f9" stroke-width="1.6"/>
            <circle cx="15" cy="16" r="2.2" fill="#5b8cff"/>
            <path d="M10.5 6.5l1.8-3.2h5.4l1.8 3.2" stroke="#e8a33d" stroke-width="1.6" stroke-linejoin="round"/>
          </svg>
          <span>{brand}<small>{brand_sub}</small></span>
        </a>
        <p style="color:var(--muted);font-size:15px;max-width:34ch">Фотозоны и AI-образы для музеев, парков, детских садов и школ. Снимаем, обрабатываем, отдаём гостю готовый кадр.</p>
      </div>
      <div>
        <h4>Разделы</h4>
        <nav>{fnav}</nav>
      </div>
      <div>
        <h4>Связаться</h4>
        <nav>
          <a href="tel:{phone_href}">{phone}</a>
          <a href="mailto:{email}">{email}</a>
          <a href="https://t.me/{telegram}" target="_blank" rel="noopener">Telegram: @{telegram}</a>
          <a href="presets.html">Библиотека пресетов</a>
        </nav>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; <span data-year></span> {brand}. {city}</span>
      <span>Работаем по договору с юрлицами и родительскими комитетами</span>
    </div>
  </div>
</footer>
<script src="assets/js/main.js"></script>
</body>
</html>
"""


def nav_html(active, css_class=""):
    out = []
    for href, label in NAV:
        cls = ' class="is-active"' if href == active else ""
        if css_class and not cls:
            cls = f' class="{css_class}"'
        out.append(f'<a href="{href}"{cls}>{label}</a>')
    return "\n      ".join(out)


def footer_nav():
    out = [f'<a href="{href}">{label}</a>' for href, label in NAV]
    return "\n          ".join(out)


PARTIALS = ROOT / "src" / "partials"


def fill(text):
    """Подстановка {{include:имя}} и значений из CONFIG."""
    def include(m):
        return (PARTIALS / (m.group(1) + ".html")).read_text(encoding="utf-8")

    text = re.sub(r"\{\{include:([a-z0-9_-]+)\}\}", include, text)
    for key, value in CONFIG.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def build():
    # библиотека пресетов собирается из src/presets.py
    sys.path.insert(0, str(ROOT / "src"))
    import presets
    presets.render()

    made = []
    for src in sorted(PAGES.glob("*.html")):
        raw = src.read_text(encoding="utf-8")
        meta = {}
        m = re.match(r"<!--\s*(.*?)\s*-->\s*", raw, re.S)
        if m:
            for line in m.group(1).splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip()] = v.strip()
            raw = raw[m.end():]
        page = LAYOUT.format(
            title=html.escape(meta.get("title", CONFIG["brand"])),
            desc=html.escape(meta.get("desc", "")),
            nav=nav_html(src.name),
            fnav=footer_nav(),
            body=fill(raw.strip()),
            **CONFIG,
        )
        (ROOT / src.name).write_text(page, encoding="utf-8")
        made.append(src.name)
    print("Собрано:", ", ".join(made))


if __name__ == "__main__":
    build()
