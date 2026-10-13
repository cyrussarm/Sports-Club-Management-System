from datetime import datetime
import random
from core.models import Transaction
from core.bank import API
from Repositories.wallet_repository import WalletRepository
from Repositories.transactions_repository import TransactionRepository
from core.exceptions import ClubError

class WalletService:
    
    @staticmethod
    def charge_wallet(member, amount, card_details):
        
        # validation_result = API.validate(
        #     card_details.get("card_number"),
        #     card_details.get("cvv2"),
        #     card_details.get("expire_date"),
        #     card_details.get("pin")
        # )   

        # API نام کلاس است
        # متد ولیدیت اینستنس متوده
        # پس اول باید یک اینستنس بسازیم
        # ترتیب آرگومانها هم مطابق فایل Bank نبود
        api = API()
        validation_result = api.validate(
                    card_details.get("card_number"),
                        card_details.get("exp_month"),
                        card_details.get("exp_year"),
                        card_details.get("pin"),
                        card_details.get("cvv2")
                    )
        
        # is_valid = validation_result if isinstance(validation_result, bool) else validation_result.get("is_valid", True)
        is_valid = validation_result if isinstance(validation_result, bool) else validation_result.get("is_valid", False)
        
        if not is_valid:
            print("Transaction failed!")
            return False
            
        # گرفتن شماره پیگیری بانکی
        _bank_tracking_no = "BNK-" + str(random.randint(100000, 999999))
            
        # پیدا کردن کیف پول عضو
        #  کیف پول از فایل والتز.جیسن خونده میشه با جستجو توسط یوزر نیم ممبر
        #  دسترسی از اینجا به فولدر دیتا که در واقع جای دیتابیس نشسته مستقیم نیست بلکه از طریق کلاس والت ریپازیتوریه
        # کلاسهای ریپازیتوری مثل کتابدار هستند. خودتان نمیرید داخل مخزن کتاب.. 
        # به کتابدار میگین اینو میخوام بیاری یا اینو ببری سرجاش بذاری یا ... 
        
        wallet = WalletRepository.find_by_member(member.username)
        if wallet is None:
            print("Wallet not found for this member.")
            return False           
            
        # افزایش موجودی
        # مقدار اولیه والت هنگام تعریف یوزر صفر شده است
        wallet.balance += amount
        WalletRepository.update(wallet)         
        print(f"wallet topped up by {amount} , new balance: {wallet.balance}")

        # ساخت تراکنش
        # تاریخ امروز
        now = datetime.now()
        dict_ = {
                "id": _bank_tracking_no,
                "user_id": member.username,
                "amount": amount,
                "subscription_name": "Wallet charging",
                "duration_months": 0,
                "start_date": now.isoformat(),
                "end_date": now.isoformat(),
                "status": "success"
        }
        # ساخت یک تراکنش جدید از دیکشنری فوق و اضافه کردن آن به مخزن تراکشن ها
        new_transaction = Transaction.from_dict(dict_)  
        TransactionRepository.add(new_transaction)

        # ذخیره در فایل متنی
        WalletService._append_to_txt(new_transaction)       
        return True        
        
    @staticmethod
    def process_subscription_purchase(member, subscription_plan):
        # سیستم خرید و تمدید اشتراک، بررسی موجودی کیف پول، کسر مبلغ، ذخیره تراکنش مالی
 
        wallet = WalletRepository.find_by_member(member.username)
        current_balance = wallet.balance        
        if current_balance < subscription_plan.price:
            print("The money in your wallet isn't enough, please top up")
            return False            

        wallet.balance -= subscription_plan.price
        WalletRepository.update(wallet)  
        
        # صادر کردن شماره پیگیری  
        transaction_id = "INT-TRX-" + str(random.randint(10000000, 99999999))
       
        new_transaction = Transaction.from_dict({
        "id": transaction_id,
        "user_id": member.username,
        "amount": subscription_plan.price,
        "subscription_name": subscription_plan.name,
        "duration_months": subscription_plan.duration_months,
        "start_date": datetime.now().isoformat(),
        "end_date": datetime.now().isoformat(),
        "status": "success" })
        TransactionRepository.add(new_transaction)
        
        # ذخیره کردن تراکنش داخلی در فایل txt
        WalletService._append_to_txt(new_transaction)
        
        print(f"The subscription bought succesfully!")
        print(f"Internal tracking number: {transaction_id}")
        print(f"Start date : {new_transaction.start_date.strftime('%Y-%m-%d')}")
        print(f"End date: {new_transaction.end_date.strftime('%Y-%m-%d')}")
        return True

    @staticmethod
    def _append_to_txt(transaction):
        file_path = "data/transactions.txt"  
        
        log_entry = (
            f"Internal Transaction ID: {transaction.id} | "
            f"User: {transaction.user_id} | "
            f"Plan: {transaction.subscription_name} | "
            f"Amount: {transaction.amount} | "
            f"Start Date: {transaction.start_date.isoformat()} | "
            f"End Date: {transaction.end_date.isoformat()} | "
            f"Status: {transaction.status}\n"
        )
        
        try:
            with open(file_path, "a", encoding="utf-8") as file:
                file.write(log_entry)
        except OSError as e:
            raise ClubError(f"failed to write transaction log: {e}") from e
        

  
