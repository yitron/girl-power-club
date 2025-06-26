from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class MembershipApplication(models.Model):
    name = models.CharField(max_length=100)
    school = models.CharField(max_length=100)
    classroom = models.CharField(max_length=20)
    application_date = models.DateTimeField(default=timezone.now)
    approved = models.BooleanField(default=False)
    approved_date = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="approved_applications")
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name="membership")
    
    def __str__(self):
        return f"{self.name} - {self.school}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    school = models.CharField(max_length=100)
    classroom = models.CharField(max_length=20)
    bio = models.TextField(blank=True)
    
    def __str__(self):
        return self.user.username

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Post by {self.user.username} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.created_at.strftime('%Y-%m-%d %H:%M')}"