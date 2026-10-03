/* Ткань: картинка этапа висит полотном, прикреплённым за верхний край.
   Ветер гонит складки, курсор или палец оставляют волны, на складках свет
   и блик. Своя реализация на WebGL 1 без библиотек - работает и в Safari.
   Подключается к блоку [data-flow]: слушает событие flow:change. */
(function () {
  'use strict';
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  var GX = 49, GY = 37;          // узлы сетки (4:3)
  var PAD = 56;                  // запас холста вокруг полотна под складки и тень (на телефоне меньше)
  var OPT = { amp: 34, drape: 34, sway: 10, light: 0.9, sheen: 0.2, radius: 16,
              persp: 1000, brush: 3.2, brushSize: 0.2, damping: 2.4, wave: 1.0 };

  var VS = [
    'attribute vec2 aUv;',
    'attribute vec3 aDyn;',      // z (px к зрителю), dz/dx, dz/dy
    'uniform vec2 uSize;',       // размер полотна, px
    'uniform float uPad, uPersp;',
    'varying vec2 vUv; varying vec3 vN;',
    'void main(){',
    '  vec2 p = aUv * uSize - uSize * 0.5;',
    '  float s = uPersp / (uPersp - aDyn.x);',
    '  p *= s;',
    '  vec2 c = uSize * 0.5 + uPad;',
    '  vec2 full = uSize + 2.0 * uPad;',
    '  vec2 q = (p + c) / full * 2.0 - 1.0;',
    '  gl_Position = vec4(q.x, -q.y, 0.0, 1.0);',
    '  vUv = aUv;',
    '  vN = normalize(vec3(-aDyn.y, -aDyn.z, 1.0));',
    '}'
  ].join('\n');

  var FS = [
    'precision mediump float;',
    'uniform sampler2D uA, uB;',
    'uniform float uMix, uLight, uSheen, uRadius;',
    'uniform highp vec2 uSize;',
    'varying vec2 vUv; varying vec3 vN;',
    'float rr(vec2 p, vec2 b, float r){ vec2 q = abs(p) - b + r; return length(max(q,0.0)) + min(max(q.x,q.y),0.0) - r; }',
    'void main(){',
    '  vec3 a = texture2D(uA, vUv).rgb, b = texture2D(uB, vUv).rgb;',
    '  vec3 col = mix(a, b, uMix);',
    '  vec3 L = normalize(vec3(-0.35, -0.55, 1.0));',
    '  float d = dot(vN, L) / L.z;',
    '  col *= mix(1.0, clamp(d, 0.25, 1.45), uLight);',
    '  vec3 H = normalize(L + vec3(0.0, 0.0, 1.0));',
    '  col += pow(max(dot(vN, H), 0.0), 40.0) * uSheen;',
    '  float sd = rr(vUv * uSize - uSize * 0.5, uSize * 0.5, uRadius);',
    '  float al = clamp(0.5 - sd, 0.0, 1.0);',
    '  gl_FragColor = vec4(col * al, al);',
    '}'
  ].join('\n');

  function shader(gl, type, src) {
    var s = gl.createShader(type);
    gl.shaderSource(s, src); gl.compileShader(s);
    if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(s));
    return s;
  }

  function Cloth(view, imgs) {
    var canvas = document.createElement('canvas');
    canvas.className = 'cloth';
    canvas.setAttribute('aria-hidden', 'true');
    var gl = canvas.getContext('webgl', { premultipliedAlpha: true, antialias: true, alpha: true });
    if (!gl) return null;
    var prog = gl.createProgram();
    gl.attachShader(prog, shader(gl, gl.VERTEX_SHADER, VS));
    gl.attachShader(prog, shader(gl, gl.FRAGMENT_SHADER, FS));
    gl.linkProgram(prog);
    if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(prog));
    gl.useProgram(prog);

    var N = GX * GY, k, x, y;
    var uv = new Float32Array(N * 2), dyn = new Float32Array(N * 3);
    for (y = 0; y < GY; y++) for (x = 0; x < GX; x++) { k = y * GX + x; uv[k * 2] = x / (GX - 1); uv[k * 2 + 1] = y / (GY - 1); }
    var idx = new Uint16Array((GX - 1) * (GY - 1) * 6), n = 0;
    for (y = 0; y < GY - 1; y++) for (x = 0; x < GX - 1; x++) {
      k = y * GX + x;
      idx[n++] = k; idx[n++] = k + 1; idx[n++] = k + GX;
      idx[n++] = k + 1; idx[n++] = k + GX + 1; idx[n++] = k + GX;
    }
    function buf(data, type) { var b = gl.createBuffer(); gl.bindBuffer(type, b); gl.bufferData(type, data, type === gl.ARRAY_BUFFER && data === dyn ? gl.DYNAMIC_DRAW : gl.STATIC_DRAW); return b; }
    var bUv = buf(uv, gl.ARRAY_BUFFER), bDyn = buf(dyn, gl.ARRAY_BUFFER);
    buf(idx, gl.ELEMENT_ARRAY_BUFFER);
    var aUv = gl.getAttribLocation(prog, 'aUv'), aDyn = gl.getAttribLocation(prog, 'aDyn');
    gl.bindBuffer(gl.ARRAY_BUFFER, bUv); gl.enableVertexAttribArray(aUv); gl.vertexAttribPointer(aUv, 2, gl.FLOAT, false, 0, 0);
    gl.bindBuffer(gl.ARRAY_BUFFER, bDyn); gl.enableVertexAttribArray(aDyn); gl.vertexAttribPointer(aDyn, 3, gl.FLOAT, false, 0, 0);
    var U = {};
    ['uSize', 'uPad', 'uPersp', 'uA', 'uB', 'uMix', 'uLight', 'uSheen', 'uRadius'].forEach(function (u) { U[u] = gl.getUniformLocation(prog, u); });
    gl.uniform1i(U.uA, 0); gl.uniform1i(U.uB, 1);
    gl.enable(gl.BLEND); gl.blendFunc(gl.ONE, gl.ONE_MINUS_SRC_ALPHA);

    // текстуры этапов
    var tex = imgs.map(function () {
      var t = gl.createTexture();
      gl.bindTexture(gl.TEXTURE_2D, t);
      gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, 1, 1, 0, gl.RGBA, gl.UNSIGNED_BYTE, new Uint8Array([13, 13, 13, 255]));
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
      return t;
    });
    function upload(i) {
      var src = imgs[i].currentSrc || imgs[i].getAttribute('src');
      var im = new Image();
      im.onload = function () {
        gl.bindTexture(gl.TEXTURE_2D, tex[i]);
        gl.pixelStorei(gl.UNPACK_PREMULTIPLY_ALPHA_WEBGL, false);
        gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, im);
        dirty = true;
      };
      im.src = src;
    }
    imgs.forEach(function (_, i) { upload(i); });

    // поле ряби от курсора: волновое уравнение, верхний край прибит
    var h = new Float32Array(N), v = new Float32Array(N), z = new Float32Array(N);
    var W = 0, H = 0, dpr = 1, cur = 0, from = 0, mixv = 1, mixStart = 0, t0 = performance.now(), last = t0, gust = 0, dirty = true;

    function size() {
      var r = view.getBoundingClientRect();
      W = r.width; H = r.height;
      PAD = W < 560 ? 12 : 56;
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      canvas.style.left = canvas.style.top = -PAD + 'px';
      canvas.style.width = (W + 2 * PAD) + 'px';
      canvas.style.height = (H + 2 * PAD) + 'px';
      canvas.width = Math.round((W + 2 * PAD) * dpr);
      canvas.height = Math.round((H + 2 * PAD) * dpr);
      gl.viewport(0, 0, canvas.width, canvas.height);
      dirty = true;
    }

    function poke(u, w, strength) {
      var R = OPT.brushSize;
      for (var yy = 1; yy < GY; yy++) for (var xx = 0; xx < GX; xx++) {
        var du = xx / (GX - 1) - u, dv = (yy / (GY - 1) - w) * (H / W);
        var d2 = (du * du + dv * dv) / (R * R);
        if (d2 < 1) v[yy * GX + xx] += strength * (1 - d2) * (1 - d2);
      }
    }

    var px = null;
    function pointer(e) {
      var r = canvas.getBoundingClientRect();
      var u = (e.clientX - r.left - PAD) / W, w = (e.clientY - r.top - PAD) / H;
      if (u < -0.05 || u > 1.05 || w < 0 || w > 1.05) { px = null; return; }
      if (px) {
        var sp = Math.min(Math.hypot(u - px[0], w - px[1]) * 60, 3);
        poke(u, w, OPT.brush * sp * 40);
      }
      px = [u, w];
    }
    canvas.addEventListener('pointermove', pointer);
    canvas.addEventListener('pointerleave', function () { px = null; });

    function step(dt, time) {
      // рябь
      var c2 = 900, damp = OPT.damping, i, xx, yy;
      for (yy = 1; yy < GY; yy++) for (xx = 0; xx < GX; xx++) {
        i = yy * GX + xx;
        var l = xx > 0 ? h[i - 1] : h[i], r = xx < GX - 1 ? h[i + 1] : h[i];
        var u = h[i - GX], d = yy < GY - 1 ? h[i + GX] : h[i];
        v[i] += (c2 * (l + r + u + d - 4 * h[i]) * (1 / ((GX - 1) * (GX - 1))) * 60 - damp * v[i]) * dt;
      }
      for (i = GX; i < N; i++) h[i] += v[i] * dt;
      // ветер, провис и рябь складываются в высоту полотна
      var A = OPT.amp * (1 + gust), sw = OPT.sway * Math.sin(time * 0.55);
      for (yy = 0; yy < GY; yy++) {
        var w = yy / (GY - 1);
        for (xx = 0; xx < GX; xx++) {
          var uu = xx / (GX - 1);
          i = yy * GX + xx;
          var wind = Math.sin(uu * 7.0 - time * 1.9 + w * 2.2) * 0.55
                   + Math.sin(uu * 3.1 + w * 5.3 - time * 1.3) * 0.35
                   + Math.sin((uu + w) * 11.0 - time * 2.7) * 0.10;
          z[i] = A * wind * w * OPT.wave
               + OPT.drape * w * w * (1 - (2 * uu - 1) * (2 * uu - 1))
               + h[i] * w
               + sw * w * w * (uu - 0.5);
        }
      }
      // градиенты для света
      for (yy = 0; yy < GY; yy++) for (xx = 0; xx < GX; xx++) {
        i = yy * GX + xx;
        var zl = z[xx > 0 ? i - 1 : i], zr = z[xx < GX - 1 ? i + 1 : i];
        var zu = z[yy > 0 ? i - GX : i], zd = z[yy < GY - 1 ? i + GX : i];
        var sx = (xx > 0 && xx < GX - 1 ? 2 : 1) * W / (GX - 1), sy = (yy > 0 && yy < GY - 1 ? 2 : 1) * H / (GY - 1);
        dyn[i * 3] = z[i];
        dyn[i * 3 + 1] = (zr - zl) / sx * 3.2;
        dyn[i * 3 + 2] = (zd - zu) / sy * 3.2;
      }
      gust *= Math.pow(0.35, dt);
    }

    function draw(now) {
      var dt = Math.min((now - last) / 1000, 1 / 30);
      last = now;
      var time = (now - t0) / 1000 * 0.9;
      step(dt, time);
      if (mixv < 1) mixv = Math.min(1, (now - mixStart) / 800);
      gl.clearColor(0, 0, 0, 0); gl.clear(gl.COLOR_BUFFER_BIT);
      gl.bindBuffer(gl.ARRAY_BUFFER, bDyn); gl.bufferSubData(gl.ARRAY_BUFFER, 0, dyn);
      gl.uniform2f(U.uSize, W, H); gl.uniform1f(U.uPad, PAD); gl.uniform1f(U.uPersp, OPT.persp);
      gl.uniform1f(U.uMix, mixv); gl.uniform1f(U.uLight, OPT.light); gl.uniform1f(U.uSheen, OPT.sheen);
      gl.uniform1f(U.uRadius, OPT.radius);
      gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, tex[from]);
      gl.activeTexture(gl.TEXTURE1); gl.bindTexture(gl.TEXTURE_2D, tex[cur]);
      gl.drawElements(gl.TRIANGLES, idx.length, gl.UNSIGNED_SHORT, 0);
      dirty = false;
    }

    var raf = 0, running = false;
    function loop(now) { if (!running) return; draw(now); raf = requestAnimationFrame(loop); }
    function start() { if (running) return; running = true; last = performance.now(); raf = requestAnimationFrame(loop); }
    function stop() { running = false; cancelAnimationFrame(raf); }

    view.insertBefore(canvas, view.firstChild);
    view.classList.add('has-cloth');
    size();
    window.addEventListener('resize', size);

    return {
      show: function (i) {
        if (i === cur) return;
        from = mixv < 1 ? cur : cur; cur = i; mixv = 0; mixStart = performance.now();
        gust = 0.45;
        poke(0.5, 0.95, 22);
      },
      start: start, stop: stop
    };
  }

  document.querySelectorAll('[data-flow]').forEach(function (flow) {
    var view = flow.querySelector('.flow__view');
    var imgs = [].slice.call(view.querySelectorAll('img'));
    var cloth;
    try { cloth = Cloth(view, imgs); } catch (e) { cloth = null; if (window.console) console.warn('cloth:', e && e.message); }
    if (!cloth) return;
    flow.addEventListener('flow:change', function (e) { cloth.show(e.detail); });
    var queued = false;
    function check() {
      var r = view.getBoundingClientRect();
      if (r.bottom > -100 && r.top < window.innerHeight + 100 && !document.hidden) cloth.start(); else cloth.stop();
    }
    window.addEventListener('scroll', function () {
      if (queued) return; queued = true;
      requestAnimationFrame(function () { queued = false; check(); });
    }, { passive: true });
    document.addEventListener('visibilitychange', check);
    check();
  });
})();
