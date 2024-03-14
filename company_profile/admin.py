from django.contrib import admin
from company_profile.models import *

class AchievementAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'description', "alt")

admin.site.register(Achievements, AchievementAdmin)


class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'quote', 'image', 'video', "alt")


admin.site.register(Testimonials, TestimonialAdmin)


class OurTeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'photo', 'designation', "alt")

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


class CompanyCountAdmin(admin.ModelAdmin):
    list_display = ('id', 'successfull_students', 'languages_trainee', 'awards_won', 'courses')

admin.site.register(CompanyCount, CompanyCountAdmin)


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

admin.site.register(Department, DepartmentAdmin)


class GalleryAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'file', 'file_link', "alt")

admin.site.register(Gallery, GalleryAdmin)


class WhatsAppNumberEnquiryAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone')

admin.site.register(WhatsAppNumberEnquiry, WhatsAppNumberEnquiryAdmin)
