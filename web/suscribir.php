<?php
/* =========================================================================
   Iron-Coding — suscribir.php
   Lista de espera: guarda un correo para avisar del lanzamiento de una app.

   Requiere PHP (cPanel lo trae). Compatible con PHP 7.4+.
   No funciona en GitHub Pages, que solo sirve archivos estáticos.

   PENDIENTE antes de publicar: cambiar AVISO_A y REMITENTE por los buzones
   reales del dominio.
   ========================================================================= */

// A dónde llega el aviso de cada suscripción nueva.
define('AVISO_A', 'contacto@iron-coding.art');

// Remitente: TIENE que ser una dirección del propio dominio.
define('REMITENTE', 'web@iron-coding.art');

// Dónde se guarda la lista.
//
// Por defecto, UNA CARPETA POR ENCIMA de la raíz web: son datos personales y no
// deben quedar servibles por HTTP bajo ninguna circunstancia. Si subes el
// contenido de web/ a public_html/, esto escribe en el directorio padre, que
// cPanel no publica.
//
// Si tu hosting no deja escribir ahí, el código cae a web/datos/, que va
// protegido con .htaccess — pero eso depende de que ese archivo oculto se haya
// subido, así que es el plan B, no el plan A.
define('ALMACEN_PREFERIDO', __DIR__ . '/../iron-coding-datos/lista-espera.csv');
define('ALMACEN_ALTERNO',   __DIR__ . '/datos/lista-espera.csv');

// Apps que aceptan suscripción. Sirve de lista blanca: cualquier otro valor
// se rechaza, y de aquí sale la URL de retorno — nunca del formulario, para
// no convertir esto en un redirector abierto.
$APPS = array(
    'health-tracker'  => 'Health Tracker',
    'run-for-win'     => 'Run For Win',
    'footcarbonprint' => 'FootCarbonPrint',
    'pituapp'         => 'PituApp',
);

function campo($nombre, $maximo) {
    if (!isset($_POST[$nombre]) || !is_string($_POST[$nombre])) {
        return '';
    }
    return mb_substr(trim($_POST[$nombre]), 0, $maximo);
}

/** Quita saltos de línea: evita la inyección de cabeceras de correo. */
function una_linea($texto) {
    return trim(str_replace(array("\r", "\n", "%0a", "%0d"), ' ', $texto));
}

function volver($app, $estado) {
    $destino = $app === ''
        ? 'index.html'
        : 'proyectos/' . rawurlencode($app) . '/index.html';
    header('Location: ' . $destino . '?estado=' . $estado . '#lista-espera', true, 303);
    exit;
}

// ---- Solo POST ----------------------------------------------------------
if (!isset($_SERVER['REQUEST_METHOD']) || $_SERVER['REQUEST_METHOD'] !== 'POST') {
    header('Allow: POST');
    http_response_code(405);
    exit('Método no permitido.');
}

$app = campo('app', 60);
if (!isset($APPS[$app])) {
    // Slug desconocido: ni siquiera sabemos a dónde devolver.
    volver('', 'error');
}

// ---- Trampa antispam ----------------------------------------------------
// Respondemos "ok" a propósito para no darle pistas al robot.
if (campo('pagina_web', 200) !== '') {
    volver($app, 'ok');
}

// ---- Validación ---------------------------------------------------------
$correo = campo('correo', 180);
$acepto = campo('acepto', 10);

if ($acepto !== 'si' || !filter_var($correo, FILTER_VALIDATE_EMAIL)) {
    volver($app, 'error');
}

// ---- Guardado -----------------------------------------------------------

/** Deja la carpeta lista y devuelve la ruta si se puede escribir en ella. */
function preparar($ruta) {
    $carpeta = dirname($ruta);
    if (!is_dir($carpeta) && !@mkdir($carpeta, 0700, true)) {
        return null;
    }
    return is_writable($carpeta) ? $ruta : null;
}

$almacen = preparar(ALMACEN_PREFERIDO);
if ($almacen === null) {
    $almacen = preparar(ALMACEN_ALTERNO);
}

$fila = array(
    date('c'),
    $app,
    $correo,
    isset($_SERVER['REMOTE_ADDR']) ? $_SERVER['REMOTE_ADDR'] : '',
);

$guardado = false;
$manejador = $almacen === null ? false : @fopen($almacen, 'a');
if ($manejador !== false) {
    // Bloqueo exclusivo: dos envíos simultáneos no pueden entremezclar filas.
    if (flock($manejador, LOCK_EX)) {
        // OJO: ftell() sobre un descriptor en modo 'a' devuelve 0 aunque el
        // archivo tenga contenido, así que la cabecera se repetiría en cada
        // envío. El tamaño real hay que sacarlo de fstat(), ya con el bloqueo
        // tomado para que dos peticiones simultáneas no la escriban las dos.
        $estado_archivo = fstat($manejador);
        if (empty($estado_archivo['size'])) {
            fputcsv($manejador, array('fecha', 'app', 'correo', 'ip'));
        }
        $guardado = fputcsv($manejador, $fila) !== false;
        fflush($manejador);
        flock($manejador, LOCK_UN);
    }
    fclose($manejador);
    @chmod($almacen, 0600);
}

if (!$guardado) {
    volver($app, 'error');
}

// ---- Aviso por correo (no bloquea el resultado) --------------------------
$asunto = '=?UTF-8?B?' . base64_encode('[iron-coding.art] Lista de espera — ' . $APPS[$app]) . '?=';
$cuerpo = "Nueva suscripcion a la lista de espera\n"
        . "--------------------------------------\n\n"
        . 'App:    ' . $APPS[$app] . ' (' . $app . ")\n"
        . 'Correo: ' . $correo . "\n"
        . 'Fecha:  ' . date('Y-m-d H:i:s') . "\n";

$cabeceras  = 'From: Iron-Coding Web <' . REMITENTE . '>' . "\r\n";
$cabeceras .= 'Reply-To: ' . una_linea($correo) . "\r\n";
$cabeceras .= 'MIME-Version: 1.0' . "\r\n";
$cabeceras .= 'Content-Type: text/plain; charset=UTF-8' . "\r\n";

@mail(AVISO_A, $asunto, $cuerpo, $cabeceras, '-f' . REMITENTE);

// El correo ya quedó guardado: aunque falle el aviso, la suscripción es válida.
volver($app, 'ok');
