from core.storage import load_data, save_data

class base_repository:
    file_name = None  
    model = None  
    
    # برگرداندن لیست همه اشیا 
    @classmethod
    def all(cls):
        list_=[]
        raw_data_as_dict = load_data(cls.file_name)
        if cls.model is None:
            print("class is none")
            return list_
        list_ = [cls.model.from_dict(dict_) for dict_ in raw_data_as_dict]      
        return list_

    @classmethod
    def save_all(cls, objects):
        # تبدیل لیست شی ها به لیست دیکشنری  
        list_ = [obj.to_dict() for obj in objects]        
        # ذخیره کردن لیست دیکشنری در فایل json        
        save_data(cls.file_name, list_)

    # پیدا کردن یک شی با استفاده از آی دی
    @classmethod
    def find_by_id(cls, id_):
        objects = cls.all()          
        for obj in objects:
            if str(obj.id) == str(id_):
                return obj
        return None

    # افزودن شی جدید
    @classmethod
    def add(cls, obj):
        existing_objects = cls.all()
        for obj_ in existing_objects:
            if str(obj_.id) == str(obj.id):
                return False
        existing_objects.append(obj)
        cls.save_all(existing_objects)
        return True
        
    @classmethod 
    def update(cls,new_obj):
        # جایگزینی شی موجود با شی جدید
        objects = cls.all()
        for index, obj_ in enumerate(objects):
            if str(obj_.id) == str(new_obj.id):
                objects[index] = new_obj
                cls.save_all(objects)
                return True
        return False

    # غیرفعال کردن یک شی
    @classmethod
    def deactivate(cls,id_):
        objects = cls.all()
        for obj_ in objects:
            if str(obj_.id)==str(id_):
                obj_.is_active = False
                cls.save_all(objects)
                return True
        return False

    # فعال کردن یک شی
    @classmethod
    def activate(cls,id_):
        objects = cls.all()
        for obj_ in objects:
            if str(obj_.id)==str(id_):
                obj_.is_active = True
                cls.save_all(objects)
                return True
        return False

    # حذف یک شیء
    @classmethod
    def delete(cls, id_):
        objects = cls.all()
        filtered = [obj for obj in objects if str(obj.id) != str(id_)]
        if len(filtered) == len(objects):
            return False
        cls.save_all(filtered)
        return True

   
        
        


            
        


