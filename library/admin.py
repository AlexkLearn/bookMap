from django.contrib import admin
from .models import Book, DamagedBook, BorrowedBook

# Register your models here.
admin.site.register(Book)
admin.site.register(BorrowedBook)
admin.site.register(DamagedBook)