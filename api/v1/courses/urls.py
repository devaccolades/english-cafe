from django.urls import path, re_path
from . import views



app_name = "api_v1_courses"

urlpatterns = [
    # ===============user=============================
    re_path(r'^programmes/$', views.programme_list, name="programmes"),
    re_path(r'^total-days/$',views.get_total_days, name="total-days"),
    re_path(r'^get-daily-topics/(?P<pk>.*)/$',views.get_daily_topics, name="daily-topics"),
    re_path(r'^daily-topic-complete/(?P<pk>.*)/$',views.daily_topic_complete, name="daily-topic-complete"), 
    re_path(r'^mark-as-complete/(?P<pk>.*)/$',views.mark_as_complete, name="mark-as-complete"), 


    # ===============admin=============================
    re_path(r'^add-programme/$',views.add_programme, name="add-programme"),
    re_path(r'^edit-programme/(?P<pk>.*)/$',views.edit_programme, name="edit-programme"),
    re_path(r'^add-daily-topics/$',views.add_daily_topics, name="add-daily-topics"),  # ================not-complete======================
    re_path(r'^days-list/(?P<pk>.*)/$',views.days_list_programme, name="list-of-days-in-programme"),
    re_path(r'^add-days/(?P<pk>.*)/$',views.add_days, name="add-days"),
    re_path(r'^add-day/(?P<pk>.*)/$',views.add_day, name="add-day"),

]