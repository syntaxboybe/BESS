from .notification_utils import count_pending_requests, get_latest_pending_requests

def add_variable_to_context(request):
    userinfo = request.user

    # Only add notification data if user is authenticated and not superadmin
    notification_data = {}
    if request.user.is_authenticated and hasattr(request.user, 'groups') and request.user.groups.exists():
        if request.user.groups.all()[0].name != 'superadmin' and request.user.id != 1:
            notification_data = {
                'pending_counts': count_pending_requests(),
                'latest_requests': get_latest_pending_requests()
            }

    context = {
        'userinfo': userinfo,
        'notifications': notification_data
    }

    return context
