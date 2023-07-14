import uuid

from django.db import models
from django.contrib.auth.models import Group, User

from general.models import BaseModel
from general.middlewares import RequestMiddleware
from general.functions import get_auto_id
from general.encryptions import encrypt


class StudentProfile(models.Model):
    # Basemodel
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_added = models.DateTimeField(db_index=True, auto_now_add=True)      
    is_deleted = models.BooleanField(default=False)

    # Auth user
    username = models.CharField(max_length=128, blank=True, null=True)
    user = models.OneToOneField("auth.User",on_delete=models.CASCADE, blank=True, null=True)
    password = models.TextField(blank=True, null=True)

    # Student data
    name = models.CharField(max_length=128, blank=True, null=True)
    phone = models.CharField(max_length=128, blank=True, null=True)
    country = models.ForeignKey('general.Country', on_delete=models.CASCADE, blank=True, null=True)
    admission_number = models.CharField(max_length=128, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    
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

    def save(self, *args, **kwargs):
        password = None
        if not self.creator:
            # First we need create an instance of that and later get the current_request assigned
            request = RequestMiddleware(get_response=None)
            request = request.thread_local.current_request

            if self._state.adding:
                auto_id = get_auto_id(ChiefProfile)
                chief_username = self.username
                if not self.password:
                    password = User.objects.make_random_password(length=12, allowed_chars="abcdefghjkmnpqrstuvwzyx#@*%$ABCDEFGHJKLMNPQRSTUVWXYZ23456789")
                else:
                    password = self.password

                user = User.objects.create_user(
                    username=chief_username,
                    password=password
                )

                chief_group, created = Group.objects.get_or_create(name='english_cafe')
                chief_group.user_set.add(user)
                self.creator = request.user
                self.updater = request.user
                self.auto_id = auto_id
                self.user = user
                self.password = encrypt(password)
        super(ChiefProfile, self).save(*args, **kwargs)

    class Meta:
        db_table = 'accounts_chief_profile'
        verbose_name = 'chief profile'
        verbose_name_plural = 'chief profiles'
        ordering = ('auto_id',)