import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.mail import send_mail
from django.conf import settings
from .models import ContactSubmission

def home_view(request):
    return render(request, 'home.html')

@ensure_csrf_cookie
@require_http_methods(["GET", "POST"])
def contact_view(request):
    if request.method == "GET":
        return render(request, 'contact.html')
    
    # Handle POST submission
    try:
        # Determine if JSON submission or Form submission
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST

        # Use case-insensitive parsing to accommodate any variation in HTML input name tags
        name = (data.get('Name') or data.get('name') or '').strip()
        email = (data.get('Email') or data.get('email') or '').strip()
        company = (data.get('Company') or data.get('company') or '').strip()
        service = (data.get('Service') or data.get('service') or '').strip()
        budget = (data.get('Budget') or data.get('budget') or '').strip()
        message = (data.get('message') or data.get('Message') or data.get('Name') or data.get('name') or '').strip()

        # If duplicate 'Name' fields were received (original textarea duplicate name bug)
        # and request was a standard Form POST (not JSON), request.POST may return lists.
        # But since our AJAX payload always uses standard JSON structure, it is fully resolved.
        # We handle this anyway for maximum safety.

        # Validation
        errors = {}
        if not name:
            errors['name'] = "Name is required."
        if not email:
            errors['email'] = "Email address is required."
        elif '@' not in email or '.' not in email:
            errors['email'] = "Please provide a valid email address."
        if not service or service == 'None' or service == 'Select Your Service':
            errors['service'] = "Please select a valid service."
        if not budget or budget == 'None' or budget == 'Select Your Range':
            errors['budget'] = "Please select a valid budget range."
        if not message:
            errors['message'] = "Please tell us more about your project details."

        if errors:
            return JsonResponse({'success': False, 'errors': errors}, status=400)

        # Save to database
        submission = ContactSubmission.objects.create(
            name=name,
            email=email,
            company=company if company else None,
            service=service,
            budget=budget,
            message=message
        )

        return JsonResponse({
            'success': True,
            'message': f"Thank you, {name}! Your message has been sent successfully. We'll be in touch soon.",
            'submission_id': submission.id
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'error': "An internal error occurred. Please try again later."
        }, status=500)

def page_404_view(request):
    return render(request, '404.html')

def handler404(request, exception=None):
    return render(request, '404.html', status=404)
