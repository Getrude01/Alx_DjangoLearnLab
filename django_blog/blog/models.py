from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.urls import reverse
from django.db.models.signals import post_save
from taggit.managers import TaggableManager

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    tags = TaggableManager() 

    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[str(self.pk)])


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio  = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} Profile"

# Auto-create or update profile when user is created/updated
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()
        
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"

    def get_edit_url(self):
        return reverse('blog:comment_update', args=[str(self.pk)])

    def get_delete_url(self):
        return reverse('blog:comment_delete', args=[str(self.pk)])