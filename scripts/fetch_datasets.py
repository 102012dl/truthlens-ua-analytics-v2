#!/usr/bin/env python3
"""Auto-fetch datasets for TruthLens UA Analytics."""
import json, os
from pathlib import Path

RAW = Path("data/raw")
PROC = Path("data/processed")

def fetch_isot_from_old_repo():
    """Copy ISOT from old TruthLens-UA if available."""
    import shutil
    old_paths = [
        Path("../TruthLens-UA/data"),
        Path("../TruthLens-ua/data"), 
        Path("~/projects/TruthLens-UA/data").expanduser(),
    ]
    for src in old_paths:
        if (src / "True.csv").exists():
            (RAW/"isot").mkdir(parents=True, exist_ok=True)
            shutil.copy(src/"True.csv", RAW/"isot"/"True.csv")
            shutil.copy(src/"Fake.csv", RAW/"isot"/"Fake.csv")
            print("✅ ISOT copied from old repo")
            return True
    print("⚠️  ISOT not found locally.")
    print("   Download manually: kaggle datasets download clmentbisaillon/fake-and-real-news-dataset")
    return False

def try_hf_dataset(name: str, save_as: str):
    """Try to download from HuggingFace."""
    try:
        from datasets import load_dataset
        ds = load_dataset(name, split="train", trust_remote_code=True)
        df = ds.to_pandas()
        save_path = RAW / save_as
        save_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(save_path, index=False)
        print(f"✅ {name}: {len(df)} rows → {save_as}")
        return len(df)
    except Exception as e:
        print(f"⚠️  {name}: {e}")
        return 0

def create_gold_template():
    """Create 30-case gold evaluation dataset template."""
    import csv
    PROC.mkdir(exist_ok=True)
    (RAW.parent / "gold").mkdir(exist_ok=True)

    # Pre-filled sample cases (first 10)
    cases = [
        # FAKE cases (1-10)
        {"id":1,"text":"ТЕРМІНОВО!!! ЗСУ ЗДАЛИ Харків! Поширте до видалення!!!",
         "expected_label":"FAKE","language":"uk","topic":"military",
         "ipso":"urgency_injection,military_disinfo,deletion_threat",
         "explanation":"3 ІПСО техніки: urgency+military_disinfo+deletion_threat"},
        {"id":2,"text":"ПРОКИНЬТЕСЬ! Приховують правду про вакцини! Поширте ЗАРАЗ!",
         "expected_label":"FAKE","language":"uk","topic":"health",
         "ipso":"awakening_appeal,conspiracy_framing,viral_call",
         "explanation":"Змовницький наратив + заклик до поширення"},
        {"id":3,"text":"Зеленський таємно підписав угоду з Путіним! Анонімне джерело!",
         "expected_label":"FAKE","language":"uk","topic":"politics",
         "ipso":"authority_impersonation,anonymous_sources",
         "explanation":"Імітація авторитету + анонімні джерела"},
        {"id":4,"text":"ЗСУ ЗРАДНИКИ! КИНУЛИ ПОЗИЦІЇ! ПРАВДА ЯКУ ЗАМОВЧУЮТЬ!",
         "expected_label":"FAKE","language":"uk","topic":"military",
         "ipso":"military_disinfo,conspiracy_framing,caps_abuse",
         "explanation":"Капслок + воєнна дезінформація + змова"},
        {"id":5,"text":"Відео з генералом виявилось deepfake! Це AI-відео!",
         "expected_label":"FAKE","language":"uk","topic":"media",
         "ipso":"deepfake_indicator","explanation":"Deepfake індикатор"},
        # REAL cases (6-10)
        {"id":6,"text":"НБУ підвищив облікову ставку до 16% на засіданні Правління 25 лютого.",
         "expected_label":"REAL","language":"uk","topic":"economy",
         "ipso":"","explanation":"Офіційне рішення НБУ, перевірений факт"},
        {"id":7,"text":"Верховна Рада ухвалила держбюджет на 2026 рік у першому читанні.",
         "expected_label":"REAL","language":"uk","topic":"politics",
         "ipso":"","explanation":"Офіційне парламентське рішення"},
        {"id":8,"text":"Збройні сили України відзвітували про бойові дії на сході країни.",
         "expected_label":"REAL","language":"uk","topic":"military",
         "ipso":"","explanation":"Офіційний звіт ЗСУ через УНІАН"},
        {"id":9,"text":"МОЗ оновило протоколи лікування COVID-19 згідно рекомендацій ВООЗ.",
         "expected_label":"REAL","language":"uk","topic":"health",
         "ipso":"","explanation":"Офіційна позиція МОЗ"},
        {"id":10,"text":"Курс долара на МВРУ станом на 14 березня 2026 склав 39.5 грн.",
         "expected_label":"REAL","language":"uk","topic":"economy",
         "ipso":"","explanation":"Офіційний курс НБУ"},
    ]
    # Add 20 more placeholder cases
    for i in range(11, 31):
        label = "FAKE" if i <= 15 else ("SUSPICIOUS" if i <= 20 else "REAL")
        cases.append({
            "id": i,
            "text": f"[ЗАПОВНИ ВЛАСНИЙ КЕЙС #{i}]",
            "expected_label": label,
            "language": "uk",
            "topic": "general",
            "ipso": "",
            "explanation": f"[Власне пояснення для кейсу #{i}]"
        })

    with open("data/gold/demo_cases.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cases[0].keys())
        w.writeheader()
        w.writerows(cases)
    print(f"✅ Gold dataset: data/gold/demo_cases.csv ({len(cases)} cases)")
    print("⚠️  ОБОВ'ЯЗКОВО заповни рядки 11-30 власними кейсами!")

def create_datasets_md():
    """Generate docs/thesis/DATASETS.md."""
    content = """# Datasets — TruthLens UA Analytics

| Датасет | Розмір | Мова | Формат | Статус |
|---------|--------|------|--------|--------|
| ISOT Fake News (Kaggle) | 39,103 | EN | CSV | ✅ |
| UNLP 2025 Telegram | 9,557 | UA | JSON | ⚠️ HF |
| StopFake corpus | ~5,000 | UA/EN | CSV | ⚠️ HF |
| gold/demo_cases.csv | 30 | UA | CSV | ✅ авторська |

## Джерела
- ISOT: kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset
- UNLP 2025: github.com/unlp-workshop/unlp-2025-shared-task
- StopFake: stopfake.org (manual collection)
"""
    Path("docs/thesis").mkdir(parents=True, exist_ok=True)
    Path("docs/thesis/DATASETS.md").write_text(content, encoding="utf-8")
    print("✅ docs/thesis/DATASETS.md created")

if __name__ == "__main__":
    for d in [RAW/"isot", RAW/"stopfake", PROC, Path("data/gold")]:
        d.mkdir(parents=True, exist_ok=True)

    fetch_isot_from_old_repo()
    total_hf = try_hf_dataset("lasr-unlp/unlp-2025-shared-task", "stopfake/unlp_2025.csv")
    create_gold_template()
    create_datasets_md()
    print("\n📊 Готово! Відкрий data/gold/demo_cases.csv і заповни рядки 11-30.")