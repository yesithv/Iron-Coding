/* =========================================================================
   Iron-Coding — formularios.js
   Lista de espera de cada producto: mensaje de resultado y validación
   en el navegador.

   Es una mejora, no un requisito: si el JavaScript no carga, el formulario
   se envía igual y suscribir.php vuelve a validarlo todo en el servidor.
   ========================================================================= */

(function () {
  'use strict';

  /* ---------- Resultado del envío (?estado=ok | ?estado=error) ----------- */

  var estado = new URLSearchParams(window.location.search).get('estado');

  if (estado === 'ok' || estado === 'error') {
    var panel = document.getElementById(estado === 'ok' ? 'resultado-ok' : 'resultado-error');
    if (panel) {
      panel.hidden = false;
      panel.scrollIntoView({ block: 'center' });
    }
    if (estado === 'ok') {
      var enviado = document.querySelector('.form--lista');
      if (enviado) enviado.reset();
    }
    // Limpia la URL para que al recargar no reaparezca el mensaje.
    if (window.history.replaceState) {
      window.history.replaceState({}, '', window.location.pathname + window.location.hash);
    }
  }

  /* ---------- Validación ------------------------------------------------- */

  var form = document.querySelector('.form--lista');
  if (!form) return;

  var correo = document.getElementById('correo');
  var acepto = document.getElementById('acepto');

  function marcar(id, error) {
    var contenedor = document.getElementById('campo-' + id);
    var salida = document.getElementById('error-' + id);
    if (!contenedor || !salida) return;

    salida.textContent = error;
    if (error) {
      contenedor.setAttribute('data-invalido', 'true');
    } else {
      contenedor.removeAttribute('data-invalido');
    }
  }

  function validarCorreo() {
    var v = correo ? correo.value.trim() : '';
    var error = '';
    if (v === '') error = 'Escribe tu correo.';
    else if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v)) error = 'Ese correo no parece válido.';
    marcar('correo', error);
    return error === '';
  }

  function validarAcepto() {
    var error = (acepto && acepto.checked) ? '' : 'Necesitamos tu autorización para escribirte.';
    marcar('acepto', error);
    return error === '';
  }

  if (correo) {
    correo.addEventListener('blur', validarCorreo);
    correo.addEventListener('input', function () {
      var c = document.getElementById('campo-correo');
      if (c && c.getAttribute('data-invalido') === 'true') validarCorreo();
    });
  }

  if (acepto) {
    acepto.addEventListener('change', function () {
      var c = document.getElementById('campo-acepto');
      if (c && c.getAttribute('data-invalido') === 'true') validarAcepto();
    });
  }

  form.addEventListener('submit', function (evento) {
    var okCorreo = validarCorreo();
    var okAcepto = validarAcepto();

    if (!okCorreo || !okAcepto) {
      evento.preventDefault();
      var foco = !okCorreo ? correo : acepto;
      if (foco) foco.focus();
      return;
    }

    var boton = form.querySelector('button[type="submit"]');
    if (boton) {
      boton.disabled = true;
      boton.textContent = 'enviando...';
    }
  });
})();
