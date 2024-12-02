import re

from django.core.cache import cache

def set_code_to_cache(code, phone_number, timeout=300):
    cache.set(phone_number, code, timeout=timeout)


def get_code_from_cache(code, phone_number):
    cached_code = cache.get(phone_number)
    if not cached_code or cached_code != code:
        return None
    return True

def verify_phone_number(phone_number):
    pattern = r"^[78]\d{10}"
    return bool(re.match(pattern, phone_number))