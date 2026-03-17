# Datasets — TruthLens UA Analytics

All datasets used in the project: name, source, size, format, license, usage.

| Name | URL / Source | Size | Format | License | Usage |
|------|--------------|------|--------|---------|--------|
| **demo_cases** | `data/gold/demo_cases.csv` (generated) | 31 rows | CSV | Project | Gold set: 15 REAL + 10 FAKE + 6 SUSPICIOUS for evaluation |
| **domain_trust_scores** | `data/processed/domain_trust_scores.csv` (generated) | 50+ domains | CSV | Project | Source credibility: domain, tier, score, source_type, notes |
| **ISOT Fake/Real News** | Kaggle / HuggingFace (optional) | ~40k | CSV | CC BY-NC 4.0 | Pre-training; fetch via `scripts/fetch_datasets.py` |
| **UNLP 2025 shared task** | HuggingFace (if available) | — | Dataset | Task license | IPSO patterns; optional |

## Gold set (demo_cases.csv)

- **Columns:** id, text, expected_label, language, topic, ipso, explanation  
- **Generation:** `python scripts/create_datasets.py`  
- **Verification:** `wc -l data/gold/demo_cases.csv` → expect 32 (header + 31)

## Domain trust (domain_trust_scores.csv)

- **Columns:** domain, tier, credibility_score, source_type, notes  
- **Sources:** Public registries; trusted/fact-checker lists (e.g. detector.media); regional/media; placeholders for untrusted (euvsdisinfo.eu public lists).  
- **Generation:** same script as above.

## Audit summary

- Gold cases: 31 (15 REAL, 10 FAKE, 6 SUSPICIOUS)  
- Domains: 50+ Ukrainian domains (trusted, factchecker, regional, untrusted placeholders)  
- Language: Ukrainian (uk) for gold set.
