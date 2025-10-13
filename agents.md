# AGENTS.md (Plantilla General, multipropósito y hexagonal)

> Marco universal para humanos y agentes (Cursor, Windsurf, Copilot, Claude…). **Hexagonal**, **story‑driven** y listo para **datos/ML**. Diseñado para trabajar bien en editores que no manejan `.ipynb` (Windsurf): usamos **Jupytext** con notebooks en `.py` (formato percent) editables y convertibles.

---

## 0) Identidad y alcance

- **Owner**: Alex (Data/MLOps, macOS).
- **Propósito**: repos multipropósito (ETL/ELT, APIs, apps, análisis) con foco en **claridad**, **tests**, **costes** y **storytelling de datos**.
- **Arquitectura guía**: **Hexagonal (Ports & Adapters)** para separar dominio, aplicación y periferia.

---

## 1) Estructura del repo (hexagonal + multipropósito)

```
.
├─ src/
│  ├─ domain/           # Reglas del negocio / modelos puros (sin I/O)
│  ├─ application/      # Casos de uso (servicios orquestan el dominio)
│  ├─ adapters/         # Puertos/Adaptadores: DB, S3, APIs externas, FS
│  └─ config/           # Settings, DI ligera (pydantic Settings)
│
├─ apps/                # Front-ends (Streamlit/Next) y CLI UX
├─ services/            # APIs (FastAPI) y workers (jobs)
├─ data/
│  ├─ schemas/          # JSON Schema / pydantic models
│  ├─ samples/          # Datos anonimizados de ejemplo (≤5MB)
│  └─ contracts/        # Contratos de entrada/salida
├─ notebooks_py/        # Notebooks en .py (Jupytext percent) ← Windsurf‑friendly
├─ reports/
│  ├─ figures/          # Gráficas exportadas (png/svg)
│  └─ artifacts/        # Tablas/CSV parciales para el informe
├─ infra/               # IaC (Terraform/Pulumi) + deploy scripts
├─ scripts/             # CLIs utilitarias (ingesta, migraciones, batch)
├─ tests/               # unit / integration / e2e (pytest)
├─ .github/workflows/   # CI/CD
├─ .cursor/             # rules específicas (opcional)
├─ .windsurf/           # global_rules.md (opcional)
├─ pyproject.toml / requirements*.txt / package.json
├─ .env.example         # variables ejemplo (sin secretos)
└─ Makefile             # atajos universales
```

**Regla de oro**: dominio y casos de uso **no** importan de adapters; adapters dependen hacia dentro.

---

## 2) Setup rápido (multiplataforma)

- macOS/Linux (WSL2 ok). Python 3.10–3.11; Node LTS si aplica.
- Gestor Python: `uv` (preferido) o `pip-tools`. Node: `pnpm`.
- Activar `pre-commit`. Copiar `.env.example` → `.env` (sin secretos).

**Comandos base**

- Python: `uv venv && source .venv/bin/activate && uv pip sync requirements.txt`
- Node: `pnpm i`
- Hooks: `pre-commit install`

---

## 3) Desarrollo diario

- **Lint/Format**: `ruff check . && ruff format .` (Py) · `pnpm lint` (TS)
- **Tipos**: `mypy` (Py) · `tsc --noEmit` (TS)
- **Tests**: `pytest -q` · `pnpm test -w`
- **Apps**: `streamlit run apps/<app>/app.py` · `pnpm dev`
- **APIs**: `uvicorn services.api.main:app --reload`
- **Docker**: `docker compose up --build`

> Agentes: correr lint + tests **antes y después** de cambios relevantes.

---

## 4) Estilo y prácticas (opinionadas)

- Funciones cortas, puras cuando se pueda; errores explícitos; **sin **`` salvo CLIs.
- **Logging** con niveles y contexto (IDs de correlación en jobs/requests).
- **Tipado** en interfaces públicas; validación con pydantic v2.
- **Idempotencia** en ETLs y migraciones.
- **Timeouts/retries** con backoff en cualquier I/O (HTTP/DB/S3).
- **Hexagonal**: dominio y casos de uso libres de dependencias técnicas.

**Don’ts**: secretos en código; queries sin límites; dependencias pesadas sin motivo; sleeps arbitrarios.

---

## 5) Datos, contratos y privacidad

- **Schemas** en `data/schemas/` (JSON Schema/pydantic) y **contratos** en `data/contracts/`.
- **Samples** anonimizados en `data/samples/` (≤5MB por archivo).
- **PII** fuera del repo. En despliegue usar almacenar secretos/roles.

---

## 6) Cloud/Infra (plantilla)

- **AWS**: perfiles `dev/stg/prd`, **IAM roles** preferidos a keys.
- **S3**: prefijo por entorno `s3://<bucket>/<env>/<domain>/…`; paginar; minimizar `List*`.
- **Lambda**: 512–1024 MB; ≤60s dev; logs en CloudWatch; empaquetado mínimo.
- **RDS**: SQLAlchemy/psycopg, retries exponenciales; **migraciones con Alembic**.
- **Costes**: batch, seleccionar columnas mínimas, TTL en staging, incremental con `updated_at`.

---

## 7) Automatización

- **n8n** por Docker Compose (local). Exportar workflows a `automation/n8n/` **sin credenciales**.
- Cualquier destrucción soporta `--dry-run` y `--limit`.

---

## 8) CI/CD (GitHub Actions)

- Pipeline: `lint → test → build → (opcional) deploy`.
- Gates: `uv pip audit`/`pip-audit`, `npm audit`, coverage mínima en servicios críticos.
- Deploy solo con tag `v*` o `main` en verde; `plan → apply` con aprobación manual en IaC.

---

## 9) Git y PRs

- Branching: `feat/…`, `fix/…`, `refactor/…`, `docs/…`.
- Commits (Conventional): `feat(domain): añadir agregados de ventas semanales`.
- Plantilla PR:

```
### Qué cambia

### Cómo se implementa (arquitectura hexagonal)
Dominio ↔ Casos de uso ↔ Adaptadores (entradas/salidas): explica límites.

### Riesgos / Rollback

### Tests / Cómo reproducir
```

---

## 10) Seguridad

- `.env` local; CI/CD con GitHub Secrets / AWS SM.
- Auditoría de dependencias en CI; rotación de pins periódica.
- Datos: anonimización, retención, *least privilege*.

---

## 11) **Reglas para agentes** (Cursor/Windsurf)

1. **Lee primero** este archivo y el README de la carpeta tocada.
2. **Planifica** antes de tocar >200 LOC o esquemas (enumera pasos/impactos).
3. **Respeta hexagonal**: no mezcles dominio con adapters; propone refactor si ya está mezclado.
4. **Tests**: crea/actualiza y ejecuta antes de abrir PR.
5. **Cost‑aware**: agrupa I/O, pagina, evita N×requests/queries.
6. **Storytelling de datos**: si produces análisis, **cuenta una historia** (ver §13) y guarda figuras en `reports/figures/`.
7. **Windsurf**: si necesitas un notebook, **crea **``** estilo Jupytext** (ver §12) y no `.ipynb` directamente.
8. **Privacidad**: no inventes credenciales ni completes `.env` real; usa `.env.example`.
9. **DB**: toda alteración con Alembic; nada de `ALTER TABLE` manual en prod.
10. **UX**: en Streamlit/Next, validar inputs y cachear (`st.cache_*` / SWR) para no bloquear.

---

## 12) **Notebooks **``** con Jupytext** (modo Windsurf)

- Ubicación: `notebooks_py/`.
- Formato: **percent format** con cabecera Jupytext. Ejemplo base:

```python
# %% [markdown]
# # Análisis Exploratorio — Ventas 2025 Q3
# **Objetivo**: entender drivers de ingresos y estacionalidad.
# **Datos**: `data/samples/sales_2025_q3.csv` (anonimizado).
# **Salida**: figuras en `reports/figures/` y tabla resumen en `reports/artifacts/`.

# %%
# jupytext: {"formats": "notebooks_py//py:percent"}
# type: ignore
import pathlib as _p
import pandas as pd
import matplotlib.pyplot as plt

ROOT = _p.Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "samples" / "sales_2025_q3.csv"
FIGS = ROOT / "reports" / "figures"
ARTS = ROOT / "reports" / "artifacts"
FIGS.mkdir(parents=True, exist_ok=True)
ARTS.mkdir(parents=True, exist_ok=True)

# %% [markdown]
# ## 1. Carga y validación
# - Sin `print()`: usar displays puntuales o logs si es script.
# - Validar columnas clave y rangos temporales.

# %%
df = pd.read_csv(DATA)
expected = {"date", "region", "revenue"}
missing = expected - set(df.columns)
if missing:
    raise ValueError(f"Faltan columnas: {missing}")

# %% [markdown]
# ## 2. Tendencias básicas
# Exportar figuras con nombres autoexplicativos.

# %%
df["date"] = pd.to_datetime(df["date"]) 
monthly = df.set_index("date").resample("M")["revenue"].sum()
ax = monthly.plot(title="Ingresos mensuales")
ax.figure.tight_layout()
ax.figure.savefig(FIGS / "ingresos_mensuales.png", dpi=144)
plt.close(ax.figure)

# %% [markdown]
# ## 3. Hallazgos y próximos pasos
# - p95 de variabilidad por región
# - hipótesis sobre campañas y estacionalidad

# %%
sum_table = df.groupby("region")["revenue"].describe(percentiles=[0.95])
sum_table.to_csv(ARTS / "resumen_por_region.csv")
```

**Conversión**: `jupytext --to ipynb notebooks_py/analisis_q3.py` (solo cuando necesites `.ipynb`).

**Criterios de calidad**:

- Markdown **con propósito** (contexto, hipótesis, hallazgos, limitaciones, próximos pasos).
- Gráficas **que aporten** (título claro, ejes legibles, leyenda si suma).
- Evitar `print()` masivo; si es script, usa `logging`.
- Artefactos versionables en `reports/`.

---

## 13) **Storytelling de datos** (checklist)

- **Contexto**: qué pregunta respondemos y por qué importa.
- **Hipótesis**: qué esperamos ver.
- **Evidencia**: tablas/figuras mínimas y concluyentes (no “mural” de charts).
- **Conclusión accionable**: qué decisión cambia.
- **Limitaciones**: muestras, sesgos, calidad.
- **Siguientes pasos**: qué validar a continuación.

> Cada notebook `.py` debe cerrar con un bloque **Hallazgos/Acciones**.

---

## 14) Variables de entorno (plantilla)

```
APP_ENV=dev
LOG_LEVEL=INFO
TZ=Europe/Madrid
# APIs
API_BASE=https://example.api
API_KEY=changeme
# AWS / Storage
AWS_REGION=eu-west-1
S3_BUCKET=changeme
S3_PREFIX=dev
# DB
PGHOST=localhost
PGPORT=5432
PGDATABASE=app
PGUSER=app
PGPASSWORD=changeme
# n8n (si aplica)
N8N_SECURE_COOKIE=false
GENERIC_TIMEZONE=Europe/Madrid
N8N_ENCRYPTION_KEY=hex64
```

---

## 15) Makefile (atajos)

```
.PHONY: setup lint test fmt audit docker app nb nb2ipynb
setup:
	uv venv || python -m venv .venv
	source .venv/bin/activate && uv pip sync requirements.txt || true
	pre-commit install || true

lint:
	ruff check . && ruff format --check . || true
	type mypy >/dev/null 2>&1 && mypy src || true
	type pnpm >/dev/null 2>&1 && pnpm lint || true

fmt:
	ruff format . && type isort >/dev/null 2>&1 && isort . || true

audit:
	uv pip audit || pip-audit || true

test:
	pytest -q || true

docker:
	docker compose up --build

app:
	streamlit run apps/<app>/app.py || true

nb:
	jupytext --set-formats notebooks_py//py:percent --sync notebooks_py/*.py

nb2ipynb:
	jupytext --to ipynb notebooks_py/*.py
```

---

## 16) Métricas y calidad

- ETL: filas leídas/escritas, % duplicados, tiempo, coste estimado.
- APIs: p50/p95, errores, timeouts.
- ML: matriz de confusión, F1/AUC; `model_card.md`.

---

## 17) Heurísticas de diseño (cómo pensar)

- **Primero contratos**, después código. Cambios de contrato = breaking change.
- **Menos es más**: elimina dependencias y código muerto.
- **Estrategia incremental**: usa `updated_at`/marcas temporales.
- **Observabilidad by default**: logs, métricas y trazas mínimas.
- **Hexagonal** siempre: dominio limpio; adapters reemplazables.

---

## 18) Referencias internas (añade enlaces locales)

- `docs/architecture.md` (diagrama hexagonal + flujos críticos)
- \`data/sche
