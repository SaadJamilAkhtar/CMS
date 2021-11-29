from django.contrib import admin
from .models import *

admin.site.register(Client)

admin.site.register(APIKEY)

admin.site.register(Group)

admin.site.register(ExtraFields)

admin.site.register(ConnectedData)
