from django.contrib import admin
from cafe.models import *
# Register your models here.

admin.site.register(User)
admin.site.register(menu_item)
admin.site.register(rating)
admin.site.register(order)
admin.site.register(bill)