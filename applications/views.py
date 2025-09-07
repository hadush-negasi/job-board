from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from jobs.models import Job
from .models import Application
from .forms import ApplicationForm
from django.contrib import messages

@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    # prevent employer from applying to their own job
    if request.user.role == "employer":
        return redirect("job_detail", job_id=job.id)
    
    # check if already applied
    if Application.objects.filter(applicant=request.user, job=job).exists():
        messages.warning(request, f"You have already applied for {job.title} at {job.company}.")
        return redirect("my_applications")

    if request.method == "POST":
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.applicant = request.user
            application.job = job
            application.save()

            messages.success(request, f"You have successfully applied for {job.title} at {job.company}.")
            return redirect("my_applications")
    else:
        form = ApplicationForm()

    return render(request, "applications/apply_job.html", {"form": form, "job": job})


@login_required
def view_applications(request, job_id):
    job = get_object_or_404(Job, id=job_id, posted_by=request.user)
    applications = job.applications.select_related("applicant").all().order_by("-applied_at")

    return render(
        request,
        "applications/view_applications.html",
        {"job": job, "applications": applications},
    )

@login_required
def application_detail(request, application_id):
    application = get_object_or_404(Application, id=application_id, job__posted_by=request.user)
    return render(request, "applications/application_detail.html", {"application": application})

@login_required
def my_applications(request):
    applications = request.user.applications.select_related("job").order_by("-applied_at")
    return render(request, "applications/my_applications.html", {"applications": applications})

@require_POST
@login_required
def update_application_status(request, application_id):
    application = get_object_or_404(Application, id=application_id, job__posted_by=request.user)
    new_status = request.POST.get("status")
    # Remove "withdrawn" from employer actions
    valid_statuses = dict(Application.STATUS_CHOICES).keys() - {"withdrawn"}

    if new_status in valid_statuses:
        application.status = new_status
        application.save()
        messages.success(request, f"Status updated to {application.get_status_display()}.")
    else:
        messages.error(request, "Invalid status update.")

    return redirect("application_detail", application_id=application.id)

@login_required
def withdraw_application(request, application_id):
    application = get_object_or_404(Application, id=application_id, applicant=request.user)
    
    if request.method == "POST":
        application.status = "withdrawn"
        application.save()
        messages.info(request, f"You have withdrawn your application for {application.job.title}.")
        return redirect("my_applications")
    
    return render(request, "applications/confirm_withdraw_application.html", {"application": application})
