from django.db import models
from users.models import CustomUser


class Room(models.Model):
    author = models.ForeignKey(
        CustomUser, related_name="author", on_delete=models.CASCADE)
    other = models.ForeignKey(
        CustomUser, related_name="other", on_delete=models.CASCADE)
    created_at = models.DateField(auto_now=True)

    class Meta:
        db_table = "room"
        unique_together = ("author", "other")
