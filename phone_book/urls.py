from django.urls import path
from phone_book.views import profile, phone_book_view, add_phone_book, del_phone_book, search_phone_book

app_name = "phone_book"

urlpatterns = [
    path("profile", profile, name="profile"),
    path("books", phone_book_view, name="books"),
    path("books/add_phone_book", add_phone_book, name="add_books"),
    path("books/del_phone_book", del_phone_book, name="del_books"),
    path("books/search_phone_book", search_phone_book, name="search_books"),
]
