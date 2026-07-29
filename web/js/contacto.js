/* =========================================================================
   Iron-Coding — contacto.js
   Mensaje de resultado y validación en el navegador.

   Es una mejora, no un requisito: si el JavaScript no carga, el formulario
   se envía igual y enviar.php vuelve a validarlo todo del lado del servidor.
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
      var enviado = document.getElementById('form-contacto');
      if (enviado) enviado.reset();
    }
    // Limpia la URL para que al recargar no reaparezca el mensaje.
    if (window.history.replaceState) {
      window.history.replaceState({}, '', window.location.pathname);
    }
  }

  /* ---------- Validación ------------------------------------------------- */

  var form = document.getElementById('form-contacto');
  if (!form) return;

  var reglas = {
    nombre: function (v) {
      if (v.trim() === '') return 'Escribe tu nombre.';
      return '';
    },
    email: function (v) {
      if (v.trim() === '') return 'Escribe tu correo.';
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim())) return 'Ese correo no parece válido.';
      return '';
    },
    tipo: function (v) {
      if (v === '') return 'Elige el tipo de proyecto.';
      return '';
    },
    mensaje: function (v) {
      if (v.trim() === '') return 'Cuéntanos qué necesitas.';
      if (v.trim().length < 20) return 'Con un poco más de detalle podemos responderte mejor.';
      return '';
    },
    consentimiento: function (v, campo) {
      if (!campo.checked) return 'Necesitamos tu autorización para responderte.';
      return '';
    }
  };

  function marcar(nombre, error) {
    var contenedor = document.getElementById('campo-' + nombre);
    var salida = document.getElementById('error-' + nombre);
    if (!contenedor || !salida) return;

    salida.textContent = error;
    if (error) {
      contenedor.setAttribute('data-invalido', 'true');
    } else {
      contenedor.removeAttribute('data-invalido');
    }
  }

  function validarCampo(nombre) {
    var campo = document.getElementById(nombre);
    if (!campo) return true;
    var error = reglas[nombre](campo.value, campo);
    marcar(nombre, error);
    return error === '';
  }

  // Revalida al salir del campo, y en vivo una vez que ya falló
  Object.keys(reglas).forEach(function (nombre) {
    var campo = document.getElementById(nombre);
    if (!campo) return;

    campo.addEventListener('blur', function () { validarCampo(nombre); });
    campo.addEventListener('input', function () {
      var contenedor = document.getElementById('campo-' + nombre);
      if (contenedor && contenedor.getAttribute('data-invalido') === 'true') validarCampo(nombre);
    });
    campo.addEventListener('change', function () {
      var contenedor = document.getElementById('campo-' + nombre);
      if (contenedor && contenedor.getAttribute('data-invalido') === 'true') validarCampo(nombre);
    });
  });

  form.addEventListener('submit', function (evento) {
    var primerError = null;

    Object.keys(reglas).forEach(function (nombre) {
      if (!validarCampo(nombre) && !primerError) primerError = nombre;
    });

    if (primerError) {
      evento.preventDefault();
      var campo = document.getElementById(primerError);
      if (campo) campo.focus();
      return;
    }

    // Evita el doble envío mientras el servidor responde
    var boton = document.getElementById('boton-enviar');
    if (boton) {
      boton.disabled = true;
      boton.textContent = 'enviando...';
    }
  });
})();
