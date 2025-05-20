# Todo List Observability Project

[![CI / CD Pipeline](https://github.com/Angelmz501/TodoList-Observability/actions/workflows/docker-image.yml/badge.svg)](https://github.com/Angelmz501/TodoList-Observability/actions/workflows/docker-image.yml)

Una aplicación **Todo List** construida en Flask y que integra un completo stack de observabilidad y despliegue automatizado:

- **Instrumentación** con OpenTelemetry (trazas y métricas OTLP).  
- **Scraping** de métricas con Prometheus.  
- **Dashboards** y persistencia con Grafana.  
- **Contenerización** con Docker & Docker Compose.  
- **Despliegue** automatizado con Ansible.  
- **CI/CD** con GitHub Actions: lint, build de imagen Docker y despliegue.

---

## 📂 Estructura del proyecto

```
.
├── .github/                   ← Workflows de GitHub Actions
│   └── workflows/
│       └── docker-image.yml   ← CI/CD pipeline
├── ansible.cfg                ← Configuración Ansible
├── deploy.yml                 ← Playbook de despliegue local
├── inventory.ini              ← Inventario (localhost)
├── Dockerfile                 ← Imagen de tu app Flask
├── docker-compose.yml         ← Orquestación local (app, OTEL, Prometheus, Grafana)
├── prometheus.yml             ← Config Prometheus
├── otel-collector-config.yaml ← Config OpenTelemetry Collector
├── .flake8                    ← Reglas de style-checking para flake8
├── requirements.txt           ← Dependencias Python
├── app.py                     ← Lógica de la aplicación Flask
├── templates/
│   └── base.html              ← Plantilla HTML principal
└── README.md                  ← Este fichero
```

---

## 🚀 Tecnologías

- **Flask** & **Flask-SQLAlchemy**  
- **OpenTelemetry** (SDK, exporters OTLP)  
- **Prometheus** & **Node Exporter**  
- **Grafana** (con volumen persistente)  
- **Docker** & **Docker Compose**  
- **Ansible** (orquestación local)  
- **GitHub Actions** (CI/CD)  
- **flake8** (linteo de código Python)

---

## 🛠️ Prerrequisitos

- Docker & Docker Compose (v2+).  
- Python 3.10+ (para tests y lint local).  
- Ansible 2.15+ (para despliegue local).  
- Git & GitHub account.

---

## 🔧 Instalación y ejecución local

1. **Clona este repositorio**  
   ```bash
   git clone git@github.com:Angelmz501/TodoList-Observability.git
   cd TodoList-Observability
   ```

2. **Instala dependencias Python** (opcional, sólo si quieres lintear o testear localmente)
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   pip install flake8
   flake8 .
   ```

3. **Arranca todo con Ansible**
   ```bash
   ansible-playbook -i inventory.ini deploy.yml
   ```

   Esto:
   * Construye y arranca tus contenedores (`docker-compose up -d --build`).
   * Espera a que Flask y Prometheus estén listos antes de finalizar.

4. **Comprueba los servicios**

   * App Flask → [http://localhost/](http://localhost/)
   * Prometheus → [http://localhost:9090](http://localhost:9090)
   * Grafana → [http://localhost:3000](http://localhost:3000)  (credenciales por defecto: **admin/admin**)

---

## 📝 Despliegue manual Docker Compose

Si prefieres hacerlo sin Ansible:

```bash
docker compose down
docker compose up -d --build
```

Y para parar TODO:

```bash
docker compose down --volumes
```

---

## 🌐 CI/CD con GitHub Actions

El workflow `.github/workflows/docker-image.yml` se dispara:

* **En cada push o PR** contra `main`.
* **Manualmente** desde la UI (botón “Run workflow”).

Jobs:

1. **build**:
   * `checkout` → `setup-python` → `pip install` → `flake8` → `docker build`.

2. **deploy** (needs: build):
   * `checkout` → instala `docker-compose` & `ansible` → `ansible-playbook`.

De este modo tu app se construye y despliega **automáticamente** en local o (con ajustes) en un servidor remoto.

---

## 💾 Persistencia de datos

- **Grafana**: volumen Docker `grafana_data` en `/var/lib/grafana` para mantener dashboards y configuraciones.
- **SQLite** (Flask): carpeta `./db` montada en `/app/db` dentro del contenedor.

---

## 🚧 Buenas prácticas / siguientes pasos

- **Versiona tus dashboards** bajo `provisioning/dashboards/` para importarlos automáticamente.
- **Define alertas** en Prometheus (`alert.rules.yml`) y configúralas en Grafana o Alertmanager.
- **Modulariza Ansible** en roles (`roles/app`, `roles/monitoring`, …).
- **Entornos separados**: crea inventarios `staging` y `production`.
- **Tests de integración**: añade un job de pruebas dentro del contenedor Docker (pytest).

---

## 🏷️ Licencia

*Proyecto libre de derechos* – úsalo, adáptalo y mejóralo sin restricciones.

---

¡Gracias por usar este proyecto! Cualquier duda o mejora, abre un *issue* o *pull request* en GitHub. 🎉