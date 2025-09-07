from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from applications.models import Application
from .models import Job
from .forms import JobForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

def job_list(request):
    jobs = Job.objects.all()
    return render(request, "jobs/job_list.html", {"jobs": jobs})

def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    back_url = request.META.get("HTTP_REFERER", reverse("home"))  # fallback to home

    already_applied = False
    if request.user.is_authenticated and request.user.role == "applicant":
        already_applied = Application.objects.filter(
            applicant=request.user, job=job
        ).exists()

    return render(request, "jobs/job_detail.html", {
        "job": job,
        "already_applied": already_applied,
        "back_url": back_url,
    })

@login_required
def post_job(request):
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.company = request.user.employer_profile.company_name
            job.save()
            return redirect("posted_jobs")
    else:
        form = JobForm()

    return render(request, "jobs/job_form.html", {
        "form": form,
        "title": "Post a Job",
        "heading": "Post a New Job",
        "button_text": "Publish Job",
        "cancel_url": reverse("dashboard")
    })


@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    # you can expand later to track applications
    return render(request, "jobs/job_detail.html", {"job": job, "applied": True})

@login_required
def posted_jobs(request):
    jobs = Job.objects.filter(posted_by=request.user).order_by('-created_at')  # latest first
    return render(request, 'jobs/posted_jobs.html', {'jobs': jobs})

@login_required
def edit_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, posted_by=request.user)

    if request.method == "POST":
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect("job_detail", job.id)
    else:
        form = JobForm(instance=job)

    return render(request, "jobs/job_form.html", {
        "form": form,
        "title": f"Edit {job.title}",
        "heading": "Edit Job",
        "button_text": "Save Changes",
        "cancel_url": reverse("job_detail", args=[job.id]),
    })


@login_required
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, posted_by=request.user)

    if request.method == "POST":
        job.delete()
        messages.success(request, "Job deleted successfully.")
        return redirect("posted_jobs")

    return render(request, "jobs/job_confirm_delete.html", {"job": job})

@login_required
def search_jobs(request):
    query = request.GET.get("q")
    location = request.GET.get("location")

    JOB_TYPE_MAP = {
        "Full-time": "FT",
        "Part-time": "PT",
        "Contract": "CT",
        "Internship": "IN",
    }

    job_type_display = request.GET.get("job_type")  # e.g. "Full-time"
    job_type = JOB_TYPE_MAP.get(job_type_display)   # "FT"

    jobs = Job.objects.all().order_by("-created_at")

    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(company__icontains=query)
        )

    if job_type and job_type != "all":
        jobs = jobs.filter(job_type=job_type)

    if location:
        jobs = jobs.filter(location__icontains=location)

    # Get all job IDs the user has applied to
    applied_job_ids = list(request.user.applications.values_list('job_id', flat=True))

    return render(request, "jobs/search_jobs.html", {
        "jobs": jobs,
        "query": query or "",
        "job_type": job_type or "all",
        "location": location or "",
        "applied_job_ids": applied_job_ids,
    })




