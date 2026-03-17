#!/usr/bin/env python3
"""TruthLens UA Analytics — Full Smoke Test"""
import httpx, sys, time, json

BASE = "http://localhost:8000"
DASH = "http://localhost:8501"
results = []

def chk(name, url, method="GET", data=None, key=None, validator=None):
    s = time.perf_counter()
    try:
        r = httpx.get(url,timeout=20) if method=="GET" else \
            httpx.post(url,json=data,timeout=30)
        ms = round((time.perf_counter()-s)*1000)
        d = r.json() if "application/json" in r.headers.get("content-type","") else {}
        ok = r.status_code == 200
        if key: ok = ok and key in d
        if validator and ok: ok = validator(d)
        results.append(("✅" if ok else "❌", name, ms,
            f"{key}={json.dumps(d.get(key,'?'))[:50]}" if key else f"HTTP {r.status_code}"))
    except Exception as e:
        results.append(("❌", name, 0, str(e)[:60]))

print("\n" + "═"*65)
print("  TruthLens UA Analytics — SMOKE TEST")
print("═"*65 + "\n")

chk("GET /",             f"{BASE}/",        key="service")
chk("GET /health",       f"{BASE}/health",  key="status",
    validator=lambda d: d.get("status") in ("ok", "degraded"))
chk("POST /check FAKE",  f"{BASE}/check",   "POST",
    {"text":"ТЕРМІНОВО!!! ЗСУ ЗДАЛИ Харків! Поширте!!!"},
    "verdict", lambda d: d["verdict"]=="FAKE")
chk("POST /check REAL",  f"{BASE}/check",   "POST",
    {"text":"НБУ підвищив ставку до 16%."},
    "credibility_score", lambda d: float(d["credibility_score"])>50)
chk("ІПСО override",     f"{BASE}/check",   "POST",
    {"text":"ТЕРМІНОВО!!! Прокиньтесь! Поширте до видалення!!!"},
    "ipso_techniques", lambda d: len(d["ipso_techniques"])>=2)
chk("URL analyze",       f"{BASE}/check",   "POST",
    {"url":"https://www.pravda.com.ua"}, "verdict")
chk("Dashboard up",      DASH)

print(f"{'':5} {'Check':<35} {'ms':>5}  Result")
print("─"*65)
for e,n,ms,d in results:
    print(f"{e:5} {n:<35} {ms:>4}ms  {d}")
p = sum(1 for r in results if r[0]=="✅")
t = len(results)
print(f"\n{'═'*65}")

# Dashboard is optional in API-only runs
api_core_passed = sum(1 for r in results if r[0]=="✅" and "Dashboard" not in r[1])
api_core_total = sum(1 for r in results if "Dashboard" not in r[1])

print(f"  RESULT: {p}/{t} total checks passed")
if api_core_passed == api_core_total:
    print("  🎯  NMVP1 READY — Core API & Models працюють!")
    if p < t:
        print("  ℹ️   Деякі опційні сервіси (Dashboard) не запущені.")
    sys.exit(0)
else:
    print(f"  ⚠️   Втрачено критичні з'єднання. {api_core_total - api_core_passed} API check(s) failed")
    sys.exit(1)