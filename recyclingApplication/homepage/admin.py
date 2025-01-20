from django.contrib import admin

from .models import *
# Register your models here.

class RequestAdmin(admin.ModelAdmin):
  list_display = ["first_name", "last_name"]

admin.site.register(Request, RequestAdmin)