from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class Status(TextChoices):
    DRAFT = "df", _("Draft"),
    PUBLISHED = "pb", _("Published")
