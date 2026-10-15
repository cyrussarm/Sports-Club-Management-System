from core.models import Subscription
from Repositories.base_repository import base_repository

class Subs_repository(base_repository):
    file_name = "subscriptions.json"
    model = Subscription

    @classmethod
    def find_by_username(cls, member_username):
            subs = cls.all()
            for sub in subs:
                if str(sub.member_username) == str(member_username):
                    return sub