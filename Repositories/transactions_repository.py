from core.models import Transaction
from Repositories.base_repository import base_repository


class TransactionRepository(base_repository):
    file_name = "transactions.json"
    model = Transaction

    @classmethod
    def list_by_user(cls, user_id):
        return [obj_ for obj_ in cls.all() if obj_.user_id == user_id]