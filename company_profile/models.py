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

class Achievements(BaseModel):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="company-profile/images/", blank=True, null=True)
    description = models.TextField()

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
    image = models.ImageField(upload_to="company_profile/testimonials/images")
    video = models.FileField(upload_to="company_profile/testimonials/video")

    class Meta:
        db_table = 'company_profile_testimonials'
        verbose_name = ('Testimonial')
        verbose_name_plural = ('Testimonials')
        ordering = ('id',)

    def __str__(self):
        return self.name


class OurTeam(BaseModel):
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to="company_profile/our_team/photo")
    designation = models.CharField(choices=COMPANY_PROFILE_JOB_DESIGNATION, max_length=255)

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
       



