from services.coach_sevices import view_coach_class
from services.coach_sevices import manage_exercise_plans
def coachpanel(coach_username):
    while True:
        a = input('Choose an option:\n' \
                '1. View Classes\n' \
                '2. Manage Excercise Plans\n' \
                '3. Exit')
        if a == 1:
            view_coach_class(coach_username)
            back = input("Type Anything To Go Back.")
            continue
        elif a == 2:
            manage_exercise_plans(coach_username)
            

        elif a == 3:
            print('You have successfully logged out.')
            return None
        
        else:
            print('Invalid input')
            continue