# Datasets — TruthLens UA Analytics

All datasets used in the project: name, source, size, format, license, usage.

| Name | URL / Source | Size | Format | License | Usage |
|------|--------------|------|--------|---------|-------|
| **demo_cases** | `data/gold/demo_cases.csv` (generated) | 31 rows | CSV | Project | Gold set: 15 REAL + 10 FAKE + 6 SUSPICIOUS for evaluation |
| **domain_trust_scores** | `data/processed/domain_trust_scores.csv` (generated) | 50+ domains | CSV | Project | Source credibility: domain, tier, score, source_type, notes |
| **ISOT Fake/Real News** | [Kaggle — fake-and-real-news-dataset](https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset) | ~40k | CSV | CC BY-NC 4.0 | Pre-training baseline (EN); not committed — see `docs/DATASET_SETUP.md` |
| **UNLP 2025 shared task** | HuggingFace `lasr-unlp/unlp-2025-shared-task` (if available) | — | Dataset | Task license | Optional; notebook audit may show `ModuleNotFoundError` if deps missing |

## Локальний аудит (02_dataset_audit)

| Датасет | Розмір | Мова | Формат | Статус |
|---------|--------|------|--------|--------|
| gold/demo_cases.csv | 31 | uk (+1 ru row in audit) | CSV | локально |
| lasr-unlp/unlp-2025-shared-task | 0 (якщо HF недоступний) | uk | HuggingFace | optional |

## Gold set (demo_cases.csv)

- **Columns:** id, text, expected_label, language, topic, ipso, explanation  
- **Generation:** `python generate_datasets.py` (або скрипти з репо, згідно `README`)  
- **Verification:** `wc -l data/gold/demo_cases.csv` → expect 32 (header + 31)

## Domain trust (domain_trust_scores.csv)

- **Columns:** domain, tier, credibility_score, source_type, notes  
- **Sources:** Public registries; trusted/fact-checker lists (e.g. detector.media); regional/media; placeholders for untrusted (euvsdisinfo.eu public lists).  
- **Generation:** same pipeline as gold set where applicable.

## Audit summary

- Gold cases: 31 (15 REAL, 10 FAKE, 6 SUSPICIOUS)  
- Мовний розподіл (з ноутбука аудиту): переважно `uk`, можливий 1 `ru`  
- Domains: 50+ Ukrainian domains (trusted, factchecker, regional, untrusted placeholders)  
- Language: Ukrainian (uk) for gold set.
