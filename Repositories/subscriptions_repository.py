from core.models import Subscription
from Repositories.base_repository import base_repository

class Subs_repository(base_repository):
    file_name = "subscriptions.json"
    model = Subscription