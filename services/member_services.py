# در services/member_services.py
from services.wallet_services import WalletService
from Repositories.wallet_repository import WalletRepository
from Repositories.users_repository import UserRepository
from Repositories.transactions_repository import TransactionRepository

def view_profile_and_subscription(member_username):
    pass

def view_available_classes(member_username):
    pass

def view_my_exercise_plan(member_username):
    pass

def wallet_menu(member_username):
    while True:
        choice = input(
            "1-view balance\n"
            "2-charge wallet\n"
            "3-view transactions\n"
            "4-back\n"
            "Select: "
        ).strip()

        if choice == "1":
            view_balance(member_username)
        elif choice == "2":
            charge_wallet_menu(member_username)
        elif choice == "3":
            view_transactions(member_username)
        elif choice == "4":
            return
        else:
            print("Invalid choice.")


def view_balance(member_username):
    wallet = WalletRepository.find_by_member(member_username)
    if wallet is None:
        print("Wallet not found.")
        return
    print(f"Your current balance: {wallet.balance}")


def view_transactions(member_username):
    transactions = TransactionRepository.list_by_user(member_username)
    if not transactions:
        print("No transactions yet.")
        return
    for t in transactions:
        print(f"{t.transaction_id} | {t.amount} | {t.subscription_name} | "
              f"{t.start_date.strftime('%Y-%m-%d')} | {t.status}")

def charge_wallet_menu(member_username):
    # ۱. مبلغ را بگیر
    while True:
        try:
            amount = float(input("Enter amount to charge: ").strip())
            if amount <= 0:
                print("Amount must be positive.")
                continue
            break
        except ValueError:
            print("Amount must be a number.")

    # ۲. اطلاعات کارت را بگیر
    print("Enter card details:")
    card_number = input("  Card number (16 digits): ").strip()

    while True:
        try:
            exp_month = int(input("  Exp month (1-12): ").strip())
            if not 1 <= exp_month <= 12:
                print("Month must be between 1 and 12.")
                continue
            break
        except ValueError:
            print("Month must be a number.")

    while True:
        try:
            exp_year = int(input("  Exp year (e.g. 1403-1408): ").strip())
            break
        except ValueError:
            print("Year must be a number.")

    pin = input("  PIN (6 digits): ").strip()
    cvv2 = input("  CVV2 (3 digits): ").strip()

    card_details = {
        "card_number": card_number,
        "exp_month": exp_month,
        "exp_year": exp_year,
        "pin": pin,
        "cvv2": cvv2,
    }

    # ۳. کاربر را پیدا کن (چون WalletService شیء member می‌خواهد)
    member = UserRepository.find_by_username(member_username)
    if member is None:
        print("Member not found.")
        return

    # ۴. صدا زدن سرویس کیف پول
    WalletService.charge_wallet(member, amount, card_details)