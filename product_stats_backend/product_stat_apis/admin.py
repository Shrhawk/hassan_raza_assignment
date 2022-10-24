from django.contrib import admin

from product_stat_apis.models import User, UserSales, Country, City

admin.site.register(User)
admin.site.register(UserSales)
admin.site.register(Country)
admin.site.register(City)
