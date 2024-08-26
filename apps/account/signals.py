from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.account.models import Account
from apps.account.tasks import send_email_task


@receiver(signal=post_save, sender=Account)
def send_email_signal(sender, instance, created, **kwargs):
    if created:
        send_email_task.delay(
            subject="Welcome to p24_news.com",
            message="Thank You for subscribe",
            recipient_list=[instance.email]
        )
