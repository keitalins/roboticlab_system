from messaging_app.models import Message, Notification


def unread_counts(request):
    if request.user.is_authenticated:
        unread_count = Message.objects.filter(recipient=request.user, is_read=False).count()
        unread_notifications = Notification.objects.filter(user=request.user, is_read=False).count()
    else:
        unread_count = 0
        unread_notifications = 0
    return {
        'unread_count': unread_count,
        'unread_notifications': unread_notifications,
    }
