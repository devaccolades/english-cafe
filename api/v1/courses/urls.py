from django.urls import path, re_path
from . import views



app_name = "api_v1_courses"

urlpatterns = [
    re_path(r'^get-daily-topics/(?P<pk>.*)/$',views.get_daily_topics, name="daily-topics")
]