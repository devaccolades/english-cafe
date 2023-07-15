from django.contrib import admin
from accounts.models import *

class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'admission_number')

admin.site.register(StudentProfile, StudentProfileAdmin)


class ChiefProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'username')

admin.site.register(ChiefProfile, ChiefProfileAdmin)
