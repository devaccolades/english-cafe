from django.contrib import admin
from company_profile.models import *

class AchievementAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'description')

admin.site.register(Achievements, AchievementAdmin)


class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'quote', 'image', 'video')


admin.site.register(Testimonials, TestimonialAdmin)


class OurTeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'photo', 'designation')

admin.site.register(OurTeam, OurTeamAdmin)


class CareerAdmin(admin.ModelAdmin):
    list_display = ('id', 'designation', 'job_type', 'job_description')

admin.site.register(Career, CareerAdmin)


class CareerEnquiryAdmin(admin.ModelAdmin):
    list_display = ('id', 'job','name', 'phone', 'email', 'cv')

admin.site.register(CareerEnquiry, CareerEnquiryAdmin)


class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'email', 'message')

admin.site.register(Enquiry, EnquiryAdmin)
