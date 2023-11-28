from django.contrib import admin
from .models import MainBooks, Category, Framework, BookBought

# Register your models here.
admin.site.register(MainBooks)
admin.site.register(Category)
admin.site.register(Framework)
admin.site.register(BookBought)
