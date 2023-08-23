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
    re_path(r'^current-day/$',views.current_day, name="current-day"),

    # ===============admin=============================
    re_path(r'^get-admin-daily-topics/(?P<pk>.*)/$',views.get_admin_daily_topics, name="admin-daily-topics"),

    re_path(r'^add-programme/$',views.add_programme, name="add-programme"),
    re_path(r'^edit-programme/(?P<pk>.*)/$',views.edit_programme, name="edit-programme"),
    re_path(r'^programme/(?P<pk>.*)/$',views.programme, name="programme"),
    re_path(r'^delete-programme/(?P<pk>.*)/$',views.delete_programme, name="delete_programme"),

    re_path(r'^add-daily-topics/$',views.add_daily_topics, name="add-daily-topics"), 
    re_path(r'^daily-topic/(?P<pk>.*)/$',views.single_topic, name="add-daily-topics"), 
    re_path(r'^edit-daily-topics/(?P<pk>.*)/$',views.edit_daily_topics, name="edit-daily-topics"), 
    re_path(r'^delete-daily-topics/(?P<pk>.*)/$',views.delete_daily_topics, name="delete-daily-topics"), 

    re_path(r'^days-list/$',views.days_list_programme, name="list-of-days-in-programme"),
    re_path(r'^add-days/(?P<pk>.*)/$',views.add_days, name="add-days"),
    re_path(r'^add-day/(?P<pk>.*)/$',views.add_day, name="add-day"),
    re_path(r'^add-number-of-content-in-a-day/(?P<pk>.*)/$',views.add_number_of_content, name="add-day"),
    re_path(r'^number-of-content-in-a-day/(?P<pk>.*)/$',views.number_of_content, name="number-of-content-in-a-day"),
    re_path(r'^student-count/$',views.student_count, name="student-count"),





]