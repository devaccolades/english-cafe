from django.urls import path, re_path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)
from . import views

app_name = "api_v1_accounts"

urlpatterns = [

    re_path(r'^chief-login/$', views.chief_profile_login, name="login-chief"),
    re_path(r'^create-student-profile/$', views.create_student_profile, name="create-student"),
    re_path(r'^login-student-profile/$', views.login_student_profile, name="login-student"),

    re_path(r'^get-students/$',views.students, name="student-list"),
    re_path(r'^student/(?P<pk>.*)/$',views.student, name="student-list"),
    re_path(r'^edit-students/(?P<pk>.*)/$',views.edit_students, name="student-edit"),


    
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]