from django.urls import reverse
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .decorators import unauthenticated_user
from apps.UserPortal.models import clearance, BusinessPermit, BuildingPermit, CertificateOfIndigency, ResidencyCertificate
from django.http import JsonResponse
from django.db.models import Q


# Create your views here.


@unauthenticated_user
def loginPage(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username = username, password = password)

        if not user:
            messages.error(request, 'Invalid username or password !')
            return render(request, "Login/login.html")

        login(request, user)

        return redirect(reverse('dashboard'))

    return render(request, "Login/login.html")

# Document tracker view - public access, no login required
def document_tracker(request):
    transaction_id = request.GET.get('txn', '')

    context = {
        'transaction_id': transaction_id
    }

    return render(request, "Tracker/document_tracker.html", context)

# API endpoint for fetching document status
def get_document_status(request):
    transaction_id = request.GET.get('txn', '')

    if not transaction_id:
        return JsonResponse({'success': False, 'error': 'No transaction ID provided'})

    # Check in all document models for the transaction ID
    document = None
    document_type = None

    # Check Clearance
    try:
        document = clearance.objects.get(transaction_id=transaction_id)
        document_type = 'Barangay Clearance'
    except clearance.DoesNotExist:
        # Check Business Permit
        try:
            document = BusinessPermit.objects.get(transaction_id=transaction_id)
            document_type = 'Business Permit'
        except BusinessPermit.DoesNotExist:
            # Check Building Permit
            try:
                document = BuildingPermit.objects.get(transaction_id=transaction_id)
                document_type = 'Building Permit'
            except BuildingPermit.DoesNotExist:
                # Check Indigency Certificate
                try:
                    document = CertificateOfIndigency.objects.get(transaction_id=transaction_id)
                    document_type = 'Certificate of Indigency'
                except CertificateOfIndigency.DoesNotExist:
                    # Check Residency Certificate
                    try:
                        document = ResidencyCertificate.objects.get(transaction_id=transaction_id)
                        document_type = 'Certificate of Residency'
                    except ResidencyCertificate.DoesNotExist:
                        # Transaction ID not found in any model
                        return JsonResponse({'success': False, 'error': 'Document not found'})

    if document:
        # Define timeline based on status
        timeline = []

        # Common first step
        timeline.append({
            'date': document.date_requested.strftime('%b %d, %Y %I:%M %p') if hasattr(document, 'date_requested') else '',
            'action': 'Document requested',
            'icon': 'far fa-file-alt',
            'color': 'primary'
        })

        # Add timeline steps based on current status
        status = document.status.document_status if hasattr(document.status, 'document_status') else ''

        if status == 'Forwarded to Kapitan':
            timeline.append({
                'date': 'Processing',
                'action': 'Request approved by secretary',
                'icon': 'fas fa-check',
                'color': 'success'
            })
            timeline.append({
                'date': 'In Progress',
                'action': 'Forwarded to Barangay Captain for signature',
                'icon': 'fas fa-arrow-right',
                'color': 'info'
            })
        elif status == 'Ready to Claim' or status == 'Ready to Claim(e-Signed)':
            timeline.append({
                'date': 'Processing',
                'action': 'Request approved by secretary',
                'icon': 'fas fa-check',
                'color': 'success'
            })
            timeline.append({
                'date': 'Processing',
                'action': 'Forwarded to Barangay Captain for signature',
                'icon': 'fas fa-arrow-right',
                'color': 'info'
            })
            timeline.append({
                'date': 'Ready for Pick-up',
                'action': f'Document ready to claim ({status})',
                'icon': 'fas fa-clipboard-check',
                'color': 'success'
            })
        elif status == 'Released' or status == 'Released(e-Signed)':
            timeline.append({
                'date': 'Processing',
                'action': 'Request approved by secretary',
                'icon': 'fas fa-check',
                'color': 'success'
            })
            timeline.append({
                'date': 'Processing',
                'action': 'Forwarded to Barangay Captain for signature',
                'icon': 'fas fa-arrow-right',
                'color': 'info'
            })
            timeline.append({
                'date': 'Ready for Pick-up',
                'action': 'Document ready to claim',
                'icon': 'fas fa-clipboard-check',
                'color': 'success'
            })
            timeline.append({
                'date': document.date_released.strftime('%b %d, %Y') if hasattr(document, 'date_released') and document.date_released else 'Released',
                'action': f'Document released ({status})',
                'icon': 'fas fa-check-circle',
                'color': 'success'
            })
        elif status == 'Reverted':
            timeline.append({
                'date': 'Rejected',
                'action': 'Request rejected: Please check your email for details',
                'icon': 'fas fa-times',
                'color': 'danger'
            })
        elif status == 'Pending':
            timeline.append({
                'date': 'In Progress',
                'action': 'Under review by secretary',
                'icon': 'fas fa-spinner fa-spin',
                'color': 'warning'
            })

        # Prepare the response
        response_data = {
            'success': True,
            'document_type': document_type,
            'date_requested': document.date_requested.strftime('%b %d, %Y %I:%M %p') if hasattr(document, 'date_requested') else '',
            'date_released': document.date_released.strftime('%b %d, %Y') if hasattr(document, 'date_released') and document.date_released else 'None',
            'status': status,
            'transaction_id': document.transaction_id,
            'purpose': document.purpose if hasattr(document, 'purpose') else '',
            'resident_name': f"{document.res_id.firstname} {document.res_id.lastname}" if hasattr(document, 'res_id') else '',
            'timeline': timeline
        }

        return JsonResponse(response_data)

    return JsonResponse({'success': False, 'error': 'Document not found'})
