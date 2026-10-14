# در services/member_services.py
from services.wallet_services import WalletService
from Repositories.wallet_repository import WalletRepository
from Repositories.users_repository import UserRepository
from Repositories.transactions_repository import TransactionRepository
from Repositories.subscriptions_repository import Subs_repository 
from Repositories.classes_repository import KelasRepository
from Repositories.sabtenam_repository import SabtenamRepository
from core.models import Enrollment
from datetime import date, datetime
import random

def view_profile_and_subscription(member_username):
    pass

def view_available_classes(member_username):
    pass

def view_my_exercise_plan(member_username):
    pass

def check_eshterak(member_username):
    # چک اول: اشتراک دارد یا نه
    eshterakha = Subs_repository.all()
    selected = None
    for e in eshterakha:
        if e.member_username == member_username and e.subscription_state == "active":
            selected = e
            break

    if not selected:
        print("You have no active subscripton")        
        return False
    
    f1 = "%Y-%m-%d"
    today = date.today()
    try:
        tarikh_eshterak = datetime.strptime(selected.end_date, f1).date()
    except (ValueError, AttributeError):
        print("Subscription date format is invalid.\n")
        return False

    if tarikh_eshterak >= today:
        return True

    print("Eshterake shoma mongazi shode ast")
    return False

def sabtenam_class(member_username):

    if not check_eshterak(member_username):
        print("laghve sabte-nam\n")
        return

    my_classes = KelasRepository.list_active_classes_a_member(member_username)
    if my_classes:
        print("your current classes: \n")
        for e in my_classes:           
            print(f"  class_id = {e.id}, class_title = {e.title}")
    else:
        print("you have no class")
           

    all_active_classes  = [c for c in KelasRepository.all() if c.coach_name]
    my_classes_id = [c.id for c in my_classes]
    enrolable_class = []
    for c in all_active_classes:
        if c.id not in my_classes_id and c.remaining_capacity()>0:
            enrolable_class.append(c)

    if not enrolable_class:
        print("You have no available class.\n")
        return

    print("\nAvailable classes for you:")    
    for i,c in enumerate(enrolable_class):
        print(f"  ID = {i+1} | class_id = {c.id} | title = {c.title} | \n")
        print(f"coach = {c.coach_name} | day = {c.day} | time = {c.time} | \n")
        print(f"remaining = {c.remaining_capacity()}/{c.capacity}")

    while True:
        choice = input("Enter the ID of selected class (or press ENTER to exit): ").strip()
        if not choice:
            return
        try:
            choice = int(choice)
        except ValueError:
            print("Please enter a number.")
            continue
        if choice < 1 or choice > len(enrolable_class):      
            print("Invalid ID, try again.")
            continue
        break

    target_class = enrolable_class[choice - 1]

    sabtenamha = SabtenamRepository.all()
    if sabtenamha:
        new_id = max(int(e.id) for e in sabtenamha) + 1
    else:
        new_id = 1    
    rahgiri_code = "PEI-" + str(random.randint(100000, 999999))
     

    enr = Enrollment.from_dict({
        "id": new_id,
        "member_username": member_username,
        "class_id": target_class.id,
        "enrollment_date": date.today().isoformat(),
        "code_rahgiri": rahgiri_code,
        "is_active": True,
    })

    try:
        SabtenamRepository.add(enr)
    except Exception as e:
        print(f"Error saving enrollment: {e}")
        return

    target_class.enrolled.append(member_username)
    KelasRepository.update(target_class)

    print(f"\n Sabtename Movafagh in '{target_class.title}'")
    print(f"   code-peigiri: {enr.code_rahgiri}")
    print(f"   Date: {enr.enrollment_date}\n")

    
# انصراف از یک کلاس
def cancel_sabtenam_class(member_username):
    my_sabtenams = SabtenamRepository.find_active_by_member(member_username)
    if not my_sabtenams:
        print("You have no active sabtenam")
        return

    print("your current classes: \n")
    for e in my_sabtenams:
        class_ = KelasRepository.find_by_id(e.class_id)
        if class_:
            print(f" class_id = {e.id}, class_title = {class_.title}")

    while True:
        choice = input("Enter the ID class to cancle (or press ENTER to exit): ").strip()
        if choice == "0":
            return
        try:
            choice = int(choice)
        except ValueError:
            print("Please enter a number.")
            continue
        for e in my_sabtenams:
            if str(e.id) == str(choice):
                target = e
                break
            else:
                target = None               
        
        if target is None:
            print("Invalid id.")
            continue

        target.is_active = False
        try:
            SabtenamRepository.update(target)
        except Exception as e:
            print(f"Error: {e}")
            return

        # حذف کلاس از لیست ثبت نامی های کاربر
        found = KelasRepository.find_by_id(target.class_id)
        if found and member_username in found.enrolled:
            found.enrolled.remove(member_username)
            KelasRepository.update(found)

        print(f"\n Sabte-nam Ba Movafaghiat Cancel shod.")

        # مشاهده سابقه ثبت نام های کاربر
def view_my_enrollments(member_username):
    sabtenams = SabtenamRepository.find_by_member(member_username)
    if not sabtenams:
        print("You have no sabegheie sabtenam")
        return
    
    for s in sabtenams:
        found = KelasRepository.find_by_id(s.class_id)
    
        if found:            
            state = "active" if s.is_active else "cancelled"
            print(f"  class = {found.title} | date = {s.enrollment_date} | "
                f"code = {s.code_rahgiri} | status ={state}")
   
    
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
        print(f"{t.id} | {t.amount} | "
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