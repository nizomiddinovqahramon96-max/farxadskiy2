from django.contrib import admin
from .models import Elon, ImageElon, CustomUser
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Elon)
admin.site.register(ImageElon)
