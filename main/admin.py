from django.contrib import admin
from .models import User, Category, ItemInOrder, Order

admin.site.register(User)
admin.site.register(Category)
admin.site.register(ItemInOrder)
admin.site.register(Order)

