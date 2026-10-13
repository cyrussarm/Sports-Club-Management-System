from datetime import datetime
import random
from core.models import Transaction
from Repositories.transactions_repository import TransactionRepository
from Bank import validate  

class WalletService:
    
    @staticmethod
    def charge_wallet(member, amount: float, card_details: dict) -> bool:
        #اعتبار سنجی کارت به کمک bank.py
        validation_result = validate(
            card_details.get("card_number"),
            card_details.get("cvv2"),
            card_details.get("expire_date"),
            card_details.get("pin")
        )
        #اگر خروجی بانک به صورت دیکشنری یا بولین باشد :
        is_valid = validation_result if isinstance(validation_result, bool) else validation_result.get("is_valid", True)
        
        if not is_valid:
            print("Transaction failed")
            return False
            
        # تولید شماره پیگیری بانک به صورت رندوم
        bank_tracking_no = "BNK-" + str(random.randint(100000, 999999))
            
        # اگر موجودی تعیین نشده بود0 در نظر میگیریم
        if not hasattr(member, 'wallet_balance'):
            member.wallet_balance = 0.0
            
        #افزایش موجودی    
        member.wallet_balance += amount
        print(f"wallet topped up by {amount} , new balance: {member.wallet_balance}")
        
        # ساختن شی تراکنش
        tx = Transaction(
            transaction_id=bank_tracking_no,
            user_id=getattr(member, 'username', 'user_unknown'),
            amount=amount,
            subscription_name="شارژ کیف پول (درگاه بانکی)",
            duration_months=0,
            status="success"
        )
        TransactionRepository.add_transaction(tx)
        return True

    @staticmethod
    def process_subscription_purchase(member, subscription_plan):
        current_balance = getattr(member, 'wallet_balance', 0.0)
        if current_balance < subscription_plan.price:
            print("The money in your wallet isn't enough, please top up")
            return False
            
        member.wallet_balance -= subscription_plan.price
        
        # صادر کردن شماره پیگیری
        transaction_id = "INT-TRX-" + str(random.randint(10000000, 99999999))
        
        #  ساخت شی تراکنش 
        new_transaction = Transaction(
            transaction_id=transaction_id,
            user_id=getattr(member, 'username', 'user_unknown'),
            amount=subscription_plan.price,
            subscription_name=subscription_plan.name,
            duration_months=subscription_plan.duration_months,
            status="success"
        )
        
        # ذخیره کردن آن از طریق Repository
        TransactionRepository.add_transaction(new_transaction)
        
        print(f"The subscription bought succesfully!")
        print(f"Internal tracking number: {transaction_id}")
        print(f"Start date : {new_transaction.start_date.strftime('%Y-%m-%d')}")
        print(f"End date: {new_transaction.end_date.strftime('%Y-%m-%d')}")
        return True