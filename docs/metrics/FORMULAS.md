# Source Credibility Formula — TruthLens UA Analytics

**Автор**: 102012dl | Neoversity MSCS DS&DA 2026
**Метод**: Багатокомпонентна зважена формула оцінки медіаджерел

## Формула

```
credibility(source) =
    0.35 × evidence_overlap
  + 0.25 × (1 − contradiction_rate)
  + 0.20 × source_consistency
  + 0.20 × domain_trust_prior
```

## Компоненти

| Компонент | Вага | Визначення | Діапазон |
|-----------|------|-----------|---------|
| evidence_overlap | 35% | Частка статей з взаємними підтвердженнями | [0, 1] |
| contradiction_inverse | 25% | 1 − частка суперечливих матеріалів | [0, 1] |
| source_consistency | 20% | Послідовність публікаційних патернів | [0, 1] |
| domain_trust_prior | 20% | Апріорна довіра з реєстру 500+ UA джерел | [0, 1] |

## Рівні достовірності
- HIGH: score ≥ 0.75
- MEDIUM: 0.45 ≤ score < 0.75
- LOW: score < 0.45
