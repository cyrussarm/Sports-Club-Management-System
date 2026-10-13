from Repositories.users_repository import UserRepository
from Repositories.wallet_repository import WalletRepository
from services.wallet_services import WalletService


def test_charge_wallet():
    # ۱. عضو را پیدا کن
    member = UserRepository.find_by_username("kobraf")
    if member is None:
        print("Member 'kobraf' not found.")
        return

    print(f"Testing with member: {member.username}")

    # ۲. وضعیت فعلی کیف پول
    wallet = WalletRepository.find_by_member(member.username)
    if wallet is None:
        print("Wallet not found for this member.")
        return
    print(f"Balance BEFORE: {wallet.balance}")

    # ۳. اطلاعات کارت نمونه
    card_details = {
        "card_number": "1234567890123456",  # ۱۶ رقم
        "exp_month": 5,                      # ۱ تا ۱۲
        "exp_year": 1404,                    # ۱۴۰۳ تا ۱۴۰۸
        "pin": "123456",                     # ۶ رقم
        "cvv2": "123",                       # ۳ رقم
    }

    # ۴. صدا زدن سرویس
    amount = 100.0
    result = WalletService.charge_wallet(member, amount, card_details)
    print(f"Result: {result}")

    # ۵. وضعیت بعد از شارژ
    wallet = WalletRepository.find_by_member(member.username)
    print(f"Balance AFTER: {wallet.balance}")