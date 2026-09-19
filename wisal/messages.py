"""
نظام الرسائل ثنائية اللغة (عربي/إنجليزي) لأداة وصال.
Bilingual (Arabic/English) message system for the Wisal CLI tool.

يتم اختيار اللغة تلقائياً من متغير البيئة LANG، أو يمكن فرضها عبر --lang.
Language is auto-detected from the LANG environment variable, or forced via --lang.
"""

import os
from enum import Enum


class Lang(str, Enum):
    AR = "ar"
    EN = "en"


def detect_language() -> Lang:
    """اكتشاف اللغة المناسبة من بيئة النظام."""
    env_lang = os.environ.get("WISAL_LANG", "").lower()
    if env_lang in ("ar", "arabic"):
        return Lang.AR
    if env_lang in ("en", "english"):
        return Lang.EN

    system_lang = os.environ.get("LANG", "") + os.environ.get("LC_ALL", "")
    if "ar" in system_lang.lower():
        return Lang.AR
    return Lang.EN


# كل رسالة لها مفتاح، وقيمة لكل لغة.
# Each message has a key, and a value per language.
MESSAGES = {
    "file_not_found": {
        Lang.AR: "خطأ: الملف '{path}' غير موجود. تأكد من المسار وحاول مرة أخرى.",
        Lang.EN: "Error: File '{path}' was not found. Check the path and try again.",
    },
    "unsupported_format": {
        Lang.AR: "خطأ: الصيغة '{ext}' غير مدعومة. الصيغ المدعومة: json, csv, yaml.",
        Lang.EN: "Error: Format '{ext}' is not supported. Supported formats: json, csv, yaml.",
    },
    "key_missing_in_row": {
        Lang.AR: "تحذير: الحقل '{field}' غير موجود في السطر {line}. تم استخدام قيمة فارغة بدلاً منه.",
        Lang.EN: "Warning: Field '{field}' is missing in row {line}. An empty value was used instead.",
    },
    "encoding_detected": {
        Lang.AR: "تم اكتشاف ترميز النص التالي: {encoding}. سيتم استخدامه لقراءة الملف.",
        Lang.EN: "Detected text encoding: {encoding}. It will be used to read the file.",
    },
    "encoding_mismatch_warning": {
        Lang.AR: "تحذير: الملف يبدو أنه بترميز '{detected}' وليس UTF-8. "
        "قد يظهر النص العربي بشكل غير صحيح إذا لم تتم معالجته.",
        Lang.EN: "Warning: The file appears to be encoded as '{detected}', not UTF-8. "
        "Arabic text may display incorrectly if this is not handled.",
    },
    "mixed_digits_warning": {
        Lang.AR: "تحذير: تم العثور على أرقام عربية-هندية (٠-٩) مختلطة مع أرقام لاتينية في العمود '{column}'. "
        "استخدم --normalize-digits لتوحيدها.",
        Lang.EN: "Warning: Arabic-Indic digits (٠-٩) found mixed with Latin digits in column '{column}'. "
        "Use --normalize-digits to unify them.",
    },
    "conversion_success": {
        Lang.AR: "تم تحويل '{source}' إلى '{target}' بنجاح. ({rows} سطر/عنصر)",
        Lang.EN: "Successfully converted '{source}' to '{target}'. ({rows} rows/items)",
    },
    "invalid_json": {
        Lang.AR: "خطأ في تحليل JSON بالقرب من السطر {line}، العمود {column}: {detail}",
        Lang.EN: "JSON parsing error near line {line}, column {column}: {detail}",
    },
    "nested_structure_warning": {
        Lang.AR: "تحذير: الحقل '{field}' يحتوي على بنية متداخلة ولا يمكن تمثيله مباشرة في CSV. "
        "تم تحويله إلى نص JSON مضمّن. استخدم --flatten لتفكيك البنية إلى أعمدة.",
        Lang.EN: "Warning: Field '{field}' contains a nested structure that cannot be represented "
        "directly in CSV. It was embedded as a JSON string. Use --flatten to expand it into columns.",
    },
    "empty_input": {
        Lang.AR: "خطأ: الملف المدخل '{path}' فارغ. لا يوجد شيء لتحويله.",
        Lang.EN: "Error: Input file '{path}' is empty. Nothing to convert.",
    },
    "output_written": {
        Lang.AR: "تم حفظ الناتج في: {path}",
        Lang.EN: "Output saved to: {path}",
    },
    "dry_run_notice": {
        Lang.AR: "وضع المعاينة فقط (dry-run): لم يتم حفظ أي ملف.",
        Lang.EN: "Dry-run mode: no file was written.",
    },
    "validation_type_mismatch": {
        Lang.AR: "تحذير: العمود '{column}' يحتوي على أنواع بيانات مختلطة "
        "(مثال: أرقام ونصوص معاً) في الأسطر: {lines}.",
        Lang.EN: "Warning: Column '{column}' has mixed data types "
        "(e.g. numbers and text together) in rows: {lines}.",
    },
    "diff_summary": {
        Lang.AR: "ملخص المقارنة: {added} حقل مُضاف، {removed} حقل محذوف، {changed} حقل مُغيّر.",
        Lang.EN: "Diff summary: {added} field(s) added, {removed} field(s) removed, {changed} field(s) changed.",
    },
}


def t(key: str, lang: Lang | None = None, **kwargs) -> str:
    """
    ترجمة مفتاح رسالة إلى نص باللغة المطلوبة، مع تعبئة المتغيرات.
    Translate a message key into text in the requested language, filling in variables.
    """
    if lang is None:
        lang = detect_language()
    template = MESSAGES.get(key, {}).get(lang)
    if template is None:
        # احتياط: استخدم الإنجليزية إذا لم توجد الرسالة باللغة المطلوبة
        template = MESSAGES.get(key, {}).get(Lang.EN, key)
    return template.format(**kwargs)
