from django.db import models
from .widgets import VisualEditorWidget


class VisualEditorField(models.TextField):
    """
    A TextField that uses the VisualEditorWidget in forms.

    Usage:
        class BlogPost(models.Model):
            content = VisualEditorField(
                config={
                    'min_height': 400,
                    'placeholder': 'Start typing...',
                }
            )
    """

    def __init__(self, *args, **kwargs):
        # Extract editor config from kwargs
        self.editor_config = kwargs.pop("config", {})
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        """
        Override formfield to use VisualEditorWidget by default
        """
        # Set the widget to VisualEditorWidget with config
        kwargs["widget"] = VisualEditorWidget(config=self.editor_config)
        return super().formfield(**kwargs)

    def deconstruct(self):
        """
        Tell Django how to serialize this field for migrations
        """
        name, path, args, kwargs = super().deconstruct()

        # Add editor_config to kwargs if it's not empty
        if self.editor_config:
            kwargs["config"] = self.editor_config

        return name, path, args, kwargs
