#!/usr/bin/env python3
"""
Сборка статического сайта «Миллениум».

Запуск:  python3 build.py
Результат: готовые .html в корне репозитория (их и деплоим).

Всё, что меняется чаще всего - контакты, имя бренда, пункты меню -
лежит в CONFIG ниже. Правим в одном месте, пересобираем, пушим.
"""
import hashlib
import html
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).parent
PAGES = ROOT / "src" / "pages"

CONFIG = {
    "brand": "Миллениум",
    "brand_sub": "photo experience",
    "phone": "+7 (921) 406-33-84",
    "phone_href": "+79214063384",
    "manager": "Андрей",
    "city": "Москва и область, выезд по России",
    "domain": "https://millenium-photo.ru",
}

NAV = [
    ("index.html", "Главная"),
    ("museums.html", "Музеям и паркам"),
    ("schools.html", "Сады и школы"),
    ("worlds.html", "Образы"),
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
<meta property="og:image" content="{domain}/assets/img/kiosk/main.jpg">
<meta property="og:locale" content="ru_RU">
{robots}
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
  <span class="preloader__flash" aria-hidden="true"></span>
  <div class="preloader__inner" aria-hidden="true">

    <p class="preloader__brand">{brand}</p>

    <div class="finder">
      <div class="finder__shots">
        <img src="assets/img/intro/role-1.jpg" alt="" width="480" height="600" fetchpriority="high">
        <img src="assets/img/intro/role-2.jpg" alt="" width="480" height="600" fetchpriority="high">
        <img src="assets/img/intro/role-3.jpg" alt="" width="480" height="600" fetchpriority="high">
        <img src="assets/img/intro/role-4.jpg" alt="" width="480" height="600" fetchpriority="high">
      </div>
      <span class="finder__grain"></span>
      <span class="finder__vignette"></span>
      <span class="finder__blink"></span>
      <span class="finder__blind finder__blind--t"></span>
      <span class="finder__blind finder__blind--b"></span>
      <span class="finder__c finder__c--tl"></span>
      <span class="finder__c finder__c--tr"></span>
      <span class="finder__c finder__c--bl"></span>
      <span class="finder__c finder__c--br"></span>
      <svg class="finder__cam" viewBox="0 0 64 44" fill="none">
        <rect class="cam-body" x="1" y="9" width="62" height="34" rx="7"/>
        <path class="cam-top" d="M19 9l3.4-6.2h19.2L45 9"/>
        <circle class="cam-ring" cx="32" cy="26" r="11"/>
        <circle class="cam-lens" cx="32" cy="26" r="5.4"/>
        <circle class="cam-flash" cx="52" cy="16" r="2.2"/>
      </svg>
    </div>

    <div class="gauge">
      <span class="gauge__num"><span>01/04</span><span>02/04</span><span>03/04</span><span>04/04</span></span>
      <span class="gauge__track"><i data-bar></i></span>
      <span class="gauge__pct"><i data-pct>0</i>%</span>
    </div>

    <p class="preloader__title">Выбери свой мир</p>
    <p class="preloader__worlds">
      <span>космонавт</span><span>пожарный</span><span>шеф-повар</span><span>хоккеист</span>
    </p>
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
      <a class="btn btn--primary btn--sm nav-cta" href="tel:{phone_href}">Позвонить</a>
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
        <p style="color:var(--muted);font-size:15px;max-width:34ch">Фотозоны и авторские образы для музеев, парков, детских садов и школ. Снимаем, обрабатываем, отдаём гостю готовый кадр.</p>
      </div>
      <div>
        <h4>Разделы</h4>
        <nav>{fnav}</nav>
      </div>
      <div>
        <h4>Связаться</h4>
        <nav>
          <a class="footer-phone" href="tel:{phone_href}">{phone}</a>
          <span class="footer-who">{manager}, по всем вопросам</span>
          <a href="presets.html">Библиотека пресетов</a>
        </nav>
      </div>
    </div>
    <div class="wordmark" aria-hidden="true">{brand}</div>
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

    # фрагменты могут включать друг друга (финал включает кольцо) - раскрываем до конца
    for _ in range(5):
        new = re.sub(r"\{\{include:([a-z0-9_-]+)\}\}", include, text)
        if new == text:
            break
        text = new
    for key, value in CONFIG.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def stamp_assets(html_text):
    """Добавляет к картинкам метку версии: assets/img/x.jpg?v=<хэш файла>.

    Картинки кешируются на сутки, стили и скрипт браузер тоже держит у себя.
    Без метки заменённый файл с тем же именем ещё показывался бы старым -
    так и случилось и с кадром первого экрана, и со стилями. Метка меняется
    вместе с файлом, и браузер забирает новый.
    """
    def one(m):
        attr, path, q = m.group(1), m.group(2), m.group(3)
        f = ROOT / path
        if not f.exists():
            return m.group(0)
        st = f.stat()
        ver = hashlib.md5(f"{st.st_size}-{int(st.st_mtime)}".encode()).hexdigest()[:8]
        return f'{attr}="{path}?v={ver}"'

    return re.sub(r'(src|data-src|href)="(assets/[^"?]+\.(?:jpg|jpeg|png|webp|svg|css|js))"()', one, html_text)


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
            title=html.escape(fill(meta.get("title", CONFIG["brand"]))),
            desc=html.escape(fill(meta.get("desc", ""))),
            nav=nav_html(src.name),
            robots='<meta name="robots" content="noindex">' if src.name == "lab.html" else "",
            fnav=footer_nav(),
            body=label_tables(fill(raw.strip())),
            **CONFIG,
        )
        (ROOT / src.name).write_text(stamp_assets(page), encoding="utf-8")
        made.append(src.name)
    print("Собрано:", ", ".join(made))


if __name__ == "__main__":
    build()
