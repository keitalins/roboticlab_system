from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Message, Notification
from .forms import ComposeForm


@login_required
def inbox(request):
    msgs = Message.objects.filter(recipient=request.user).select_related('sender')
    return render(request, 'messaging_app/inbox.html', {'messages_list': msgs})


@login_required
def sent(request):
    msgs = Message.objects.filter(sender=request.user).select_related('recipient')
    return render(request, 'messaging_app/sent.html', {'messages_list': msgs})


@login_required
def message_detail(request, pk):
    msg = get_object_or_404(Message, pk=pk)
    if msg.recipient == request.user and not msg.is_read:
        msg.is_read = True
        msg.save()
    return render(request, 'messaging_app/message_detail.html', {'msg': msg})


@login_required
def compose(request):
    if request.method == 'POST':
        form = ComposeForm(request.POST, user=request.user)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.save()
            # Create notification for recipient
            Notification.objects.create(
                user=msg.recipient,
                message=f'New message from {request.user.get_full_name() or request.user.username}: {msg.subject}',
                notif_type=Notification.TYPE_INFO,
                link=f'/messages/{msg.pk}/',
            )
            messages.success(request, 'Message sent.')
            return redirect('messaging_app:inbox')
    else:
        form = ComposeForm(user=request.user)
    return render(request, 'messaging_app/compose.html', {'form': form})


@login_required
def reply(request, pk):
    original = get_object_or_404(Message, pk=pk)
    if request.method == 'POST':
        form = ComposeForm(request.POST, user=request.user)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.parent = original
            msg.save()
            messages.success(request, 'Reply sent.')
            return redirect('messaging_app:message_detail', pk=original.pk)
    else:
        form = ComposeForm(user=request.user, initial={
            'recipient': original.sender,
            'subject': f'Re: {original.subject}',
        })
    return render(request, 'messaging_app/compose.html', {'form': form, 'replying_to': original})


@login_required
def notifications(request):
    notifs = Notification.objects.filter(user=request.user)
    notifs.filter(is_read=False).update(is_read=True)
    return render(request, 'messaging_app/notifications.html', {'notifications': notifs})
