from Services.member_services import view_profile_and_subscription, view_available_classes, view_my_exxercise_plans, wallet_menu

def user_menu(member_username):
    while True:
        option = input('Choose an option:\n' \
        '1. View profile and subscription\n' \
        '2. Manage wallet\n' \
        '3. Manage classes\n' \
        '4. View exercise plans\n' \
        '5. Exit')
        if option == '1':
            view_profile_and_subscription(member_username)
            continue
        elif option == '2':
            wallet_menu(member_username)
            continue
        elif option == '3':
            view_available_classes(member_username)
            continue
        elif option == '4':
            view_my_exxercise_plans(member_username)
            continue
        elif option == '5':
            print('You have successfully logged out.')
            return None
        else:
            print('Invalid input.')
            continue