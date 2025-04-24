from django.contrib import admin

# Register your models here.
from .models import User, Category, Transaction, Budget

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Transaction)
admin.site.register(Budget)