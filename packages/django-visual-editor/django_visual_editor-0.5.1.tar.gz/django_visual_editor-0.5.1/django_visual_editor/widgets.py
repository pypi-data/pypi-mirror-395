from django import forms
from django.conf import settings
from django.urls import reverse
import json


class VisualEditorWidget(forms.Textarea):
    """
    Widget for the Visual Editor
    """

    template_name = "django_visual_editor/widget.html"

    class Media:
        css = {"all": ("django_visual_editor/css/editor.css",)}
        js = ("django_visual_editor/js/editor.bundle.js",)

    def __init__(self, attrs=None, config=None):
        default_attrs = {"class": "visual-editor-textarea"}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)

        self.config = config or {}

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)

        # Add editor configuration
        editor_config = {
            "uploadUrl": reverse("django_visual_editor:upload_image"),
            "minHeight": self.config.get("min_height", 300),
            "maxHeight": self.config.get("max_height", 600),
            "placeholder": self.config.get("placeholder", "Start typing..."),
            **self.config,
        }

        context["widget"]["editor_config"] = json.dumps(editor_config)

        # Add AI configuration if enabled
        ai_config = getattr(settings, "VISUAL_EDITOR_AI_CONFIG", {})
        if ai_config.get("enabled", False):
            ai_frontend_config = {
                "enabled": True,
                "endpoint": reverse("django_visual_editor:ai_assist"),
                "models": ai_config.get(
                    "models",
                    [
                        {"id": "gpt-4o", "name": "GPT-4o", "provider": "OpenAI"},
                    ],
                ),
                "defaultModel": ai_config.get("default_model", "gpt-4o"),
            }
            context["widget"]["ai_config"] = json.dumps(ai_frontend_config)
        else:
            context["widget"]["ai_config"] = "null"

        return context
