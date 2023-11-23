"""
Module with models for personal accounts
"""

from django.db import models

from apps.accounts.models import LeafseeUser
from apps.videos.models import Video


class ViewedVideo(models.Model):
    """
    Model for tracking the history of viewed video

    Fields:
        user - ForeignKey(LeafseeUser) - user who watched video
        video - ForeignKey(Video) - video that was watched by user
        view_date - DateField - video watched date
        video_rating - IntegerField - video rating
    """

    class VideoRating(models.IntegerChoices):
        """
        Choices for rating video
        """

        LIKE = 1, "Like"
        NONE = 0, "None"
        DISLIKE = -1, "Dislike"

    user = models.ForeignKey(LeafseeUser, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    view_date = models.DateField(auto_now=True)
    video_rating = models.IntegerField(
        default=VideoRating.NONE, choices=VideoRating.choices
    )
