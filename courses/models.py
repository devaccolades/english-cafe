import uuid
import re

from django.db import models

from general.models import BaseModel
from general.middlewares import RequestMiddleware
from general.functions import get_auto_id


STUDENT_DAY_STATUS_CHOICES = (
    ('locked', 'Locked'),
    ('ongoing', 'Ongoing'),
    ('completed', 'Completed'),
)


class Programme(BaseModel):
    name = models.CharField(max_length=255)
    duration = models.CharField(max_length=155)
    description = models.TextField()
    order_id = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        if not self.creator:
            # First we need create an instance of that and later get the current_request assigned
            request = RequestMiddleware(get_response=None)
            request = request.thread_local.current_request

            if self._state.adding:
                auto_id = get_auto_id(Programme)
                self.creator = request.user
                self.updater = request.user
                self.auto_id = auto_id

                self.search_campus_name = "".join(re.sub("[^a-zA-Z]+", "", self.name).lower())

            
        super(Programme, self).save(*args, **kwargs)

    class Meta:
        db_table = 'courses_programme'
        verbose_name = ('Programme')
        verbose_name_plural = ('Programmes')
        ordering = ('id',)

    def __str__(self):
        return self.name


class Day(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    programme = models.ForeignKey('courses.Programme', on_delete=models.CASCADE, null=True, blank=True)
    day_number = models.CharField(max_length=255)
    no_of_contents = models.CharField(max_length=255)

    class Meta:
        db_table = 'courses_day'
        verbose_name = ('Day')
        verbose_name_plural = ('Days')
        ordering = ('id',)

    def __str__(self):
        return "{}_{}".format(self.programme.__str__(), self.day_number)


class DailyTopics(BaseModel):
    day = models.ForeignKey("courses.Day", on_delete=models.CASCADE, null=True, blank=True)
    video_url_1 = models.CharField(max_length=255, null=True, blank=True)
    video_url_2 = models.CharField(max_length=255, null=True, blank=True)
    video_url_3 = models.CharField(max_length=255, null=True, blank=True)
    text_1 = models.TextField()
    text_2 = models.TextField()
    text_3 = models.TextField()
    audio_1 = models.CharField(max_length=255, null=True, blank=True)
    audio_2 = models.CharField(max_length=255, null=True, blank=True)
    audio_3= models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(max_length=255, null=True, blank=True)
    order_id = models.CharField(max_length=125)

    def save(self, *args, **kwargs):
        if not self.creator:
            # First we need create an instance of that and later get the current_request assigned
            request = RequestMiddleware(get_response=None)
            request = request.thread_local.current_request

            if self._state.adding:
                auto_id = get_auto_id(DailyTopics)
                self.auto_id = auto_id

                self.search_campus_name = "".join(re.sub("[^a-zA-Z]+", "", self.name).lower())

            
        super(DailyTopics, self).save(*args, **kwargs)

    class Meta:
        db_table = 'courses_daily_topics'
        verbose_name = ('Daily topic')
        verbose_name_plural = ('Daily topics')
        ordering = ('id',)

    def __str__(self):
        return "{}_{}".format(self.day.__str__())
    

class StudentDay(BaseModel):
    day = models.ForeignKey("courses.Day", on_delete=models.CASCADE)
    student = models.ForeignKey("accounts.StudentProfile", on_delete=models.CASCADE)
    status = models.CharField(max_length=128, choices=STUDENT_DAY_STATUS_CHOICES, default="ongoing")
    is_completed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.creator:
            # First we need create an instance of that and later get the current_request assigned
            request = RequestMiddleware(get_response=None)
            request = request.thread_local.current_request

            if self._state.adding:
                auto_id = get_auto_id(StudentDay)
                self.auto_id = auto_id

                self.search_campus_name = "".join(re.sub("[^a-zA-Z]+", "", self.name).lower())

            
        super(StudentDay, self).save(*args, **kwargs)

    class Meta:
        db_table = 'courses_student_day'
        verbose_name = ('Student Day')
        verbose_name_plural = ('Student Days')
        ordering = ('id',)

    def __str__(self):
        return "{}-{}".format(self.day.__str__(),self.student.__str__())
    
    




    
    


