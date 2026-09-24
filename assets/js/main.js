/* Миллениум - поведение сайта. Без зависимостей. */
(function () {
  'use strict';

  /* ---- экран загрузки -----------------------------------------------------
     Показывает видоискатель с локациями и полосу реального прогресса.
     Правила прежние: ждём только кадры первого экрана, минимум 1.9 с
     (чтобы успели смениться два-три стиля), предохранитель 3.6 с от старта
     навигации, внутри сессии показывается один раз.
     Финал - щелчок затвора: шторки видоискателя, чернота, вспышка. */
  var pre = document.getElementById('preloader');
  if (pre) {
    var bar = pre.querySelector('[data-bar]');
    var pct = pre.querySelector('[data-pct]');
    var MIN_MS = 1900, MAX_MS = 3600;
    var shown = 0, real = 0.05, finished = false, raf = null;
    var seen = false;
    try { seen = sessionStorage.getItem('aib-intro') === '1'; } catch (e) {}
    // ?intro в адресе показывает вступление принудительно - удобно показывать клиенту
    if (/[?&]intro/.test(location.search)) seen = false;
    var still = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    function draw(p) {
      if (bar) bar.style.transform = 'scaleX(' + p + ')';
      if (pct) pct.textContent = String(Math.round(p * 100));
    }

    function finish(instant) {
      if (finished) return;
      finished = true;
      if (raf) cancelAnimationFrame(raf);
      try { sessionStorage.setItem('aib-intro', '1'); } catch (e) {}
      draw(1);

      if (instant) {
        pre.classList.add('is-instant', 'is-out');
        document.body.classList.remove('is-loading');
        pre.classList.add('is-done');
        return;
      }

      pre.classList.add('is-snap');                                  // шторки закрываются, экран чернеет
      setTimeout(function () { pre.classList.add('is-flash'); }, 240); // вспышка
      setTimeout(function () {                                        // сайт открывается под вспышкой
        pre.classList.add('is-out');
        document.body.classList.remove('is-loading');
      }, 320);
      setTimeout(function () { pre.classList.add('is-done'); }, 1300);
    }

    if (seen || still) {
      finish(true);
    } else {
      // ждём только кадры первого экрана: остальные грузятся лениво и
      // никогда не дождались бы события load без прокрутки
      var imgs = [].slice.call(document.querySelectorAll('.hero img, .phero img'))
        .filter(function (i) { return i.getAttribute('src'); });
      var total = imgs.length, done = 0;

      function frame() {
        // страховка от замирания: пока ждём картинки, полоса всё равно
        // ползёт по времени, но выше 90% без реальной загрузки не поднимается
        var creep = Math.min(0.9, performance.now() / MAX_MS * 0.9);
        var target = Math.max(real, creep);
        shown += (target - shown) * 0.12;
        draw(shown);
        raf = requestAnimationFrame(frame);
      }

      function tick() {
        done++;
        real = total ? Math.min(done / total, 1) : 1;
        if (done >= total) ready();
      }

      function ready() {
        real = 1;
        setTimeout(function () { finish(false); }, Math.max(0, MIN_MS - performance.now()));
      }

      raf = requestAnimationFrame(frame);
      imgs.forEach(function (img) {
        if (img.complete) { tick(); return; }
        img.addEventListener('load', tick, { once: true });
        img.addEventListener('error', tick, { once: true });
      });
      if (!total) ready();
      // предохранитель считаем от старта навигации, а не от запуска скрипта
      setTimeout(function () { finish(false); }, Math.max(0, MAX_MS - performance.now()));
    }
  }

  /* ---- переключатель темы ------------------------------------------------
     Светлая тема - по умолчанию. Выбор гостя живёт в localStorage и
     применяется до отрисовки скриптом в <head>, здесь только кнопка. */
  var themeBtn = document.querySelector('.theme-toggle');
  if (themeBtn) {
    var root = document.documentElement;
    var meta = document.querySelector('meta[name="theme-color"]');
    var BG = { light: '#f7f5f2', dark: '#08090c' };

    function paint(theme) {
      var dark = theme === 'dark';
      if (dark) { root.setAttribute('data-theme', 'dark'); }
      else { root.removeAttribute('data-theme'); }
      themeBtn.setAttribute('aria-pressed', String(dark));
      themeBtn.setAttribute('aria-label', dark ? 'Светлая тема' : 'Тёмная тема');
      if (meta) meta.setAttribute('content', dark ? BG.dark : BG.light);
    }

    paint(root.getAttribute('data-theme') === 'dark' ? 'dark' : 'light');

    themeBtn.addEventListener('click', function () {
      var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      paint(next);
      try { localStorage.setItem('aib-theme', next); } catch (e) {}
    });
  }

  /* ---- коллаж первого экрана ----------------------------------------------
     Плитки слегка следуют за курсором: каждая со своим коэффициентом глубины,
     поэтому получается лёгкая параллакс-сцена. Двигаем только transform. */
  var rings = document.querySelectorAll('.ring');
  if (rings.length) {
    var onScrollRing = function () {
      var r = (window.scrollY * 0.03).toFixed(2) + 'deg';
      rings.forEach(function (el) { el.style.setProperty('--sr', r); });
    };
    window.addEventListener('scroll', onScrollRing, { passive: true });
  }

  var collage = document.querySelector('.collage');
  if (collage && !window.matchMedia('(prefers-reduced-motion: reduce)').matches
      && window.matchMedia('(hover: hover)').matches) {
    var tx = 0, ty = 0, cx = 0, cy = 0, ticking = false;

    window.addEventListener('pointermove', function (e) {
      tx = (e.clientX / window.innerWidth - .5) * 26;
      ty = (e.clientY / window.innerHeight - .5) * 18;
      if (!ticking) { ticking = true; requestAnimationFrame(step); }
    }, { passive: true });

    function step() {
      cx += (tx - cx) * .06;
      cy += (ty - cy) * .06;
      collage.style.setProperty('--px', cx.toFixed(2) + 'px');
      collage.style.setProperty('--py', cy.toFixed(2) + 'px');
      if (Math.abs(tx - cx) > .1 || Math.abs(ty - cy) > .1) requestAnimationFrame(step);
      else ticking = false;
    }
  }

  /* ---- «фильм»: раскрытие большой картинки по прокрутке -------------------
     --p растёт от 0, когда верх блока у нижнего края окна, до 1, когда блок
     поднялся на две трети. Считаем в requestAnimationFrame, без дребезга. */
  var film = document.querySelector('[data-film]');
  if (film && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    var filmTick = false;
    var filmUpdate = function () {
      filmTick = false;
      var b = film.getBoundingClientRect(), vh = window.innerHeight;
      var p = (vh - b.top) / (vh * 0.8);
      p = Math.max(0, Math.min(1, p));
      film.style.setProperty('--p', p.toFixed(3));
    };
    window.addEventListener('scroll', function () {
      if (!filmTick) { filmTick = true; requestAnimationFrame(filmUpdate); }
    }, { passive: true });
    window.addEventListener('resize', filmUpdate);
    filmUpdate();
  }

  /* ---- стеклянная линза в меню --------------------------------------------
     Линза - индикатор выбранного пункта. Внутри неё увеличенная копия
     пунктов, выровненная по настоящим, поэтому текст под стеклом выглядит
     преломлённым. Движение - пружина (жёсткость 420, затухание 30: чуть
     перелетает и возвращается), на скорости стекло вытягивается. */
  (function () {
    var nav = document.querySelector('.nav-links');
    if (!nav) return;
    var links = [].slice.call(nav.querySelectorAll('a:not(.nav-cta)'));
    if (!links.length) return;
    var still = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    var glass = document.createElement('span');
    glass.className = 'glass';
    glass.setAttribute('aria-hidden', 'true');
    var lens = document.createElement('span');
    lens.className = 'glass__lens';
    var copy = document.createElement('span');
    copy.className = 'glass__copy';
    links.forEach(function (a) {
      var s = document.createElement('span');
      s.className = 'glass__item';
      s.textContent = a.textContent.trim();
      copy.appendChild(s);
    });
    lens.appendChild(copy);
    glass.appendChild(lens);
    nav.appendChild(glass);
    nav.classList.add('has-glass');

    var active = links.filter(function (a) { return a.classList.contains('is-active'); })[0] || null;
    var cur = { x: 0, y: 0, w: 0, h: 0 }, vel = { x: 0, y: 0, w: 0, h: 0 };
    var target = null, raf = null, shown = false, last = 0, hovered = null;
    var K = 420, D = 30, ZOOM = 1.16;
    var originX = null;   // точка увеличения: центр пилюли или начало текста у широких строк

    function rectOf(a) {
      var nb = nav.getBoundingClientRect(), b = a.getBoundingClientRect();
      return { x: b.left - nb.left + nav.scrollLeft, y: b.top - nb.top + nav.scrollTop, w: b.width, h: b.height };
    }

    // копия пунктов стоит ровно там же, где настоящие, с тем же шрифтом и отступами
    function layoutCopy() {
      var items = copy.children;
      links.forEach(function (a, i) {
        var r = rectOf(a), cs = getComputedStyle(a), s = items[i];
        s.style.left = r.x + 'px'; s.style.top = r.y + 'px';
        s.style.width = r.w + 'px'; s.style.height = r.h + 'px';
        s.style.padding = cs.padding; s.style.fontSize = cs.fontSize;
        s.style.fontFamily = cs.fontFamily;
        s.style.justifyContent = cs.textAlign === 'center' ? 'center' : 'flex-start';
      });
      // если пункт заметно шире текста (строки в мобильном меню) - увеличиваем от начала текста
      var a0 = links[0], cs0 = getComputedStyle(a0);
      originX = (rectOf(a0).w > a0.scrollWidth + 40 || cs0.display === 'block') ? parseFloat(cs0.paddingLeft) || 0 : null;
    }

    function paint() {
      var sp = Math.abs(vel.x) + Math.abs(vel.y);
      var stretch = Math.min(sp / 2600, 0.16);
      var horizontal = Math.abs(vel.x) >= Math.abs(vel.y);
      var sx = horizontal ? 1 + stretch : 1 - stretch * 0.5;
      var sy = horizontal ? 1 - stretch * 0.5 : 1 + stretch;
      glass.style.width = cur.w + 'px';
      glass.style.height = cur.h + 'px';
      glass.style.transform = 'translate(' + cur.x.toFixed(2) + 'px,' + cur.y.toFixed(2) + 'px) scale(' + sx.toFixed(3) + ',' + sy.toFixed(3) + ')';
      var cx = cur.x + (originX === null ? cur.w / 2 : originX), cy = cur.y + cur.h / 2;
      copy.style.transformOrigin = cx + 'px ' + cy + 'px';
      copy.style.transform = 'translate(' + (-cur.x).toFixed(2) + 'px,' + (-cur.y).toFixed(2) + 'px) scale(' + ZOOM + ')';
    }

    function step(now) {
      var dt = last ? Math.min((now - last) / 1000, 1 / 30) : 1 / 60;
      last = now;
      var moving = false;
      ['x', 'y', 'w', 'h'].forEach(function (k) {
        var f = -K * (cur[k] - target[k]) - D * vel[k];
        vel[k] += f * dt;
        cur[k] += vel[k] * dt;
        if (Math.abs(cur[k] - target[k]) > 0.25 || Math.abs(vel[k]) > 0.25) moving = true;
      });
      paint();
      if (moving) { raf = requestAnimationFrame(step); }
      else { cur = { x: target.x, y: target.y, w: target.w, h: target.h }; vel = { x: 0, y: 0, w: 0, h: 0 }; paint(); raf = null; last = 0; }
    }

    function go(a, instant) {
      if (!a) { glass.classList.remove('is-on'); return; }
      target = rectOf(a);
      glass.classList.add('is-on');
      if (!shown || instant || still) {
        cur = { x: target.x, y: target.y, w: target.w, h: target.h };
        vel = { x: 0, y: 0, w: 0, h: 0 };
        shown = true; paint(); return;
      }
      if (!raf) raf = requestAnimationFrame(step);
    }

    // пересчёт раскладки не должен дёргать линзу с пункта, над которым курсор
    function settle() { layoutCopy(); go(hovered || active, true); }

    // стартовая позиция: если пришли с другой страницы кликом по меню -
    // начинаем со старого пункта и доезжаем до нового
    layoutCopy();
    var from = null;
    try { from = JSON.parse(sessionStorage.getItem('aib-glass') || 'null'); sessionStorage.removeItem('aib-glass'); } catch (e) {}
    if (from && Date.now() - from.t < 4000 && active && !still) {
      cur = { x: from.x, y: from.y, w: from.w, h: from.h };
      shown = true; glass.classList.add('is-on'); paint();
      requestAnimationFrame(function () { go(active); });
    } else {
      go(active, true);
    }

    nav.addEventListener('pointerover', function (e) {
      var a = e.target.closest && e.target.closest('a');
      if (a && links.indexOf(a) > -1) { hovered = a; go(a); }
    });
    nav.addEventListener('pointerleave', function (e) {
      if (e.pointerType !== 'touch') { hovered = null; go(active); }
    });
    nav.addEventListener('focusin', function (e) {
      if (links.indexOf(e.target) > -1) go(e.target);
    });
    nav.addEventListener('focusout', function () { go(active); });

    // на телефоне линза едет за пальцем по списку
    nav.addEventListener('pointermove', function (e) {
      if (e.pointerType !== 'touch') return;
      var el = document.elementFromPoint(e.clientX, e.clientY);
      var a = el && el.closest && el.closest('a');
      if (a && links.indexOf(a) > -1) go(a);
    });

    links.forEach(function (a) {
      a.addEventListener('click', function () {
        go(a);
        try { sessionStorage.setItem('aib-glass', JSON.stringify({ x: cur.x, y: cur.y, w: cur.w, h: cur.h, t: Date.now() })); } catch (e) {}
      });
    });

    window.addEventListener('resize', settle);
    if ('ResizeObserver' in window) new ResizeObserver(settle).observe(nav);
    document.fonts && document.fonts.ready.then(settle);
  })();

  /* ---- sticky header ---------------------------------------------------- */
  var header = document.querySelector('.site-header');
  function onScroll() {
    if (!header) return;
    header.classList.toggle('is-stuck', window.scrollY > 24);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---- mobile menu ------------------------------------------------------ */
  var burger = document.querySelector('.burger');
  if (burger) {
    burger.addEventListener('click', function () {
      var open = document.body.classList.toggle('menu-open');
      burger.setAttribute('aria-expanded', String(open));
    });
    document.querySelectorAll('.nav-links a').forEach(function (a) {
      a.addEventListener('click', function () {
        document.body.classList.remove('menu-open');
        burger.setAttribute('aria-expanded', 'false');
      });
    });
  }

  /* ---- scroll reveal ---------------------------------------------------- */
  var targets = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && targets.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        var el = e.target;
        var delay = parseInt(el.getAttribute('data-delay') || '0', 10);
        if (!el.hasAttribute('data-delay') && el.parentElement) {
          var sib = [].slice.call(el.parentElement.children).filter(function (c) { return c.classList.contains('reveal'); });
          if (sib.length > 1) delay = Math.min(sib.indexOf(el), 7) * 70;
        }
        setTimeout(function () { el.classList.add('is-in'); }, delay);
        io.unobserve(el);
      });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.08 });
    targets.forEach(function (t) { io.observe(t); });
  } else {
    targets.forEach(function (t) { t.classList.add('is-in'); });
  }

  /* ---- photo slots ------------------------------------------------------
     Карточка живёт без фотографии: пока файла нет, видна фирменная заливка.
     Как только файл появляется в assets/img/works/, он подставляется сам. */
  document.querySelectorAll('img[data-src]').forEach(function (img) {
    var probe = new Image();
    probe.onload = function () {
      img.src = img.getAttribute('data-src');
      img.removeAttribute('data-src');
    };
    probe.onerror = function () { img.remove(); };
    probe.src = img.getAttribute('data-src');
  });
  document.querySelectorAll('.shot img[src], .split__media img[src], .dir__bg img[src]').forEach(function (img) {
    img.addEventListener('error', function () { img.remove(); });
  });

  /* ---- copy prompt ------------------------------------------------------ */
  document.querySelectorAll('.copy').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var box = btn.closest('.preset').querySelector('pre');
      var text = box ? box.innerText : '';
      var done = function () {
        var old = btn.querySelector('span').textContent;
        btn.querySelector('span').textContent = 'Скопировано';
        btn.classList.add('is-done');
        setTimeout(function () {
          btn.querySelector('span').textContent = old;
          btn.classList.remove('is-done');
        }, 1800);
      };
      if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(done);
      } else {
        var ta = document.createElement('textarea');
        ta.value = text; ta.style.position = 'fixed'; ta.style.opacity = '0';
        document.body.appendChild(ta); ta.select();
        try { document.execCommand('copy'); done(); } catch (e) {}
        document.body.removeChild(ta);
      }
    });
  });

  /* ---- preset filters --------------------------------------------------- */
  var filters = document.querySelector('.filters');
  if (filters) {
    filters.addEventListener('click', function (e) {
      var btn = e.target.closest('button');
      if (!btn) return;
      filters.querySelectorAll('button').forEach(function (b) { b.classList.remove('is-on'); });
      btn.classList.add('is-on');
      var key = btn.getAttribute('data-filter');
      document.querySelectorAll('[data-group]').forEach(function (block) {
        var show = key === 'all' || block.getAttribute('data-group') === key;
        block.style.display = show ? '' : 'none';
      });
    });
  }

  /* ---- current year ----------------------------------------------------- */
  document.querySelectorAll('[data-year]').forEach(function (el) {
    el.textContent = String(new Date().getFullYear());
  });
})();
