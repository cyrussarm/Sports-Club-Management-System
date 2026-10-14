from core.storage import load_data, save_data
from core.models import Transaction

class TransactionRepository:
    file_name = "transactions.json" 
    
    @classmethod
    def all_transactions(cls):
        #تبدیل تراکنش های داخل json به شی
        raw_data = load_data(cls.file_name)
        if not raw_data:
            return []
        return [Transaction.from_dict(item) for item in raw_data]

    @classmethod
    def save_all(cls, transactions):
        # ذخیره تراکنش ها در فایل json
        data_list = [tx.to_dict() for tx in transactions]
        save_data(cls.file_name, data_list)

    @classmethod
    def add_transaction(cls, transaction: Transaction):
        # append کردن تراکنش های جدید در فایل json
        transactions = cls.all_transactions()
        transactions.append(transaction)
        cls.save_all(transactions)