from django.db import models
from django.utils.translation import gettext as _

class PaymentStatus(models.TextChoices):
    CREATED = "created"
    COMPLETED = "comleted"
    FAILED = "failed"


