from django.db import models


class Source(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField(unique=True)
    is_rss = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']