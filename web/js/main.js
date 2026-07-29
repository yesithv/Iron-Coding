/* =========================================================================
   Iron-Coding — main.js
   Lo mínimo indispensable: menú de navegación en móvil y año del pie.
   Sin dependencias. Si el script no carga, el menú queda desplegado
   (regla `html:not(.js)` en base.css), así que nada queda inaccesible.
   ========================================================================= */

(function () {
  'use strict';

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
