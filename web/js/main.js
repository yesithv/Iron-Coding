/* =========================================================================
   Iron-Coding — main.js
   Lo mínimo indispensable: menú de navegación en móvil y año del pie.
   Sin dependencias. Si el script no carga, el menú queda desplegado
   (regla `html:not(.js)` en base.css), así que nada queda inaccesible.
   ========================================================================= */

(function () {
  'use strict';

  /* ---------- Revelado al entrar en pantalla ----------------------------- */
  /* Va primero, antes que cualquier otra cosa que pudiera fallar: si esto no
     corre, el contenido con [data-revelar] se queda oculto hasta que salte la
     salvaguarda de 3 s del <head>. */

  (function revelado() {
    var elementos = document.querySelectorAll('[data-revelar]');
    if (!elementos.length) return;

    var mostrarTodo = function () {
      for (var i = 0; i < elementos.length; i++) elementos[i].classList.add('visible');
    };

    // Sin soporte del navegador, o si la persona pidió menos movimiento:
    // se muestra todo de una vez, sin animación.
    var menosMovimiento = window.matchMedia &&
      window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    if (!('IntersectionObserver' in window) || menosMovimiento) {
      mostrarTodo();
      return;
    }

    // Escalonado por grupo: los hermanos que se revelan juntos entran
    // uno detrás de otro, no todos de golpe.
    var contadores = [];
    for (var j = 0; j < elementos.length; j++) {
      var padre = elementos[j].parentNode;
      var pos = contadores.indexOf(padre);
      if (pos === -1) { contadores.push(padre); pos = contadores.length - 1; }
      if (!padre.__n) padre.__n = 0;
      elementos[j].style.setProperty('--retraso', Math.min(padre.__n, 5) * 70 + 'ms');
      padre.__n++;
    }

    var observador = new IntersectionObserver(function (entradas) {
      for (var k = 0; k < entradas.length; k++) {
        if (!entradas[k].isIntersecting) continue;
        entradas[k].target.classList.add('visible');
        observador.unobserve(entradas[k].target); // una sola vez
      }
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });

    for (var m = 0; m < elementos.length; m++) observador.observe(elementos[m]);
  })();

  /* ---------- Menú móvil ------------------------------------------------- */

  var toggle = document.querySelector('.nav-toggle');
  var menu = document.getElementById('nav-menu');

  if (toggle && menu) {
    var setOpen = function (open) {
      toggle.setAttribute('aria-expanded', String(open));
      menu.setAttribute('data-open', String(open));
      toggle.querySelector('.nav-toggle__label').textContent = open ? 'cerrar()' : 'menu()';
    };

    setOpen(false);

    toggle.addEventListener('click', function () {
      setOpen(toggle.getAttribute('aria-expanded') !== 'true');
    });

    // Cerrar al elegir un destino
    menu.addEventListener('click', function (event) {
      if (event.target.closest('a')) setOpen(false);
    });

    // Cerrar con Escape, devolviendo el foco al botón
    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
        setOpen(false);
        toggle.focus();
      }
    });

    // Cerrar al tocar fuera del encabezado
    document.addEventListener('click', function (event) {
      if (toggle.getAttribute('aria-expanded') !== 'true') return;
      if (!event.target.closest('.site-header')) setOpen(false);
    });

    // Al volver a escritorio el menú deja de estar oculto: normalizamos estado
    var desktop = window.matchMedia('(min-width: 861px)');
    var onChange = function (event) { if (event.matches) setOpen(false); };
    if (desktop.addEventListener) desktop.addEventListener('change', onChange);
    else desktop.addListener(onChange); // Safari antiguo
  }

  /* ---------- Año en curso ----------------------------------------------- */

  var year = document.querySelector('[data-year]');
  if (year) year.textContent = String(new Date().getFullYear());
})();
