import uuid
from django.db import models

from ckeditor.fields import RichTextField
from django.template.defaultfilters import slugify



class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    auto_id = models.PositiveIntegerField(db_index=True,unique=True)
    date_added = models.DateTimeField(db_index=True,auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Country(models.Model):
    name = models.CharField(max_length=128)
    web_code = models.CharField(max_length=128)
    country_code = models.CharField(max_length=128,blank=True,null=True)
    flag = models.ImageField(upload_to="countries/flags/",blank=True,null=True)
    phone_code = models.CharField(max_length=128,blank=True,null=True)
    is_active = models.BooleanField(default=True)
    phone_number_length = models.PositiveIntegerField(blank=True,null=True)

    class Meta:
        db_table = 'general_country'
        verbose_name = ('country')
        verbose_name_plural = ('countries')
        ordering = ('name',)

    def __str__(self):
        return self.name
    

class Blog(BaseModel):
    title = models.CharField(max_length=125, null=True, blank=True)
    sub_title = models.CharField(max_length=125, null=True, blank=True)
    description = RichTextField()
    thumbnail = models.ImageField(upload_to="blogs/images/", null=True, blank=True)
    thumbnail_alt = models.CharField(max_length=125, null=True, blank=True)
    image = models.ImageField(upload_to="blogs/images/", null=True, blank=True)
    image_alt = models.CharField(max_length=125, null=True, blank=True)
    author = models.CharField(max_length=125, null=True, blank=True)
    meta_title = models.CharField(max_length=200, null=True, blank=True)
    meta_description = models.CharField(max_length=200, null=True, blank=True)
    slug = models.SlugField(unique=True, default="")
    created_at = models.DateField(null=True, blank=True)
    tags = models.ManyToManyField("general.Tags", blank=True)

    class Meta:
        db_table = 'company_profile_blog'
        verbose_name = ('Blog')
        verbose_name_plural = ('Blogs')
        ordering = ('id',)

    def __str__(self):
        return self.title


class Tags(BaseModel):
    name = models.CharField(max_length=125, null=True, blank=True)

    class Meta:
        db_table = 'company_profile_tags'
        verbose_name = ('Tag')
        verbose_name_plural = ('Tags')
        ordering = ('date_added',)

    def __str__(self):
        return self.name






        