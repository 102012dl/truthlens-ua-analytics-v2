# PDF → PowerPoint (TruthLens)

## Готові файли

- **`TRUTHLENS-UA-ANALYTICS-from-pdf.pptx`** — конвертація з PDF, формат слайда 16:9 за замовчуванням.
- **`TRUTHLENS-UA-ANALYTICS-diploma-template.pptx`** — та сама конвертація, але **розміри слайда** взяті з шаблону дипломної роботи  
  (`Шаблон презентації для дипломної роботи - Copy.pptx` у папці проєкту).

Обидва файли: `docs/presentation/`. На кожному слайді — зображення сторінки PDF (вигляд як у Canva/PDF).

## Як повторити / оновити

З кореня репозиторія (потрібні пакети: `pymupdf`, `python-pptx`):

```bash
pip install pymupdf python-pptx
python scripts/pdf_to_pptx.py "C:\path\to\TRUTHLENS-UA-ANALYTICS.pdf" -o docs/presentation/TRUTHLENS-UA-ANALYTICS-from-pdf.pptx
```

З **шаблоном дипломної роботи** (розміри слайда як у вашому `.pptx`):

```bash
python scripts/pdf_to_pptx.py "C:\path\to\report.pdf" ^
  -t "C:\Users\home2\Downloads\ACS Capstone Project 2058 130226\Шаблон презентації для дипломної роботи - Copy.pptx" ^
  -o docs/presentation/TRUTHLENS-UA-ANALYTICS-diploma-template.pptx
```

Параметри:

| Параметр | Опис |
|----------|------|
| `--zoom 2` | Чіткість (за замовчуванням 2); більше — важчий файл |
| `-t шаблон.pptx` | Беруться **лише ширина та висота** слайда з шаблону (16:9 Neoversity тощо). Тло майстра з шаблону на кожен слайд **не** накладається автоматично |

## Шаблон `.pptx` від університету

Фактичний шаблон дипломної роботи:  
`ACS Capstone Project 2058 130226\Шаблон презентації для дипломної роботи - Copy.pptx` — передавайте його як `-t` (див. приклад вище).

Інший офіційний файл (Neoversity тощо):

1. Збережіть у проєкт, наприклад `docs/presentation/template-neoversity.pptx`.
2. Запустіть:

```bash
python scripts/pdf_to_pptx.py "your.pdf" -t docs/presentation/template-neoversity.pptx -o docs/presentation/out.pptx
```

Щоб **додати фірмове тло** під зображення з PDF, у PowerPoint: **View → Slide Master** — вставте тло на майстер-слайд, потім на звичайних слайдах зменште картинку з PDF (поля) або накладіть прозорість — це вже ручне доопрацювання після конвертації.

## Редагований текст

Цей спосіб зберігає **піксельну** копію слайдів. Щоб мати окремі текстові поля, потрібен ручний перенос або інший пайплайн (OCR / експорт з Canva в PPTX напряму, якщо доступно).
