# Proyecto: Formateo, Estilo y Análisis con SonarQube

Este es un proyecto de API de Flask como práctica para aplicar formateo de código (PEP 8), análisis de calidad con SonarQube y automatización con GitHub Actions.

## 🚀 Cómo ejecutar la aplicación (Docker)

Para construir y ejecutar la aplicación en modo de producción simple:

1.  **Construir la imagen:**
    ```bash
    docker build -t mi-app:1.0 .
    ```

2.  **Ejecutar el contenedor:**
    ```bash
    docker run --rm -p 8000:8000 mi-app:1.0
    ```

3.  Abre [http://localhost:8000](http://localhost:8000) en tu navegador.

## 🛠️ Entorno de Desarrollo

Este proyecto utiliza un contenedor de desarrollo (`Dockerfile.dev` y `docker-compose.yml`) para asegurar un entorno consistente para las pruebas y el formateo.

**Ejecutar formateador (Black):**
```bash
docker compose run --rm -T dev black .
Ejecutar tests (Pytest):

Bash

docker compose run --rm -T dev pytest
🔍 Cómo lanzar el análisis de SonarQube (Local)
El análisis de calidad se realiza con SonarQube, ejecutándose localmente en Docker.

Paso 1: Iniciar el servidor SonarQube:

Bash

docker run -d --name sonarqube -p 9000:9000 sonarqube:latest
Accede a http://localhost:9000 (admin/admin) y genera un token.

Paso 2: Ejecutar el análisis (Sonar Scanner): Reemplaza TU_TOKEN_SECRETO por el token generado en SonarQube.

PowerShell

docker run --rm `
  -e SONAR_HOST_URL="[http://host.docker.internal:9000](http://host.docker.internal:9000)" `
  -e SONAR_TOKEN="TU_TOKEN_SECRETO" `
  -v "${PWD}:/usr/src" `
  sonarsource/sonar-scanner-cli `
  "-Dsonar.projectKey=testSonar" `
  "-Dsonar.sources=."
Después, revisa los resultados actualizados en http://localhost:9000.

✨ Buenas Prácticas Seguidas
PEP 8: Formateo de código estándar de Python (snake_case, PascalCase, etc.).

Git: Uso de ramas (feature/fix/refactor) y Pull Requests para la integración de código.

Clean Code: Refactorización de código duplicado ("literales mágicos") en constantes para mejorar la mantenibilidad, siguiendo las sugerencias de SonarQube.

CI/CD: Automatización de análisis con GitHub Actions (configurado para ejecutarse en push a main).
