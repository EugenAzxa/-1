/* Миллениум - поведение сайта. Без зависимостей. */
(function () {
  'use strict';

  /* ---- экран загрузки -----------------------------------------------------
     Показывает видоискатель с локациями и полосу реального прогресса.
     Правила прежние: ждём только кадры первого экрана, минимум 0.75 с,
     предохранитель 3.2 с от старта навигации, внутри сессии один раз.
     Финал - щелчок затвора: шторки видоискателя, чернота, вспышка. */
  var pre = document.getElementById('preloader');
  if (pre) {
    var bar = pre.querySelector('[data-bar]');
    var pct = pre.querySelector('[data-pct]');
    var MIN_MS = 750, MAX_MS = 3200;
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
