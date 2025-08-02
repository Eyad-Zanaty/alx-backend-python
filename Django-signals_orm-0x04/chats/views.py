from django.shortcuts import render
from messaging.Models.models import Message
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page


@cache_page(60)
@login_required
def conversation_view(request, username):
    messages = Message.objects.filter(
        sender__username=username,
        receiver=request.user
    ) | Message.objects.filter(
        sender=request.user,
        receiver__username=username
    )
    messages = messages.order_by('timestamp')

    return render(request, 'chats/conversation.html', {'messages': messages})
