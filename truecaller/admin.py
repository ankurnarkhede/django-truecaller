from django.contrib import admin

from .models import *

admin.site.register(Contact)
admin.site.register(UserContactMapping)
admin.site.register(UserProfile)
