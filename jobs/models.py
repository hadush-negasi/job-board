from django.db import models
from django.conf import settings

class Job(models.Model):
    JOB_TYPES = (
        ("FT", "Full-time"),
        ("PT", "Part-time"),
        ("CT", "Contract"),
        ("IN", "Internship"),
    )

    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.TextField()
    job_type = models.CharField(max_length=2, choices=JOB_TYPES, default="FT")
    salary = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)  # numeric salary
    deadline = models.DateField(blank=True, null=True)  # optional application deadline
    created_at = models.DateTimeField(auto_now_add=True)

    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # this points at your custom User model
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.title} at {self.company}"
