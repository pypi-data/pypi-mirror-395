import secrets
from string import ascii_letters, digits


def make_random_string(length, alphabet=ascii_letters + digits):
    return ''.join(secrets.choice(alphabet) for _ in range(length))
