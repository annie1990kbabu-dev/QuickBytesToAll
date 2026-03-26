from django.contrib import admin
from .models import Food, Category
from django.contrib import admin
from .models import AdminUser
admin.site.register(AdminUser)

admin.site.register(Food)
admin.site.register(Category)



# Register your models here.
