from django.contrib import admin
from .models import News, Publications, Updates

# Register your models here.

admin.site.register(News)
admin.site.register(Publications)
admin.site.register(Updates)
