from django.contrib import admin
from .models import *



admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(OrederItem)
admin.site.register(Oreder)
admin.site.register(ShippingAddress)