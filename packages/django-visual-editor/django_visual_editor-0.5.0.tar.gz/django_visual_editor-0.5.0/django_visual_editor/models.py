from django.db import models
from django.conf import settings
import uuid
import os


def upload_editor_image(instance, filename):
    """Generate upload path for editor images"""
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join("editor_uploads", filename)


class EditorImage(models.Model):
    """Model to store uploaded images from the editor"""

    image = models.ImageField(upload_to=upload_editor_image)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="uploaded_editor_images",
    )

    class Meta:
        ordering = ["-uploaded_at"]
        verbose_name = "Editor Image"
        verbose_name_plural = "Editor Images"

    def __str__(self):
        return f"Image {self.id} - {self.uploaded_at}"
