from django.urls import path, re_path
from . import views


app_name = "api_v1_company_profile"

urlpatterns =[
    # =================user==================
    re_path(r'^create-career-enquiry/$', views.create_career_enquiry, name="add-career-enquiry"),
    re_path(r'^company-count-data/$', views.company_count_data, name="company-count-data"),
    re_path(r'^create-enquiry-email/$', views.create_enquiry, name="send-email"),
    re_path(r'^get-galley/$', views.get_gallery, name="get-gallery"),
    re_path(r'^get-youtube-links/$', views.get_youtube_links, name="get-youtube-links"),
    re_path(r'^get-whatsapp-number/$', views.get_list_whatsapp_number, name="get-list-whatsapp-number"), 
    re_path(r'^get-whatsapp-number-user/$', views.get_list_whatsapp_number_user, name="get-list-whatsapp-number-user"), 

    # ================admin================
    re_path(r'^add-achievement/$', views.add_achievement, name="add-achievement"),
    re_path(r'^achievements/$', views.achievements_view, name="list-achievement"),
    re_path(r'^edit-achievement/(?P<pk>.*)/$', views.edit_achievements, name="edit-achievement"),
    re_path(r'^achievement/(?P<pk>.*)/$', views.single_achievements, name="single-achievement"),
    re_path(r'^delete-achievement/(?P<pk>.*)/$', views.delete_achievements, name="delete-achievement"),

    re_path(r'^add-testimonials/$', views.add_testimonials, name="add-testimonials"),
    re_path(r'^testimonials/$', views.view_testimonials, name="list-testimonials"),
    re_path(r'^edit-testimonials/(?P<pk>.*)/$', views.edit_testimonials, name="edit-testimonials"),
    re_path(r'^testimonial/(?P<pk>.*)/$', views.single_testimonials, name="single-testimonials"),
    re_path(r'^delete-testimonial/(?P<pk>.*)/$', views.delete_testimonials, name="delete-testimonials"),

    re_path(r'^get-department/$', views.get_department, name="get-department"),
    re_path(r'^add-our-team/$', views.add_our_team, name="add-our-team"),
    re_path(r'^get-our-team/$', views.get_our_team, name="get-our-team"),
    re_path(r'^get-our-team-admin/$', views.get_our_team_admin, name="get-our-team-admin"),
    re_path(r'^our-team/(?P<pk>.*)/$', views.our_team, name="get-our-team"),
    re_path(r'^edit-our-team/(?P<pk>.*)/$', views.edit_our_team, name="edit-our-team"),
    re_path(r'^delete-our-team/(?P<pk>.*)/$', views.delete_our_team, name="delete-our-team"),

    re_path(r'^add-careers/$', views.add_careers, name="add_career"),
    re_path(r'^get-careers/$', views.view_careers, name="get_career"),
    re_path(r'^delete-careers/(?P<pk>.*)/$', views.delete_careers, name="delete_career"),

    re_path(r'^get-career-enquiry/$', views.get_career_enquiry, name="get-career-enquiry"),
    re_path(r'^get-enquiry/$', views.get_enquiry, name="get-enquiry"),
    re_path(r'^enquiry/download/$', views.get_enquiry_list_download, name="enquiry-list-download"),

    re_path(r'^add-company-profile-count/$', views.add_company_profile_count, name="add-company-profile-count"),
    re_path(r'^get-company-profile-count/$', views.get_company_profile_count, name="get-company-profile-count"),
    re_path(r'^edit-company-profile-count/(?P<pk>.*)/$', views.edit_company_profile_count, name="edit-company-profile-count"),

    re_path(r'^add-gallery-image/$', views.add_gallery_image, name="add-gallery"),
    re_path(r'^get-galleries-admin/$', views.get_galleries, name="get-gallery"),
    re_path(r'^delete-gallery-image/(?P<pk>.*)/$', views.delete_gallery_image, name="delete-gallery"),

    re_path(r'^get-whatsapp-number/$', views.get_list_whatsapp_number, name="get-list-whatsapp-number"), 
    re_path(r'^single-whatsapp-number/(?P<pk>.*)/$', views.single_whatsapp_number, name="single-whatsapp-number"), 
    re_path(r'^edit-whatsapp-number/(?P<pk>.*)/$', views.edit_whatsapp_number, name="edit-whatsapp-number"), 

]