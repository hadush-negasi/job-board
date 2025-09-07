from django.urls import path
from . import views

urlpatterns = [
    path("apply/<int:job_id>/", views.apply_job, name="apply_job"),
    path("job/<int:job_id>/applications/", views.view_applications, name="view_applications"),
    path("my-applications/", views.my_applications, name="my_applications"),
    path("application/<int:application_id>/status/", views.update_application_status, name="update_application_status"),
    path("application/<int:application_id>/", views.application_detail, name="application_detail"),
    path("applications/<int:application_id>/withdraw/", views.withdraw_application, name="withdraw_application"),
]
