from passlib.context import CryptContext

hashing_context = CryptContext(schemes=["sha256_crypt"])

class HashPassword():

    def hash_password(self, password: str) -> str:
        return hashing_context.hash(password)

    def check_password(self, input_pasword: str, hashed_password: str) -> bool:
        return hashing_context.verify(input_pasword, hashed_password)