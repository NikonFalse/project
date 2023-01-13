from django.contrib import admin
from .models import JobInformation
# Register your models here.
@admin.register(JobInformation)
class AdminJobInformation(admin.ModelAdmin):
    list_display = ['name','year','city','salary','skills']