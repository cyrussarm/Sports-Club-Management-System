from datetime import datetime
#--------------------------------------------
# کلاس کاربرها
#-------------------------------------------
class Users:
    _ALLOW_INIT = False
    def __init__(self,id_,name,username,password,email,role,is_active):
        if not Users._ALLOW_INIT:
            raise RuntimeError(
                " instance creating directly is not allowed "
            )

        self.id = id_
        self.name = name
        self.username = username
        self.password = password
        self.email = email
        self.role = role
        self.is_active = is_active

    def to_dict(self):
        d={}
        d["id"] = self.id
        d["name"] = self.name
        d["username"] = self.username
        d["password"] = self.password
        d["email"] = self.email
        d["role"] = self.role
        d["is_active"] = self.is_active
        return d

    @classmethod
    def from_dict(cls,d):
        cls._ALLOW_INIT = True
        try:
            return cls(id_=d["id"], name = d["name"], username = d["username"], password = d["password"],
                   email = d["email"], role = d["role"], is_active = d.get("is_active", True))
        finally:
            cls._ALLOW_INIT = False
       
#--------------------------------------------
# کلاس سالن
#-------------------------------------------
class Salon:
    _ALLOW_INIT = False
    def __init__(self,name,capacity,equipments,is_active):
        if not Salon._ALLOW_INIT:
            raise RuntimeError(
                " instance creating directly is not allowed "
            )
        self.name = name
        self.capacity = capacity
        self.equipments = equipments        
        self.is_active = is_active

    def to_dict(self):
        d={}
        d["name"] = self.name
        d["capacity"] = self.capacity
        d["equipments"] = self.equipments           
        d["is_active"] = self.is_active
        return d

    @classmethod
    def from_dict(cls,d):
        cls._ALLOW_INIT = True
        try:
            return cls (name=d["name"], capacity = d["capacity"], equipments = d["equipments"], is_active = d.get("is_active", True))
        finally:
            cls._ALLOW_INIT = False
#--------------------------------------------
# کلاس کلاسها
#-------------------------------------------
class SportClass:
    _ALLOW_INIT = False
    def __init__(self, title,sport_type, coach_username, hall_name, day, time, capacity, enrolled, is_active):
        if not SportClass._ALLOW_INIT:
            raise RuntimeError(
                " instance creating directly is not allowed. "
            )
        self.title = title
        self.sport_type = sport_type
        self.coach_username = coach_username
        self.hall_name = hall_name
        self.day = day
        self.time = time
        self.capacity = capacity
        self.enrolled = enrolled
        self.is_active = is_active    
    
    def to_dict(self):
        d={}
        d["title"] = self.title
        d["sport_type"] = self.sport_type           
        d["coach_username"] = self.coach_username
        d["hall_name"] = self.hall_name
        d["day"] = self.day
        d["time"] = self.time
        d["capacity"] = self.capacity
        d["enrolled"] = self.enrolled
        d["is_active"] = self.is_active
        return d

    @classmethod
    def from_dict(cls,d):
        cls._ALLOW_INIT = True
        try:
            return cls(title = d["title"], sport_type = d["sport_type"], 
                   coach_username = d["coach_username"], hall_name = d["hall_name"], 
                   day = d["day"], time = d["time"], capacity = d["capacity"], 
                   enrolled = d.get("enrolled",[]), is_active = d.get("is_active", True))
        finally:
            cls._ALLOW_INIT = False

    # ظرفیت باقی‌مانده 
    def remaining_capacity(self):
        return self.capacity-len(self.enrolled)


# ------------------------------
#     کلاس اشتراک
# ------------------------------                   
class Subscription:
    def __init__(self, subscription_id: int, name: str, duration_months: int, price: float):
        self.subscription_id = subscription_id
        self.name = name
        self.duration_months = duration_months
        self.price = price

    def to_dict(self):
        return {
            "id": self.subscription_id,
            "name": self.name,
            "duration_months": self.duration_months,
            "price": self.price
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            subscription_id=data.get("id"),
            name=data.get("name"),
            duration_months=data.get("duration_months"),
            price=data.get("price")
        )

#--------------------------------------------
# کلاس تراکنش
#-------------------------------------------
class Transaction:
    def __init__(self, transaction_id: str, user_id: str, amount: float, subscription_name: str, duration_months: int, status: str = "موفق"):
        self.transaction_id = transaction_id
        self.user_id = user_id
        self.amount = amount
        self.subscription_name = subscription_name
        self.duration_months = duration_months
        
        self.start_date = datetime.now()
        
        self.end_date = self._calculate_end_date(self.start_date, duration_months)
        
        self.status = status

    def _calculate_end_date(self, start: datetime, months: int) -> datetime:
        new_year = start.year
        new_month = start.month + months
        
        if new_month > 12:
            new_year += new_month // 12
            new_month = new_month % 12
            if new_month == 0:
                new_month = 12
                new_year -= 1

        new_day = start.day

        return start.replace(year=new_year, month=new_month, day=new_day)

    def to_dict(self):
        return {
            "transaction_id": self.transaction_id,
            "user_id": self.user_id,
            "amount": self.amount,
            "subscription_name": self.subscription_name,
            "duration_months": self.duration_months,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data: dict):
        obj = cls.__new__(cls)
        obj.transaction_id = data.get("transaction_id")
        obj.user_id = data.get("user_id")
        obj.amount = data.get("amount")
        obj.subscription_name = data.get("subscription_name")
        obj.duration_months = data.get("duration_months")
        obj.start_date = datetime.fromisoformat(data["start_date"])
        obj.end_date = datetime.fromisoformat(data["end_date"])
        obj.status = data.get("status", "succes")
        return obj