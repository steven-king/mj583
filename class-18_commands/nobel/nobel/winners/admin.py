from django.contrib import admin

from . import models

admin.site.register(models.Category)
admin.site.register(models.Country)
admin.site.register(models.Person)
admin.site.register(models.Winner)
