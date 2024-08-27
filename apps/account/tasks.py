import os

from django.core.mail import send_mail

from config.celery import app


@app.task(bind=True, ignore_result=True)
def send_email_task(self, subject, message, recipient_list):
    send_mail(
        subject=subject,
        message=message,
        from_email=os.getenv("SENDER_EMAIL"),
        recipient_list=recipient_list
    )
