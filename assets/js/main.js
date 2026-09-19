/* AI BUREAU - site behaviour. No dependencies. */
(function () {
  'use strict';

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

  /* ---- request form ----------------------------------------------------- */
  var form = document.querySelector('.form');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var data = new FormData(form);
      var lines = [];
      data.forEach(function (v, k) { if (v) lines.push(k + ': ' + v); });
      var subject = 'Заявка с сайта AI BUREAU';
      var body = lines.join('\n');
      var mail = form.getAttribute('data-mail') || 'hello@example.com';
      window.location.href = 'mailto:' + mail + '?subject=' + encodeURIComponent(subject) +
        '&body=' + encodeURIComponent(body);
      var ok = form.querySelector('.form__ok');
      if (ok) ok.classList.add('is-on');
      form.reset();
    });
  }

  /* ---- current year ----------------------------------------------------- */
  document.querySelectorAll('[data-year]').forEach(function (el) {
    el.textContent = String(new Date().getFullYear());
  });
})();
