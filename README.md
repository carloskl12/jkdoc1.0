# jkdoc1.0
El presente programa surge con el ánimo de generar una base de datos con soluciones a problemas puntuales en diferentes lenguajes de programación. Esto es con el fin de tener a la mano código que ya hemos utilizado de forma rápida.

Todo empezó debido a que en el caso del autor, debido a sus necesidades variadas al requerir diferentes lenguajes de programación, debe revisar cómo se háce algo en algún lenguaje de programación particular. Como es  normal, luego de un tiempo de no trabajar en un lenguaje se olvidan algunas cosas. El hecho de pasar a trabajar entre diferentes lenguajes, sin ser un genio de programación implica al autor, el hecho de debe volver a buscar el código que funcionó bien ya sea en el proyecto pasado, o en en google. Por tal razón, busqué implementar esta solución.

Aunque finalmente, por buscar perfeccionar el proyecto, terminé dejándo incompleta una versión que reemplazaría la actual, decidí dejar esta versión funcional libre para quien la encuentre útil.

# Organización del programa
La organización de la interfaz del programa es sencilla, consta de una ventana principal, donde se halla información relacionada a las respuestas agregadas, y desde la cual, atravéz de íconos se puede acceder a dos ventanas secundarias:
* La ventana para filtrar respuestas.
* La ventana para agregar una nueva respuesta.

# Base de datos y campos de las respuestas
La base de datos se implementa utilizando Sqlite, y cada respuesta tiene los siguientes campos:
* Lenguaje: lenguaje de programación, aunque en mi caso también lo uso para relacionarlo con algún programa.
* Versión: versión del lenguaje o programa, esto es para los casos donde los códigos varian de una a otra versión, en caso de que no exista este problema, se puede colocar **estandar**.
* Librería: si el código está relacionado con una librería en particular, en caso contrario, se puede utilizar **estandar**.
* Verbo: El verbo asociado al problema o acción que se quiere realizar con el código.
* SustantivoA: sustantivo que se quiere modificar.
* SustantivoB: sustantivo o palabra que ayuda a especificar mejor el objeto a modificar.
* Descripción: Una frase que describe la acción o problema que se resuelve con el código.
* Código: Código en el lenguaje de programación especificado que realiza la acción descrita en el campo de descripción.

La ventana de filtros, permite buscar en la base de datos las respuestas asociadas a los comodines que se hayan seleccionado.

# Distribución de directorio
* src: codigo fuente de clases
* icons: iconos de los botones de acceso a las ventanas secundarias
* data: base de datos donde se guardan las respuestas

# Requisitos
Las librerías requeridas son:
* wx: probada la version 3.0.2.0
* sqlite: probada la versión 3.11.0

Se ha probado el programa en la versión 2.7.12 de python.
