from django.urls import path
from . import views

urlpatterns = [
    path("", views.job_list, name="job_list"),
    path("<int:job_id>/", views.job_detail, name="job_detail"),
    path("post/", views.post_job, name="job_post"),
    path('posted-jobs/', views.posted_jobs, name='posted_jobs'),
    path("<int:job_id>/apply/", views.apply_job, name="apply_job"),
    path("<int:job_id>/edit/", views.edit_job, name="job_edit"),
    path("<int:job_id>/delete/", views.delete_job, name="job_delete"),
    path("search/", views.search_jobs, name="search_jobs"),

]
