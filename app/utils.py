from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])


def get_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_pwd(password, hashed_pwd) -> bool:
    return pwd_context.verify(password, hashed_pwd)
