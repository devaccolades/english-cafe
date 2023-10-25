from django.urls import path, re_path
from . import views

app_name = "api_v1_general"

urlpatterns = [
    re_path(r'^list-blogs/$', views.list_blogs, name="programmes"),
    re_path(r'^list-tags/$', views.list_tags, name="tags"),
    re_path(r'^list-blogs-tags/(?P<pk>.*)/$', views.list_blogs_tags, name="blog-tags"),
    path('single-blogs/<slug:slug>/', views.single_blog, name="single-blog"),

]