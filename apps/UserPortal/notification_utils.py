from .models import (
    Notification,
    clearance,
    CertificateOfIndigency,
    BuildingPermit,
    BusinessPermit,
    ResidencyCertificate,
    DocumentStatus
)

def create_notification(document_type, request_obj):
    """Create a new notification when a document request is made."""
    Notification.objects.create(
        document_type=document_type,
        resident=request_obj.res_id,
        request_id=request_obj.id
    )

def mark_as_read(notification_id):
    """Mark a notification as read."""
    try:
        notification = Notification.objects.get(id=notification_id)
        notification.is_read = True
        notification.save()
        return True
    except Notification.DoesNotExist:
        return False

def get_unread_notifications():
    """Get all unread notifications."""
    return Notification.objects.filter(is_read=False)

def count_unread_notifications():
    """Count unread notifications."""
    return get_unread_notifications().count()

def count_pending_requests():
    """Count all pending document requests (with status=1)."""
    pending_status = DocumentStatus.objects.get(id=1)  # Assuming 1 is the ID for 'Pending' status

    clearance_count = clearance.objects.filter(status=pending_status).count()
    indigency_count = CertificateOfIndigency.objects.filter(status=pending_status).count()
    business_count = BusinessPermit.objects.filter(status=pending_status).count()
    building_count = BuildingPermit.objects.filter(status=pending_status).count()
    residency_count = ResidencyCertificate.objects.filter(status=pending_status).count()

    # Return individual counts and total
    return {
        'clearance': clearance_count,
        'indigency': indigency_count,
        'business': business_count,
        'building': building_count,
        'residency': residency_count,
        'total': clearance_count + indigency_count + business_count + building_count + residency_count
    }

def get_latest_pending_requests():
    """Get the most recent pending requests for each document type."""
    pending_status = DocumentStatus.objects.get(id=1)  # Assuming 1 is the ID for 'Pending' status

    latest_clearance = clearance.objects.filter(status=pending_status).order_by('-date_requested')[:5]
    latest_indigency = CertificateOfIndigency.objects.filter(status=pending_status).order_by('-date_requested')[:5]
    latest_business = BusinessPermit.objects.filter(status=pending_status).order_by('-date_requested')[:5]
    latest_building = BuildingPermit.objects.filter(status=pending_status).order_by('-date_requested')[:5]
    latest_residency = ResidencyCertificate.objects.filter(status=pending_status).order_by('-date_requested')[:5]

    return {
        'clearance': latest_clearance,
        'indigency': latest_indigency,
        'business': latest_business,
        'building': latest_building,
        'residency': latest_residency
    }
