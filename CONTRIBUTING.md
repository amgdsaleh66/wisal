# المساهمة في وصال / Contributing to Wisal

شكراً لاهتمامك بالمساهمة! / Thanks for your interest in contributing!

## خطوات البدء / Getting Started

```bash
git clone https://github.com/amgdsaleh66/wisal.git
cd wisal
pip install -e ".[dev]"
pytest tests/
```

## إضافة رسائل جديدة / Adding New Messages

كل الرسائل موجودة في `wisal/messages.py`. عند إضافة رسالة جديدة، يجب توفيرها
بالعربي والإنجليزي معاً في نفس الوقت.

All messages live in `wisal/messages.py`. When adding a new message, you must
provide both Arabic and English versions at the same time.

## إرسال Pull Request

1. Fork المشروع
2. أنشئ فرعاً جديداً (`git checkout -b feature/my-feature`)
3. تأكد أن الاختبارات تعمل (`pytest tests/`)
4. أرسل Pull Request مع وصف واضح للتغيير
