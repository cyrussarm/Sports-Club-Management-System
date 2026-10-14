from datetime import datetime
#--------------------------------------------
# کلاس کاربرها
#-------------------------------------------
class Users:
    _ALLOW_INIT = False
    def __init__(self, id_, name, username, password, email, role, is_active ,wallet_balance = 0.0):
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
        self.wallet_balance = wallet_balance

    def to_dict(self):
        d = {}
        d["id"] = self.id
        d["name"] = self.name
        d["username"] = self.username
        d["password"] = self.password
        d["email"] = self.email
        d["role"] = self.role
        d["is_active"] = self.is_active
        d["wallet_balance"] = self.wallet_balance
        return d

    @classmethod
    def from_dict(cls, d):
        cls._ALLOW_INIT = True
        try:
            return cls(id_=d["id"], name=d["name"], username=d["username"], password=d["password"],
                       email=d["email"], role=d["role"], is_active=d.get("is_active", True), 
                       wallet_balance=d.get("wallet_balance", 0.0))
        finally:
            cls._ALLOW_INIT = False
       
#--------------------------------------------
# کلاس سالن
#-------------------------------------------
class Salon:
    _ALLOW_INIT = False
    def __init__(self, id_, name, capacity, equipments, is_active):
        if not Salon._ALLOW_INIT:
            raise RuntimeError(
                " instance creating directly is not allowed "
            )
        self.id = id_
        self.name = name
        self.capacity = capacity
        self.equipments = equipments         
        self.is_active = is_active

    def to_dict(self):
        d = {}
        d["id"] = self.id
        d["name"] = self.name
        d["capacity"] = self.capacity
        d["equipments"] = self.equipments         
        d["is_active"] = self.is_active
        return d

    @classmethod
    def from_dict(cls, d):
        cls._ALLOW_INIT = True
        try:
            return cls(id_=d["id"], name=d["name"], capacity=d["capacity"], equipments=d["equipments"], is_active=d.get("is_active", True))
        finally:
            cls._ALLOW_INIT = False

#--------------------------------------------
# کلاس کلاسها
#-------------------------------------------
class SportClass:
    _ALLOW_INIT = False

    def __init__(self, id_, title, sport_type, coach_name, coach_username,
                 hall_name, day, time, capacity, enrolled, is_active):
        if not SportClass._ALLOW_INIT:
            raise RuntimeError("instance creating directly is not allowed.")
        self.id = id_
        self.title = title
        self.sport_type = sport_type
        self.coach_name = coach_name
        self.coach_username = coach_username
        self.hall_name = hall_name
        self.day = day
        self.time = time
        self.capacity = capacity
        self.enrolled = enrolled
        self.is_active = is_active

    def to_dict(self):
        d = {}
        d["id"] = self.id
        d["title"] = self.title
        d["sport_type"] = self.sport_type
        d["coach_name"] = self.coach_name
        d["coach_username"] = self.coach_username
        d["hall_name"] = self.hall_name
        d["day"] = self.day
        d["time"] = self.time
        d["capacity"] = self.capacity
        d["enrolled"] = self.enrolled
        d["is_active"] = self.is_active
        return d

    @classmethod
    def from_dict(cls, d):
        cls._ALLOW_INIT = True
        try:
            return cls(
                id_=d["id"],
                title=d["title"],
                sport_type=d["sport_type"],
                coach_name=d["coach_name"],
                coach_username=d["coach_username"],
                hall_name=d["hall_name"],
                day=d["day"],
                time=d["time"],
                capacity=d["capacity"],
                enrolled=d.get("enrolled", []),
                is_active=d.get("is_active", True),
            )
        finally:
            cls._ALLOW_INIT = False

    def remaining_capacity(self):
        return self.capacity - len(self.enrolled)

# ------------------------------
#   کلاس اشتراک
# ------------------------------                     
class Subscription:
    _ALLOW_INIT = False
    def __init__(self, id_, member_username, subscription_type, amount, payment_date, 
                 start_date, end_date, subscription_code, subscription_state):
        if not Subscription._ALLOW_INIT:
            raise RuntimeError(
                " instance creating directly is not allowed. "
            )
        self.id = id_
        self.member_username = member_username
        self.subscription_type = subscription_type
        self.amount = amount
        self.payment_date = payment_date
        self.start_date = start_date
        self.end_date = end_date
        self.subscription_code = subscription_code
        self.subscription_state = subscription_state  # active/expired/no-subscription

    def to_dict(self):
        d = {}
        d["id"] = self.id
        d["member_username"] = self.member_username
        d["subscription_type"] = self.subscription_type         
        d["amount"] = self.amount
        d["payment_date"] = self.payment_date
        d["start_date"] = self.start_date
        d["end_date"] = self.end_date           
        d["subscription_code"] = self.subscription_code
        d["subscription_state"] = self.subscription_state
        return d

    @classmethod
    def from_dict(cls, d):
        cls._ALLOW_INIT = True
        try:
            return cls(id_=d["id"], member_username=d["member_username"],
                       subscription_type=d["subscription_type"],
                       amount=d["amount"],
                       payment_date=d["payment_date"],
                       start_date=d["start_date"],
                       end_date=d["end_date"],           
                       subscription_code=d["subscription_code"],
                       subscription_state=d.get("subscription_state", "no-subscription"))
        finally:
            cls._ALLOW_INIT = False

#--------------------------------------------
# کلاس تراکنش
#-------------------------------------------
class Transaction:
    _ALLOW_INIT = False

    def __init__(self, transaction_id, user_id, amount, subscription_name, duration_months, status):
        if not Transaction._ALLOW_INIT:
            raise RuntimeError("instance creating directly is not allowed.")
        self.id = transaction_id             
        self.user_id = user_id
        self.amount = amount
        self.subscription_name = subscription_name
        self.duration_months = duration_months   
        self.start_date = datetime.now()
        self.end_date = self._calculate_end_date(self.start_date, duration_months)
        self.status = status

    def _calculate_end_date(self, start, months):
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
        d = {}
        d["id"] = self.id
        d["user_id"] = self.user_id
        d["amount"] = self.amount
        d["subscription_name"] = self.subscription_name
        d["duration_months"] = self.duration_months
        d["start_date"] = self.start_date.isoformat()
        d["end_date"] = self.end_date.isoformat()
        d["status"] = self.status
        return d

    @classmethod
    def from_dict(cls, d):
        cls._ALLOW_INIT = True
        try:
            obj = cls(
                transaction_id=d["id"],             
                user_id=d["user_id"],
                amount=d["amount"],
                subscription_name=d["subscription_name"],
                duration_months=d["duration_months"],
                status=d.get("status", "success")
            )
            obj.start_date = datetime.fromisoformat(d["start_date"])
            obj.end_date = datetime.fromisoformat(d["end_date"])
            return obj
        finally:
            cls._ALLOW_INIT = False
#--------------------------------------------
#  تمرین ورزش
#-------------------------------------------
class Exercise:
    _ALLOW_INIT = False
    def __init__(self, id_, name, sets, tekrars, rest_time, description):
        if not Exercise._ALLOW_INIT:
            raise RuntimeError(
                " instance creating directly is not allowed. "
            )
        self.id = id_
        self.name= name     # نام تمرین
        self.sets = sets    # تعداد ست
        self.tekrars = tekrars # تعداد تکرار
        self.rest_time = rest_time # زمان استراحت
        self.description = description        

    def to_dict(self):
        d={}
        d["id"] = self.id
        d["name"] = self.name
        d["sets"] = self.sets           
        d["tekrars"] = self.tekrars
        d["rest_time"] = self.rest_time
        d["description"] = self.description       
        return d

    @classmethod
    def from_dict(cls, d):
        cls._ALLOW_INIT = True
        try:
            return cls(id_=d["id"], name = d["name"],
                        sets = d["sets"],
                        tekrars = d["tekrars"],
                        rest_time = d["rest_time"],
                        description = d["description"]
                        )  
        finally:
            cls._ALLOW_INIT = False

#--------------------------------------------
#  برنامه ورزش
#-------------------------------------------
class ExercisePlan:
    _ALLOW_INIT = False
    def __init__(self, id_, class_title , member_username, coach_username, exercises):
        if not ExercisePlan._ALLOW_INIT:
            raise RuntimeError(
                " instance creating directly is not allowed. "
            )
        self.id = id_
        self.class_title= class_title     # نام کلاس
        self.member_username = member_username    # یوزر عضو
        self.coach_username = coach_username #  یوزر مربی         
        self.exercises = exercises    # لیست تمرین ها (هر تمرین یک شی)    

    def to_dict(self):
        d={}
        d["id"] = self.id
        d["class_title"] = self.class_title
        d["member_username"] = self.member_username           
        d["coach_username"] = self.coach_username
        d["exercises"] = self.exercises           
        return d

    @classmethod
    def from_dict(cls,d):
        cls._ALLOW_INIT = True
        try:
            return cls(id_=d["id"], class_title = d["class_title"],
                        member_username = d["member_username"],
                        coach_username = d["coach_username"],
                        exercises = d["exercises"]                      
                        )  
        finally:
            cls._ALLOW_INIT = False

# -----------------------------------------------------------------
# کلاس کیف پول
# -------------------------------------------------------------------------------------------
class Wallet:
    _ALLOW_INIT = False
    def __init__(self, id_, member_username, balance):
        if not Wallet._ALLOW_INIT:
            raise RuntimeError(" instance creating directly is not allowed ")
        self.id = id_
        self.member_username = member_username
        self.balance = balance

    def to_dict(self):
        d = {}
        d["id"] = self.id
        d["member_username"] = self.member_username
        d["balance"] = self.balance
        return d

    @classmethod
    def from_dict(cls, d):
        cls._ALLOW_INIT = True
        try:
            return cls(id_=d["id"], member_username=d["member_username"],
                       balance=d.get("balance", 0.0))
        finally:
            cls._ALLOW_INIT = False
# ------------------------------------------------------------------
# کلاص ثبت نام 
# -----------------------------------------------------------------
class Enrollment:
    _ALLOW_INIT = False
    def __init__(self, id_, member_username, class_id, enrollment_date,
                 code_rahgiri, is_active=True):
        if not Enrollment._ALLOW_INIT:
            raise RuntimeError(" instance creating directly is not allowed ")
        self.id = id_
        self.member_username = member_username
        self.class_id = class_id
        self.enrollment_date = enrollment_date
        self.code_rahgiri = code_rahgiri
        self.is_active = is_active

    def to_dict(self):
        d = {}
        d["id"] = self.id
        d["member_username"] = self.member_username
        d["class_id"] = self.class_id
        d["enrollment_date"] = self.enrollment_date
        d["code_rahgiri"] = self.code_rahgiri
        d["is_active"] = self.is_active
        return d

    @classmethod
    def from_dict(cls, d):
        cls._ALLOW_INIT = True
        try:
            return cls(id_=d["id"], member_username=d["member_username"],
                       class_id=d["class_id"],
                       enrollment_date=d["enrollment_date"],
                       code_rahgiri=d["code_rahgiri"],
                       is_active=d.get("is_active", True))
        finally:
            cls._ALLOW_INIT = False

