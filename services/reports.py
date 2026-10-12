from Repositories.users_repository import UserRepository
from Repositories.KelasRepository import KelasRepository
from Repositories.SubscriptionsRepository import SubsRepository

def show_reports():
    users = UserRepository.all()
    classes = KelasRepository.all()
    subscriptions = SubsRepository.all()

    # --- basic reports ---
    active_members = 0
    active_coaches = 0
    for u in users:
        if u.is_active and u.role == "member":
            active_members += 1
        if u.is_active and u.role == "coach":
            active_coaches += 1

    active_classes = 0
    for c in classes:
        if c.is_active:
            active_classes += 1

    total_revenue = 0
    for s in subscriptions:
        total_revenue += s["amount"]

    print("===== Reports =====")
    print(f"Active members: {active_members}")
    print(f"Active coaches: {active_coaches}")
    print(f"Active classes: {active_classes}")
    print(f"Total revenue: {total_revenue}")

    # --- advanced: revenue per subscription type ---
    revenue_by_type = {}
    for s in subscriptions:
        sub_type = s["subscription_type"]
        if sub_type not in revenue_by_type:
            revenue_by_type[sub_type] = 0
        revenue_by_type[sub_type] += s["amount"]

    print("----- Revenue by subscription -----")
    if not revenue_by_type:
        print("No subscriptions yet.")
    for sub_type, amount in revenue_by_type.items():
        print(f"{sub_type}: {amount}")

    # --- advanced: most popular class ---
    print("----- Most popular class -----")
    best_class = None
    for c in classes:
        if best_class is None or len(c.enrolled) > len(best_class.enrolled):
            best_class = c
    if best_class is None:
        print("No classes yet.")
    else:
        print(f"{best_class.title} ({len(best_class.enrolled)} members)")


def export_people_txt():
    users = UserRepository.all()
    with open("people.txt", "w", encoding="utf-8") as file:
        file.write("All people of the club\n")
        file.write("======================\n")
        for u in users:
            if u.is_active:
                status = "active"
            else:
                status = "inactive"
            file.write(f"{u.name} | {u.username} | {u.role} | {u.email} | {status}\n")
        file.write(f"\nTotal people: {len(users)}\n")
    print("people.txt created.")