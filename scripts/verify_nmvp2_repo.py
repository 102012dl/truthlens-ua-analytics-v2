#!/usr/bin/env python3
"""
Automated NMVP2 repository checks (A-H) for CI and Cursor Composer.
(Section H uses CheckResponse.model_json_schema only -- not app.openapi().)

Run from repo root:
  python scripts/verify_nmvp2_repo.py

Exit code: 0 if all checks pass, 1 otherwise.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# Running `python scripts/verify_nmvp2_repo.py` puts `scripts/` on sys.path, not repo root.
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
FAILURES: list[str] = []
WARNINGS: list[str] = []


def fail(msg: str) -> None:
    FAILURES.append(msg)
    print(f"FAIL: {msg}")


def ok(msg: str) -> None:
    print(f"OK:   {msg}")


def warn(msg: str) -> None:
    WARNINGS.append(msg)
    print(f"WARN: {msg}")


def must_exist(rel: str, desc: str) -> None:
    p = ROOT / rel
    if p.is_file() or p.is_dir():
        ok(f"[A] {desc}: {rel}")
    else:
        fail(f"[A] Missing {desc}: {rel}")


def read_text(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8", errors="replace")


# --- A. Repo completeness ---


def check_a() -> None:
    print("\n=== A. Repo completeness ===")
    must_exist("notebooks", "notebooks/")
    must_exist("notebooks/01_isot_fake_news_mlflow.ipynb", "ISOT notebook")
    must_exist("app/agents/verdict_engine.py", "verdict engine")
    must_exist("app/api/routes/feedback.py", "feedback route")
    must_exist("app/main.py", "main (feedback mount)")
    must_exist("dashboard/pages/5_Analytics_Trends.py", "analytics page")
    must_exist("tests/test_verdict_engine.py", "verdict tests")
    must_exist("tests/test_feedback.py", "feedback tests")
    must_exist("data/README.md", "data README")
    must_exist("docs/DATASET_SETUP.md", "dataset instructions")


# --- B. Functional consistency ---


def check_b() -> None:
    print("\n=== B. Functional consistency ===")
    ve = read_text("app/agents/verdict_engine.py")
    orch = read_text("app/agents/orchestrator.py")
    readme = read_text("README.md")
    fb = read_text("app/api/routes/feedback.py")
    models = read_text("app/db/models.py")
    home = read_text("dashboard/Home.py")

    # Weights in VerdictEngine
    if "0.3" in ve and "0.4" in ve and "0.3" in ve and "VerdictEngine" in ve:
        ok("[B] verdict_engine.py declares 0.3/0.4/0.3 weights")
    else:
        fail("[B] verdict_engine.py missing expected weight constants")

    if "verdict_engine.evaluate" in orch or "self.verdict_engine.evaluate" in orch:
        ok("[B] orchestrator calls VerdictEngine.evaluate")
    else:
        fail("[B] orchestrator does not call VerdictEngine.evaluate")

    if ("Final_Score" in readme) or ("0.3" in readme and "RoBERTa" in readme):
        ok("[B] README mentions NMVP2 formula / weights")
    else:
        fail("[B] README missing formula / weights section")

    if "/api/v1/feedback" in read_text("app/main.py"):
        ok("[B] main.py mounts /api/v1/feedback")
    else:
        fail("[B] feedback not mounted at /api/v1/feedback")

    for field in ("verdict", "credibility_score", "fake_score"):
        if field in home:
            ok(f"[B] Home.py references {field}")
            break
    else:
        fail("[B] Home.py may not display API-aligned fields")

    if "UncertaintyPool" in models and ("UserFeedback" in models or "user_feedback" in models.lower()):
        ok("[B] DB models include self-learning related tables")
    else:
        fail("[B] Missing UncertaintyPool / feedback models")

    if "ClaimCheck" in fb or "submit_feedback" in fb:
        ok("[B] feedback route module present")
    else:
        fail("[B] feedback route content unexpected")

    slp = ROOT / "scripts/self_learning_pipeline.py"
    if slp.is_file() and slp.read_text(encoding="utf-8")[:200]:
        ok("[B] scripts/self_learning_pipeline.py exists")
    else:
        fail("[B] self_learning_pipeline.py missing or empty")


# --- C. Migration completeness (git remotes optional) ---


def check_c() -> None:
    print("\n=== C. Migration completeness (git) ===")
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=10,
        )
        if out.returncode != 0:
            fail("[C] Not a git repo - skip remote comparison")
            return
    except (OSError, subprocess.TimeoutExpired) as e:
        fail(f"[C] git check failed: {e}")
        return

    for remote, name in [("legacy", "TruthLens-UA"), ("nmvp1", "truthlens-ua-analytics")]:
        r = subprocess.run(
            ["git", "ls-remote", "--heads", remote, "main"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=30,
        )
        if r.returncode == 0 and r.stdout.strip():
            ok(f"[C] Remote `{remote}` reachable ({name})")
        else:
            ok(f"[C] Remote `{remote}` missing or unreachable - add: git remote add {remote} <url>")

    # Expected migrated notebook names (documentary check)
    for nb in ("01_isot_fake_news_mlflow.ipynb", "03_ua_nlp_training.ipynb"):
        p = ROOT / "notebooks" / nb
        if p.is_file():
            ok(f"[C] Migrated notebook present: notebooks/{nb}")
        else:
            fail(f"[C] Expected notebook missing: notebooks/{nb}")


# --- E. API JSON (CheckResponse) <-> Home.py ---


def _check_response_field_names() -> set[str]:
    """Import CheckResponse from repo (requires deps from requirements.txt)."""
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "check_schema",
        ROOT / "app" / "schemas" / "check.py",
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("Cannot load app/schemas/check.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    cr = mod.CheckResponse
    return set(cr.model_fields.keys())


def _home_result_keys(home_py: str) -> set[str]:
    keys: set[str] = set()
    for m in re.finditer(r"""result\[(['"])(?P<k>\w+)\1\]""", home_py):
        keys.add(m.group("k"))
    for m in re.finditer(r"""result\.get\((['"])(?P<k>\w+)\1""", home_py):
        keys.add(m.group("k"))
    return keys


def check_e_api_dashboard() -> None:
    print("\n=== E. CheckResponse <-> dashboard/Home.py ===")
    try:
        api_fields = _check_response_field_names()
    except Exception as e:
        fail(f"[E] Cannot import CheckResponse: {e}")
        return

    home_py = read_text("dashboard/Home.py")
    home_keys = _home_result_keys(home_py)

    for fname in sorted(api_fields):
        if fname in home_keys:
            ok(f"[E] API field `{fname}` referenced on Home (result[...] / .get)")
        else:
            warn(f"[E] API field `{fname}` not referenced on Home - verify UI/export")

    # Built-in local dict must return same keys (analyze_text_locally)
    if "article_id" in home_keys and "source_domain" in home_keys:
        ok("[E] Home uses extended metadata keys (article_id, source_domain, ...)")
    else:
        warn("[E] Home may lack metadata keys for API parity")


# --- H. Pydantic JSON Schema vs CheckResponse.model_fields (no app.openapi()) ---


def _check_response_json_schema_property_names() -> set[str]:
    """Keys from CheckResponse.model_json_schema() -- no FastAPI / OpenAPI build."""
    from app.schemas.check import CheckResponse

    schema = CheckResponse.model_json_schema()
    props = schema.get("properties")
    if not isinstance(props, dict):
        raise KeyError("CheckResponse.model_json_schema() missing properties")
    return set(props.keys())


def check_h_jsonschema_vs_model() -> None:
    print("\n=== H. CheckResponse JSON Schema <-> model_fields (no OpenAPI) ===")
    try:
        pydantic_fields = _check_response_field_names()
    except Exception as e:
        fail(f"[H] Cannot load CheckResponse: {e}")
        return

    try:
        schema_fields = _check_response_json_schema_property_names()
    except Exception as e:
        fail(f"[H] Cannot build model_json_schema: {e}")
        return

    if schema_fields == pydantic_fields:
        ok("[H] model_json_schema properties match CheckResponse.model_fields")
        return

    only_pyd = sorted(pydantic_fields - schema_fields)
    only_s = sorted(schema_fields - pydantic_fields)
    if only_pyd:
        fail(f"[H] JSON Schema missing vs model: {only_pyd}")
    if only_s:
        fail(f"[H] JSON Schema extra vs model: {only_s}")


# --- F. README content (smoke sections) ---


def check_f_readme_smak() -> None:
    print("\n=== F. README content (required phrases) ===")
    readme = read_text("README.md")
    required = [
        ("NMVP2", "NMVP2 label"),
        ("truthlens-ua-analytics-v2", "v2 repo URL or name"),
        ("Verdict", "verdict / formula section"),
        ("docker-compose", "Docker or compose"),
        ("pytest", "testing"),
    ]
    for needle, desc in required:
        if needle.lower() in readme.lower():
            ok(f"[F] README contains {desc}: `{needle}`")
        else:
            fail(f"[F] README missing {desc} (expected substring: {needle})")


# --- G. Visual / manual dashboard (documentation only) ---


def check_g_visual_doc() -> None:
    print("\n=== G. Visual regression (doc present) ===")
    p = ROOT / "docs" / "DASHBOARD_VISUAL_SMOKE.md"
    if p.is_file():
        ok("[G] docs/DASHBOARD_VISUAL_SMOKE.md exists")
    else:
        warn("[G] Add docs/DASHBOARD_VISUAL_SMOKE.md for manual UI pass")


# --- D. PR readiness ---


def check_d() -> None:
    print("\n=== D. PR readiness ===")
    must_exist("docs/CHANGELOG_NMVP2.md", "changelog")
    must_exist("docs/PR_SUMMARY_NMVP2.md", "PR summary")
    readme = read_text("README.md")
    if "pytest" in readme.lower() or "tests/" in readme:
        ok("[D] README mentions testing")
    else:
        fail("[D] README should mention pytest / tests")

    # Branch: informational only
    br = subprocess.run(
        ["git", "branch", "--show-current"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=10,
    )
    if br.returncode == 0 and br.stdout.strip():
        ok(f"[D] Current git branch: {br.stdout.strip()}")
    else:
        ok("[D] Branch: (could not detect - not fatal)")


def main() -> int:
    print("NMVP2 verify - root:", ROOT)
    check_a()
    check_b()
    check_c()
    check_d()
    check_e_api_dashboard()
    check_h_jsonschema_vs_model()
    check_f_readme_smak()
    check_g_visual_doc()

    print("\n=== Summary ===")
    if WARNINGS:
        print(f"Warnings: {len(WARNINGS)}")
        for w in WARNINGS:
            print(" -", w)
    if FAILURES:
        print(f"Failed {len(FAILURES)} check(s).")
        for f in FAILURES:
            print(" -", f)
        return 1
    print("All checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
