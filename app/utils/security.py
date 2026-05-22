from passlib.context import CryptContext
from passlib.exc import UnknownHashError

pwd_context = CryptContext(schemes=["bcrypt", "argon2"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password using bcrypt/argon2. Truncates to 72 chars (bcrypt limit)."""
    return pwd_context.hash(password[:72])


def verify_password(plain_password: str, password_hash: str) -> tuple[bool, str | None]:
    """Verify a password and return (is_valid, replacement_hash_if_rehash_needed)."""
    try:
        return pwd_context.verify_and_update(plain_password, password_hash)
    except UnknownHashError:
        return False, None
