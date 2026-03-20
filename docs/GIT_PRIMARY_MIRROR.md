# Git: primary (GitHub) + mirror (GitLab)

## Політика

| Роль | Remote | URL |
|------|--------|-----|
| **Primary** | `origin` | https://github.com/102012dl/truthlens-ua-analytics-v2 |
| **Mirror** | `gitlab` | https://gitlab.com/102012dl/truthlens-ua-analytics-v2 |

Усі зміни спочатку потрапляють на **GitHub** (`git push origin …`). **GitLab** оновлюється другим кроком тим самим ref’ом (`git push gitlab …`), або через вбудоване **Repository mirroring** у GitLab (push mirror на GitHub) — тоді достатньо одного `git push origin`.

---

## Поточний стан гілок (NMVP2)

- **`main` на GitHub** — канонічна повна кодова база NMVP2.
- **`nmvp2/development`** — робоча гілка; має збігатися з `main` після релізних злиттів.
- **`.gitlab-ci.yml`** — у тому ж репозиторії, що й код (SAST через шаблон GitLab), щоб CI не жив у «сиротському» коміті лише на GitLab.

Якщо **`gitlab/main`** колись був окремим коренем (наприклад, лише CI), його треба **вирівняти** під GitHub (див. розділ нижче).

---

## Перевірка перед push

У корені репозиторію:

```powershell
cd path\to\truthlens-ua-analytics-v2
git status
git log --oneline -5 main
python -m pytest tests/ -q
```

Очікування: робоче дерево чисте (`git status`), останній коміт на `main` — NMVP2, **pytest** проходить.

---

## Push primary (GitHub), потім mirror (GitLab)

Переконайтеся, що ви на гілці `main` і вона містить потрібні коміти:

```powershell
git checkout main
git pull origin main
```

Якщо віддалений `origin/main` — лише «Initial commit», а локальна `main` повна (інша історія), безпечне оновлення:

```powershell
git push origin main --force-with-lease
```

Якщо історія вже спільна і звичайний push достатній:

```powershell
git push origin main
```

Дзеркало на GitLab (той самий SHA), якщо **fast-forward** можливий:

```powershell
git push gitlab main
```

Якщо GitLab відхиляє push (`protected branch`, `non-fast-forward`), виконайте **один** з варіантів (потрібні права Owner/Maintainer у [truthlens-ua-analytics-v2 на GitLab](https://gitlab.com/102012dl/truthlens-ua-analytics-v2)):

- **A.** Тимчасово зняти захист з `main` → `git push gitlab main --force-with-lease` → знову увімкнути protection.  
- **B.** **Settings → Repository → Mirroring repositories** — Pull mirror з GitHub (`https://github.com/102012dl/truthlens-ua-analytics-v2.git`), щоб `main` оновлювався автоматично.  
- **C.** Видалити гілку `main` на GitLab (якщо дозволено) і створити заново з `origin/main`.

Синхронізація гілки розробки (за потреби):

```powershell
git push origin nmvp2/development
git push gitlab nmvp2/development
```

---

## Перевірка: однаковий SHA на `main`

Після вирівнювання:

```powershell
git fetch origin
git fetch gitlab
git rev-parse origin/main gitlab/main
```

Обидва рядки мають показати **однаковий** commit hash.

---

## Альтернатива: лише один `push` (mirror з GitLab на GitHub)

У GitLab: **Settings → Repository → Mirroring repositories** — додати mirror на `https://github.com/102012dl/truthlens-ua-analytics-v2.git` з **Push** після змін на GitLab. Тоді primary фактично GitLab; для цього репо зручніше лишити **GitHub primary**, як у таблиці вище.

---

## Теги релізу (опційно)

```powershell
git tag -a nmvp2-v1.0.0 -m "NMVP2 default main + docs"
git push origin nmvp2-v1.0.0
git push gitlab nmvp2-v1.0.0
```
