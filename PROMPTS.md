# Библиотека пресетов «Миллениум»

Рабочий документ для фотографов и ретушёров. Промпты собраны под портреты гостей музея: главное требование - сохранить сходство.

## Порядок работы

1. **Отбор.** Берём кадр по пояс, с открытым лицом и ровным светом. Брак на входе останется браком на выходе.
2. **Промпт.** Копируем карточку целиком. Базовый блок сохранения внешности уже внутри, ничего не дописываем.
3. **Параметры.** Режим image-to-image, сила изменения 0.45-0.6, лицо дополнительно фиксируем маской.
4. **Серия.** Четыре варианта на кадр. Меньше - не из чего выбирать, больше - теряем время смены.
5. **Отбор и сдача.** Проверяем по чек-листу, апскейлим выбранный кадр, отдаём в печать и в галерею.

## Параметры генерации

| Параметр | Значение |
| --- | --- |
| Режим | image-to-image по исходному кадру, не text-to-image |
| Сила изменения | 0.45-0.55 для портрета по грудь, 0.55-0.65 для общего плана |
| Лицо | маска по лицу с силой 0.2-0.3, при потере сходства опускаем до 0.15 |
| Кадр | 4:5 для печати 10x15 и 20x30, 9:16 для соцсетей, 3:2 для постера |
| Разрешение | генерация от 1024 по короткой стороне, финал - апскейл до 3000 px |
| Серия | 4 кадра на сюжет, фиксируем seed удачного варианта для повторов |

## Чек-лист перед выдачей

- [ ] Гостей узнают с первого взгляда: лица, причёски, возраст - свои
- [ ] Свет на костюме совпадает с направлением света на лице
- [ ] Руки и пальцы целы, ничего лишнего в кадре не выросло
- [ ] Нет чужих логотипов, надписей и узнаваемых персонажей
- [ ] Глаза резкие, кожа с текстурой, без пластикового замыливания
- [ ] Шея и воротник соединяются естественно, головы «не приклеены»
- [ ] Кадр выдержит печать 20x30: нет каши в деталях после апскейла

## Служебные

### Базовый блок сохранения внешности

Вставляется в начало любого промпта. Держит лица гостей неизменными - это то, за что платят.

```text
Keep every person's face, facial features, skin tone, hair and age exactly as in the source photo. Keep the original position and order of people in the frame. Do not beautify, do not age up or down, do not change ethnicity or body type. Photorealistic editorial portrait, natural proportions, real fabric texture, fine skin texture preserved.
Shot on 85mm f/2.0, soft key light matching the direction of light in the source photo, gentle rim light, shallow depth of field, true-to-life colour, no plastic skin, print-ready detail.
```

Примечание: Никогда не убирайте этот блок ради «более красивого» результата.

### Негативный промпт

Один на все сюжеты. Ставится в поле negative prompt целиком.

```text
cartoon, anime, 3d render, cgi, plastic skin, waxy skin, airbrushed, beauty filter, changed face, different person, swapped faces, distorted eyes, crossed eyes, extra fingers, deformed hands, floating head, detached collar, mismatched lighting, harsh cutout edges, double exposure ghosting, modern objects in period scenes, text, watermark, signature, logo, brand marks, copyrighted characters, blurry, low resolution, oversharpen halo, heavy noise, blown highlights
```

Примечание: Если в кадре появляется чужое лицо - в первую очередь поднимаем вес этого блока.

## История и эпохи

### Императорский бал

Главный сюжет для дворцовых экспозиций. Парадный портрет семьи в бальных костюмах XVIII века.

```text
Keep every person's face, facial features, skin tone, hair and age exactly as in the source photo. Keep the original position and order of people in the frame. Do not beautify, do not age up or down, do not change ethnicity or body type. Photorealistic editorial portrait, natural proportions, real fabric texture, fine skin texture preserved.
The guests wear 18th-century court ball costumes: embroidered silk gowns with pearls, dark green or blue caftans with gold braid, lace cuffs. Background: grand palace ballroom with gilded carving, tall mirrors, crystal chandeliers and parquet floor, softly out of focus. Warm golden candlelight.
Shot on 85mm f/2.0, soft key light matching the direction of light in the source photo, gentle rim light, shallow depth of field, true-to-life colour, no plastic skin, print-ready detail.
```

Примечание: Позолоту держим в расфокусе: резкий узор спорит с лицами.

### Петровская эпоха

Для экспозиций начала XVIII века: камзолы, треуголки, карты и навигационные приборы.

```text
Keep every person's face, facial features, skin tone, hair and age exactly as in the source photo. Keep the original position and order of people in the frame. Do not beautify, do not age up or down, do not change ethnicity or body type. Photorealistic editorial portrait, natural proportions, real fabric texture, fine skin texture preserved.
The guests wear early 18th-century clothing: long buttoned coats, tricorn hats, linen shirts, simple wool dresses with aprons. Background: a study with nautical charts, a brass astrolabe, a globe and a window onto a river with sailing ships. Cool daylight from the window, warm candle accent.
Shot on 85mm f/2.0, soft key light matching the direction of light in the source photo, gentle rim light, shallow depth of field, true-to-life colour, no plastic skin, print-ready detail.
```

Примечание: Парики не надеваем: прятать волосы гостя значит терять сходство.

### Начало XX века

Портрет в стиле салонной фотографии начала прошлого века. Эпоху задаём одной фразой.

```text
Keep every person's face, facial features, skin tone, hair and age exactly as in the source photo. Keep the original position and order of people in the frame. Do not beautify, do not age up or down, do not change ethnicity or body type. Photorealistic editorial portrait, natural proportions, real fabric texture, fine skin texture preserved.
The guests wear authentic early twentieth century outfits with period-correct fabric and buttons, photographed in a period interior with patterned wallpaper, a tall window and a carved chair. Soft window light, restrained colour palette, subtle film grain, no modern objects in the frame.
Shot on 85mm f/2.0, soft key light matching the direction of light in the source photo, gentle rim light, shallow depth of field, true-to-life colour, no plastic skin, print-ready detail.
```

Примечание: Проверяем, что в кадр не попали современные предметы: часы, серьги, телефоны.

## Искусство

### Портрет в художественном стиле

Для художественных музеев: гость как герой картины, но фотографичный и узнаваемый.

```text
Keep every person's face, facial features, skin tone, hair and age exactly as in the source photo. Keep the original position and order of people in the frame. Do not beautify, do not age up or down, do not change ethnicity or body type. Photorealistic editorial portrait, natural proportions, real fabric texture, fine skin texture preserved.
Render the scene as a classical oil portrait in the manner of old masters: warm umber shadows, soft chiaroscuro, visible but fine brush texture on clothing and background only, faces remain photographic and sharp. Background: dark draped fabric and a hint of a marble column.
Shot on 85mm f/2.0, soft key light matching the direction of light in the source photo, gentle rim light, shallow depth of field, true-to-life colour, no plastic skin, print-ready detail.
```

Примечание: Мазок только на фоне и одежде. Лицо не «закрашиваем» - иначе гость себя не узнаёт.

### Мастерская художника

Семейный сюжет: палитры, мольберты, гипсовые головы, тёплый свет из высокого окна.

```text
Keep every person's face, facial features, skin tone, hair and age exactly as in the source photo. Keep the original position and order of people in the frame. Do not beautify, do not age up or down, do not change ethnicity or body type. Photorealistic editorial portrait, natural proportions, real fabric texture, fine skin texture preserved.
The guests wear linen shirts, artist aprons and simple period dresses, holding a palette and brushes. Background: a sunlit painter's studio with canvases, plaster busts, shelves with jars of pigment, a tall arched window. Warm afternoon light, dust in the air.
Shot on 85mm f/2.0, soft key light matching the direction of light in the source photo, gentle rim light, shallow depth of field, true-to-life colour, no plastic skin, print-ready detail.
```

Примечание: Кисти и палитры чаще всего ломают руки - проверяем пальцы отдельно.

## Морской и парадный Петербург

### Морской Петербург

Для морских экспозиций: парусный флот, мундиры, канаты и латунь.

```text
Keep every person's face, facial features, skin tone, hair and age exactly as in the source photo. Keep the original position and order of people in the frame. Do not beautify, do not age up or down, do not change ethnicity or body type. Photorealistic editorial portrait, natural proportions, real fabric texture, fine skin texture preserved.
The guests wear 19th-century naval uniforms and elegant travel dresses. Background: the deck of a tall sailing ship at a granite embankment, rigging and furled sails, a misty northern river behind. Cool silver morning light, light breeze in hair and fabric.
Shot on 85mm f/2.0, soft key light matching the direction of light in the source photo, gentle rim light, shallow depth of field, true-to-life colour, no plastic skin, print-ready detail.
```

Примечание: Знаки различия и флаги не воспроизводим точно: только обобщённые морские детали.

### Белые ночи

Летний сюжет: прогулка по набережной в костюмах XIX века под светлым ночным небом.

```text
Keep every person's face, facial features, skin tone, hair and age exactly as in the source photo. Keep the original position and order of people in the frame. Do not beautify, do not age up or down, do not change ethnicity or body type. Photorealistic editorial portrait, natural proportions, real fabric texture, fine skin texture preserved.
The guests wear 19th-century summer promenade clothes: light dresses, parasols, frock coats and top hats. Background: a wide granite river embankment with classical facades and a drawbridge in soft focus, pale pink and lilac sky of a northern white night.
Shot on 85mm f/2.0, soft key light matching the direction of light in the source photo, gentle rim light, shallow depth of field, true-to-life colour, no plastic skin, print-ready detail.
```

Примечание: Небо держим светлым и мягким, без заката: это не вечер, а белая ночь.

## Приключения и наука

### Экспедиция к динозаврам

Для палеонтологических и естественнонаучных залов. Хорошо продаётся семьям.

```text
Keep every person's face, facial features, skin tone, hair and age exactly as in the source photo. Keep the original position and order of people in the frame. Do not beautify, do not age up or down, do not change ethnicity or body type. Photorealistic editorial portrait, natural proportions, real fabric texture, fine skin texture preserved.
The guests wear expedition clothes: canvas shirts, wide-brimmed hats, field bags. Background: lush prehistoric valley with a waterfall and a large friendly dinosaur in the distance. Golden afternoon light, humid haze.
Shot on 85mm f/2.0, soft key light matching the direction of light in the source photo, gentle rim light, shallow depth of field, true-to-life colour, no plastic skin, print-ready detail.
```

Примечание: Динозавр всегда на заднем плане и не страшный.

### Кабинет редкостей

Для естественнонаучных и антропологических собраний: шкафы с диковинами, глобусы, микроскопы.

```text
Keep every person's face, facial features, skin tone, hair and age exactly as in the source photo. Keep the original position and order of people in the frame. Do not beautify, do not age up or down, do not change ethnicity or body type. Photorealistic editorial portrait, natural proportions, real fabric texture, fine skin texture preserved.
The guests wear 18th-century scholar clothing: dark coats with brass buttons, lace collars, modest dresses. Background: a cabinet of curiosities with glass cases of shells, minerals, skeletons of small animals, old globes and leather books. Warm candlelight, mysterious but friendly atmosphere.
Shot on 85mm f/2.0, soft key light matching the direction of light in the source photo, gentle rim light, shallow depth of field, true-to-life colour, no plastic skin, print-ready detail.
```

Примечание: Никаких заспиртованных экспонатов в кадре - только минералы, раковины, приборы.

### Подводный мир

Для морских и океанографических экспозиций, хорошо идёт летом.

```text
Keep every person's face, facial features, skin tone, hair and age exactly as in the source photo. Keep the original position and order of people in the frame. Do not beautify, do not age up or down, do not change ethnicity or body type. Photorealistic editorial portrait, natural proportions, real fabric texture, fine skin texture preserved.
The guests wear modern exploration diving suits with transparent bubble helmets showing faces clearly, surrounded by a coral reef, rays of sunlight from the surface, schools of small fish, a calm sea turtle nearby. Turquoise light, clear water, no bubbles covering faces.
Shot on 85mm f/2.0, soft key light matching the direction of light in the source photo, gentle rim light, shallow depth of field, true-to-life colour, no plastic skin, print-ready detail.
```

Примечание: Шлемы прозрачные и без бликов поверх лица, иначе теряется сходство.

## Космос

### Семейный экипаж

Групповой кадр для космических экспозиций. Самый продаваемый сюжет темы.

```text
Keep every person's face, facial features, skin tone, hair and age exactly as in the source photo. Keep the original position and order of people in the frame. Do not beautify, do not age up or down, do not change ethnicity or body type. Photorealistic editorial portrait, natural proportions, real fabric texture, fine skin texture preserved.
The family wears worn white flight suits with red stripes, seated together inside an orbital station module beside a large round window with the Earth behind them. Warm interior light, cool light from the window, visible fabric wear and straps.
Shot on 85mm f/2.0, soft key light matching the direction of light in the source photo, gentle rim light, shallow depth of field, true-to-life colour, no plastic skin, print-ready detail.
```

Примечание: Групповые кадры генерируем сериями по четыре: сходство держится не в каждом.

### Исследователи Марса

Сюжет на общий план, хорошо продаётся в формате постера.

```text
Keep every person's face, facial features, skin tone, hair and age exactly as in the source photo. Keep the original position and order of people in the frame. Do not beautify, do not age up or down, do not change ethnicity or body type. Photorealistic editorial portrait, natural proportions, real fabric texture, fine skin texture preserved.
The guests stand on a red rocky plain in dusty explorer spacesuits with open visors, looking at a distant research base with domes and antennas. Warm orange sunset haze, long soft shadows, fine dust in the air.
Shot on 85mm f/2.0, soft key light matching the direction of light in the source photo, gentle rim light, shallow depth of field, true-to-life colour, no plastic skin, print-ready detail.
```

Примечание: Для постера просим 3:2 и оставляем воздух справа под заголовок.

## Сказка и сезоны

### Сказочное королевство

Путешествие в сказку: замок на скале, парадные костюмы, тёплый закат.

```text
Keep every person's face, facial features, skin tone, hair and age exactly as in the source photo. Keep the original position and order of people in the frame. Do not beautify, do not age up or down, do not change ethnicity or body type. Photorealistic editorial portrait, natural proportions, real fabric texture, fine skin texture preserved.
The guests wear fairy-tale royal costumes: embroidered velvet doublets, flowing gowns, light circlets. Background: a castle on a cliff above a valley with a river, flowering garden terrace, warm sunset light.
Shot on 85mm f/2.0, soft key light matching the direction of light in the source photo, gentle rim light, shallow depth of field, true-to-life colour, no plastic skin, print-ready detail.
```

Примечание: Короны лёгкие и не закрывают лоб: причёска гостя должна читаться.

### Зимний город

Декабрьский набор: зимний город XIX века, огни, снег. Снимаем в ноябре, продаём весь декабрь.

```text
Keep every person's face, facial features, skin tone, hair and age exactly as in the source photo. Keep the original position and order of people in the frame. Do not beautify, do not age up or down, do not change ethnicity or body type. Photorealistic editorial portrait, natural proportions, real fabric texture, fine skin texture preserved.
The guests wear 19th-century winter clothes: fur-trimmed coats, muffs, warm hats. Background: an evening winter embankment with lanterns, a decorated tree and a horse-drawn sleigh in soft focus, gently falling snow. Warm light on faces, cool blue background.
Shot on 85mm f/2.0, soft key light matching the direction of light in the source photo, gentle rim light, shallow depth of field, true-to-life colour, no plastic skin, print-ready detail.
```

Примечание: Фонари держим в расфокусе: резкие огни перетягивают внимание с лиц.
