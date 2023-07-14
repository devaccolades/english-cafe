from django.contrib import admin
from django.urls import path

admin.site.site_header = "English Cafe Admin"
admin.site.site_title = "English Cafe Admin"
admin.site.index_title = "Welcome to English Cafe Admin Portal"

urlpatterns = [
    path('85a7d858-1370-4f11-b2bb-c914f0d9db4a/', admin.site.urls),
]
