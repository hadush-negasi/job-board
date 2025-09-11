from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.conf.urls import handler403, handler404, handler500

def home(request):
    return render(request, "home.html")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path("jobs/", include("jobs.urls")),
    path("applications/", include("applications.urls")),
    path('', home, name="home"),
]

# Custom error handlers
handler403 = 'jobboard.views.custom_403_view'
handler404 = 'jobboard.views.custom_404_view'
handler500 = 'jobboard.views.custom_500_view'
