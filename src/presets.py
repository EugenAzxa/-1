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
    ("space", "Космос"),
    ("pro", "Профессии"),
    ("speed", "Скорость и спорт"),
    ("fantasy", "Фэнтези и сказка"),
    ("museum", "Музейные темы"),
    ("holiday", "Праздники"),
]

IDENTITY = (
    "Keep the child's face, facial features, skin tone, hair and age exactly as in the source photo. "
    "Do not beautify, do not age up, do not change ethnicity or body type. "
    "Photorealistic editorial portrait, natural child proportions, real fabric texture, fine skin texture preserved."
)
CAMERA = (
    "Shot on 85mm f/2.0, soft key light matching the direction of light in the source photo, gentle rim light, "
    "shallow depth of field, true-to-life colour, no plastic skin, print-ready detail."
)

PRESETS = [
    {
        "group": "base",
        "tag": "База",
        "title": "Базовый блок сохранения внешности",
        "desc": "Вставляется в начало любого промпта. Держит лицо ребёнка неизменным - это то, за что родители платят.",
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
            "changed face, different person, adult face, older child, distorted eyes, crossed eyes, "
            "extra fingers, deformed hands, malformed helmet, floating head, detached collar, "
            "mismatched lighting, harsh cutout edges, double exposure ghosting, "
            "text, watermark, signature, logo, brand marks, copyrighted characters, "
            "blurry, low resolution, oversharpen halo, heavy noise, blown highlights"
        ),
        "note": "Если в кадре появляется чужое лицо - в первую очередь поднимаем вес этого блока.",
    },
    {
        "group": "space",
        "tag": "Космос",
        "title": "Космонавт будущего",
        "desc": "Основной кадр космической темы. Шлем держим в руках, а не на голове: лицо должно быть открыто.",
        "prompt": (
            IDENTITY + "\n"
            "The child wears a modern white and graphite spacesuit with soft blue indicator lights, "
            "holding a mirrored helmet under one arm. Background: museum hall of a space centre, "
            "a lunar module and a large planet projection softly out of focus. "
            "Cool ambient light with warm accent from the left.\n" + CAMERA
        ),
        "note": "Отражения в стекле шлема проверяем отдельно: там чаще всего появляется мусор.",
    },
    {
        "group": "space",
        "tag": "Космос",
        "title": "Исследователь Марса",
        "desc": "Сюжет на общий план, хорошо продаётся в формате постера.",
        "prompt": (
            IDENTITY + "\n"
            "The child stands on a red rocky plain in a dusty explorer spacesuit with a life-support backpack, "
            "pointing at a distant research base with domes and antennas. Warm orange sunset haze, long soft shadows, "
            "fine dust in the air, epic wide scene.\n" + CAMERA
        ),
        "note": "Для постера просим 3:2 и оставляем воздух справа под заголовок миссии.",
    },
    {
        "group": "space",
        "tag": "Космос",
        "title": "Семейный экипаж",
        "desc": "Групповой кадр. Сохраняем расстановку людей из исходника, иначе теряется узнаваемость.",
        "prompt": (
            IDENTITY.replace("the child's", "each person's").replace("child", "person") + "\n"
            "The family wears worn white flight suits with red stripes, seated together inside an orbital station module "
            "beside a large round window with the Earth behind them. Keep the original position and order of people. "
            "Warm interior light, cool light from the window, visible fabric wear and straps.\n" + CAMERA
        ),
        "note": "Групповые кадры генерируем сериями по четыре: сходство держится не в каждом.",
    },
    {
        "group": "pro",
        "tag": "Профессии",
        "title": "Пожарный",
        "desc": "Самый востребованный образ у мальчиков 5-9 лет.",
        "prompt": (
            IDENTITY + "\n"
            "The child wears authentic fire-service turnout gear: dark jacket with reflective stripes, "
            "helmet pushed slightly back so the face stays fully visible. Background: fire station bay with a truck, "
            "warm amber light and soft smoke haze in the depth of the frame. Confident calm expression.\n" + CAMERA
        ),
        "note": "Никакого открытого огня рядом с ребёнком: только отсветы и дымка на фоне.",
    },
    {
        "group": "pro",
        "tag": "Профессии",
        "title": "Врач",
        "desc": "Хорошо работает для школьных наборов «кем я стану».",
        "prompt": (
            IDENTITY + "\n"
            "The child wears a crisp white medical coat over a light shirt, stethoscope around the neck. "
            "Background: bright modern clinic room, softly blurred equipment and a window with daylight. "
            "Friendly, calm expression, clean neutral colour palette.\n" + CAMERA
        ),
        "note": "Следим за бейджем: любые надписи убираем, они всегда выходят кривыми.",
    },
    {
        "group": "pro",
        "tag": "Профессии",
        "title": "Пилот",
        "desc": "Даёт эффектный кадр даже с посредственного исходника.",
        "prompt": (
            IDENTITY + "\n"
            "The child wears a navy airline pilot uniform with shoulder stripes and a cap, standing in an aircraft cockpit "
            "with instrument panels glowing softly. Sunrise light through the windshield, clouds far below. "
            "Proud, relaxed posture.\n" + CAMERA
        ),
        "note": "Погоны и кокарду делаем нейтральными, без эмблем авиакомпаний.",
    },
    {
        "group": "pro",
        "tag": "Профессии",
        "title": "Шеф-повар",
        "desc": "Тёплый бытовой сюжет, который любят родители девочек и мальчиков одинаково.",
        "prompt": (
            IDENTITY + "\n"
            "The child wears a white chef jacket and a classic chef hat, standing at a professional kitchen pass "
            "with copper pans and herbs around. Warm tungsten light, light steam in the air, "
            "cheerful working atmosphere.\n" + CAMERA
        ),
        "note": "Руки в кадре - частая проблема. Проще просить кадр по грудь.",
    },
    {
        "group": "speed",
        "tag": "Скорость",
        "title": "Гонщик",
        "desc": "Флагман для детских парков. Шлем под мышкой, лицо открыто.",
        "prompt": (
            IDENTITY + "\n"
            "The child wears a racing suit in deep red and graphite with plain unbranded patches and a fireproof collar, "
            "holding a racing helmet under one arm. Background: pit lane with a blurred race car and team garage lights. "
            "Late afternoon sun, slight heat haze, energetic mood.\n" + CAMERA
        ),
        "note": "Логотипы команд и спонсоров не рисуем: только выдуманные нашивки.",
    },
    {
        "group": "speed",
        "tag": "Скорость",
        "title": "Футболист",
        "desc": "Ставим под вечерний стадионный свет: кадр сразу читается как постер.",
        "prompt": (
            IDENTITY + "\n"
            "The child wears a plain football kit in blue and white with no logos, standing on a stadium pitch at dusk. "
            "Stadium floodlights create a strong rim light, crowd softly blurred in the background, "
            "light mist in the beams. Determined, happy expression.\n" + CAMERA
        ),
        "note": "Номер на футболке ставим двузначный, буквы не пишем.",
    },
    {
        "group": "speed",
        "tag": "Скорость",
        "title": "Балерина на сцене",
        "desc": "Сильный образ для девочек, продаётся в паре с парадным портретом.",
        "prompt": (
            IDENTITY + "\n"
            "The child wears a classical ballet costume with a soft tutu, standing on a theatre stage. "
            "Warm spotlight from above and behind, deep velvet darkness of the auditorium, delicate dust in the light beam. "
            "Graceful posture, calm confident expression.\n" + CAMERA
        ),
        "note": "Позу не меняем сильно: руки из исходника всегда достовернее сгенерированных.",
    },
    {
        "group": "fantasy",
        "tag": "Фэнтези",
        "title": "Галактический страж",
        "desc": "Наша замена «супергероям»: собственный костюм, никаких чужих франшиз.",
        "prompt": (
            IDENTITY + "\n"
            "The child wears an original heroic suit: matte navy armour plates with gold trim and a flowing deep-red cape, "
            "an abstract star emblem on the chest that belongs to no existing brand. "
            "Background: city rooftop at blue hour, distant lights, light wind in the cape. Brave, kind expression.\n" + CAMERA
        ),
        "note": "Эмблема всегда абстрактная. Любой намёк на известного персонажа - брак.",
    },
    {
        "group": "fantasy",
        "tag": "Фэнтези",
        "title": "Волшебная школа",
        "desc": "Атмосфера старой библиотеки без отсылок к конкретной франшизе.",
        "prompt": (
            IDENTITY + "\n"
            "The child wears a dark academic robe over a knitted vest, holding an old leather-bound book. "
            "Background: ancient library with tall shelves, floating candles, warm golden light and soft dust. "
            "Curious, slightly mischievous expression.\n" + CAMERA
        ),
        "note": "Никаких шарфов с цветами факультетов и узнаваемых гербов.",
    },
    {
        "group": "fantasy",
        "tag": "Фэнтези",
        "title": "Мир динозавров",
        "desc": "Приключенческий сюжет для парков и детских музеев.",
        "prompt": (
            IDENTITY + "\n"
            "The child wears a young palaeontologist outfit: khaki vest, rolled sleeves, field hat, "
            "standing in a prehistoric valley at sunrise with ferns and a huge peaceful sauropod far in the background. "
            "Golden light, morning mist, sense of wonder.\n" + CAMERA
        ),
        "note": "Хищников в детском наборе не ставим, только травоядные и на расстоянии.",
    },
    {
        "group": "fantasy",
        "tag": "Фэнтези",
        "title": "Подводный мир",
        "desc": "Хорошо заходит для океанариумов и летних сезонов.",
        "prompt": (
            IDENTITY + "\n"
            "The child wears a modern exploration diving suit with a transparent bubble helmet showing the face clearly, "
            "surrounded by a coral reef, rays of sunlight from the surface, schools of small fish, a calm sea turtle nearby. "
            "Turquoise light, clear water, no bubbles covering the face.\n" + CAMERA
        ),
        "note": "Шлем прозрачный и без бликов поверх лица, иначе теряется сходство.",
    },
    {
        "group": "museum",
        "tag": "Музей",
        "title": "Небылицы: сказочный портрет",
        "desc": "Для музеев небылиц и сказок: портрет в стиле старой книжной иллюстрации, но фотографичный.",
        "prompt": (
            IDENTITY + "\n"
            "The child wears a folk-tale costume: embroidered linen shirt, woven belt, soft fur-trimmed cloak. "
            "Background: wooden fairy-tale interior with a painted stove, warm candlelight, a cat on a bench. "
            "Slightly theatrical but photorealistic, storybook warmth.\n" + CAMERA
        ),
        "note": "Орнаменты берём обобщённые, без привязки к конкретному региону.",
    },
    {
        "group": "museum",
        "tag": "Музей",
        "title": "Мистика: готический портрет",
        "desc": "Взрослая версия. Для детей всегда собираем облегчённый вариант: меньше тьмы, больше тепла.",
        "prompt": (
            IDENTITY + "\n"
            "The subject wears a Victorian-style coat with a high collar, holding an old brass lantern. "
            "Background: dim study of a collector, glass cabinets, maps, fog behind the window, single candle warmth. "
            "Mysterious but not frightening, deep shadows with detail retained.\n" + CAMERA
        ),
        "note": "Для детского набора убираем туман и поднимаем экспозицию фона на две ступени.",
    },
    {
        "group": "museum",
        "tag": "Музей",
        "title": "Историческая эпоха",
        "desc": "Портрет в костюме выбранного века. Эпоху задаём одним словом в промпте.",
        "prompt": (
            IDENTITY + "\n"
            "The subject wears an authentic early twentieth century outfit with period-correct fabric and buttons, "
            "photographed in a period interior with patterned wallpaper and a tall window. "
            "Soft window light, restrained colour palette, subtle film grain, no modern objects in the frame.\n" + CAMERA
        ),
        "note": "Эпоху меняем одной фразой. Проверяем, что в кадр не попали современные предметы.",
    },
    {
        "group": "holiday",
        "tag": "Праздник",
        "title": "Новогодняя сказка",
        "desc": "Декабрьский набор. Снимаем в ноябре, продаём весь декабрь.",
        "prompt": (
            IDENTITY + "\n"
            "The child wears a cosy winter outfit: knitted sweater, soft scarf, light snow on the shoulders. "
            "Background: evening winter town with a decorated tree, warm garland bokeh, gently falling snow. "
            "Warm golden light on the face, cool blue tones in the background, joyful calm expression.\n" + CAMERA
        ),
        "note": "Гирлянды держим в расфокусе: резкие лампочки перетягивают внимание с лица.",
    },
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
    "Ребёнка узнают с первого взгляда: лицо, причёска, возраст - свои",
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
      'все промпты уже проверены на детских портретах.</p>\n'
      '    <div class="phero__actions">\n'
      '      <a class="btn btn--ghost" href="worlds.html">Витрина образов для клиента</a>\n'
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
           "Промпты отредактированы под детский портрет: главное требование - сохранить сходство.\n",
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
