from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Ticketing)
class TicketingAdmin(admin.ModelAdmin):
    pass

