# Guía de ejecución y entrega

## Archivos
- informe-arquitectura.pdf: informe de cinco páginas.
- informe-arquitectura.md: contenido editable.
- arbol-src-app.txt: archivos de producción.
- validacion-build.txt: resultado de verificaciones.

## Ejecutar
1. Configurar Oracle según tarea07-backend/src/main/resources/application-dev.yaml.
2. En tarea07-backend: `mvnw.cmd spring-boot:run` (Java 21).
3. Revisar http://localhost:8080/swagger-ui.html y GET /api/v1/clientes.
4. En tarea07-frontend: `npm ci`, `npm start`.
5. Abrir http://localhost:4200/clientes.
6. Compilar: `npm run build`; probar: `npm test -- --watch=false`.

## Evidencias pendientes
Ejecutar los once casos de A7 indicados en el informe y guardar las capturas con Red visible. Debe verse método, URL, estado y cuerpo pertinente. Para comprobar ausencia de POST o peticiones de búsqueda, limpiar Red primero. No se incluyen capturas simuladas.

## Git y aula
Estas carpetas no son un checkout Git. Incorporar los cambios al repositorio real, partir de develop y crear feature/clientes-APELLIDO. Registrar avances reales con mensajes convencionales; el requisito de tres días distintos no puede recrearse en una sola sesión. Abrir PR a develop, añadir su enlace al informe y completar nombre del estudiante. Renombrar una copia a Apellido_LP2_S7_Autonoma.pdf y subirla al aula. No se ha realizado ninguna publicación ni subida.

## Cambios
Frontend: listado paginado, tamaño 5/10/20, orden DNI/apellidos, filtro local, metadatos y recarga tras baja; servicio con HttpParams. Formulario y rutas existentes conservados.
Backend: listado paginado, campos de orden permitidos, baja lógica y conflicto por baja repetida. Categorías no se modificó.

## Repositorio de entrega

Código guardado en https://github.com/Irxui666/autonoma07 con ramas independientes:
- backend: Spring Boot y pruebas Java.
- frontend: Angular, pruebas e informe en docs/.

El informe conserva el estado de revisión previo a crear el repositorio; la ausencia de Git que describe es histórica. Ahora existen las dos ramas solicitadas. No se ha creado develop ni un PR, porque esta entrega respeta backend/frontend. Siguen pendientes las capturas integradas y la entrega en el aula. Para arrancar backend, definir DB_USERNAME y DB_PASSWORD; las credenciales locales no se publican.
