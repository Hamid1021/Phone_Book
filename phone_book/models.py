from django.db import models
from account.models import USER
from extensions.utils import get_filename_ext
from django.db.models import Q


def avatar_uploadTo(instance, fileName):
    name, ext = get_filename_ext(fileName)
    return f"avatars/{name}{ext}"


class Avatar(models.Model):
    avatar = models.ImageField("آواتار", upload_to=avatar_uploadTo, blank=False, null=False, default="None.jpg")
    alt = models.CharField(
        "متن جایگزین تصویر", max_length=255, blank=True, null=True, default="",
        help_text="اگر تصویر به هر دلیل ممکن لود نشود این متن به جای تصویر نمایش داده خواهد شد"
    )
    status = models.BooleanField("فعال/غیر فعال", null=False, blank=False, default=True, 
        help_text="مشخص کنید در صورت فعال بودن قابل انتخاب خواهد بود برای خارج کردن از دسترس غیر فعال نمایید"
    )
    is_deleted = models.BooleanField("فعال/غیر فعال", null=True, blank=True, default=False, 
        editable=False
    )
    
    class Meta:
        verbose_name = "1-"+"آواتار"
        verbose_name_plural = "1-"+"آواتار"


class BookPhone(models.Model):
    name = models.CharField(
        "نام فرد", max_length=255, blank=False, null=False, default="",
    )
    last_name = models.CharField(
        "نام خانوادگی فرد", max_length=255, blank=False, null=False, default="",
    )
    phone_number = models.CharField(
        "شماره همراه فرد", max_length=13, blank=False, null=False, default="",
    )
    phone_number_1 = models.CharField(
        "شماره تلفن فرد", max_length=13, blank=True, null=True, default="",
    )
    avatar = models.ForeignKey(Avatar, blank=True, null=True, default="", on_delete=models.DO_NOTHING, verbose_name="آواتار")
    post = models.CharField(
        "شغل یا سمت فرد", max_length=255, blank=True, null=True, default="",
    )
    is_deleted = models.BooleanField("فعال/غیر فعال", null=True, blank=True, default=False, 
        editable=False
    )

    class Meta:
        verbose_name = "2-"+"مخاطب"
        verbose_name_plural = "2-"+"مخاطب"


class BookOwner(models.Model):
    user = models.ForeignKey(USER, blank=True, null=True, default="", on_delete=models.DO_NOTHING, verbose_name="کاربر")
    avatar = models.ForeignKey(Avatar, blank=True, null=True, default="", on_delete=models.DO_NOTHING, verbose_name="آواتار")
    status = models.BooleanField("فعال/غیر فعال", null=False, blank=False, default=True, 
        help_text="مشخص کنید در صورت فعال بودن کاربر مجاز خواهد بود برای خارج کردن از دسترس غیر فعال نمایید"
    )
    is_deleted = models.BooleanField("فعال/غیر فعال", null=True, blank=True, default=False, 
        editable=False
    )
    
    class Meta:
        verbose_name = "3-"+"کاربر های من"
        verbose_name_plural = "3-"+"کاربر های من"


class Book_UserManager(models.Manager):
    def get_all_books_by_user_or_none(self, user):
        try:
            return self.get_queryset().filter(
                book_owner__user=user, book_owner__status=True,
                book_phone__is_deleted=False, status=True, is_deleted=False,
            )
        except:
            return None

    def get_all_product_filterd_or_none(self, user, query):
        try:
            return self.get_queryset().filter(
                Q(book_phone__name__icontains=query)|Q(book_phone__last_name__icontains=query)|
                Q(book_phone__phone_number__startswith=query)|Q(book_phone__phone_number_1__startswith=query)|
                Q(book_phone__post__icontains=query),book_owner__user=user, book_owner__status=True,
                book_phone__is_deleted=False, status=True, is_deleted=False,
            ).distinct()
        except:
            return None


class Book_User(models.Model):
    book_owner = models.ForeignKey(BookOwner, blank=False, null=False, on_delete=models.DO_NOTHING, verbose_name="کاربر")
    book_phone = models.ForeignKey(BookPhone, blank=False, null=False, on_delete=models.DO_NOTHING, verbose_name="مخاطب")
    status = models.BooleanField("فعال/غیر فعال", null=False, blank=False, default=True, 
        help_text="مشخص کنید در صورت فعال بودن قابل انتخاب خواهد بود برای خارج کردن از دسترس غیر فعال نمایید"
    )
    is_deleted = models.BooleanField("فعال/غیر فعال", null=True, blank=True, default=False, 
        editable=False
    )

    objects = Book_UserManager()
    
    class Meta:
        verbose_name = "انتساب شماره به کاربر"
        verbose_name_plural = "انتساب شماره به کاربر"
