# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

def user_profile_picture_upload_to(instance, filename):
    return f"profile_pics/user_{instance.id}/{filename}"

class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to=user_profile_picture_upload_to, blank=True, null=True)
    # Users that THIS user follows
    following = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="followers",  # user.followers -> users that follow this user
        blank=True
    )

    def __str__(self):
        return self.username
