from django.urls import path, re_path
from . import views



app_name = "api_v1_courses"

urlpatterns = [
    # ===============user=============================
    re_path(r'^total-days/$',views.get_total_days, name="total-days"),
    re_path(r'^get-daily-topics/(?P<pk>.*)/$',views.get_daily_topics, name="daily-topics"),
    re_path(r'^daily-topic-complete/(?P<pk>.*)/$',views.daily_topic_complete, name="daily-topic-complete"), 
    re_path(r'^mark-as-complete/(?P<pk>.*)/$',views.mark_as_complete, name="mark-as-complete"), 
    # ===============admin=============================
    re_path(r'^add-daily-topics/$',views.add_daily_topics, name="add-daily-topics"),


]