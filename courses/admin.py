from django.contrib import admin
from .models import *


class DayAdmin(admin.ModelAdmin):
    list_display = ('id', 'programme', 'day_number')
    ordering = ('day_number', )
admin.site.register(Day, DayAdmin)

class ProgrammeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'duration', 'description', 'order_id')
admin.site.register(Programme, ProgrammeAdmin)


admin.site.register(DailyTopics)

# class StudentDayAdmin(admin.ModelAdmin):
#     list_display = ('id', '')
