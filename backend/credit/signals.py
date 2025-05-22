from typing import Type

from django.core.mail import send_mail
from django.db.models.signals import pre_save
from django.dispatch import receiver

from backend.base.const import CreditRequestStatusType
from backend.credit.models import CreditRequest


@receiver(pre_save, sender=CreditRequest)
def handle_request_status(sender: Type[CreditRequest], instance: CreditRequest, **kwargs) -> None:
    if instance.id is None:
        return  # If we force create with accepted status by admin

    if (
        sender.objects.only("status").get(id=instance.id).status == CreditRequestStatusType.PENDING 
        and instance.status in (CreditRequestStatusType.ACCEPTED, CreditRequestStatusType.REJECTED)
    ):

        if instance.status == CreditRequestStatusType.ACCEPTED:
            text = f"Ваша кредитна заявка на {instance.amount} гривень схвалена оператором. Очікуйте наступної комунікації."
        else:
            text = f"На жаль, ваша кредитна заявка на {instance.amount} гривень відхилена оператором."

        send_mail(
            subject="Інформування щодо кредитної заявки",
            recipient_list=[instance.user.email],
            fail_silently=True,
            from_email=None,
            message=text,
        )
