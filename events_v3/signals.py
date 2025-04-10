from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Event
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


@receiver(m2m_changed, sender=Event.participants.through)
def send_rsvp_confirmation_email(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':
        for user_id in pk_set:
            try:
                user = User.objects.get(pk=user_id)
                send_mail(
                    subject=f'RSVP Confirmation: {instance.name}',
                    message=(
                        f'Hi {user.first_name},\n\n'
                        f'Thank you for RSVPing to "{instance.name}".\n\n'
                        f'Date: {instance.date}\n'
                        f'Time: {instance.time}\n'
                        f'Location: {instance.location}\n\n'
                        f'See you there!'
                    ),
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
            except User.DoesNotExist:
                continue
