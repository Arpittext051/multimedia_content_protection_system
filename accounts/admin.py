from django.contrib import admin
from .models import *
# Register your models here.



@admin.register(Upload)
class UploadAdmin(admin.ModelAdmin):
    list_display =['id']

