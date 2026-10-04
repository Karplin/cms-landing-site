(function () {
  "use strict";

  /* --- Slider del hero --- */
  var slides = Array.prototype.slice.call(document.querySelectorAll(".slide"));
  var dots = Array.prototype.slice.call(document.querySelectorAll(".dots button"));
  var index = 0;
  var timer = null;
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function show(next) {
    index = (next + slides.length) % slides.length;
    slides.forEach(function (s, i) {
      s.setAttribute("data-active", String(i === index));
    });
    dots.forEach(function (d, i) {
      d.setAttribute("aria-selected", String(i === index));
    });
  }

  function play() {
    if (reduced || slides.length < 2) return;
    stop();
    timer = window.setInterval(function () { show(index + 1); }, 7000);
  }

  function stop() {
    if (timer) { window.clearInterval(timer); timer = null; }
  }

  dots.forEach(function (dot, i) {
    dot.addEventListener("click", function () { show(i); play(); });
  });

  var hero = document.querySelector(".hero");
  if (hero) {
    hero.addEventListener("mouseenter", stop);
    hero.addEventListener("mouseleave", play);
    hero.addEventListener("focusin", stop);
  }
  play();

  /* --- Modo claro / oscuro --- */
  var raiz = document.documentElement;
  var temaBtn = document.getElementById("theme-toggle");

  function pintarTema(tema) {
    if (tema === "dark") {
      raiz.setAttribute("data-theme", "dark");
    } else {
      raiz.setAttribute("data-theme", "light");
    }
    if (temaBtn) temaBtn.setAttribute("aria-pressed", String(tema === "dark"));
  }

  if (temaBtn) {
    var guardado = null;
    try { guardado = localStorage.getItem("tema"); } catch (e) {}
    var inicial = raiz.getAttribute("data-theme") || guardado || "light";
    pintarTema(inicial === "dark" ? "dark" : "light");
    temaBtn.addEventListener("click", function () {
      var siguiente = raiz.getAttribute("data-theme") === "dark" ? "light" : "dark";
      pintarTema(siguiente);
      try { localStorage.setItem("tema", siguiente); } catch (e) {}
    });
  }

  /* --- Menú móvil --- */
  var toggle = document.querySelector(".nav-toggle");
  var list = document.getElementById("nav-list");
  if (toggle && list) {
    toggle.addEventListener("click", function () {
      var open = list.getAttribute("data-open") === "true";
      list.setAttribute("data-open", String(!open));
      toggle.setAttribute("aria-expanded", String(!open));
    });
  }

  /* --- Galería: visor a pantalla completa --- */
  var fotos = Array.prototype.slice.call(document.querySelectorAll("[data-galeria]"));
  if (fotos.length) {
    var visor = document.createElement("div");
    visor.className = "visor";
    visor.hidden = true;
    visor.setAttribute("role", "dialog");
    visor.setAttribute("aria-modal", "true");
    visor.setAttribute("aria-label", "Foto ampliada");
    visor.innerHTML =
      '<button type="button" class="visor-cerrar" aria-label="Cerrar">×</button>' +
      '<button type="button" class="visor-ant" aria-label="Foto anterior">‹</button>' +
      '<img alt="">' +
      '<button type="button" class="visor-sig" aria-label="Foto siguiente">›</button>' +
      '<p class="visor-cuenta"></p>';
    document.body.appendChild(visor);

    var imagen = visor.querySelector("img");
    var cuenta = visor.querySelector(".visor-cuenta");
    var abierta = 0;
    var origen = null;

    var mostrar = function (i) {
      abierta = (i + fotos.length) % fotos.length;
      imagen.src = fotos[abierta].getAttribute("href");
      imagen.alt = fotos[abierta].querySelector("img").alt;
      cuenta.textContent = (abierta + 1) + " / " + fotos.length;
    };
    var cerrar = function () {
      visor.hidden = true;
      document.body.style.overflow = "";
      if (origen) origen.focus();
    };

    fotos.forEach(function (enlace, i) {
      enlace.addEventListener("click", function (evento) {
        evento.preventDefault();
        origen = enlace;
        mostrar(i);
        visor.hidden = false;
        document.body.style.overflow = "hidden";
        visor.querySelector(".visor-cerrar").focus();
      });
    });
    visor.querySelector(".visor-cerrar").addEventListener("click", cerrar);
    visor.querySelector(".visor-ant").addEventListener("click", function () { mostrar(abierta - 1); });
    visor.querySelector(".visor-sig").addEventListener("click", function () { mostrar(abierta + 1); });
    visor.addEventListener("click", function (evento) { if (evento.target === visor) cerrar(); });
    document.addEventListener("keydown", function (evento) {
      if (visor.hidden) return;
      if (evento.key === "Escape") cerrar();
      if (evento.key === "ArrowLeft") mostrar(abierta - 1);
      if (evento.key === "ArrowRight") mostrar(abierta + 1);
    });
  }

  /* --- Aviso de cookies --- */
  var cookie = document.getElementById("cookie");
  var ok = document.getElementById("cookie-ok");
  if (cookie && ok) {
    ok.addEventListener("click", function () {
      /* Se recuerda un año en todas las páginas; es una cookie técnica. */
      var seguro = location.protocol === "https:" ? "; Secure" : "";
      document.cookie = "cookies_ok=1; Max-Age=31536000; Path=/; SameSite=Lax" + seguro;
      cookie.hidden = true;
    });
  }
})();
