# وصال (Wisal)

**أداة سطر أوامر ثنائية اللغة (عربي/إنجليزي) لتحويل البيانات بين JSON وCSV وYAML.**
**A bilingual (Arabic/English) CLI tool to convert data between JSON, CSV, and YAML.**

---

## لماذا وصال؟ / Why Wisal?

<details open>
<summary><b>بالعربي</b></summary>

معظم أدوات تحويل البيانات (jc، Miller، dasel...) ممتازة لكنها إنجليزية بالكامل: رسائل الأخطاء، التحذيرات، حتى التوثيق. هذا يخلق حاجزاً حقيقياً أمام آلاف المطورين الناطقين بالعربية، خصوصاً عند تصحيح الأخطاء (debugging) في بيانات معقدة.

**وصال** أداة صغيرة ومركّزة تحل هذه المشكلة بالذات:

- 🌐 كل رسالة (خطأ، تحذير، مساعدة) متوفرة بالعربي والإنجليزي، وتُكتشف اللغة تلقائياً من بيئة النظام
- 🔢 كشف ومعالجة الأرقام العربية-الهندية (٠-٩) المختلطة مع أرقام لاتينية في نفس البيانات
- 🔤 اكتشاف مشاكل الترميز الشائعة (Windows-1256 مقابل UTF-8) التي تُفسد النصوص العربية
- ✅ فحص جودة البيانات قبل التحويل (أنواع بيانات مختلطة، حقول متداخلة) بدل تحويل أعمى قد يفشل بصمت
- 📦 بدون تعقيد: أداة واحدة، أمر واحد، سلوك يمكن توقعه

</details>

<details open>
<summary><b>English</b></summary>

Most data conversion tools (jc, Miller, dasel...) are excellent but entirely English: error messages, warnings, even documentation. This creates a real barrier for thousands of Arabic-speaking developers, especially when debugging complex data.

**Wisal** is a small, focused tool that solves exactly this problem:

- 🌐 Every message (error, warning, help) is available in Arabic and English, auto-detected from the system environment
- 🔢 Detects and handles Arabic-Indic digits (٠-٩) mixed with Latin digits in the same data
- 🔤 Detects common encoding issues (Windows-1256 vs UTF-8) that corrupt Arabic text
- ✅ Validates data quality before converting (mixed types, nested fields) instead of silently failing
- 📦 No bloat: one tool, one command, predictable behavior

</details>

---

## التثبيت / Installation

```bash
pip install wisal-cli
```

أو من المصدر / or from source:

```bash
git clone https://github.com/amgdsaleh66/wisal.git
cd wisal
pip install -e .
```

## الاستخدام / Usage

```bash
# تحويل بسيط / Simple conversion
wisal convert data.json data.csv

# فرض اللغة العربية للرسائل / Force Arabic messages
wisal convert data.json data.csv --lang ar

# تفكيك الحقول المتداخلة عند التحويل إلى CSV
# Flatten nested fields when converting to CSV
wisal convert data.json data.csv --flatten

# توحيد الأرقام العربية-الهندية إلى لاتينية
# Normalize Arabic-Indic digits to Latin
wisal convert data.json data.csv --normalize-digits

# معاينة الناتج دون حفظ / Preview without saving
wisal convert data.json data.csv --dry-run
```

### مثال / Example

**input.json:**
```json
[
  {"name": "أحمد", "age": "٣٠", "city": "الرياض"},
  {"name": "Sara", "age": 25, "city": "Dubai"}
]
```

```bash
wisal convert input.json output.csv --lang ar --normalize-digits
```

```
⚠ تحذير: العمود 'age' يحتوي على أنواع بيانات مختلطة (مثال: أرقام ونصوص معاً) في الأسطر: 1, 2.
تم تحويل 'input.json' إلى 'output.csv' بنجاح. (2 سطر/عنصر)
```

## الصيغ المدعومة / Supported Formats

| From \ To | JSON | CSV | YAML |
|-----------|------|-----|------|
| JSON      | —    | ✅  | ✅   |
| CSV       | ✅   | —   | ✅   |
| YAML      | ✅   | ✅  | —    |

## المساهمة / Contributing

المساهمات مرحّب بها! افتح issue أو pull request.
Contributions welcome! Open an issue or pull request.

```bash
pip install -e ".[dev]"
pytest tests/
```

## الترخيص / License

MIT
