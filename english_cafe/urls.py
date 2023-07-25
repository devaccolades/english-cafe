from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings

admin.site.site_header = "English Cafe Admin"
admin.site.site_title = "English Cafe Admin"
admin.site.index_title = "Welcome to English Cafe Admin Portal"

urlpatterns = [
    path('85a7d858-1370-4f11-b2bb-c914f0d9db4a/', admin.site.urls),

    path('api/v1/accounts/', include('api.v1.accounts.urls', namespace='api_v1_accounts')),
    path('api/v1/courses/', include('api.v1.courses.urls', namespace='api_v1_courses')),
    path('api/v1/company_profile/', include('api.v1.company_profile.urls', namespace='api_v1_company_profile')),

    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]
