"""
Django Visual Editor - A rich text editor with image upload support
"""

__version__ = "0.3.0"

default_app_config = "django_visual_editor.apps.DjangoVisualEditorConfig"

# Expose main components for easy import
from .fields import VisualEditorField
from .widgets import VisualEditorWidget

__all__ = ["VisualEditorField", "VisualEditorWidget"]
