from django.urls import path, re_path
from . import views


app_name = "api_v1_company_profile"

urlpatterns =[
    # =================user==================
    re_path(r'^create-career-enquiry/$', views.create_career_enquiry, name="add-career-enquiry"),

    # ================admin================
    re_path(r'^add-achievement/$', views.add_achievement, name="add-achievement"),
    re_path(r'^achievements/$', views.achievements_view, name="list-achievement"),
    re_path(r'^edit-achievement/(?P<pk>.*)/$', views.edit_achievements, name="edit-achievement"),
    re_path(r'^achievement/(?P<pk>.*)/$', views.single_achievements, name="single-achievement"),

    re_path(r'^add-testimonials/$', views.add_testimonials, name="add-testimonials"),
    re_path(r'^testimonials/$', views.view_testimonials, name="list-testimonials"),
    re_path(r'^edit-testimonials/(?P<pk>.*)/$', views.edit_testimonials, name="edit-testimonials"),
    re_path(r'^testimonial/(?P<pk>.*)/$', views.single_testimonials, name="single-testimonials"),
    re_path(r'^delete-testimonial/(?P<pk>.*)/$', views.delete_testimonials, name="delete-testimonials"),

    re_path(r'^add-our-team/$', views.add_our_team, name="add-our-team"),
    re_path(r'^get-our-team/$', views.get_our_team, name="get-our-team"),
    re_path(r'^delete-our-team/(?P<pk>.*)/$', views.delete_our_team, name="delete-our-team"),

    re_path(r'^add-careers/$', views.add_careers, name="add_career"),
    re_path(r'^get-careers/$', views.view_careers, name="get_career"),
    re_path(r'^delete-careers/(?P<pk>.*)/$', views.delete_careers, name="delete_career"),

    re_path(r'^get-career-enquiry/$', views.get_career_enquiry, name="get-career-enquiry"),

]