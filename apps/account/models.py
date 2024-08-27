import uuid

from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, BooleanField, TextField, URLField, ForeignKey, CASCADE, ImageField, EmailField, UUIDField


from apps.account.choices import AccountRole
from apps.shared.models import BaseModel
from django.utils.translation import gettext_lazy as _


class Account(BaseModel, AbstractUser):
    email = EmailField(_("Email address"), unique=True)
    role = CharField(max_length=128, choices=AccountRole.choices, default=AccountRole.MEMBER)
    activation_token = UUIDField(default=uuid.uuid4,unique=True)
    is_subscribe = BooleanField(default=False)
    avatar = ImageField(upload_to="avatar/", null=True, blank=True)


class Feed(BaseModel):
    name = CharField(max_length=128)
    body = TextField()
    website = URLField(blank=True, null=True)
    account = ForeignKey("account.Account", CASCADE, "feeds")


class Blog(BaseModel):
    title = CharField(max_length=256)
    body = TextField()
    image = ImageField(upload_to="blog/images/")
    owner = ForeignKey("account.Account", CASCADE, "blogs")
