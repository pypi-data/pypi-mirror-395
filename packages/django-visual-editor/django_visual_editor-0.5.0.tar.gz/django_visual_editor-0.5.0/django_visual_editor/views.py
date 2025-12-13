from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import EditorImage
from .ai_service import AIService
import json


@require_http_methods(["POST"])
@login_required
def upload_image(request):
    """
    Handle image upload from the editor
    """
    try:
        if "image" not in request.FILES:
            return JsonResponse({"error": "No image provided"}, status=400)

        image_file = request.FILES["image"]

        # Validate file type
        allowed_types = ["image/jpeg", "image/png", "image/gif", "image/webp"]
        if image_file.content_type not in allowed_types:
            return JsonResponse({"error": "Invalid file type"}, status=400)

        # Validate file size (max 5MB)
        max_size = 5 * 1024 * 1024
        if image_file.size > max_size:
            return JsonResponse(
                {"error": "File too large. Max size is 5MB"}, status=400
            )

        # Create image instance
        editor_image = EditorImage(
            image=image_file,
            uploaded_by=request.user if request.user.is_authenticated else None,
        )
        editor_image.save()

        return JsonResponse(
            {"success": True, "url": editor_image.image.url, "id": editor_image.id}
        )

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@require_http_methods(["POST"])
@login_required
def ai_assist(request):
    """
    Handle AI content generation and editing requests

    Expects JSON body with:
    - prompt: str (user's request)
    - context_blocks: list[str] (optional, HTML of selected blocks)
    - model: str (optional, AI model to use)
    - mode: str (optional, 'generate' or 'edit', default 'generate')
    - additional_instructions: str (optional, extra instructions from UI)

    Returns JSON with:
    - success: bool
    - content: str (generated HTML)
    - model: str (model used)
    - error: str (if failed)
    """
    try:
        # Parse request body
        data = json.loads(request.body)

        # Validate required fields
        prompt = data.get("prompt", "").strip()
        if not prompt:
            return JsonResponse(
                {"success": False, "error": "Prompt is required"}, status=400
            )

        # Initialize AI service
        ai_service = AIService()

        # Check if AI is enabled
        if not ai_service.is_enabled():
            return JsonResponse(
                {
                    "success": False,
                    "error": "AI features are not enabled. Please configure VISUAL_EDITOR_AI_CONFIG in settings.",
                },
                status=503,
            )

        # Extract parameters
        context_blocks = data.get("context_blocks", [])
        model = data.get("model")  # None will use default from settings
        mode = data.get("mode", "generate")
        additional_instructions = data.get("additional_instructions", "")

        # Validate mode
        if mode not in ["generate", "edit"]:
            return JsonResponse(
                {"success": False, "error": "Mode must be 'generate' or 'edit'"},
                status=400,
            )

        # Generate content
        result = ai_service.generate_content(
            prompt=prompt,
            context_blocks=context_blocks,
            model=model,
            mode=mode,
            additional_instructions=additional_instructions,
        )

        # Return result
        if result["success"]:
            return JsonResponse(result)
        else:
            return JsonResponse(result, status=400)

    except json.JSONDecodeError:
        return JsonResponse(
            {"success": False, "error": "Invalid JSON in request body"}, status=400
        )

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)
