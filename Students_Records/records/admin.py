from django.contrib import admin
from .models import Records

admin.site.register(Records)

class RecordsAdmin(admin.ModelAdmin):
    list_display = ('name','stack','created_at')
