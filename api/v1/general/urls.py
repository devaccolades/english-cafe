from django.urls import path, re_path
from . import views

app_name = "api_v1_general"

urlpatterns = [
    re_path(r'^list-blogs/$', views.list_blogs, name="programmes"),

]