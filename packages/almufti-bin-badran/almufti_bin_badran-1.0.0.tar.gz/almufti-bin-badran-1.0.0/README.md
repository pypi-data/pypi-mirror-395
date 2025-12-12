# 🤖 المفتي بن بدران - Almufti Bin Badran

**A Lightweight AI Assistant with Arabic Language Support**

[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/s200077761/almufti-bin-badran)
[![Hugging Face](https://img.shields.io/badge/Hugging%20Face-Spaces-yellow?logo=huggingface)](https://huggingface.co/spaces/s200077761/almufti-bin-badran)
[![PyPI](https://img.shields.io/badge/PyPI-Package-blue?logo=pypi)](https://pypi.org/project/almufti-bin-badran/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)](https://www.python.org/)

---

## 📖 جدول المحتويات | Table of Contents

- [المميزات](#-المميزات--features)
- [المتطلبات](#-المتطلبات--requirements)
- [التثبيت](#-التثبيت--installation)
- [الاستخدام](#-الاستخدام--usage)
- [الأمثلة](#-الأمثلة--examples)
- [البنية](#-البنية--architecture)
- [المساهمة](#-المساهمة--contributing)
- [الترخيص](#-الترخيص--license)
- [التواصل](#-التواصل--contact)

---

## ✨ المميزات | Features

### 🧠 محادثة ذكية | Smart Chat
- **دعم اللغة العربية والإنجليزية** - Full Arabic & English support
- **فهم السياق** - Context awareness across conversations
- **حفظ المحادثات** - Persistent conversation history
- **استرجاع المحادثات** - Retrieve previous conversations
- **تحليل المشاعر** - Sentiment analysis

### 🔍 بحث ذكي | Intelligent Search
- **بحث عام على الإنترنت** - General web search
- **بحث أكاديمي** - Academic search
- **استخراج المحتوى** - Content extraction
- **تلخيص النتائج** - Result summarization
- **معالجة الروابط** - Link processing

### 🧮 حل المسائل | Problem Solving
- **معادلات خطية وتربيعية** - Linear & quadratic equations
- **مسائل هندسية** - Geometric problems
- **حساب النسب المئوية** - Percentage calculations
- **شرح الخطوات** - Step-by-step explanations
- **التحقق من الحلول** - Solution verification

### 📚 معالجة اللغة الطبيعية | NLP
- **كشف اللغة التلقائي** - Automatic language detection
- **استخراج الكلمات المفتاحية** - Keyword extraction
- **استخراج الكيانات** - Named entity recognition
- **حساب التشابه** - Similarity computation
- **تحليل النصوص** - Text analysis

### 🧠 التعلم المستمر | Continuous Learning
- **تسجيل التفاعلات** - Interaction logging
- **تحليل الملاحظات** - Feedback analysis
- **تقارير الأداء** - Performance reports
- **توصيات التحسن** - Improvement suggestions
- **التطور الذاتي** - Self-improvement

### 💾 إدارة البيانات | Data Management
- **قاعدة بيانات SQLite** - SQLite database
- **نسخ احتياطية تلقائية** - Automatic backups
- **حفظ المعرفة** - Knowledge persistence
- **استرجاع سريع** - Fast retrieval
- **تشفير البيانات** - Data encryption

---

## 🔧 المتطلبات | Requirements

### الحد الأدنى للنظام | Minimum System Requirements
- **Python:** 3.8 أو أحدث | Python 3.8+
- **الذاكرة:** 512 MB على الأقل | 512 MB RAM minimum
- **المساحة:** 100 MB على الأقل | 100 MB disk space
- **الإنترنت:** اختياري (للبحث فقط) | Optional (search only)

### المكتبات المطلوبة | Required Libraries
```
requests>=2.28.0
beautifulsoup4>=4.11.0
nltk>=3.8.0
scikit-learn>=1.1.0
gradio>=4.0.0
```

---

## 📥 التثبيت | Installation

### 1. التثبيت من PyPI (الطريقة الموصى بها)
```bash
pip install almufti-bin-badran
```

### 2. التثبيت من المصدر
```bash
# استنساخ المستودع
git clone https://github.com/s200077761/almufti-bin-badran.git
cd almufti-bin-badran

# تثبيت المتطلبات
pip install -r requirements.txt

# تثبيت المشروع
pip install -e .
```

### 3. التثبيت باستخدام Docker
```bash
# بناء الصورة
docker build -t almufti-bin-badran:latest .

# تشغيل الحاوية
docker run -p 7860:7860 almufti-bin-badran:latest
```

### 4. التثبيت على Hugging Face Spaces
```
اذهب إلى: https://huggingface.co/spaces/s200077761/almufti-bin-badran
```

---

## 🚀 الاستخدام | Usage

### استخدام واجهة سطر الأوامر | CLI Usage

```python
from almufti import ChatEngine

# إنشاء محرك المحادثة
chat = ChatEngine()

# محادثة بسيطة
response = chat.chat("السلام عليكم، كيف حالك؟")
print(response)

# مع البحث على الإنترنت
response = chat.chat("ما هي أحدث أخبار التكنولوجيا؟", search=True)
print(response)

# حل مسألة رياضية
response = chat.chat("حل المعادلة: x^2 + 5x + 6 = 0")
print(response)
```

### استخدام واجهة Gradio | Gradio Interface

```bash
python app.py
```

ثم اذهب إلى: `http://localhost:7860`

### استخدام API البرمجية | Python API

```python
from almufti.core import LanguageProcessor, ChatEngine
from almufti.search import WebSearch
from almufti.homework import MathSolver
from almufti.learning import ContinuousLearning
from almufti.database import DatabaseManager

# معالج اللغة
lp = LanguageProcessor()
language = lp.detect_language("مرحبا بك")
keywords = lp.extract_keywords("هذا نص عربي مهم جداً")

# البحث الذكي
search = WebSearch()
results = search.search("Python programming")
summary = search.summarize_results(results)

# حل المسائل الرياضية
solver = MathSolver()
solution = solver.solve_quadratic(1, 5, 6)

# التعلم المستمر
learning = ContinuousLearning()
learning.log_interaction("user_query", "bot_response", "positive")
report = learning.generate_report()

# إدارة البيانات
db = DatabaseManager()
db.save_conversation("user_id", "conversation_text")
history = db.get_conversation_history("user_id")
```

---

## 💡 الأمثلة | Examples

### مثال 1: محادثة بسيطة
```python
from almufti import ChatEngine

chat = ChatEngine()

# محادثة عادية
response = chat.chat("ما هو الذكاء الاصطناعي؟")
print(response)
# Output: الذكاء الاصطناعي هو فرع من فروع علوم الحاسوب...
```

### مثال 2: بحث على الإنترنت
```python
from almufti import ChatEngine

chat = ChatEngine()

# بحث عن معلومات
response = chat.chat("أخبرني عن أحدث تطورات في الذكاء الاصطناعي", search=True)
print(response)
```

### مثال 3: حل مسائل رياضية
```python
from almufti.homework import MathSolver

solver = MathSolver()

# حل معادلة تربيعية
solution = solver.solve_quadratic(1, -5, 6)
print(f"الحل: {solution}")
# Output: الحل: [2, 3]

# حل معادلة خطية
solution = solver.solve_linear(2, 4)
print(f"الحل: {solution}")
# Output: الحل: -2
```

### مثال 4: تحليل النصوص
```python
from almufti.core import LanguageProcessor

lp = LanguageProcessor()

# كشف اللغة
text = "Hello, how are you?"
language = lp.detect_language(text)
print(f"اللغة: {language}")
# Output: اللغة: en

# استخراج الكلمات المفتاحية
text = "الذكاء الاصطناعي والتعلم الآلي هما مستقبل التكنولوجيا"
keywords = lp.extract_keywords(text)
print(f"الكلمات المفتاحية: {keywords}")
```

### مثال 5: التعلم المستمر
```python
from almufti.learning import ContinuousLearning

learning = ContinuousLearning()

# تسجيل تفاعل إيجابي
learning.log_interaction(
    user_query="ما هو Python؟",
    bot_response="Python هي لغة برمجة...",
    feedback="positive"
)

# الحصول على تقرير الأداء
report = learning.generate_report()
print(report)
```

---

## 🏗️ البنية | Architecture

### هيكل المشروع
```
almufti-bin-badran/
├── almufti/                    # المكتبة الرئيسية
│   ├── __init__.py
│   ├── cli.py                 # واجهة سطر الأوامر
│   ├── core/                  # المكونات الأساسية
│   │   ├── chat_engine.py     # محرك المحادثة
│   │   └── language_processor.py  # معالج اللغة
│   ├── search/                # البحث الذكي
│   │   └── web_search.py      # البحث على الإنترنت
│   ├── homework/              # حل الواجبات
│   │   └── math_solver.py     # حل المسائل الرياضية
│   ├── learning/              # التعلم المستمر
│   │   └── continuous_learning.py
│   └── database/              # إدارة البيانات
│       └── db_manager.py      # مدير قاعدة البيانات
├── config/                    # الإعدادات
│   └── settings.yaml
├── data/                      # البيانات
│   ├── conversations/
│   ├── knowledge/
│   └── models/
├── examples/                  # الأمثلة
│   └── basic_usage.py
├── tests/                     # الاختبارات
│   └── test_basic.py
├── app.py                     # تطبيق Gradio
├── requirements.txt           # المكتبات المطلوبة
├── setup.py                   # إعداد الحزمة
├── Dockerfile                 # ملف Docker
├── docker-compose.yml         # Docker Compose
└── README.md                  # هذا الملف
```

### مخطط المكونات
```
┌─────────────────────────────────────────┐
│         User Interface Layer            │
│  (CLI, Gradio, API)                     │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│      Chat Engine (Core Logic)           │
│  - Context Management                   │
│  - Response Generation                  │
└──────────────────┬──────────────────────┘
                   │
        ┌──────────┼──────────┐
        │          │          │
┌───────▼──┐ ┌────▼────┐ ┌──▼──────┐
│ Language │ │  Search │ │ Problem │
│Processor │ │ Engine  │ │ Solver  │
└───────┬──┘ └────┬────┘ └──┬──────┘
        │         │         │
        └─────────┼─────────┘
                  │
        ┌─────────▼────────┐
        │ Database Manager │
        │ (SQLite)         │
        └──────────────────┘
```

---

## 🤝 المساهمة | Contributing

نرحب بمساهماتك! يرجى اتباع الخطوات التالية:

### خطوات المساهمة

1. **استنساخ المستودع**
```bash
git clone https://github.com/s200077761/almufti-bin-badran.git
cd almufti-bin-badran
```

2. **إنشاء فرع جديد**
```bash
git checkout -b feature/your-feature-name
```

3. **إجراء التغييرات**
```bash
# قم بإجراء التغييرات المطلوبة
# تأكد من اتباع معايير الكود
```

4. **اختبار التغييرات**
```bash
python -m pytest tests/
```

5. **إرسال Pull Request**
```bash
git add .
git commit -m "Add your feature description"
git push origin feature/your-feature-name
```

### معايير الكود | Code Standards

- استخدم **PEP 8** لتنسيق الكود
- أضف **docstrings** لكل دالة
- اكتب **unit tests** للميزات الجديدة
- تأكد من أن **جميع الاختبارات تمر**
- أضف **comments** للكود المعقد

### قائمة التحقق | Checklist

- [ ] الكود يتبع معايير PEP 8
- [ ] تمت إضافة docstrings
- [ ] تم كتابة الاختبارات
- [ ] جميع الاختبارات تمر
- [ ] تم تحديث الوثائق
- [ ] تم إضافة أمثلة إن لزم الأمر

---

## 📋 متطلبات التطوير | Development Requirements

```bash
# تثبيت متطلبات التطوير
pip install -r requirements-dev.txt

# التي تتضمن:
# - pytest (للاختبارات)
# - black (لتنسيق الكود)
# - flake8 (للتحقق من الكود)
# - mypy (للتحقق من الأنواع)
```

---

## 🧪 الاختبارات | Testing

### تشغيل الاختبارات
```bash
# تشغيل جميع الاختبارات
pytest

# تشغيل اختبارات محددة
pytest tests/test_basic.py

# مع تقرير التغطية
pytest --cov=almufti tests/
```

### مثال على اختبار
```python
import pytest
from almufti import ChatEngine

def test_chat_response():
    chat = ChatEngine()
    response = chat.chat("مرحبا")
    assert response is not None
    assert isinstance(response, str)
```

---

## 🐛 الإبلاغ عن الأخطاء | Bug Reports

إذا وجدت خطأ، يرجى:

1. **تحقق من أنه لم يتم الإبلاغ عنه بالفعل**
2. **أنشئ issue جديد** مع:
   - وصف واضح للمشكلة
   - خطوات لإعادة إنتاج المشكلة
   - النتيجة المتوقعة والفعلية
   - معلومات النظام (Python version, OS, etc.)

---

## 📚 الوثائق الإضافية | Additional Documentation

- [INSTALLATION.md](INSTALLATION.md) - دليل التثبيت المفصل
- [DOCUMENTATION.md](DOCUMENTATION.md) - التوثيق التقني الشامل
- [CONTRIBUTING.md](CONTRIBUTING.md) - دليل المساهمة
- [CHANGELOG.md](CHANGELOG.md) - سجل التغييرات
- [DEPLOYMENT.md](DEPLOYMENT.md) - دليل النشر

---

## 📄 الترخيص | License

هذا المشروع مرخص تحت رخصة MIT - انظر ملف [LICENSE](LICENSE) للتفاصيل.

```
MIT License

Copyright (c) 2024 Almufti Bin Badran

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## 📞 التواصل | Contact

- **البريد الإلكتروني:** dev@almufti.ai
- **GitHub Issues:** [Report Issues](https://github.com/s200077761/almufti-bin-badran/issues)
- **GitHub Discussions:** [Ask Questions](https://github.com/s200077761/almufti-bin-badran/discussions)
- **Hugging Face:** [Try Online](https://huggingface.co/spaces/s200077761/almufti-bin-badran)

---

## 🙏 شكر خاص | Special Thanks

شكر خاص لـ:
- مجتمع Python العربي
- مجتمع الذكاء الاصطناعي
- جميع المساهمين والداعمين

---

## 📊 الإحصائيات | Statistics

![GitHub Stars](https://img.shields.io/github/stars/s200077761/almufti-bin-badran?style=social)
![GitHub Forks](https://img.shields.io/github/forks/s200077761/almufti-bin-badran?style=social)
![GitHub Issues](https://img.shields.io/github/issues/s200077761/almufti-bin-badran)
![GitHub Pull Requests](https://img.shields.io/github/issues-pr/s200077761/almufti-bin-badran)

---

## 🗺️ خارطة الطريق | Roadmap

### الإصدار 1.1.0 (قريباً)
- [ ] دعم الصوت
- [ ] تحسين سرعة البحث
- [ ] إضافة المزيد من اللغات
- [ ] تحسين واجهة Gradio

### الإصدار 1.2.0
- [ ] دعم الصور
- [ ] نموذج تعلم عميق مخصص
- [ ] API متقدمة
- [ ] تطبيق موبايل

### الإصدار 2.0.0
- [ ] دعم متعدد المستخدمين
- [ ] نظام توصيات متقدم
- [ ] تكامل مع خدمات خارجية
- [ ] لوحة تحكم إدارية

---

## 📝 ملاحظات | Notes

- هذا المشروع قيد التطوير المستمر
- الميزات قد تتغير في الإصدارات المستقبلية
- نرحب بالملاحظات والاقتراحات
- يرجى الإبلاغ عن أي أخطاء

---

## 🎯 الأهداف | Goals

✅ توفير مساعد ذكي خفيف الوزن  
✅ دعم كامل للغة العربية  
✅ سهولة الاستخدام والتثبيت  
✅ وثائق شاملة وسهلة الفهم  
✅ مجتمع نشط وداعم  
✅ تطوير مستمر وتحسينات دورية  

---

<div align="center">

**شكراً لاستخدامك المفتي بن بدران! 🙏**

**Made with ❤️ for the Arabic AI Community**

**آخر تحديث:** 2024-12-04  
**الإصدار:** 1.0.0  
**الحالة:** ✅ مكتمل بنجاح

</div>
