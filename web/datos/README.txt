Carpeta de respaldo para la lista de espera.

Por defecto, suscribir.php NO escribe aqui: guarda lista-espera.csv una carpeta
por ENCIMA de la raiz web (al lado de public_html, no dentro), porque son datos
personales y ahi no hay manera de que se sirvan por HTTP.

Esta carpeta es el plan B: solo se usa si el hosting no deja escribir arriba.
En ese caso el .htaccess de aqui bloquea el acceso web — comprueba que se subio
activando "Mostrar archivos ocultos" en el Administrador de archivos de cPanel.

Donde buscar el archivo, en este orden:
  1. /home/<tu-usuario>/iron-coding-datos/lista-espera.csv   <- lo normal
  2. public_html/datos/lista-espera.csv                      <- solo si fallo 1

El CSV no esta en el repositorio a proposito: son correos de personas reales y
no deben viajar en git ni subirse a GitHub.
