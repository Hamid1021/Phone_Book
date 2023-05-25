from django.contrib import admin
from phone_book.models import Avatar, BookOwner, BookPhone, Book_User

# Register your models here.
admin.site.register(Avatar)
admin.site.register(BookOwner)
admin.site.register(BookPhone)
admin.site.register(Book_User)