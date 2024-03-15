"""Models for the blog app"""

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


class PublishManger(models.Manager):
    """Custom manager to handle published posts"""

    def get_queryset(self):
        """Returns the main queryset for published posts"""
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    """Post model."""

    class Status(models.TextChoices):
        """Available stauts to a post"""

        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date="publish")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="blog_posts",
    )
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    objects = models.Manager()
    published = PublishManger()

    class Meta:
        """Metadata for Post model"""

        ordering = ["-publish"]
        indexes = [models.Index(fields=["-publish"])]

    def get_absolute_url(self) -> str:
        """Returns the canonical url of this model"""
        return reverse(
            "blog:post_detail",
            args=[
                self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug,
            ],
        )

    def __str__(self) -> str:
        return f"{self.title}"


class ActiveManger(models.Manager):
    """Manger to handle active comments"""

    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(active=True)


class Comment(models.Model):
    """Comments model class"""

    post = models.ForeignKey(
        Post, on_delete=models.Case, related_name="comments"
    )
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    objects = models.Manager()
    actives = ActiveManger()

    class Meta:
        ordering = ["created"]
        indexes = [models.Index(fields=["created"])]

    def __str__(self) -> str:
        return f"Comment by {self.name} on {self.post}"
