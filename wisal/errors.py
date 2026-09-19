"""استثناءات وصال المخصصة. Custom Wisal exceptions."""


class WisalError(Exception):
    """خطأ متوقع يجب عرضه للمستخدم برسالة واضحة، دون traceback كامل."""
    pass
