# خطاهای پروژه

# همه اعضا تیم فقط از این کلاسها برای پرتاب خطا استفاده میکنند
class ClubError(Exception):
    pass

class ValidationError(ClubError):
    pass

class NotFoundError(ClubError):
    pass

class AuthError(ClubError):
    pass

class BusinessError(ClubError):
    pass

class StorageError(ClubError):
    pass

class BackToMenu(Exception):
    pass

class NotEnoughMoney(Exception) :
    pass