# Библиотека пресетов AI BUREAU

Рабочий документ для фотографов и ретушёров. Промпты отредактированы под детский портрет: главное требование - сохранить сходство.

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

- [ ] Ребёнка узнают с первого взгляда: лицо, причёска, возраст - свои
- [ ] Свет на костюме совпадает с направлением света на лице
- [ ] Руки и пальцы целы, ничего лишнего в кадре не выросло
- [ ] Нет чужих логотипов, надписей и узнаваемых персонажей
- [ ] Глаза резкие, кожа с текстурой, без пластикового замыливания
- [ ] Шея и воротник соединяются естественно, головы «не приклеены»
- [ ] Кадр выдержит печать 20x30: нет каши в деталях после апскейла

## Служебные

### Базовый блок сохранения внешности

Вставляется в начало любого промпта. Держит лицо ребёнка неизменным - это то, за что родители платят.

```text
Keep the child's face, facial features, skin tone, hair and age exactly as in the source photo. Do not beautify, do not age up, do not change ethnicity or body type. Photorealistic editorial portrait, natural child proportions, real fabric texture, fine skin texture preserved.
Shot on 85mm f/2.0, soft key light matching the direction of light in the source photo, gentle rim light, shallow depth of field, true-to-life colour, no plastic skin, print-ready detail.
```

Примечание: Никогда не убирайте этот блок ради «более красивого» результата.

### Негативный промпт

Один на все сюжеты. Ставится в поле negative prompt целиком.

```text
cartoon, anime, 3d render, cgi, plastic skin, waxy skin, airbrushed, beauty filter, changed face, different person, adult face, older child, distorted eyes, crossed eyes, extra fingers, deformed hands, malformed helmet, floating head, detached collar, mismatched lighting, harsh cutout edges, double exposure ghosting, text, watermark, signature, logo, brand marks, copyrighted characters, blurry, low resolution, oversharpen halo, heavy noise, blown highlights
```

Примечание: Если в кадре появляется чужое лицо - в первую очередь поднимаем вес этого блока.

## Космос

### Космонавт будущего

Основной кадр космической темы. Шлем держим в руках, а не на голове: лицо должно быть открыто.

```text
Keep the child's face, facial features, skin tone, hair and age exactly as in the source photo. Do not beautify, do not age up, do not change ethnicity or body type. Photorealistic editorial portrait, natural child proportions, real fabric texture, fine skin texture preserved.
The child wears a modern white and graphite spacesuit with soft blue indicator lights, holding a mirrored helmet under one arm. Background: museum hall of a space centre, a lunar module and a large planet projection softly out of focus. Cool ambient light with warm accent from the left.
Shot on 85mm f/2.0, soft key light matching the direction of light in the source photo, gentle rim light, shallow depth of field, true-to-life colour, no plastic skin, print-ready detail.
```

Примечание: Отражения в стекле шлема проверяем отдельно: там чаще всего появляется мусор.

### Исследователь Марса

Сюжет на общий план, хорошо продаётся в формате постера.

```text
Keep the child's face, facial features, skin tone, hair and age exactly as in the source photo. Do not beautify, do not age up, do not change ethnicity or body type. Photorealistic editorial portrait, natural child proportions, real fabric texture, fine skin texture preserved.
The child stands on a red rocky plain in a dusty explorer spacesuit with a life-support backpack, pointing at a distant research base with domes and antennas. Warm orange sunset haze, long soft shadows, fine dust in the air, epic wide scene.
Shot on 85mm f/2.0, soft key light matching the direction of light in the source photo, gentle rim light, shallow depth of field, true-to-life colour, no plastic skin, print-ready detail.
```

Примечание: Для постера просим 3:2 и оставляем воздух справа под заголовок миссии.

### Семейный экипаж

Групповой кадр. Сохраняем расстановку людей из исходника, иначе теряется узнаваемость.

```text
Keep each person's face, facial features, skin tone, hair and age exactly as in the source photo. Do not beautify, do not age up, do not change ethnicity or body type. Photorealistic editorial portrait, natural person proportions, real fabric texture, fine skin texture preserved.
The family wears worn white flight suits with red stripes, seated together inside an orbital station module beside a large round window with the Earth behind them. Keep the original position and order of people. Warm interior light, cool light from the window, visible fabric wear and straps.
Shot on 85mm f/2.0, soft key light matching the direction of light in the source photo, gentle rim light, shallow depth of field, true-to-life colour, no plastic skin, print-ready detail.
```

Примечание: Групповые кадры генерируем сериями по четыре: сходство держится не в каждом.

## Профессии

### Пожарный

Самый востребованный образ у мальчиков 5-9 лет.

```text
Keep the child's face, facial features, skin tone, hair and age exactly as in the source photo. Do not beautify, do not age up, do not change ethnicity or body type. Photorealistic editorial portrait, natural child proportions, real fabric texture, fine skin texture preserved.
The child wears authentic fire-service turnout gear: dark jacket with reflective stripes, helmet pushed slightly back so the face stays fully visible. Background: fire station bay with a truck, warm amber light and soft smoke haze in the depth of the frame. Confident calm expression.
Shot on 85mm f/2.0, soft key light matching the direction of light in the source photo, gentle rim light, shallow depth of field, true-to-life colour, no plastic skin, print-ready detail.
```

Примечание: Никакого открытого огня рядом с ребёнком: только отсветы и дымка на фоне.

### Врач

Хорошо работает для школьных наборов «кем я стану».

```text
Keep the child's face, facial features, skin tone, hair and age exactly as in the source photo. Do not beautify, do not age up, do not change ethnicity or body type. Photorealistic editorial portrait, natural child proportions, real fabric texture, fine skin texture preserved.
The child wears a crisp white medical coat over a light shirt, stethoscope around the neck. Background: bright modern clinic room, softly blurred equipment and a window with daylight. Friendly, calm expression, clean neutral colour palette.
Shot on 85mm f/2.0, soft key light matching the direction of light in the source photo, gentle rim light, shallow depth of field, true-to-life colour, no plastic skin, print-ready detail.
```

Примечание: Следим за бейджем: любые надписи убираем, они всегда выходят кривыми.

### Пилот

Даёт эффектный кадр даже с посредственного исходника.

```text
Keep the child's face, facial features, skin tone, hair and age exactly as in the source photo. Do not beautify, do not age up, do not change ethnicity or body type. Photorealistic editorial portrait, natural child proportions, real fabric texture, fine skin texture preserved.
The child wears a navy airline pilot uniform with shoulder stripes and a cap, standing in an aircraft cockpit with instrument panels glowing softly. Sunrise light through the windshield, clouds far below. Proud, relaxed posture.
Shot on 85mm f/2.0, soft key light matching the direction of light in the source photo, gentle rim light, shallow depth of field, true-to-life colour, no plastic skin, print-ready detail.
```

Примечание: Погоны и кокарду делаем нейтральными, без эмблем авиакомпаний.

### Шеф-повар

Тёплый бытовой сюжет, который любят родители девочек и мальчиков одинаково.

```text
Keep the child's face, facial features, skin tone, hair and age exactly as in the source photo. Do not beautify, do not age up, do not change ethnicity or body type. Photorealistic editorial portrait, natural child proportions, real fabric texture, fine skin texture preserved.
The child wears a white chef jacket and a classic chef hat, standing at a professional kitchen pass with copper pans and herbs around. Warm tungsten light, light steam in the air, cheerful working atmosphere.
Shot on 85mm f/2.0, soft key light matching the direction of light in the source photo, gentle rim light, shallow depth of field, true-to-life colour, no plastic skin, print-ready detail.
```

Примечание: Руки в кадре - частая проблема. Проще просить кадр по грудь.

## Скорость и спорт

### Гонщик

Флагман для детских парков. Шлем под мышкой, лицо открыто.

```text
Keep the child's face, facial features, skin tone, hair and age exactly as in the source photo. Do not beautify, do not age up, do not change ethnicity or body type. Photorealistic editorial portrait, natural child proportions, real fabric texture, fine skin texture preserved.
The child wears a racing suit in deep red and graphite with plain unbranded patches and a fireproof collar, holding a racing helmet under one arm. Background: pit lane with a blurred race car and team garage lights. Late afternoon sun, slight heat haze, energetic mood.
Shot on 85mm f/2.0, soft key light matching the direction of light in the source photo, gentle rim light, shallow depth of field, true-to-life colour, no plastic skin, print-ready detail.
```

Примечание: Логотипы команд и спонсоров не рисуем: только выдуманные нашивки.

### Футболист

Ставим под вечерний стадионный свет: кадр сразу читается как постер.

```text
Keep the child's face, facial features, skin tone, hair and age exactly as in the source photo. Do not beautify, do not age up, do not change ethnicity or body type. Photorealistic editorial portrait, natural child proportions, real fabric texture, fine skin texture preserved.
The child wears a plain football kit in blue and white with no logos, standing on a stadium pitch at dusk. Stadium floodlights create a strong rim light, crowd softly blurred in the background, light mist in the beams. Determined, happy expression.
Shot on 85mm f/2.0, soft key light matching the direction of light in the source photo, gentle rim light, shallow depth of field, true-to-life colour, no plastic skin, print-ready detail.
```

Примечание: Номер на футболке ставим двузначный, буквы не пишем.

### Балерина на сцене

Сильный образ для девочек, продаётся в паре с парадным портретом.

```text
Keep the child's face, facial features, skin tone, hair and age exactly as in the source photo. Do not beautify, do not age up, do not change ethnicity or body type. Photorealistic editorial portrait, natural child proportions, real fabric texture, fine skin texture preserved.
The child wears a classical ballet costume with a soft tutu, standing on a theatre stage. Warm spotlight from above and behind, deep velvet darkness of the auditorium, delicate dust in the light beam. Graceful posture, calm confident expression.
Shot on 85mm f/2.0, soft key light matching the direction of light in the source photo, gentle rim light, shallow depth of field, true-to-life colour, no plastic skin, print-ready detail.
```

Примечание: Позу не меняем сильно: руки из исходника всегда достовернее сгенерированных.

## Фэнтези и сказка

### Галактический страж

Наша замена «супергероям»: собственный костюм, никаких чужих франшиз.

```text
Keep the child's face, facial features, skin tone, hair and age exactly as in the source photo. Do not beautify, do not age up, do not change ethnicity or body type. Photorealistic editorial portrait, natural child proportions, real fabric texture, fine skin texture preserved.
The child wears an original heroic suit: matte navy armour plates with gold trim and a flowing deep-red cape, an abstract star emblem on the chest that belongs to no existing brand. Background: city rooftop at blue hour, distant lights, light wind in the cape. Brave, kind expression.
Shot on 85mm f/2.0, soft key light matching the direction of light in the source photo, gentle rim light, shallow depth of field, true-to-life colour, no plastic skin, print-ready detail.
```

Примечание: Эмблема всегда абстрактная. Любой намёк на известного персонажа - брак.

### Волшебная школа

Атмосфера старой библиотеки без отсылок к конкретной франшизе.

```text
Keep the child's face, facial features, skin tone, hair and age exactly as in the source photo. Do not beautify, do not age up, do not change ethnicity or body type. Photorealistic editorial portrait, natural child proportions, real fabric texture, fine skin texture preserved.
The child wears a dark academic robe over a knitted vest, holding an old leather-bound book. Background: ancient library with tall shelves, floating candles, warm golden light and soft dust. Curious, slightly mischievous expression.
Shot on 85mm f/2.0, soft key light matching the direction of light in the source photo, gentle rim light, shallow depth of field, true-to-life colour, no plastic skin, print-ready detail.
```

Примечание: Никаких шарфов с цветами факультетов и узнаваемых гербов.

### Мир динозавров

Приключенческий сюжет для парков и детских музеев.

```text
Keep the child's face, facial features, skin tone, hair and age exactly as in the source photo. Do not beautify, do not age up, do not change ethnicity or body type. Photorealistic editorial portrait, natural child proportions, real fabric texture, fine skin texture preserved.
The child wears a young palaeontologist outfit: khaki vest, rolled sleeves, field hat, standing in a prehistoric valley at sunrise with ferns and a huge peaceful sauropod far in the background. Golden light, morning mist, sense of wonder.
Shot on 85mm f/2.0, soft key light matching the direction of light in the source photo, gentle rim light, shallow depth of field, true-to-life colour, no plastic skin, print-ready detail.
```

Примечание: Хищников в детском наборе не ставим, только травоядные и на расстоянии.

### Подводный мир

Хорошо заходит для океанариумов и летних сезонов.

```text
Keep the child's face, facial features, skin tone, hair and age exactly as in the source photo. Do not beautify, do not age up, do not change ethnicity or body type. Photorealistic editorial portrait, natural child proportions, real fabric texture, fine skin texture preserved.
The child wears a modern exploration diving suit with a transparent bubble helmet showing the face clearly, surrounded by a coral reef, rays of sunlight from the surface, schools of small fish, a calm sea turtle nearby. Turquoise light, clear water, no bubbles covering the face.
Shot on 85mm f/2.0, soft key light matching the direction of light in the source photo, gentle rim light, shallow depth of field, true-to-life colour, no plastic skin, print-ready detail.
```

Примечание: Шлем прозрачный и без бликов поверх лица, иначе теряется сходство.

## Музейные темы

### Небылицы: сказочный портрет

Для музеев небылиц и сказок: портрет в стиле старой книжной иллюстрации, но фотографичный.

```text
Keep the child's face, facial features, skin tone, hair and age exactly as in the source photo. Do not beautify, do not age up, do not change ethnicity or body type. Photorealistic editorial portrait, natural child proportions, real fabric texture, fine skin texture preserved.
The child wears a folk-tale costume: embroidered linen shirt, woven belt, soft fur-trimmed cloak. Background: wooden fairy-tale interior with a painted stove, warm candlelight, a cat on a bench. Slightly theatrical but photorealistic, storybook warmth.
Shot on 85mm f/2.0, soft key light matching the direction of light in the source photo, gentle rim light, shallow depth of field, true-to-life colour, no plastic skin, print-ready detail.
```

Примечание: Орнаменты берём обобщённые, без привязки к конкретному региону.

### Мистика: готический портрет

Взрослая версия. Для детей всегда собираем облегчённый вариант: меньше тьмы, больше тепла.

```text
Keep the child's face, facial features, skin tone, hair and age exactly as in the source photo. Do not beautify, do not age up, do not change ethnicity or body type. Photorealistic editorial portrait, natural child proportions, real fabric texture, fine skin texture preserved.
The subject wears a Victorian-style coat with a high collar, holding an old brass lantern. Background: dim study of a collector, glass cabinets, maps, fog behind the window, single candle warmth. Mysterious but not frightening, deep shadows with detail retained.
Shot on 85mm f/2.0, soft key light matching the direction of light in the source photo, gentle rim light, shallow depth of field, true-to-life colour, no plastic skin, print-ready detail.
```

Примечание: Для детского набора убираем туман и поднимаем экспозицию фона на две ступени.

### Историческая эпоха

Портрет в костюме выбранного века. Эпоху задаём одним словом в промпте.

```text
Keep the child's face, facial features, skin tone, hair and age exactly as in the source photo. Do not beautify, do not age up, do not change ethnicity or body type. Photorealistic editorial portrait, natural child proportions, real fabric texture, fine skin texture preserved.
The subject wears an authentic early twentieth century outfit with period-correct fabric and buttons, photographed in a period interior with patterned wallpaper and a tall window. Soft window light, restrained colour palette, subtle film grain, no modern objects in the frame.
Shot on 85mm f/2.0, soft key light matching the direction of light in the source photo, gentle rim light, shallow depth of field, true-to-life colour, no plastic skin, print-ready detail.
```

Примечание: Эпоху меняем одной фразой. Проверяем, что в кадр не попали современные предметы.

## Праздники

### Новогодняя сказка

Декабрьский набор. Снимаем в ноябре, продаём весь декабрь.

```text
Keep the child's face, facial features, skin tone, hair and age exactly as in the source photo. Do not beautify, do not age up, do not change ethnicity or body type. Photorealistic editorial portrait, natural child proportions, real fabric texture, fine skin texture preserved.
The child wears a cosy winter outfit: knitted sweater, soft scarf, light snow on the shoulders. Background: evening winter town with a decorated tree, warm garland bokeh, gently falling snow. Warm golden light on the face, cool blue tones in the background, joyful calm expression.
Shot on 85mm f/2.0, soft key light matching the direction of light in the source photo, gentle rim light, shallow depth of field, true-to-life colour, no plastic skin, print-ready detail.
```

Примечание: Гирлянды держим в расфокусе: резкие лампочки перетягивают внимание с лица.
