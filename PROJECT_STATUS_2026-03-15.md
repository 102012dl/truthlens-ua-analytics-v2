# TruthLens UA Analytics — Project Status Report

## Timestamp

- **Date**: 2026-03-15
- **Audit scope**: local runtime, repo cleanliness, startup scripts, README accuracy, public links

## Current status

- **Local API**: working
- **Local dashboard**: working
- **Dashboard to API integration**: fixed for local mode using `http://127.0.0.1:8000`
- **Database dependency**: degraded-but-working local mode when PostgreSQL is unavailable
- **Docker config**: present and aligned with current entrypoints

## Fixes confirmed in repository

- `app.main:app` is the active FastAPI entrypoint
- `/check` no longer hard-fails when DB persistence is unavailable
- `dashboard/Home.py` prefers `127.0.0.1` for local API access
- URL inputs from dashboard are submitted as `url`, not plain `text`
- `docker-compose.yml` runs `streamlit run Home.py` (context `./dashboard`)
- startup scripts point to current entrypoints

## Cleanup status

- obsolete references were removed from docs/scripts
- repository still contains removable noise files pending deletion confirmation:
  - `dashboard/app_old.py`
  - `dashboard/app_conflict.py`
  - `dashboard/Dockerfile_old`
  - `dashboard/requirements_dash.txt`

## Documentation status

- `README.md` updated with:
  - current local entrypoints
  - quick restart commands for Windows PowerShell
  - quick restart commands for WSL/Linux
  - Docker restart command
  - API smoke-test commands
  - corrected Render links explanation

## Public links status

- **GitHub**: reachable
  - `https://github.com/102012dl/truthlens-ua-analytics`
- **GitLab**: not publicly readable during audit (`403 Forbidden`)
  - `https://gitlab.com/102012dl/truthlens-ua-analytics`
- **Render dashboard app**: reachable as public Streamlit app
  - `https://truthlens-ua-analytics.onrender.com`
- **Render project dashboard**: internal/admin URL, not suitable as public demo link
  - `https://dashboard.render.com/project/prj-d6mam39aae7s73ffbna0`
- **Render API/root service**: separate accessible endpoint
  - `https://truthlens-ua.onrender.com`

## Remaining cautions

- local `/health` may show:
  - `status: degraded`
  - `db: disconnected`
- this is acceptable for demo if API responses still succeed and dashboard works
- Windows PowerShell 5.1 may still display Ukrainian JSON text with broken console encoding, while the browser UI remains correct

## Recommended demo links

- **Primary demo UI**: `https://truthlens-ua-analytics.onrender.com`
- **Primary local UI**: `http://localhost:8501`
- **Local API docs**: `http://127.0.0.1:8000/docs`
- **Local health**: `http://127.0.0.1:8000/health`

## Quick restart commands

### Windows PowerShell

```powershell
cd C:\Users\home2\Downloads\truthlens-ua-analytics
python -m uvicorn app.main:app --reload --port 8000
```

```powershell
cd C:\Users\home2\Downloads\truthlens-ua-analytics\dashboard
streamlit run dashboard/Home.py --server.port 8501
```

### WSL / Linux

```bash
cd /mnt/c/Users/home2/Downloads/truthlens-ua-analytics
python -m uvicorn app.main:app --reload --port 8000
```

```bash
cd /mnt/c/Users/home2/Downloads/truthlens-ua-analytics/dashboard
streamlit run dashboard/Home.py --server.port 8501
```

### Docker

```bash
docker-compose up --build
```

## Audit conclusion

- the project is now substantially cleaner and more internally consistent than before
- local runtime is operational
- repo still needs commit/push/deploy follow-through after review
- the public demo link for external users should be the Streamlit Render URL, not the Render admin dashboard URL
