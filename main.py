from core.storage import load_data
from services.add_user import add_user
from core.exceptions import ClubError
from Repositories.users_repository import UserRepository

from tests.test_models import test_model

test_model()


try:
    res = load_data("users.json")
    for r in res:
        print(f"{r}\n")
except ClubError as e:
    print(f"Error: {e}")

try:
    current_user = {"id": 4,
        "name": "kobra",
        "username": "kobraf",
        "password": "password1&",
        "email": "kobra.k@gmail.com",
        "role": "member",
        "is_active": True}
    add_user(current_user, "kobra","kobraf","password2&","kobra.k@gmail.com","member")
except ClubError as e:
    print(f"Error: {e}")

# test repository
# چاپ نام همه کاربران از فایل users.json
for i in range(len(UserRepository.allusers())):
    print(UserRepository.allusers()[i].name) 

objs = UserRepository.allusers()
UserRepository.save_all(objs)
