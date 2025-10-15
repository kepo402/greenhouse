from django.contrib import admin
from .models import Room, Contribution, Expense, Announcement

admin.site.register(Room)
admin.site.register(Contribution)
admin.site.register(Expense)
admin.site.register(Announcement)
