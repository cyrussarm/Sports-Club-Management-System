from core.models import SportClass
from Repositories.BaseRepository import BaseRepository

class KelasRepository(BaseRepository):
    file_name = "SportClasses.json"
    model = SportClass

    # افزودن شی جدید
    @classmethod
    def add(cls, obj):
        existing_objects = cls.all()
        for obj_ in existing_objects:
            if str(obj_.title) == str(obj.title):
                return False
        existing_objects.append(obj)
        cls.save_all(existing_objects)
        return True

    @classmethod
    def find_by_title(cls, name):
        return next((obj_ for obj_ in cls.all() if obj_.title == name),None)    