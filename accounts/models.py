import uuid

from django.db import models
from django.contrib.auth.models import Group, User

from general.models import BaseModel
# from general.middlewares import RequestMiddleware
# from general.functions import get_auto_id
# from general.encryptions import encrypt


class StudentProfile(models.Model):
    # Basemodel
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_added = models.DateTimeField(db_index=True, auto_now_add=True)      
    is_deleted = models.BooleanField(default=False)
    auto_id = models.PositiveIntegerField(db_index=True,unique=True)

    # Auth user
    username = models.CharField(max_length=128, blank=True, null=True, unique=True)
    user = models.OneToOneField("auth.User",on_delete=models.CASCADE, blank=True, null=True)
    password = models.TextField(blank=True, null=True)

    # Student data
    name = models.CharField(max_length=128, blank=True, null=True)
    phone = models.CharField(max_length=128, blank=True, null=True)
    # country = models.ForeignKey('general.Country', on_delete=models.CASCADE, blank=True, null=True)
    admission_number = models.CharField(max_length=128, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    programmes = models.ForeignKey('courses.Programme', on_delete=models.CASCADE, blank=True, null=True)
    
    class Meta:
        db_table = 'accounts_student_profile'
        verbose_name = ('student profile')
        verbose_name_plural = ('student profiles')
        ordering = ('name',)
        
    def __str__(self):
        if self.name:
            return self.name
        else:
            return self.phone
        
class ChiefProfile(BaseModel):
    username = models.CharField(max_length=128)
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    password = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'accounts_chief_profile'
        verbose_name = 'chief profile'
        verbose_name_plural = 'chief profiles'
        ordering = ('auto_id',)