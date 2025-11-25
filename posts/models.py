import os
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError


# -----------------------------
# File size validations
# -----------------------------
def validate_image_size(image):
    """Validate image file size (max 5MB)"""
    if image.size > 5 * 1024 * 1024:
        raise ValidationError("Image file size cannot exceed 5MB.")


def validate_video_size(video):
    """Validate video file size (max 25MB)"""
    if video.size > 25 * 1024 * 1024:
        raise ValidationError("Video file size cannot exceed 25MB.")


# -----------------------------
# Upload path functions
# -----------------------------
def post_image_path(instance, filename):
    """Generate path for post images"""
    return f'posts/images/{instance.author.username}/{filename}'


def post_video_path(instance, filename):
    """Generate path for post videos"""
    return f'posts/videos/{instance.author.username}/{filename}'


# -----------------------------
# Main Post Model
# -----------------------------
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    caption = models.TextField(max_length=2000, blank=True)
    image = models.ImageField(
        upload_to=post_image_path,
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif']),
            validate_image_size
        ]
    )
    video = models.FileField(
        upload_to=post_video_path,
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['mp4', 'mov', 'avi', 'mkv']),
            validate_video_size
        ]
    )
    anonymous = models.BooleanField(default=False)  # Anonymous post support

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def clean(self):
        """Ensure at least one media file is uploaded"""
        if not self.image and not self.video:
            raise ValidationError("At least one image or video must be uploaded.")

    def __str__(self):
        return f"{self.author.username} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"


    # Helper methods for likes and comments count
    def total_likes(self):
        return self.likes.count()

    def total_comments(self):
        return self.comments.count()

    def is_liked_by(self, user):
        return self.likes.filter(user=user).exists()


# -----------------------------
# Like Model
# -----------------------------
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')  # Prevent duplicates

    def __str__(self):
        return f"{self.user.username} likes Post {self.post.id}"


# -----------------------------
# Comment Model
# -----------------------------
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments')
    text = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']  # Oldest comment first

    def __str__(self):
        return f"Comment by {self.user.username} on Post {self.post.id}"
