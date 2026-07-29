<?php
/* =========================================================================
   Iron-Coding — enviar.php
   Recibe el formulario de pages/contacto.html y lo manda por correo.

   Requiere PHP en el hosting (cPanel lo trae). Compatible con PHP 7.4+.
   Este archivo NO funciona en GitHub Pages, que solo sirve archivos
   estáticos: allí el formulario dará 404. El envío real es en cPanel.

   PENDIENTE antes de publicar: cambiar DESTINO y REMITENTE por los
   buzones reales del dominio, creados en cPanel > Cuentas de correo.
   ========================================================================= */

// A dónde llegan los mensajes.
define('DESTINO', 'contacto@iron-coding.art');

// Desde qué dirección se envían. TIENE que ser del propio dominio:
// si aquí se pone el correo de quien escribe, los servidores lo marcan
// como suplantación y el mensaje termina en spam o se rechaza.
define('REMITENTE', 'web@iron-coding.art');

define('PAGINA', 'pages/contacto.html');

/**
 * Devuelve al visitante al formulario con el resultado en la URL.
 * Solo viajan valores fijos ("ok" / "error"), nunca texto del usuario.
 */
function volver($estado) {
    header('Location: ' . PAGINA . '?estado=' . $estado, true, 303);
    exit;
}

/** Quita saltos de línea: evita la inyección de cabeceras de correo. */
function una_linea($texto) {
    return trim(str_replace(array("\r", "\n", "%0a", "%0d"), ' ', $texto));
}

/** Lee un campo del POST como texto plano y acotado. */
function campo($nombre, $maximo) {
    if (!isset($_POST[$nombre]) || !is_string($_POST[$nombre])) {
        return '';
    }
    return mb_substr(trim($_POST[$nombre]), 0, $maximo);
}

// ---- Solo se acepta POST ------------------------------------------------
if (!isset($_SERVER['REQUEST_METHOD']) || $_SERVER['REQUEST_METHOD'] !== 'POST') {
    header('Allow: POST');
    http_response_code(405);
    exit('Método no permitido.');
}

// ---- Trampa antispam ----------------------------------------------------
// Un robot rellena todos los campos, incluido el que está oculto.
// Le respondemos "ok" a propósito para no darle pistas de que lo detectamos.
if (campo('sitio_web', 200) !== '') {
    volver('ok');
}

// ---- Lectura y validación ----------------------------------------------
$nombre  = campo('nombre', 120);
$email   = campo('email', 180);
$empresa = campo('empresa', 120);
$tipo    = campo('tipo', 60);
$mensaje = campo('mensaje', 4000);
$consent = campo('consentimiento', 10);

$tipos_validos = array('App nueva', 'Evolucion', 'Consultoria', 'Diseno', 'Otro');

if ($nombre === '' || $mensaje === '' || $consent !== 'si') {
    volver('error');
}

if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    volver('error');
}

if (!in_array($tipo, $tipos_validos, true)) {
    $tipo = 'Otro';
}

// ---- Composición del correo --------------------------------------------
$asunto = '[iron-coding.art] ' . $tipo . ' — ' . una_linea($nombre);

// El asunto lleva tildes: hay que codificarlo o llega ilegible.
$asunto_codificado = '=?UTF-8?B?' . base64_encode($asunto) . '?=';

$cuerpo = "Nuevo mensaje desde el formulario de iron-coding.art\n"
        . "-------------------------------------------------\n\n"
        . "Nombre:  " . $nombre . "\n"
        . "Correo:  " . $email . "\n"
        . "Empresa: " . ($empresa !== '' ? $empresa : '(no indicada)') . "\n"
        . "Tipo:    " . $tipo . "\n\n"
        . "Mensaje:\n"
        . $mensaje . "\n\n"
        . "-------------------------------------------------\n"
        . "Enviado: " . date('Y-m-d H:i:s') . "\n";

$cabeceras  = 'From: Iron-Coding Web <' . REMITENTE . '>' . "\r\n";
$cabeceras .= 'Reply-To: ' . una_linea($email) . "\r\n";
$cabeceras .= 'MIME-Version: 1.0' . "\r\n";
$cabeceras .= 'Content-Type: text/plain; charset=UTF-8' . "\r\n";
$cabeceras .= 'Content-Transfer-Encoding: 8bit' . "\r\n";

// El quinto parámetro fija el remitente del sobre; sin él muchos
// servidores compartidos rechazan el mensaje.
$enviado = @mail(
    DESTINO,
    $asunto_codificado,
    $cuerpo,
    $cabeceras,
    '-f' . REMITENTE
);

volver($enviado ? 'ok' : 'error');
