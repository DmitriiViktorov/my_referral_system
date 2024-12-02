from django.core.cache import cache

def set_code_to_cache(code, phone_number, timeout=300):
    cache.set(phone_number, code, timeout=timeout)


def get_code_from_cache(code, phone_number):
    cached_code = cache.get(phone_number)
    if not cached_code or cached_code != code:
        return None
    return True