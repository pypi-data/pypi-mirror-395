from argon2 import PasswordHasher
from argon2.exceptions import InvalidHash, VerifyMismatchError

from .error import SecurityError


def verify_text(encoded_hash, candidate_text):
    try:
        password_hasher.verify(encoded_hash, candidate_text)
    except VerifyMismatchError as e:
        x = 'text does not match hash'
        raise SecurityError(x) from e
    except InvalidHash as e:
        x = 'hash is not valid'
        raise SecurityError(x) from e


password_hasher = PasswordHasher()
hash_text = password_hasher.hash
