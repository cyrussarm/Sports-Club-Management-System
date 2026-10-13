from core.models import Subscription
from Repositories.BaseRepository import BaseRepository

class SubsRepository(BaseRepository):
    file_name = "Subscriptions.json"
    model = Subscription