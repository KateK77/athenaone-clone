"""Scoped per-user unread state, independent of shared sender read receipts."""
from core.access import patients_for, role
from engagement.models import Message, MessageRead

MESSAGE_ROLES = {'admin', 'manager', 'frontdesk', 'physician', 'nurse', 'assistant', 'patient'}


def unread_messages(user):
    if role(user) not in MESSAGE_ROLES:
        return Message.objects.none()
    return Message.objects.filter(thread__patient__in=patients_for(user)).exclude(sender=user).exclude(
        pk__in=MessageRead.objects.filter(user=user).values('message_id'))


def mark_read(user, messages):
    incoming = [msg for msg in messages if msg.sender_id != user.pk]
    MessageRead.objects.bulk_create([MessageRead(message=msg, user=user) for msg in incoming], ignore_conflicts=True)
    Message.objects.filter(pk__in=[msg.pk for msg in incoming]).update(read=True)
    for msg in incoming:
        msg.read = True
