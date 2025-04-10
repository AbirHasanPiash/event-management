from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string

User = get_user_model()

@receiver(post_save, sender=User)
def send_activation_email(sender, instance, created, **kwargs):
    if created and not instance.is_active:
        token = default_token_generator.make_token(instance)
        activation_url = f"{settings.FRONTEND_URL}/accounts/activate/{instance.id}/{token}/"

        subject = 'Activate Your Account'
        context = {
            'user': instance,
            'activation_url': activation_url,
        }

        text_content = render_to_string('accounts/activation_email.txt', context)
        html_content = render_to_string('accounts/activation_email.html', context)

        try:
            msg = EmailMultiAlternatives(
                subject,
                text_content,
                settings.EMAIL_HOST_USER,
                [instance.email]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
        except Exception as e:
            print(f"Failed to send activation email to {instance.email}: {str(e)}")