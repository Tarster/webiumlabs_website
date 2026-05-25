from django.db import models

class ContactSubmission(models.Model):
    name = models.CharField(max_length=255, verbose_name="Name")
    email = models.EmailField(verbose_name="Email Address")
    company = models.CharField(max_length=255, blank=True, null=True, verbose_name="Company Name")
    service = models.CharField(max_length=100, verbose_name="Requested Service")
    budget = models.CharField(max_length=100, verbose_name="Budget Range")
    message = models.TextField(verbose_name="Project Details")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Submission Time")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Submission"
        verbose_name_plural = "Contact Submissions"

    def __str__(self):
        return f"{self.name} - {self.service} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"
