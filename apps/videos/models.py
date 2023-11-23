"""
Modules with models for video
"""

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from apps.accounts.models import LeafseeUser


def video_directory_path(instance, filename):
    """
    Generate path to load video file

    Video file will be uploaded to MEDIA_ROOT/videos/user_<id>/<filename>
    """
    return "videos/user_{0}/{1}".format(instance.user.id, filename)


def preview_directory_path(instance, filename):
    """
    Generate path to load preview image file

    Preview image will be uploaded to MEDIA_ROOT/preview/user_<id>/<filename>
    """
    return "preview/user_{0}/{1}".format(instance.user.id, filename)


class Tag(models.Model):
    """
    Model for tag for video

    Fields:
        name - CharField - name of tag
    """

    name = models.CharField(max_length=150)


class Video(models.Model):
    """
    Model for video

    Fields:
        video_file - FileField - path to video
        name - CharField - video name in site
        description - TextField - video description
        author - ForeignKey(LeafseeUser) - user who is author of video
        publication_date - DateField - video publication date
        preview_image - ImageField - path for preview image video
        tags - ManyToManyField(Tag) - video tags
        likes - ManyToManyField(LeafseeUser) - users who pressed like for video
        dislikes - ManyToManyField(LeafseeUser) - users who pressed dislike for video
        views - ManyToManyField(LeafseeUser) - users who watched video
    """

    video_file = models.FileField(upload_to=video_directory_path)
    name = models.CharField(max_length=150)
    description = models.TextField()
    author = models.ForeignKey(LeafseeUser, on_delete=models.SET_NULL, null=True)
    publication_date = models.DateField(auto_now_add=True)
    preview_image = models.ImageField(upload_to=preview_directory_path)
    tags = models.ManyToManyField(Tag)
    likes = models.ManyToManyField(LeafseeUser, related_name="liked_videos")
    dislikes = models.ManyToManyField(LeafseeUser, related_name="disliked_videos")
    views = models.ManyToManyField(LeafseeUser, related_name="watched_videos")


class Comment(models.Model):
    """
    Model for comments for video or other comments

    Fields:
        text - TextField - comment text
        publication_date - DateField - comment publication date
        author - ForeignKey(LeafseeUser) - user who is author of comment
        likes - ManyToManyField(LeafseeUser) - users who pressed like for comment
        dislikes - ManyToManyField(LeafseeUser) - users who pressed dislike for comment
        source - GenericForeignKey - video or other comment that this comment responds to
        source_type - ForeignKey(ContentType) - type of source model
        source_id - PositiveIntegerField - id of source model
    """

    text = models.TextField()
    publication_date = models.DateField(auto_now_add=True)
    author = models.ForeignKey(LeafseeUser, on_delete=models.SET_NULL, null=True)
    likes = models.ManyToManyField(LeafseeUser, related_name="liked_comments")
    dislikes = models.ManyToManyField(LeafseeUser, related_name="disliked_comments")
    source_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=(
            models.Q(app_label="video", model="Video")
            | models.Q(app_label="video", model="Comment")
        ),
    )
    source_id = models.PositiveIntegerField()
    source = GenericForeignKey("source_type", "source_id")
