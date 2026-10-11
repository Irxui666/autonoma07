# PharmaSoft - Backend

API Spring Boot de la actividad autónoma 7. Incluye Clientes con paginación, orden y baja lógica.

Requisitos: Java 21 y Oracle. Antes de iniciar, definir DB_USERNAME y DB_PASSWORD con las credenciales locales. La conexión de desarrollo se configura en src/main/resources/application-dev.yaml.

Ejecutar: `mvnw.cmd spring-boot:run`.
Swagger: http://localhost:8080/swagger-ui.html.
Pruebas unitarias: `mvnw.cmd "-Dtest=CategoriaServiceRulesTest,ClienteServiceRulesTest" test`.

El frontend y el informe técnico están en la rama frontend de este repositorio.
