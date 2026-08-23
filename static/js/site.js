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

  /* --- Aviso de cookies --- */
  var cookie = document.getElementById("cookie");
  var ok = document.getElementById("cookie-ok");
  if (cookie && ok) {
    ok.addEventListener("click", function () { cookie.hidden = true; });
  }
})();
