from core.models import Wallet
from Repositories.base_repository import base_repository


class WalletRepository(base_repository):
    # فایل داده مربوط به این کلاس برای خواندن و نوشتن
    # خواندن و نوشتن در کلاس والد انجام میشن
    file_name = "wallets.json"
    # نام کلاسی مربوط به این فایل (cls)
    model = Wallet

    @classmethod
    # یک جنریتور درست میکند و شی های آن را پیمایش میکند تا برسد به شی ای که یوزرنیم ش سازگار باشد
    # اولین عضو را پیدا کرد ریترن میکند اگر پیدا نکرد نان
    def find_by_member(cls, member_username):
        return next((obj_ for obj_ in cls.all() if obj_.member_username == member_username), None)