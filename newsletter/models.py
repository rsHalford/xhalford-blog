from django.db import models


class Subscriber(models.Model):
    email = models.EmailField(null=False, blank=True, unique=True)
    confirmed = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.email
