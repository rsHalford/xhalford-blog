from django.contrib import admin

from .models import Subscriber


class SubscriberAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "confirmed",
        "created_on",
    )
    list_filter = ("confirmed", "updated_on", "created_on")
    search_fields = ["email"]


admin.site.register(Subscriber, SubscriberAdmin)
