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

class DailyAudioTopicAdmin(admin.ModelAdmin):
    list_display = ('auto_id','id', 'day', 'audio',  'order_id')

admin.site.register(DailyAudioTopic, DailyAudioTopicAdmin)


class StudentDailyAudioTopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'daily_audio_topic', 'student_profile', 'is_completed')

admin.site.register(StudentDailyAudioTopic, StudentDailyAudioTopicAdmin)


class DailyVideoTopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'day', 'video', 'order_id')

admin.site.register(DailyVideoTopic, DailyVideoTopicAdmin)


class StudentDailyVideoTopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'daily_video_topic', 'student_profile', 'is_completed')

admin.site.register(StudentDailyVideoTopic, StudentDailyVideoTopicAdmin)


class DailyTextTopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'day', 'daily_text', 'order_id')

admin.site.register(DailyTextTopic, DailyTextTopicAdmin)


class StudentDailyTextTopicAdmin(admin.ModelAdmin):
    list_display = ("id", "daily_text_topic", "student_profile", "is_completed")

admin.site.register(StudentDailyTextTopic,StudentDailyTextTopicAdmin)


class DailyImageTopicAdmin(admin.ModelAdmin):
    list_display = ("id", "day", "daily_image", "order_id", "alt")

admin.site.register(DailyImageTopic, DailyImageTopicAdmin)


class StudentDailyImageTopicAdmin(admin.ModelAdmin):
    list_display = ("id", "daily_image_topic", "student_profile", "is_completed")

admin.site.register(StudentDailyImageTopic, StudentDailyImageTopicAdmin)


class StudentDayAdmin(admin.ModelAdmin):
    list_display = ("id", "day", "student", "status", "is_completed")

admin.site.register(StudentDay, StudentDayAdmin)

