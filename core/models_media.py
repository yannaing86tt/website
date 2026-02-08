from django.db import models
from django.utils.text import slugify
from django.utils import timezone

class MediaItem(models.Model):
    KIND_CHOICES = [
        ("audio", "Audio (MP3)"),
        ("video", "Video (URL/MP4)"),
    ]
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("published", "Published"),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)

    kind = models.CharField(max_length=10, choices=KIND_CHOICES, default="audio")
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="draft")

    # audio/video file upload (mp3/mp4)
    file = models.FileField(upload_to="library/%Y/%m/", blank=True, null=True)

    # for tutorial video: YouTube/Vimeo link (recommended)
    video_url = models.URLField(blank=True)

    cover_image = models.ImageField(upload_to="library_covers/%Y/%m/", blank=True, null=True)
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)[:200] or "media"
            slug = base
            i = 1
            while MediaItem.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                i += 1
                slug = f"{base}-{i}"
            self.slug = slug

        if self.status == "published" and not self.published_at:
            self.published_at = timezone.now()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
class MediaTrack(models.Model):
    item = models.ForeignKey(MediaItem, related_name="tracks", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    audio_file = models.FileField(upload_to="library_tracks/%Y/%m/")
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["order", "id"]
        constraints = [
            models.UniqueConstraint(fields=["item", "order"], name="uniq_media_track_order_per_item")
        ]

    def __str__(self):
        return f"{self.item.title} - {self.order}. {self.title}"
