from django.contrib import admin
from lms.models import Book, BookInstance, BorrowRecord, Reserve

# Register your models here.
admin.site.register(BorrowRecord)
admin.site.register(Book)
admin.site.register(BookInstance)
admin.site.register(Reserve)