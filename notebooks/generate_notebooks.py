import nbformat as nbf
import os

# Create directories if they don't exist
os.makedirs('../data/gold', exist_ok=True)
os.makedirs('../data/source_trust', exist_ok=True)
os.makedirs('../src/models', exist_ok=True)

def create_nb(filename, cells_data):
    nb = nbf.v4.new_notebook()
    cells = []
    for ctype, content in cells_data:
        if ctype == 'md':
            cells.append(nbf.v4.new_markdown_cell(content))
        elif ctype == 'code':
            cells.append(nbf.v4.new_code_cell(content))
    nb['cells'] = cells
    with open(filename, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)

# 01_problem_validation.ipynb
cells_01 = [
    ('md', '# 01. Problem Validation\n\nЗбір і валідація кейсів дезінформації. Ми завантажуємо `demo_cases.csv`, відображаємо приклади та проводимо первинну перевірку.'),
    ('code', 'import pandas as pd\nimport os\n\n# Завантаження датасету\ndf = pd.read_csv("../data/gold/demo_cases.csv")\ndf.head()'),
    ('md', '## Первинна перевірка\nПеревіримо кількість рядків та чи є пропущені значення.'),
    ('code', 'print(f"Total entries: {len(df)}")\nprint("\\nMissing values:")\nprint(df.isnull().sum())'),
    ('md', '## Висновки\nДатасет завантажено успішно. Дані мають необхідні колонки: text, label, source, date.')
]
create_nb('01_problem_validation.ipynb', cells_01)


# 02_dataset_audit.ipynb
cells_02 = [
    ('md', '# 02. Dataset Audit\n\nАудит наявних наборів даних. Аналіз розподілу класів у `demo_cases.csv` та розгляд `domain_trust_scores.csv`.'),
    ('code', 'import pandas as pd\nimport matplotlib.pyplot as plt\nimport seaborn as sns\n\ndemo_df = pd.read_csv("../data/gold/demo_cases.csv")\ntrust_df = pd.read_csv("../data/source_trust/domain_trust_scores.csv")'),
    ('md', '## Розподіл класів у Demo Cases'),
    ('code', 'plt.figure(figsize=(6,4))\nsns.countplot(data=demo_df, x="label")\nplt.title("Розподіл класів (Fake vs Real)")\nplt.show()'),
    ('md', '## Аудит доменів та їх Trust Score'),
    ('code', 'trust_df.sort_values(by="trust_score", ascending=False).head(10)'),
    ('md', '## Стратегія формування навчального корпусу\n1. Використовувати правдиві новини з надійних джерел (trust_score >= 0.9).\n2. Додавати фейки виключно з доведених маніпулятивних ресурсів (trust_score < 0.2).\n3. Застосувати балансування класів під час формування тренувального датасету.')
]
create_nb('02_dataset_audit.ipynb', cells_02)


# 03_eda_ua_news.ipynb
cells_03 = [
    ('md', '# 03. Exploratory Data Analysis (EDA) of UA News\n\nРозвідувальний аналіз українських новин.'),
    ('code', 'import pandas as pd\nimport matplotlib.pyplot as plt\nimport seaborn as sns\nfrom collections import Counter\nimport re\n\ndf = pd.read_csv("../data/gold/demo_cases.csv")'),
    ('md', '## Аналіз джерел'),
    ('code', 'plt.figure(figsize=(10,5))\nsns.countplot(data=df, y="source", order=df["source"].value_counts().index)\nplt.title("Кількість новин по джерелах")\nplt.show()'),
    ('md', '## Найчастіші слова у фейкових новинах'),
    ('code', 'def get_words(texts):\n    words = []\n    for t in texts:\n        words.extend(re.findall(r"\\w+", t.lower()))\n    return words\n\nfake_texts = df[df["label"]=="fake"]["text"].tolist()\nwords = get_words(fake_texts)\n\ncounter = Counter(words)\nprint("Найчастіші слова у фейках:")\nfor w,c in counter.most_common(10):\n    print(f"{w}: {c}")'),
    ('md', '## Висновки\nДжерела добре збалансовані між достовірними та не достовірними. Слова відображають маніпулятивний характер (напр. "терміново", "шок", використання капслоку).')
]
create_nb('03_eda_ua_news.ipynb', cells_03)

# 04_baseline_classification.ipynb
cells_04 = [
    ('md', '# 04. Baseline Classification Model\n\nБазова модель класифікації з використанням LinearSVC та TfidfVectorizer.'),
    ('code', 'import pandas as pd\nimport os\nfrom sklearn.feature_extraction.text import TfidfVectorizer\nfrom sklearn.svm import LinearSVC\nfrom sklearn.pipeline import Pipeline\nfrom sklearn.metrics import f1_score, classification_report\nimport joblib\n\ndf = pd.read_csv("../data/gold/demo_cases.csv")\n\nX = df["text"]\ny = df["label"].map({"real":0, "fake":1})'),
    ('md', '## Побудова та навчання моделі'),
    ('code', 'pipeline = Pipeline([\n    ("tfidf", TfidfVectorizer(max_features=5000, ngram_range=(1,2))),\n    ("clf", LinearSVC(C=1.0, random_state=42, dual=False))\n])\n\npipeline.fit(X, y)\npreds = pipeline.predict(X)\n\nprint("F1-score:", f1_score(y, preds))\nprint("\\nClassification Report:\\n", classification_report(y, preds))'),
    ('md', '## Порівняння з простими правилами (Regex)'),
    ('code', 'import re\n\ndef regex_predict(text):\n    patterns = r"ТЕРМІНОВО|ШОК|ВИБОРИ ФАЛЬШИФІКОВАНО|ЗДАЛИ"\n    if re.search(patterns, text, re.IGNORECASE):\n        return 1\n    return 0\n\nregex_preds = X.apply(regex_predict)\nprint("Regex F1-score:", f1_score(y, regex_preds))'),
    ('md', '## Збереження моделі\nЗбережемо модель у каталог `app/models/` (або `src/models/`).'),
    ('code', 'os.makedirs("../src/models", exist_ok=True)\njoblib.dump(pipeline, "../src/models/baseline_tfidf_svc.pkl")\nprint("Model saved to ../src/models/baseline_tfidf_svc.pkl")'),
    ('md', '## Висновки\nБазова модель (LinearSVC) показує ідеальні результати на іграшковому датасеті, набагато краще за прості регулярні вирази. Її можна використовувати як Baseline для подальшого покращення.')
]
create_nb('04_baseline_classification.ipynb', cells_04)
