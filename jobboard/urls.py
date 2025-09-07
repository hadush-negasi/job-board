from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

def home(request):
    return render(request, "home.html")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path("jobs/", include("jobs.urls")),
    path("applications/", include("applications.urls")),
    path('', home, name="home"),
]
