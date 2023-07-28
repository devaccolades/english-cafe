import uuid
import re

from django.db import models

from general.models import BaseModel


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
    no_of_contents = models.CharField(max_length=255, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)


    class Meta:
        db_table = 'courses_day'
        verbose_name = ('Day')
        verbose_name_plural = ('Days')
        ordering = ('day_number',)

    def __str__(self):
        return "{}_{}".format(self.programme.__str__(), self.day_number)


class DailyTopics(BaseModel):
    daily_audio_topic = models.ForeignKey("courses.DailyAudioTopic", on_delete=models.CASCADE, null=True, blank=True)
    daily_video_topic = models.ForeignKey("courses.DailyVideoTopic", on_delete=models.CASCADE, null=True, blank=True)
    daily_text_topic = models.ForeignKey("courses.DailyTextTopic", on_delete=models.CASCADE, blank=True, null=True)
    daily_image_topic = models.ForeignKey("courses.DailyImageTopic", on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'courses_daily_topic'
        verbose_name = ('Daily Topic')
        verbose_name_plural = ('Daily Topics')
        ordering = ('id',)

    def __str__(self):
        return "{}-{}".format(self.daily_audio_topic.__str__(),self.daily_video_topic.__str__(),self.daily_text_topic.__str__())


class StudentDay(BaseModel):
    day = models.ForeignKey("courses.Day", on_delete=models.CASCADE)
    student = models.ForeignKey("accounts.StudentProfile", on_delete=models.CASCADE)
    status = models.CharField(max_length=128, choices=STUDENT_DAY_STATUS_CHOICES, default="ongoing")
    is_completed = models.BooleanField(default=False)

    class Meta:
        db_table = 'courses_student_day'
        verbose_name = ('Student Day')
        verbose_name_plural = ('Student Days')
        ordering = ('id',)

    def __str__(self):
        return "{}-{}".format(self.day.__str__(),self.student.__str__())
    

class DailyAudioTopic(BaseModel):
    day = models.ForeignKey('courses.Day', on_delete=models.CASCADE, null=True, blank=True)
    audio = models.FileField(upload_to="courses/audio/", null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    next_topic_id = models.CharField(max_length=255,null=True, blank=True)
    order_id = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        db_table = 'courses_daily_audio_topic'
        verbose_name = ('Daily Audio topic')
        verbose_name_plural = ('Daily Audio topics')
        ordering = ('id',)
    
    def __str__(self):
        return "{}-{}".format(self.day.__str__(), self.audio.__str__())

    
class StudentDailyAudioTopic(BaseModel):
    daily_audio_topic = models.ForeignKey("courses.DailyAudioTopic", on_delete=models.CASCADE, null=True, blank=True)
    student_profile = models.ForeignKey("accounts.StudentProfile", on_delete=models.CASCADE, null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    is_processed = models.BooleanField(default=False)

    class Meta:
        db_table = 'courses_student_daily_audio_topic'
        verbose_name = ('Student Daily Audio topic')
        verbose_name_plural = ('Student Daily Audio topics')
        ordering = ('id',)

    def __str__(self):
        return "{}-{}".format(self.daily_audio_topic.__str__(), self.student_profile.__str__()) 
    

class DailyVideoTopic(BaseModel):
    day = models.ForeignKey('courses.Day', on_delete=models.CASCADE, null=True, blank=True)
    video = models.FileField(upload_to="courses/video/", null=True, blank=True)
    next_topic_id = models.CharField(max_length=255,null=True, blank=True)
    order_id = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        db_table = 'courses_daily_video_topic'
        verbose_name = ('Daily Video topic')
        verbose_name_plural = ('Daily Video topics')
        ordering = ('id',)
    
    def __str__(self):
        return "{}-{}".format(self.day.__str__(), self.video.__str__()) 
    

class StudentDailyVideoTopic(BaseModel):
    daily_video_topic = models.ForeignKey("courses.DailyVideoTopic", on_delete=models.CASCADE, null=True, blank=True)
    student_profile = models.ForeignKey("accounts.StudentProfile", on_delete=models.CASCADE, null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    is_processed = models.BooleanField(default=False)


    class Meta:
        db_table = 'courses_student_daily_video_topic'
        verbose_name = ('Student Daily Video topic')
        verbose_name_plural = ('Student Daily Video topics')
        ordering = ('id',)

    def __str__(self):
        return "{}-{}".format(self.daily_video_topic.__str__(), self.student_profile.__str__()) 
    

class DailyTextTopic(BaseModel):
    day = models.ForeignKey('courses.Day', on_delete=models.CASCADE, null=True, blank=True)
    daily_text = models.TextField(null=True, blank=True)
    next_topic_id = models.CharField(max_length=255,null=True, blank=True)
    order_id = models.PositiveIntegerField( null=True, blank=True)


    class Meta:
        db_table = 'courses_daily_text_topic'
        verbose_name = ('Daily Text Topic')
        verbose_name_plural = ('Daily Text Topics')
        ordering = ('id',)

    def __str__(self):
        return "{}-{}".format(self.day.__str__(), self.daily_text.__str__()) 
    

class StudentDailyTextTopic(BaseModel):
    daily_text_topic = models.ForeignKey("courses.DailyTextTopic", on_delete=models.CASCADE, blank=True, null=True)
    student_profile = models.ForeignKey("accounts.StudentProfile", on_delete=models.CASCADE, null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    is_processed = models.BooleanField(default=False)


    class Meta:
        db_table = 'courses_student_daily_text_topic'
        verbose_name = ('Student Daily Text Topic')
        verbose_name_plural = ('Student Daily Text Topics')
        ordering = ('id',)

    def __str__(self):
        return "{}-{}".format(self.daily_text_topic.__str__(), self.student_profile.__str__()) 
    

class DailyImageTopic(BaseModel):
    day = models.ForeignKey('courses.Day', on_delete=models.CASCADE, null=True, blank=True)
    daily_image = models.FileField(upload_to="courses/image", blank=True, null=True)
    next_topic_id = models.CharField(max_length=255,null=True, blank=True)
    order_id = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'courses_daily_image_topic'
        verbose_name = ('Daily Image Topic')
        verbose_name_plural = ('Daily Image Topics')
        ordering = ('id',)

    def __str__(self):
        return "{}-{}".format(self.day.__str__(), self.daily_image.__str__()) 
    

class StudentDailyImageTopic(BaseModel):
    daily_image_topic = models.ForeignKey("courses.DailyImageTopic", on_delete=models.CASCADE, blank=True, null=True)
    student_profile = models.ForeignKey("accounts.StudentProfile", on_delete=models.CASCADE, null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    is_processed = models.BooleanField(default=False)



    class Meta:
        db_table = 'courses_student_daily_image_topic'
        verbose_name = ('Student Daily Image Topic')
        verbose_name_plural = ('Student Daily Image Topics')
        ordering = ('id',)

    def __str__(self):
        return "{}-{}".format(self.daily_image_topic.__str__(), self.student_profile.__str__()) 








    







    
    




    
    


