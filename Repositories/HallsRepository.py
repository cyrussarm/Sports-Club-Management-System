from core.models import Salon
from Repositories.BaseRepository import BaseRepository

class SalonsRepository(BaseRepository):
    file_name = "Salon.json"
    model = Salon

    @classmethod
    def active_halls_list(cls):
        return [obj_ for obj_ in cls.all() if obj_.is_active]

    @classmethod
    def find_hall_by_name(cls, hall_name):
        return next((obj_ for obj_ in cls.all() if obj_.name == hall_name),None)

    @classmethod
    def find_active_hall(cls, hall_name):
        return next((obj_ for obj_ in cls.active_halls_list() if obj_.name == hall_name),None)

    # افزودن شی جدید
    @classmethod
    def add(cls, obj):
        existing_objects = cls.all()
        for obj_ in existing_objects:
            if str(obj_.name) == str(obj.name):
                return False
        existing_objects.append(obj)
        cls.save_all(existing_objects)
        return True

    