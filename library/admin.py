from django.contrib import admin
from .models import Librarian, Book, DamagedBook, BorrowedBook

# Register your models here.
admin.site.register(Librarian)
admin.site.register(Book)
admin.site.register(BorrowedBook)
admin.site.register(DamagedBook)