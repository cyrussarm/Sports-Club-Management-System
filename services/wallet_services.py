from datetime import datetime
import random
from core.models import Transaction
from Bank import validate


class WalletService:
    
    @staticmethod
    def charge_wallet(member, amount: float, card_details: dict):
        validation_result = validate(
            card_details.get("card_number"),
            card_details.get("cvv2"),
            card_details.get("expire_date"),
            card_details.get("pin")
        )
        
        # اگر خروجی بانک به صورت دیکشنری یا بولین باشد:
        is_valid = validation_result if isinstance(validation_result, bool) else validation_result.get("is_valid", True)
        
        if not is_valid:
            print("Transaction failed!")
            return False
            
        # گرفتن شماره پیگیری بانکی
        bank_tracking_no = "BNK-" + str(random.randint(100000, 999999))
            
        # اگر موجودی تعیین نشده بود 0 در نظر میگیریم
        if not hasattr(member, 'wallet_balance'):
            member.wallet_balance = 0.0
            
        # افزایش موجودی
        member.wallet_balance += amount
        print(f"wallet topped up by {amount} , new balance: {member.wallet_balance}")
        
        # ذخیره تراکنش و شماره پیگیری در فایل txt
        WalletService._save_log_to_text_file(
            tx_id=bank_tracking_no,
            user_id=getattr(member, 'username', 'user_unknown'),
            plan_name="Topping up wallet",
            amount=amount,
            start="N/A",
            end="N/A",
            status="success"
        )
        return True

    @staticmethod
    def process_subscription_purchase(member, subscription_plan):
        # سیستم خرید و تمدید اشتراک، بررسی موجودی کیف پول، کسر مبلغ، ذخیره تراکنش مالی
        current_balance = getattr(member, 'wallet_balance', 0.0)
        if current_balance < subscription_plan.price:
            print("The money in your wallet isn't enough, please top up")
            return False
            
        member.wallet_balance -= subscription_plan.price
        
        # صادر کردن شماره پیگیری  
        transaction_id = "INT-TRX-" + str(random.randint(10000000, 99999999))
        
        new_transaction = Transaction(
            transaction_id=transaction_id,
            user_id=getattr(member, 'username', 'user_unknown'),
            amount=subscription_plan.price,
            subscription_name=subscription_plan.name,
            duration_months=subscription_plan.duration_months,
            status="success"
        )
        
        # ذخیره کردن تراکنش داخلی در فایل txt
        WalletService._save_transaction_to_text_file(new_transaction)
        
        print(f"The subscription bought succesfully!")
        print(f"Internal tracking number: {transaction_id}")
        print(f"Start date : {new_transaction.start_date.strftime('%Y-%m-%d')}")
        print(f"End date: {new_transaction.end_date.strftime('%Y-%m-%d')}")
        return True

    @staticmethod
    def _save_transaction_to_text_file(transaction: Transaction):
        file_path = "transactions.txt"
        
        log_entry = (
            f"Internal Transaction ID: {transaction.transaction_id} | "
            f"User: {transaction.user_id} | "
            f"Plan: {transaction.subscription_name} | "
            f"Amount: {transaction.amount} | "
            f"Start Date: {transaction.start_date.isoformat()} | "
            f"End Date: {transaction.end_date.isoformat()} | "
            f"Status: {transaction.status}\n"
        )
        
        with open(file_path, "a", encoding="utf-8") as file:
            file.write(log_entry)

    @staticmethod
    def _save_log_to_text_file(tx_id, user_id, plan_name, amount, start, end, status):
        #تابع برای  ثبت تراکنش و ذخیره شماره پیگیری
        file_path = "transactions.txt"
        log_entry = (
            f"Bank Tracking No: {tx_id} | "
            f"User: {user_id} | "
            f"Plan: {plan_name} | "
            f"Amount: {amount} | "
            f"Start Date: {start} | "
            f"End Date: {end} | "
            f"Status: {status}\n"
        )
        with open(file_path, "a", encoding="utf-8") as file:
            file.write(log_entry)