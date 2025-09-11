from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.urls import reverse
from .forms import CustomUserCreationForm, EmployerProfileForm, ApplicantProfileForm
from django.contrib.auth.decorators import login_required
from applications.models import Application
from jobs.models import Job
from .models import EmployerProfile, ApplicantProfile
from django.contrib.auth import login
from django.db import OperationalError, DatabaseError

def select_role_view(request):
    try: 
        return render(request, "users/select_role.html")
    except Exception as e:
        messages.error(request, "Unable to load page. Please try again.")
        return redirect('home')

def signup_view(request):
    try:
        # Get role from query params
        role = request.GET.get('role')
        if role not in ['employer', 'applicant']:
            return redirect('select_role')  # force user to pick a role

        if request.method == "POST":
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.role = role  # set role from query param
                user.save()

                # Create related profile automatically
                if role == "employer":
                    EmployerProfile.objects.create(user=user)
                else:
                    ApplicantProfile.objects.create(user=user)

                # Log the user in
                login(request, user)
                return redirect('complete_profile')  # let them fill additional info
        else:
            form = CustomUserCreationForm()

        return render(request, "users/signup.html", {"form": form, "role": role})
    
    except (OperationalError, DatabaseError):
        messages.error(request, "Registration service is temporarily unavailable. Please try again later.")
        return redirect('select_role')
    except Exception as e:
        messages.error(request, "An unexpected error occurred during registration.")
        return redirect('select_role')


@login_required
def complete_profile(request, edit=False):
    try:
        user = request.user

        # Determine profile and template
        if user.role == "employer":
            profile = user.employer_profile
            form_class = EmployerProfileForm
            template = "users/profile_form.html"
            heading = "Edit Employer Profile" if edit else "Complete Employer Profile"
        else:
            profile = user.applicant_profile
            form_class = ApplicantProfileForm
            template = "users/profile_form.html"
            heading = "Edit Applicant Profile" if edit else "Complete Applicant Profile"

        if request.method == "POST":
            form = form_class(request.POST, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(request, "Your profile has been saved successfully!")
                return redirect("account") if edit else redirect("dashboard")
        else:
            form = form_class(instance=profile)

        return render(request, template, {"form": form, "heading": heading})
    
    except (OperationalError, DatabaseError):
        messages.error(request, "Unable to save profile. Please try again later.")
        return redirect('dashboard')
    except Exception:
        messages.error(request, "An unexpected error occurred.")
        return redirect('dashboard')
    
def custom_login_view(request):
    try:
        # Use Django's built-in LoginView but wrap it in error handling
        return LoginView.as_view(template_name="users/login.html")(request)
    except (OperationalError, DatabaseError):
        messages.error(request, "Login service is temporarily unavailable. Please try again later.")
        return render(request, "users/login.html")
    except Exception:
        messages.error(request, "An unexpected error occurred during login.")
        return render(request, "users/login.html")

@login_required
def custom_logout_view(request):
    try:
        # Use Django's built-in LogoutView but wrap it in error handling
        return LogoutView.as_view()(request)
    except (OperationalError, DatabaseError):
        messages.error(request, "Logout service is temporarily unavailable.")
        return redirect('home')
    except Exception:
        messages.error(request, "An unexpected error occurred during logout.")
        return redirect('home')


def dashboard(request):
    try:
        if request.user.is_authenticated:
            if request.user.role == "employer":
                jobs = Job.objects.filter(posted_by=request.user).order_by('-created_at')  # latest first
                return render(request, "users/employer_dashboard.html", {"jobs": jobs})
            else:  # applicant
                jobs = Job.objects.all().order_by('-created_at') # latest first
                applied_job_ids = Application.objects.filter(applicant=request.user).values_list("job_id", flat=True)
                return render(request, "users/applicant_dashboard.html", {
                    "jobs": jobs,
                    "applied_job_ids": set(applied_job_ids),
                })    
        return redirect("login")
    
    except (OperationalError, DatabaseError):
        messages.error(request, "Unable to load dashboard. Please try again later.")
        return render(request, "users/dashboard_error.html")
    except Exception:
        messages.error(request, "An unexpected error occurred.")
        return render(request, "users/dashboard_error.html")

@login_required
def account_view(request):
    try:
        return render(request, "users/account.html")
    except Exception:
        messages.error(request, "Unable to load account page.")
        return redirect('dashboard')

