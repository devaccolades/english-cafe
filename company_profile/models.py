from django.db import models
from general.models import BaseModel


COMPANY_PROFILE_JOB_DESIGNATION = (
    ('ceo', 'CEO'),
    ('managing_director', 'Managing Director'),
    ('language_trainer', 'Language Trainer'),
    ('admission_counsellor', 'Admission Counsellors'),
    ('ielts_trainer', 'IELTS Trainer'),
    ('video_presenter', 'Video Presenter'),
    ('content_writers', 'Content Writer'),
    ('telecaller', 'Telecaller')
)

COMPANY_PROFILE_JOB_TYPE = (
    ('full_time', 'Full Time'),
    ('part_timr', 'Part Time')
)

COMPANY_PROFILE_GALLERY_TYPE = (
    ('image', 'Image'),
    ('video', 'video'),
    ('link', 'Link')
)

COMPANY_PROFILE_GALLERY_SLOT = (
    ('slot_1', 'Slot 1'),
    ('slot_2', 'Slot 2'),
    ('slot_3', 'Slot 3'),
    ('slot_4', 'Slot 4'),
    ('slot_5', 'Slot 5'),
    ('slot_6', 'Slot 6'),
    ('slot_7', 'Slot 7'),
    ('slot_8', 'Slot 8'),
)

class Achievements(BaseModel):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="company-profile/images/", blank=True, null=True)
    alt = models.CharField(max_length=255,null=True, blank=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'company_profile_achievements'
        verbose_name = ('Achievement')
        verbose_name_plural = ('Achievements')
        ordering = ('id',)

    def __str__(self):
        return self.title
    

class Testimonials(BaseModel):
    name = models.CharField(max_length=255)
    quote = models.TextField()
    rating_count = models.PositiveIntegerField()
    image = models.ImageField(upload_to="company_profile/testimonials/images",  null=True, blank=True)
    alt = models.CharField(max_length=255,null=True, blank=True)
    video = models.FileField(upload_to="company_profile/testimonials/video")

    class Meta:
        db_table = 'company_profile_testimonials'
        verbose_name = ('Testimonial')
        verbose_name_plural = ('Testimonials')
        ordering = ('id',)

    def __str__(self):
        return self.name


class Department(BaseModel):
    name = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'company_profile_deparment'
        verbose_name = ('Department')
        verbose_name_plural = ('Department')
        ordering = ('id',)

    def __str__(self):
        return self.name


class OurTeam(BaseModel):
    name = models.CharField(max_length=255)
    photo = models.FileField(upload_to="company_profile/our_team/photo", null=True, blank=True)
    designation = models.CharField(max_length=255)
    alt = models.CharField(max_length=255,null=True, blank=True)
    head = models.BooleanField(default=False)
    department = models.ForeignKey("company_profile.Department", on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'company_profile_our_team'
        verbose_name = ('Our Team')
        verbose_name_plural = ('Our Teams')
        ordering = ('id',)

    def __str__(self):
        return self.name


class Career(BaseModel):
    designation = models.CharField(max_length=255)
    job_description = models.TextField()
    job_type = models.CharField(choices=COMPANY_PROFILE_JOB_TYPE, max_length=255)

    class Meta:
        db_table = 'company_profile_career'
        verbose_name = ('Career')
        verbose_name_plural = ('Careers')
        ordering = ('id',)

    def __str__(self):
        return self.designation
    

class CareerEnquiry(BaseModel):
    job = models.ForeignKey('company_profile.Career', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=110)
    email = models.CharField(max_length=110)
    cv = models.FileField(upload_to="company_profile/career_enquiry/cv/")

    class Meta:
        db_table = 'company_profile_career_enquiry'
        verbose_name = ('Career Enquiry')
        verbose_name_plural = ('Careers Enquiry')
        ordering = ('id',)

    def __str__(self):
        return self.name
    

class Enquiry(BaseModel):
    name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    message = models.TextField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'company_profile__enquiry'
        verbose_name = (' Enquiry')
        verbose_name_plural = ('Enquiries')
        ordering = ('id',)

    def __str__(self):
        return self.name
    

class CompanyCount(BaseModel):
    successfull_students = models.IntegerField( null=True, blank=True)
    languages_trainee = models.IntegerField( null=True, blank=True)
    awards_won = models.IntegerField( null=True, blank=True)
    courses = models.IntegerField( null=True, blank=True)

    class Meta:
        db_table = 'courses_company_count'
        verbose_name = ('Company Count')
        verbose_name_plural = ('Company Count')
        ordering = ('id',)
    
    def __str__(self):
        return str(self.successfull_students)
    

class Gallery(BaseModel):
    type = models.CharField(choices=COMPANY_PROFILE_GALLERY_TYPE, max_length=255)
    file = models.FileField(upload_to='company_profile/gallery/', null=True, blank=True)
    alt = models.CharField(max_length=255,null=True, blank=True)
    file_link = models.CharField(max_length=255, null=True, blank=True)
    slot = models.CharField(choices=COMPANY_PROFILE_GALLERY_SLOT, max_length=122, null=True, blank=True)
    
    class Meta:
        db_table = 'courses_gallery'
        verbose_name = ('Gallery')
        verbose_name_plural = ('Galleries')
        ordering = ('id',)

    def __str__(self):
        return self.type


