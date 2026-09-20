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
<meta name="theme-color" content="#f7f5f2">
<script>
  // выполняется до отрисовки: иначе выбранная гостем тёмная тема моргнёт белым
  try {{
    var t = localStorage.getItem("aib-theme");
    if (t === "dark") {{
      document.documentElement.setAttribute("data-theme", "dark");
    }}
  }} catch (e) {{}}
</script>
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
<noscript><style>
  .preloader{{display:none!important}}
  body.is-loading{{overflow:auto}}
  body.is-loading .hero__text>*,body.is-loading .hero__shot,body.is-loading .phero>.wrap>*{{opacity:1}}
</style></noscript>
</head>
<body class="is-loading">

<div class="preloader" id="preloader" role="status" aria-live="off" aria-label="Загрузка страницы">
  <span class="preloader__panel preloader__panel--t"></span>
  <span class="preloader__panel preloader__panel--b"></span>
  <div class="preloader__inner">
    <svg class="preloader__mark" viewBox="0 0 64 64" fill="none" aria-hidden="true">
      <circle class="preloader__track" cx="32" cy="32" r="27" stroke-width="2"/>
      <circle class="preloader__arc" cx="32" cy="32" r="27" stroke-width="2"
              stroke-linecap="round" stroke-dasharray="169.6" stroke-dashoffset="169.6"
              transform="rotate(-90 32 32)"/>
      <g class="preloader__blades" stroke-width="1.3" stroke-linejoin="round" stroke-linecap="round">
        <path class="p-hex" d="M45.0 32.0L38.5 20.7L25.5 20.7L19.0 32.0L25.5 43.3L38.5 43.3Z"/>
        <path d="M45.0 32.0L46.7 10.3"/>
        <path d="M38.5 20.7L20.5 8.5"/>
        <path d="M25.5 20.7L5.9 30.2"/>
        <path d="M19.0 32.0L17.3 53.7"/>
        <path d="M25.5 43.3L43.5 55.5"/>
        <path d="M38.5 43.3L58.1 33.8"/>
      </g>
      <circle class="preloader__iris" cx="32" cy="32" r="5.5"/>
    </svg>
    <span class="preloader__name" aria-hidden="true">AI BUREAU</span>
    <span class="preloader__pct" aria-hidden="true"><i data-pct>0</i>%</span>
  </div>
</div>

<header class="site-header">
  <div class="wrap nav">
    <a class="brand" href="index.html" aria-label="{brand}, на главную">
      <svg class="brand__mark" width="30" height="30" viewBox="0 0 30 30" fill="none" aria-hidden="true">
        <rect class="m-frame" x="1" y="6.5" width="28" height="19" rx="5" stroke-width="1.6"/>
        <circle class="m-lens" cx="15" cy="16" r="6" stroke-width="1.6"/>
        <circle class="m-dot" cx="15" cy="16" r="2.2"/>
        <path class="m-top" d="M10.5 6.5l1.8-3.2h5.4l1.8 3.2" stroke-width="1.6" stroke-linejoin="round"/>
      </svg>
      <span>{brand}<small>{brand_sub}</small></span>
    </a>
    <nav class="nav-links">
      {nav}
      <a class="btn btn--primary btn--sm nav-cta" href="contacts.html">Обсудить проект</a>
    </nav>
    <button class="theme-toggle" type="button" aria-label="Тёмная тема" aria-pressed="false">
      <svg class="i-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" aria-hidden="true">
        <circle cx="12" cy="12" r="4.2"/><path d="M12 2.6v2.2M12 19.2v2.2M2.6 12h2.2M19.2 12h2.2M5.3 5.3l1.6 1.6M17.1 17.1l1.6 1.6M18.7 5.3l-1.6 1.6M6.9 17.1l-1.6 1.6"/>
      </svg>
      <svg class="i-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
        <path d="M20 14.2A8.2 8.2 0 019.8 4a8.4 8.4 0 102 10.2 8.2 8.2 0 018.2 0z"/>
      </svg>
    </button>
    <button class="burger" type="button" aria-label="Меню" aria-expanded="false"><span></span></button>
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
          <svg class="brand__mark" width="30" height="30" viewBox="0 0 30 30" fill="none" aria-hidden="true">
            <rect class="m-frame" x="1" y="6.5" width="28" height="19" rx="5" stroke-width="1.6"/>
            <circle class="m-lens" cx="15" cy="16" r="6" stroke-width="1.6"/>
            <circle class="m-dot" cx="15" cy="16" r="2.2"/>
            <path class="m-top" d="M10.5 6.5l1.8-3.2h5.4l1.8 3.2" stroke-width="1.6" stroke-linejoin="round"/>
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


def label_tables(html_text):
    """Проставляет каждой ячейке подпись её колонки.

    На телефоне таблицы разворачиваются в карточки, и подпись из шапки
    становится заголовком строки - иначе на узком экране непонятно,
    что означает каждое значение.
    """
    def one_table(m):
        table = m.group(0)
        heads = re.findall(r"<th[^>]*>(.*?)</th>", table, re.S)
        heads = [re.sub(r"<[^>]+>", "", h).strip() for h in heads]
        if not heads:
            return table

        def row(rm):
            cells = re.split(r"(<td[^>]*>)", rm.group(0))
            idx = [0]

            def cell(cm):
                i = idx[0]
                idx[0] += 1
                if i < len(heads) and "data-label" not in cm.group(0):
                    return cm.group(0)[:-1] + ' data-label="%s">' % heads[i]
                return cm.group(0)

            return re.sub(r"<td[^>]*>", cell, rm.group(0))

        body = re.search(r"<tbody>.*?</tbody>", table, re.S)
        if not body:
            return table
        new_body = re.sub(r"<tr>.*?</tr>", row, body.group(0), flags=re.S)
        return table.replace(body.group(0), new_body)

    return re.sub(r"<table class=\"tbl\">.*?</table>", one_table, html_text, flags=re.S)


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
            body=label_tables(fill(raw.strip())),
            **CONFIG,
        )
        (ROOT / src.name).write_text(page, encoding="utf-8")
        made.append(src.name)
    print("Собрано:", ", ".join(made))


if __name__ == "__main__":
    build()
