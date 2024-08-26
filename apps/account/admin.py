from django.contrib import admin

from apps.account.models import Account, Feed, Blog

admin.site.register([Account, Feed, Blog])
