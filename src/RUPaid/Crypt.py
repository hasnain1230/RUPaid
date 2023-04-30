from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from src.RUPaid.DatabaseConnection import DBConnection


class Hashing:
    def __init__(self):
        self.cursor = DBConnection().get_cursor()

    @staticmethod
    def hash_password(password):
        digest = hashes.Hash(hashes.SHA3_512(), backend=default_backend())
        digest.update(password.encode())
        return digest.finalize().hex()

    def get_hashed_password(self, user_id):
        self.cursor.execute(f"SELECT password FROM users WHERE id = {user_id}")
        return self.cursor.fetchone()[0]

    def update_password(self, user_id, password):
        hashed_password = self.hash_password(password)
        self.cursor.execute(f"UPDATE users SET password = '{hashed_password}' WHERE id = {user_id}")
        self.cursor.commit()

    def verify_password(self, user_id, password):
        hashed_password = self.get_hashed_password(user_id)
        return hashed_password == self.hash_password(password)

