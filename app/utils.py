import time
from django.utils.crypto import get_random_string
from django.utils.text import slugify
from re import sub


def snake_case(s):
    return '_'.join(
        sub('([A-Z][a-z]+)', r' \1',
            sub('([A-Z]+)', r' \1',
                s.replace('-', ' '))).split()).lower()


def unique_slugify(instance, slug):
    model = instance.__class__
    unique_slug = slugify(slug)
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = slugify(
            slug) + f"-{get_random_string(length=4)}"
    return unique_slug


def unique_name(instance, name):
    model = instance.__class__
    count = 1
    unique_name = "{} {}".format(name, count)
    while model.objects.filter(name=unique_name).exists():
        count = count + 1
        unique_name = "{} {}".format(name, count)
    return unique_name


def backoff(delay=2, retries=3):
    def decorator(func):
        def wrapper(*args, **kwargs):
            current_retry = 0
            current_delay = delay
            while current_retry < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    current_retry += 1
                    if current_retry >= retries:
                        raise e
                    print(
                        f"Failed to execute function '{func.__name__}'. Retrying in {current_delay} seconds...")
                    time.sleep(current_delay)
                    current_delay *= 2
        return wrapper
    return decorator
