from core.models import Salon
from Repositories.base_repository import base_repository

class SalonsRepository(base_repository):
    file_name = "salons.json"
    model = Salon

    @classmethod
    def active_halls_list(cls):
        return [obj for obj in cls.all() if obj.is_active]

    @classmethod
    def find_hall_by_name(cls, hall_name):
        return next((obj for obj in cls.all() if obj.name == hall_name),None)

    @classmethod
    def find_active_hall(cls, hall_name):
        return next((obj for obj in cls.active_halls_list() if obj.name == hall_name),None)

    # افزودن شی جدید
    @classmethod
    def add(cls, new_obj):
        existing_objects = cls.all()
        for obj in existing_objects:
            if str(obj.name) == str(new_obj.name):
                return False
        existing_objects.append(new_obj)
        cls.save_all(existing_objects)
        return True

    