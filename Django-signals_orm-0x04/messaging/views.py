from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Message, Notification, MessageHistory
from django.contrib.auth.models import User

# ["user.delete()", "delete_user"], ["Message.objects.filter", "delete()"]
@login_required
def send_message(request):
    if request.method == 'POST':
        receiver_id = request.POST.get('receiver_id')
        content = request.POST.get('content')
        receiver = get_object_or_404(User, id=receiver_id)
        Message.objects.create(
            sender=request.user,
            receiver=receiver,
            content=content,
        )
        return redirect('inbox')

    users = User.objects.exclude(id=request.user.id)
    return render(request, 'messaging/send_message.html', {'users': users})


@login_required
def inbox(request):
    messages = Message.objects.filter(receiver=request.user).order_by('-timestamp')
    notifications = Notification.objects.filter(user=request.user, is_read=False)
    return render(request, 'messaging/inbox.html', {
        'messages': messages,
        'notifications': notifications
    })


@login_required
def notification_detail(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return render(request, 'messaging/notification_detail.html', {
        'notification': notification
    })


@login_required
def message_detail(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if message.receiver != request.user and message.sender != request.user:
        return redirect('inbox')
    history = message.history.all().order_by('-edited_at')
    return render(request, 'messaging/message_detail.html', {
        'message': message,
        'history': history
    })

