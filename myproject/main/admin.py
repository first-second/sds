from django.contrib import admin
from .models import Registration
# Register your models here.


class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('username', 'address', 'phone', 'email_address', 'date', 'photo')
    readonly_fields = ('display_photo',)

    def display_photo(self, obj):
        return obj.photo.url if obj.photo else ''

    display_photo.short_description = 'Photo'

admin.site.register(Registration, RegistrationAdmin)
