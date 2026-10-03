/* Примеры работ: стопка снимков.
   - при первом показе снимки падают сверху и ложатся в кучку;
   - любой снимок можно схватить и бросить: летит по инерции, наклоняется
     по ходу движения, отскакивает от краёв;
   - нажатие открывает снимок на весь экран, он вылетает из своего места
     и при закрытии возвращается туда же (как layout-анимации Motion);
   - кнопка раскладывает кучку в сетку и собирает обратно. */
(function () {
  'use strict';
  var pile = document.querySelector('[data-pile]');
  if (!pile) return;
  var cards = [].slice.call(pile.querySelectorAll('.pile__card'));
  var toggle = document.querySelector('[data-pile-toggle]');
  var still = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var S = cards.map(function () { return { x: 0, y: 0, r: 0, s: 1, base: 0 }; });
  var grid = false, dropped = false, top = 10, W = 0, H = 0, cw = 230;
  var SPRING = 'cubic-bezier(.2,1.25,.35,1)', SMOOTH = 'cubic-bezier(.16,1,.3,1)';

  // стабильный «случайный» разброс, чтобы кучка не прыгала при каждом заходе
  var seed = 7;
  function rnd() { seed = (seed * 16807) % 2147483647; return seed / 2147483647; }
  var jitter = cards.map(function () { return [rnd() * 2 - 1, rnd() * 2 - 1, rnd() * 2 - 1]; });

  function tf(st) { return 'translate(' + st.x.toFixed(1) + 'px,' + st.y.toFixed(1) + 'px) rotate(' + st.r.toFixed(2) + 'deg) scale(' + st.s.toFixed(3) + ')'; }
  function apply(i) { cards[i].style.transform = tf(S[i]); }
  function cardH(i) { return cards[i].offsetHeight; }

  function measure() {
    W = pile.clientWidth;
    cw = W < 520 ? Math.round(W * 0.44) : W < 900 ? 200 : 236;
    pile.style.setProperty('--cw', cw + 'px');
  }

  function pileLayout() {
    H = W < 520 ? 520 : Math.min(640, Math.max(520, W * 0.5));
    pile.style.height = H + 'px';
    var sx = W < 520 ? W * 0.16 : W * 0.3, sy = H * 0.2;
    return cards.map(function (c, i) {
      var j = jitter[i], h = cardH(i);
      return { x: W / 2 - cw / 2 + j[0] * sx, y: H / 2 - h / 2 + j[1] * sy, r: j[2] * 15, s: 1 };
    });
  }

  function gridLayout() {
    var cols = W >= 1000 ? 4 : W >= 640 ? 3 : 2, gap = W < 520 ? 10 : 16;
    var cell = (W - gap * (cols - 1)) / cols, sc = cell / cw, y = 0, out = [];
    for (var i = 0; i < cards.length; i += cols) {
      var rowH = 0;
      for (var k = i; k < Math.min(i + cols, cards.length); k++) rowH = Math.max(rowH, cardH(k) * sc);
      for (k = i; k < Math.min(i + cols, cards.length); k++) {
        var h = cardH(k) * sc, col = k - i;
        // карточка масштабируется от центра: сдвигаем так, чтобы левый верх лёг в ячейку
        out[k] = { x: col * (cell + gap) + (cell - cw) / 2, y: y + (h - cardH(k)) / 2, r: 0, s: sc };
      }
      y += rowH + gap;
    }
    H = y - gap;
    pile.style.height = H + 'px';
    return out;
  }

  function moveAll(targets, dur, ease, stagger) {
    cards.forEach(function (c, i) {
      var from = tf(S[i]);
      S[i].x = targets[i].x; S[i].y = targets[i].y; S[i].r = targets[i].r; S[i].s = targets[i].s; S[i].base = targets[i].r;
      if (still || !dur) { apply(i); return; }
      c.animate([{ transform: from }, { transform: tf(S[i]) }], { duration: dur, easing: ease, delay: (stagger || 0) * i, fill: 'backwards' });
      apply(i);
    });
  }

  function dropIn() {
    dropped = true;
    var t = pileLayout();
    pile.classList.add('is-ready');
    cards.forEach(function (c, i) {
      S[i].x = t[i].x; S[i].y = t[i].y; S[i].r = t[i].r; S[i].s = 1; S[i].base = t[i].r;
      c.style.zIndex = ++top;
      apply(i);
      if (still) return;
      var start = 'translate(' + t[i].x.toFixed(1) + 'px,' + (-H - 260).toFixed(1) + 'px) rotate(' + (t[i].r * 3).toFixed(1) + 'deg) scale(1.05)';
      c.animate([{ transform: start, opacity: 1 }, { transform: tf(S[i]), opacity: 1 }],
        { duration: 1000, easing: SPRING, delay: 110 * i, fill: 'backwards' });
    });
  }

  measure();
  // до падения карточки стоят в кучке невидимыми, чтобы высота была правильной
  var init = pileLayout();
  init.forEach(function (t, i) { S[i].x = t.x; S[i].y = t.y; S[i].r = t.r; S[i].base = t.r; apply(i); });

  function checkDrop() {
    if (dropped) return;
    var r = pile.getBoundingClientRect();
    if (r.top < window.innerHeight * 0.8 && r.bottom > 0) dropIn();
  }
  var q = false;
  window.addEventListener('scroll', function () {
    if (q) return; q = true;
    requestAnimationFrame(function () { q = false; checkDrop(); });
  }, { passive: true });
  checkDrop();

  window.addEventListener('resize', function () {
    measure();
    moveAll(grid ? gridLayout() : pileLayout(), 0);
  });

  if (toggle) toggle.addEventListener('click', function () {
    if (!dropped) dropIn();
    grid = !grid;
    pile.classList.toggle('is-grid', grid);
    toggle.textContent = grid ? 'Собрать в кучку' : 'Разложить';
    toggle.setAttribute('aria-pressed', grid ? 'true' : 'false');
    moveAll(grid ? gridLayout() : pileLayout(), 800, SMOOTH, 30);
  });

  /* ---- перетаскивание с инерцией -------------------------------------- */
  cards.forEach(function (c, i) {
    var drag = null;
    c.addEventListener('pointerdown', function (e) {
      if (e.button !== 0) return;
      c.getAnimations().forEach(function (a) { a.finish(); });
      c.style.zIndex = ++top;
      drag = { id: e.pointerId, sx: e.clientX, sy: e.clientY, ox: S[i].x, oy: S[i].y, moved: false,
               lx: e.clientX, ly: e.clientY, lt: performance.now(), vx: 0, vy: 0 };
      if (S[i].fly) { cancelAnimationFrame(S[i].fly); S[i].fly = 0; }
    });
    c.addEventListener('pointermove', function (e) {
      if (!drag || e.pointerId !== drag.id || grid) return;
      var dx = e.clientX - drag.sx, dy = e.clientY - drag.sy;
      if (!drag.moved && Math.hypot(dx, dy) < 6) return;
      if (!drag.moved) { drag.moved = true; c.setPointerCapture(e.pointerId); c.classList.add('is-lifted'); }
      var now = performance.now(), dt = Math.max(now - drag.lt, 1);
      drag.vx = (e.clientX - drag.lx) / dt * 16; drag.vy = (e.clientY - drag.ly) / dt * 16;
      drag.lx = e.clientX; drag.ly = e.clientY; drag.lt = now;
      S[i].x = drag.ox + dx; S[i].y = drag.oy + dy;
      S[i].r = S[i].base + Math.max(-22, Math.min(22, drag.vx * 0.9));
      S[i].s = 1.04;
      apply(i);
    });
    function end(e) {
      if (!drag || e.pointerId !== drag.id) return;
      var d = drag; drag = null;
      c.classList.remove('is-lifted');
      if (!d.moved) { if (e.type === 'pointerup') open(i); return; }
      fling(i, d.vx, d.vy);
    }
    c.addEventListener('pointerup', end);
    c.addEventListener('pointercancel', end);
    c.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(i); } });
    c.addEventListener('click', function (e) { if (e.detail === 0) open(i); });
  });

  function fling(i, vx, vy) {
    var st = S[i], h = cardH(i);
    var minX = -cw * 0.25, maxX = W - cw * 0.75, minY = -h * 0.2, maxY = H - h * 0.8;
    function stepFly() {
      vx *= 0.93; vy *= 0.93;
      st.x += vx; st.y += vy;
      if (st.x < minX) { st.x = minX; vx = -vx * 0.5; } else if (st.x > maxX) { st.x = maxX; vx = -vx * 0.5; }
      if (st.y < minY) { st.y = minY; vy = -vy * 0.5; } else if (st.y > maxY) { st.y = maxY; vy = -vy * 0.5; }
      st.r += (st.base + vx * 0.6 - st.r) * 0.2;
      st.s += (1 - st.s) * 0.25;
      apply(i);
      if (Math.abs(vx) + Math.abs(vy) > 0.3 || Math.abs(st.s - 1) > 0.002) st.fly = requestAnimationFrame(stepFly);
      else { st.base = st.r; st.fly = 0; }
    }
    if (still) { st.s = 1; apply(i); return; }
    st.fly = requestAnimationFrame(stepFly);
  }

  /* ---- просмотр на весь экран ----------------------------------------- */
  var box = null, cur = -1;
  function capOf(i) { return cards[i].querySelector('.pile__cap').innerHTML; }
  function fit(i) {
    var img = cards[i].querySelector('img'), ar = img.naturalWidth && img.naturalHeight ? img.naturalWidth / img.naturalHeight : 1.5;
    var vw = window.innerWidth, vh = window.innerHeight;
    var maxW = Math.min(vw * (vw < 700 ? 0.94 : 0.86), 1180), maxH = vh * (vw < 700 ? 0.66 : 0.8) - 60;
    var w = Math.min(maxW - 20, maxH * ar);
    return w + 20;
  }
  function fromCard(i, figW, figH) {
    var pr = pile.getBoundingClientRect(), st = S[i];
    var cx = pr.left + st.x + cw / 2, cy = pr.top + st.y + cardH(i) / 2;
    var k = (cw * st.s) / figW;
    return 'translate(' + (cx - window.innerWidth / 2).toFixed(1) + 'px,' + (cy - window.innerHeight / 2).toFixed(1) + 'px) translate(-50%,-50%) rotate(' + st.r.toFixed(2) + 'deg) scale(' + k.toFixed(4) + ')';
  }
  var CENTER = 'translate(0px,0px) translate(-50%,-50%) rotate(0deg) scale(1)';

  function fill(i) {
    var fig = box.querySelector('.lbx__fig'), img = fig.querySelector('img');
    fig.style.width = fit(i) + 'px';
    img.src = cards[i].querySelector('img').currentSrc || cards[i].querySelector('img').src;
    img.alt = cards[i].querySelector('img').alt;
    var full = new Image();
    full.onload = function () { if (cur === i) img.src = full.src; };
    full.src = cards[i].getAttribute('data-full');
    fig.querySelector('.lbx__cap').innerHTML = capOf(i);
  }

  function open(i) {
    if (box) return;
    cur = i;
    box = document.createElement('div');
    box.className = 'lbx';
    box.setAttribute('role', 'dialog');
    box.setAttribute('aria-modal', 'true');
    box.setAttribute('aria-label', 'Просмотр снимка');
    var arrow = function (d) { return '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="' + d + '"/></svg>'; };
    box.innerHTML = '<div class="lbx__bg"></div>' +
      '<figure class="lbx__fig"><img alt=""><figcaption class="lbx__cap"></figcaption></figure>' +
      '<button class="lbx__btn lbx__close" type="button" aria-label="Закрыть">' + arrow('M6 6l12 12M18 6L6 18') + '</button>' +
      '<button class="lbx__btn lbx__prev" type="button" aria-label="Предыдущий снимок">' + arrow('M15 5l-7 7 7 7') + '</button>' +
      '<button class="lbx__btn lbx__next" type="button" aria-label="Следующий снимок">' + arrow('M9 5l7 7-7 7') + '</button>';
    document.body.appendChild(box);
    fill(i);
    var fig = box.querySelector('.lbx__fig');
    cards[i].style.visibility = 'hidden';
    var dur = still ? 0 : 620;
    fig.animate([{ transform: fromCard(i, fig.offsetWidth, fig.offsetHeight) }, { transform: CENTER }], { duration: dur, easing: SMOOTH, fill: 'both' });
    box.querySelector('.lbx__bg').animate([{ opacity: 0 }, { opacity: 1 }], { duration: dur * 0.8, fill: 'both' });
    requestAnimationFrame(function () { box.classList.add('is-open'); });
    box.querySelector('.lbx__bg').addEventListener('click', close);
    box.querySelector('.lbx__close').addEventListener('click', close);
    box.querySelector('.lbx__prev').addEventListener('click', function () { go(-1); });
    box.querySelector('.lbx__next').addEventListener('click', function () { go(1); });
    document.addEventListener('keydown', onKey);
    document.documentElement.style.overflow = 'hidden';
    box.querySelector('.lbx__close').focus({ preventScroll: true });
  }

  function go(d) {
    if (!box) return;
    var fig = box.querySelector('.lbx__fig');
    cards[cur].style.visibility = '';
    cur = (cur + d + cards.length) % cards.length;
    cards[cur].style.visibility = 'hidden';
    fig.animate([{ opacity: 1, transform: CENTER }, { opacity: 0, transform: 'translate(' + (-30 * d) + 'px,0) translate(-50%,-50%)' }], { duration: still ? 0 : 160, fill: 'forwards' }).onfinish = function () {
      fill(cur);
      fig.getAnimations().forEach(function (a) { a.cancel(); });
      fig.animate([{ opacity: 0, transform: 'translate(' + (30 * d) + 'px,0) translate(-50%,-50%)' }, { opacity: 1, transform: CENTER }], { duration: still ? 0 : 260, easing: SMOOTH, fill: 'both' });
    };
  }

  function close() {
    if (!box) return;
    var b = box, fig = b.querySelector('.lbx__fig'), i = cur;
    box = null;
    document.removeEventListener('keydown', onKey);
    b.classList.remove('is-open');
    var dur = still ? 0 : 520;
    fig.getAnimations().forEach(function (a) { a.cancel(); });
    var a = fig.animate([{ transform: CENTER }, { transform: fromCard(i, fig.offsetWidth, fig.offsetHeight) }], { duration: dur, easing: SMOOTH, fill: 'forwards' });
    b.querySelector('.lbx__bg').animate([{ opacity: 1 }, { opacity: 0 }], { duration: dur, fill: 'forwards' });
    a.onfinish = function () {
      cards[i].style.visibility = '';
      b.remove();
      document.documentElement.style.overflow = '';
      cards[i].focus({ preventScroll: true });
    };
  }

  function onKey(e) {
    if (e.key === 'Escape') close();
    else if (e.key === 'ArrowRight') go(1);
    else if (e.key === 'ArrowLeft') go(-1);
  }
})();
