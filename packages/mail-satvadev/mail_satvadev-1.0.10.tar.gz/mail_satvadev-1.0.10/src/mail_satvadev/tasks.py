from smtplib import SMTPException
from typing import Optional

from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from project.celery import app


@app.task(bind=True, max_retries=settings.CELERY_MAX_RETRIES_COUNT)
def send_email(self, subject: str, recipients: list[str], body: str,
               backoff: Optional[int] = None) -> None:
    """Celery task отправления email"""
    try:
        msg = EmailMultiAlternatives(
            subject=subject, body=body,
            to=recipients, from_email=settings.EMAIL_HOST_USER,
        )
        msg.mixed_subtype = 'related'
        msg.attach_alternative(body, 'text/html')
        msg.send()
    except SMTPException as ex:
        countdown = backoff * pow(2, self.request.retries) if backoff else None
        raise self.retry(exc=ex, countdown=countdown)
