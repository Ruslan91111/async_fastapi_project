from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher:
    @staticmethod
    def get_hash_of_password(password_from_user: str) -> str:
        return password_context.hash(password_from_user)

    @staticmethod
    def verify_password(password_from_user: str, hash_of_password: str) -> str:
        return password_context.verify(password_from_user, hash_of_password)
