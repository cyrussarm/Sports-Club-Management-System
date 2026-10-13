from datetime import datetime

#--------------------------------------------
# کلاس کاربرها
#-------------------------------------------
class Users:
    _ALLOW_INIT = False
    def __init__(self, id_, name, username, password, email, role, is_active):
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
        d = {}
        d["id"] = self.id
        d["name"] = self.name
        d["username"] = self.username
        d["password"] = self.password
        d["email"] = self.email
        d["role"] = self.role
        d["is_active"] = self.is_active
        return d

    @classmethod
    def from_dict(cls, d):
        cls._ALLOW_INIT = True
        try:
            return cls(id_=d["id"], name=d["name"], username=d["username"], password=d["password"],
                       email=d["email"], role=d["role"], is_active=d.get("is_active", True))
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
        d["equipments"] = equipments         
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
        d["subscription_type"] = subscription_type         
        d["amount"] = self.amount
        d["payment_date"] = self.payment_date
        d["start_date"] = self.start_date
        d["end_date"] = end_date           
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
    def __init__(self, id_, username, tx_type, amount, date_, description, code_peigiri):
        if not Transaction._ALLOW_INIT:
            raise RuntimeError(
                " instance creating directly is not allowed. "
            )
        self.id = id_
        self.username = username
        self.tx_type = tx_type         
        self.amount = amount
        self.date = date_
        self.description = description
        self.code_peigiri = code_peigiri  

    def to_dict(self):
        d = {}
        d["id"] = self.id
        d["username"] = self.username
        d["tx_type"] = self.tx_type         
        d["amount"] = self.amount
        d["date"] = self.date
        d["description"] = self.description
        d["code_peigiri"] = self.code_peigiri  
        return d

    @classmethod
    def from_dict(cls, d):
        cls._ALLOW_INIT = True
        try:
            return cls(id_=d["id"], username=d["username"],
                       tx_type=d["tx_type"],
                       amount=d["amount"],
                       date_=d["date"],
                       description=d["description"],
                       code_peigiri=d["code_peigiri"])  
        finally:
            cls._ALLOW_INIT = False