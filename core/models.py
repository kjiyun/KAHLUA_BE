from django.db import models

class TimeStampedModel(models.Model):
    """Time stamped Model"""

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True #admin에서 안보이게