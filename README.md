# PharmaSoft — Semana 7

Frontend Angular adaptado al backend `../tarea05` (Java 21, Spring Boot y Oracle).

## Ejecutar

1. Iniciar Oracle. Revisar la conexión en `tarea05/src/main/resources/application-dev.yaml`: `localhost:1522/freepdb1`, esquema `ACTIVIDAD01`.
2. Ejecutar `Actividad01Application` desde el IDE con Java 21, o `mvnw.cmd spring-boot:run` dentro de tarea05. La API utiliza el puerto 8080.
3. Dentro de este frontend ejecutar `npm.cmd install` si faltan dependencias y `npm.cmd start`.
4. Abrir http://localhost:4200.

El proxy de desarrollo redirige `/api/**` al puerto 8080. Solo debe haber un backend utilizando ese puerto.

## Alcance de la semana 7

- Inicio, layout y navegación PharmaSoft.
- Categorías: listar, buscar por nombre, crear, editar y eliminar.
- Clientes: listar, buscar por DNI/nombre/correo, crear, editar y eliminar.
- Formularios reactivos, mensajes de validación, estados de carga y errores del servidor.
- Rutas diferidas y separación de listados, formularios, modelos y servicios.

Los servicios consumen `/api/v1/categorias` y `/api/v1/clientes`: GET/POST en la colección y GET/PUT/DELETE por identificador. Las listas son arrays. Clientes requiere DNI de 8 dígitos, nombres y apellidos de 2–100 caracteres y correo válido. Teléfono es opcional y, si se introduce, debe tener 9 dígitos; los campos opcionales vacíos se envían como null.

Los duplicados y las eliminaciones con registros asociados devuelven 409; los datos inválidos, 400; los identificadores inexistentes, 404. La eliminación correcta devuelve 204. Productos y Ventas permanecen disponibles en el backend, fuera del alcance de esta interfaz de semana 7.

## Comprobación

Ejecutar `npm.cmd run build` y `npm.cmd test -- --watch=false`.
En tarea05, `mvnw.cmd -Dtest=CategoriaServiceRulesTest test` comprueba las reglas de categorías sin conectarse a Oracle. La prueba de contexto original sí requiere la base de datos configurada.

Con Oracle y la API iniciados, comprobar altas, edición, búsqueda, cancelación de eliminación, duplicados y eliminación de una categoría con productos asociados. Confirmar que los cambios permanecen al recargar la página.

El PDF anterior de Historia Clínica corresponde a otra versión y debe sustituirse antes de entregar la documentación de PharmaSoft.
