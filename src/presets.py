#!/usr/bin/env python3
"""
Библиотека пресетов - единый источник правды.

Отсюда собираются:
  * src/pages/presets.html - страница для фотографов и ретушёров
  * PROMPTS.md             - та же библиотека текстом, чтобы отдать команде

Правим промпты только здесь, потом `python3 build.py` (он вызывает этот файл сам).
"""
import html
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

GROUPS = [
    ("base", "Служебные"),
    ("history", "История и эпохи"),
    ("art", "Искусство"),
    ("city", "Морская история и парадные залы"),
    ("adventure", "Приключения и наука"),
    ("space", "Космос"),
    ("fairy", "Сказка и сезоны"),
]

IDENTITY = (
    "Keep every person's face, facial features, skin tone, hair and age exactly as in the source photo. "
    "Keep the original position and order of people in the frame. "
    "Do not beautify, do not age up or down, do not change ethnicity or body type. "
    "Photorealistic editorial portrait, natural proportions, real fabric texture, fine skin texture preserved."
)
CAMERA = (
    "Shot on 85mm f/2.0, soft key light matching the direction of light in the source photo, gentle rim light, "
    "shallow depth of field, true-to-life colour, no plastic skin, print-ready detail."
)


def preset(group, tag, title, desc, scene, note):
    return {"group": group, "tag": tag, "title": title, "desc": desc,
            "prompt": IDENTITY + "\n" + scene + "\n" + CAMERA, "note": note}


PRESETS = [
    {
        "group": "base",
        "tag": "База",
        "title": "Базовый блок сохранения внешности",
        "desc": "Вставляется в начало любого промпта. Держит лица гостей неизменными - это то, за что платят.",
        "prompt": IDENTITY + "\n" + CAMERA,
        "note": "Никогда не убирайте этот блок ради «более красивого» результата.",
    },
    {
        "group": "base",
        "tag": "База",
        "title": "Негативный промпт",
        "desc": "Один на все сюжеты. Ставится в поле negative prompt целиком.",
        "prompt": (
            "cartoon, anime, 3d render, cgi, plastic skin, waxy skin, airbrushed, beauty filter, "
            "changed face, different person, swapped faces, distorted eyes, crossed eyes, "
            "extra fingers, deformed hands, floating head, detached collar, "
            "mismatched lighting, harsh cutout edges, double exposure ghosting, modern objects in period scenes, "
            "text, watermark, signature, logo, brand marks, copyrighted characters, "
            "blurry, low resolution, oversharpen halo, heavy noise, blown highlights"
        ),
        "note": "Если в кадре появляется чужое лицо - в первую очередь поднимаем вес этого блока.",
    },
    preset("history", "Эпоха", "Императорский бал",
           "Главный сюжет для дворцовых экспозиций. Парадный портрет семьи в бальных костюмах XVIII века.",
           "The guests wear 18th-century court ball costumes: embroidered silk gowns with pearls, "
           "dark green or blue caftans with gold braid, lace cuffs. Background: grand palace ballroom with gilded carving, "
           "tall mirrors, crystal chandeliers and parquet floor, softly out of focus. Warm golden candlelight.",
           "Позолоту держим в расфокусе: резкий узор спорит с лицами."),
    preset("history", "Эпоха", "Петровская эпоха",
           "Для экспозиций начала XVIII века: камзолы, треуголки, карты и навигационные приборы.",
           "The guests wear early 18th-century clothing: long buttoned coats, tricorn hats, linen shirts, simple wool dresses with aprons. "
           "Background: a study with nautical charts, a brass astrolabe, a globe and a window onto a river with sailing ships. "
           "Cool daylight from the window, warm candle accent.",
           "Парики не надеваем: прятать волосы гостя значит терять сходство."),
    preset("history", "Эпоха", "Начало XX века",
           "Портрет в стиле салонной фотографии начала прошлого века. Эпоху задаём одной фразой.",
           "The guests wear authentic early twentieth century outfits with period-correct fabric and buttons, "
           "photographed in a period interior with patterned wallpaper, a tall window and a carved chair. "
           "Soft window light, restrained colour palette, subtle film grain, no modern objects in the frame.",
           "Проверяем, что в кадр не попали современные предметы: часы, серьги, телефоны."),
    preset("art", "Искусство", "Портрет в художественном стиле",
           "Для художественных музеев: гость как герой картины, но фотографичный и узнаваемый.",
           "Render the scene as a classical oil portrait in the manner of old masters: warm umber shadows, soft chiaroscuro, "
           "visible but fine brush texture on clothing and background only, faces remain photographic and sharp. "
           "Background: dark draped fabric and a hint of a marble column.",
           "Мазок только на фоне и одежде. Лицо не «закрашиваем» - иначе гость себя не узнаёт."),
    preset("art", "Искусство", "Мастерская художника",
           "Семейный сюжет: палитры, мольберты, гипсовые головы, тёплый свет из высокого окна.",
           "The guests wear linen shirts, artist aprons and simple period dresses, holding a palette and brushes. "
           "Background: a sunlit painter's studio with canvases, plaster busts, shelves with jars of pigment, a tall arched window. "
           "Warm afternoon light, dust in the air.",
           "Кисти и палитры чаще всего ломают руки - проверяем пальцы отдельно."),
    preset("city", "История", "Морская история",
           "Для морских экспозиций: парусный флот, мундиры, канаты и латунь.",
           "The guests wear 19th-century naval uniforms and elegant travel dresses. "
           "Background: the deck of a tall sailing ship at a granite embankment, rigging and furled sails, a misty northern river behind. "
           "Cool silver morning light, light breeze in hair and fabric.",
           "Знаки различия и флаги не воспроизводим точно: только обобщённые морские детали."),
    preset("city", "История", "Белые ночи",
           "Летний сюжет: прогулка по набережной в костюмах XIX века под светлым ночным небом.",
           "The guests wear 19th-century summer promenade clothes: light dresses, parasols, frock coats and top hats. "
           "Background: a wide granite river embankment with classical facades and a drawbridge in soft focus, "
           "pale pink and lilac sky of a northern white night.",
           "Небо держим светлым и мягким, без заката: это не вечер, а белая ночь."),
    preset("adventure", "Приключения", "Экспедиция к динозаврам",
           "Для палеонтологических и естественнонаучных залов. Хорошо продаётся семьям.",
           "The guests wear expedition clothes: canvas shirts, wide-brimmed hats, field bags. "
           "Background: lush prehistoric valley with a waterfall and a large friendly dinosaur in the distance. "
           "Golden afternoon light, humid haze.",
           "Динозавр всегда на заднем плане и не страшный."),
    preset("adventure", "Приключения", "Кабинет редкостей",
           "Для естественнонаучных и антропологических собраний: шкафы с диковинами, глобусы, микроскопы.",
           "The guests wear 18th-century scholar clothing: dark coats with brass buttons, lace collars, modest dresses. "
           "Background: a cabinet of curiosities with glass cases of shells, minerals, skeletons of small animals, old globes and leather books. "
           "Warm candlelight, mysterious but friendly atmosphere.",
           "Никаких заспиртованных экспонатов в кадре - только минералы, раковины, приборы."),
    preset("adventure", "Приключения", "Подводный мир",
           "Для морских и океанографических экспозиций, хорошо идёт летом.",
           "The guests wear modern exploration diving suits with transparent bubble helmets showing faces clearly, "
           "surrounded by a coral reef, rays of sunlight from the surface, schools of small fish, a calm sea turtle nearby. "
           "Turquoise light, clear water, no bubbles covering faces.",
           "Шлемы прозрачные и без бликов поверх лица, иначе теряется сходство."),
    preset("space", "Космос", "Семейный экипаж",
           "Групповой кадр для космических экспозиций. Самый продаваемый сюжет темы.",
           "The family wears worn white flight suits with red stripes, seated together inside an orbital station module "
           "beside a large round window with the Earth behind them. Warm interior light, cool light from the window, "
           "visible fabric wear and straps.",
           "Групповые кадры генерируем сериями по четыре: сходство держится не в каждом."),
    preset("space", "Космос", "Исследователи Марса",
           "Сюжет на общий план, хорошо продаётся в формате постера.",
           "The guests stand on a red rocky plain in dusty explorer spacesuits with open visors, "
           "looking at a distant research base with domes and antennas. Warm orange sunset haze, long soft shadows, fine dust in the air.",
           "Для постера просим 3:2 и оставляем воздух справа под заголовок."),
    preset("fairy", "Сказка", "Сказочное королевство",
           "Путешествие в сказку: замок на скале, парадные костюмы, тёплый закат.",
           "The guests wear fairy-tale royal costumes: embroidered velvet doublets, flowing gowns, light circlets. "
           "Background: a castle on a cliff above a valley with a river, flowering garden terrace, warm sunset light.",
           "Короны лёгкие и не закрывают лоб: причёска гостя должна читаться."),
    preset("fairy", "Сезон", "Зимний город",
           "Декабрьский набор: зимний город XIX века, огни, снег. Снимаем в ноябре, продаём весь декабрь.",
           "The guests wear 19th-century winter clothes: fur-trimmed coats, muffs, warm hats. "
           "Background: an evening winter embankment with lanterns, a decorated tree and a horse-drawn sleigh in soft focus, gently falling snow. "
           "Warm light on faces, cool blue background.",
           "Фонари держим в расфокусе: резкие огни перетягивают внимание с лиц."),
]

WORKFLOW = [
    ("01", "Отбор", "Берём кадр по пояс, с открытым лицом и ровным светом. Брак на входе останется браком на выходе."),
    ("02", "Промпт", "Копируем карточку целиком. Базовый блок сохранения внешности уже внутри, ничего не дописываем."),
    ("03", "Параметры", "Режим image-to-image, сила изменения 0.45-0.6, лицо дополнительно фиксируем маской."),
    ("04", "Серия", "Четыре варианта на кадр. Меньше - не из чего выбирать, больше - теряем время смены."),
    ("05", "Отбор и сдача", "Проверяем по чек-листу, апскейлим выбранный кадр, отдаём в печать и в галерею."),
]

PARAMS = [
    ("Режим", "image-to-image по исходному кадру, не text-to-image"),
    ("Сила изменения", "0.45-0.55 для портрета по грудь, 0.55-0.65 для общего плана"),
    ("Лицо", "маска по лицу с силой 0.2-0.3, при потере сходства опускаем до 0.15"),
    ("Кадр", "4:5 для печати 10x15 и 20x30, 9:16 для соцсетей, 3:2 для постера"),
    ("Разрешение", "генерация от 1024 по короткой стороне, финал - апскейл до 3000 px"),
    ("Серия", "4 кадра на сюжет, фиксируем seed удачного варианта для повторов"),
]

CHECKS = [
    "Гостей узнают с первого взгляда: лица, причёски, возраст - свои",
    "Свет на костюме совпадает с направлением света на лице",
    "Руки и пальцы целы, ничего лишнего в кадре не выросло",
    "Нет чужих логотипов, надписей и узнаваемых персонажей",
    "Глаза резкие, кожа с текстурой, без пластикового замыливания",
    "Шея и воротник соединяются естественно, головы «не приклеены»",
    "Кадр выдержит печать 20x30: нет каши в деталях после апскейла",
]


def page_html():
    out = []
    a = out.append
    a('<!--\ntitle: Библиотека пресетов для фотографов и ретушёров - {{brand}}\n'
      'desc: Рабочая страница команды: промпты по сюжетам, параметры генерации и чек-лист отбора кадров.\n-->\n')
    a('<section class="phero phero--blue">\n  <div class="wrap">\n'
      '    <span class="eyebrow eyebrow--blue">Для фотографов и ретушёров</span>\n'
      '    <h1>Библиотека пресетов</h1>\n'
      '    <p class="lede">Рабочая страница смены. Берём исходник, копируем карточку сюжета целиком, '
      'генерируем серию, отбираем по чек-листу. Ничего придумывать на ходу не нужно: '
      'все промпты собраны под семейные и индивидуальные портреты в музее.</p>\n'
      '    <div class="phero__actions">\n'
      '      <a class="btn btn--ghost" href="worlds.html">Витрина сюжетов для клиента</a>\n'
      '    </div>\n'
      '    <div class="phero__strip"><span><b>%d</b> пресетов в наборе</span>'
      '<span><b>4 кадра</b> серия на сюжет</span>'
      '<span><b>1 базовый блок</b> во всех промптах</span></div>\n'
      '  </div>\n</section>\n' % (len([p for p in PRESETS if p["group"] != "base"])))

    a('<section class="section section--alt">\n  <div class="wrap">\n'
      '    <div class="head reveal"><span class="eyebrow">Порядок работы</span><h2>Пять шагов смены</h2></div>\n'
      '    <div class="steps reveal">\n')
    for num, title, text in WORKFLOW:
        a(f'      <div class="step"><b>{num}</b><h4>{title}</h4><p>{text}</p></div>\n')
    a('    </div>\n  </div>\n</section>\n')

    a('<section class="section">\n  <div class="wrap">\n'
      '    <div class="head reveal"><span class="eyebrow eyebrow--blue">Промпты</span>'
      '<h2>Пресеты по сюжетам</h2>'
      '<p class="lede">Кнопка копирует текст карточки целиком, вместе с блоком сохранения внешности.</p></div>\n')
    a('    <div class="filters reveal">\n      <button class="is-on" data-filter="all">Все</button>\n')
    for key, label in GROUPS:
        a(f'      <button data-filter="{key}">{label}</button>\n')
    a('    </div>\n    <div class="grid grid--2">\n')
    for p in PRESETS:
        a(f'      <div class="preset reveal" data-group="{p["group"]}">\n'
          f'        <div class="preset__head"><h3>{html.escape(p["title"])}</h3>'
          f'<span class="preset__tag">{html.escape(p["tag"])}</span></div>\n'
          f'        <p class="preset__desc">{html.escape(p["desc"])}</p>\n'
          f'        <pre>{html.escape(p["prompt"])}</pre>\n'
          f'        <div class="preset__foot">\n'
          f'          <button class="copy" type="button">'
          f'<svg width="15" height="15" viewBox="0 0 16 16" fill="none" aria-hidden="true">'
          f'<rect x="5" y="5" width="9" height="9" rx="2" stroke="currentColor" stroke-width="1.5"/>'
          f'<path d="M11 5V4a2 2 0 00-2-2H4a2 2 0 00-2 2v5a2 2 0 002 2h1" stroke="currentColor" stroke-width="1.5"/></svg>'
          f'<span>Копировать</span></button>\n'
          f'          <span class="preset__note">{html.escape(p["note"])}</span>\n'
          f'        </div>\n      </div>\n')
    a('    </div>\n  </div>\n</section>\n')

    a('<section class="section section--alt">\n  <div class="wrap">\n'
      '    <div class="grid grid--2">\n'
      '      <div class="reveal">\n'
      '        <span class="eyebrow">Параметры</span><h2>Настройки генерации</h2>\n'
      '        <div class="tbl-scroll mt-m"><table class="tbl"><tbody>\n')
    for k, v in PARAMS:
        a(f'          <tr><td style="width:34%"><b>{k}</b></td><td>{v}</td></tr>\n')
    a('        </tbody></table></div>\n      </div>\n'
      '      <div class="reveal" data-delay="80">\n'
      '        <span class="eyebrow eyebrow--blue">Контроль</span><h2>Чек-лист перед выдачей</h2>\n'
      '        <ul class="list list--blue mt-m">\n')
    for c in CHECKS:
        a(f'          <li>{c}</li>\n')
    a('        </ul>\n'
      '        <p class="note mt-s">Если хотя бы один пункт не выполнен, кадр не уходит гостю. '
      'Лучше переснять, чем вернуть деньги и репутацию.</p>\n'
      '      </div>\n    </div>\n  </div>\n</section>\n')

    a('{{include:cta}}\n')
    return "".join(out)


def markdown():
    out = ["# Библиотека пресетов «Миллениум»\n",
           "\nРабочий документ для фотографов и ретушёров. "
           "Промпты собраны под портреты гостей музея: главное требование - сохранить сходство.\n",
           "\n## Порядок работы\n\n"]
    for num, title, text in WORKFLOW:
        out.append(f"{int(num)}. **{title}.** {text}\n")
    out.append("\n## Параметры генерации\n\n| Параметр | Значение |\n| --- | --- |\n")
    for k, v in PARAMS:
        out.append(f"| {k} | {v} |\n")
    out.append("\n## Чек-лист перед выдачей\n\n")
    for c in CHECKS:
        out.append(f"- [ ] {c}\n")
    current = None
    for p in PRESETS:
        label = dict(GROUPS)[p["group"]]
        if label != current:
            current = label
            out.append(f"\n## {label}\n")
        out.append(f"\n### {p['title']}\n\n{p['desc']}\n\n```text\n{p['prompt']}\n```\n\nПримечание: {p['note']}\n")
    return "".join(out)


def render():
    (ROOT / "src" / "pages" / "presets.html").write_text(page_html(), encoding="utf-8")
    (ROOT / "PROMPTS.md").write_text(markdown(), encoding="utf-8")


if __name__ == "__main__":
    render()
    print("presets.html и PROMPTS.md обновлены")
