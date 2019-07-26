from django.db import models


class DateTimeModel(models.Model):
    """Abstract model can be used to add time info.

    Note: This should be used by every model instead of manually adding `created_at` and `updated_at` field.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Class meta info."""

        abstract = True
