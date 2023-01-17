from django.contrib import admin
from .models import Main
from .models import Registration
# Register your models here.

#admin.site.register(Main)
class RegistrationAdmin(admin.ModelAdmin):

    search_fields=['name','address','phone','date']
admin.site.register(Registration,RegistrationAdmin)
