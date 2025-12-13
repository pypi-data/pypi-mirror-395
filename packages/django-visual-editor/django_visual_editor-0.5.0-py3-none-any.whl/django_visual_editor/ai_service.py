"""
AI Service for django-visual-editor.
Uses OpenAI library for AI provider access.
"""

from typing import Dict, List, Optional, Any
from django.conf import settings
import logging

try:
    import openai

    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logging.warning(
        "openai is not installed. AI features will not work. Install with: pip install openai"
    )

logger = logging.getLogger(__name__)


class AIService:
    """
    AI Service that uses OpenAI library to communicate with AI providers.

    Supports any OpenAI-compatible API endpoint including:
    - OpenAI (gpt-4o, gpt-3.5-turbo, etc.)
    - Anthropic Claude (via OpenAI compatibility)
    - YandexGPT (via OpenAI compatibility)
    - Any other OpenAI-compatible providers
    """

    # Default English system prompts for best AI performance
    DEFAULT_PROMPTS = {
        "generate": """You are an expert content writer for articles and blog posts.

Task: Generate high-quality content based on the user's request.

Rules:
1. Return ONLY clean HTML using semantic tags: <h2>, <h3>, <p>, <ul>, <ol>, <li>, <blockquote>, <code>
2. NO <h1> tags (the article already has a main title)
3. Use proper heading hierarchy (h2 → h3 → h4)
4. Write engaging, clear, and well-structured content
5. If context blocks are provided, use them as reference for style, tone, and topic
6. DO NOT wrap output in markdown code blocks - return raw HTML only

Output format: Raw HTML without any markdown formatting or code fences.""",
        "edit": """You are an expert editor improving article content.

Task: Edit and improve the provided content based on user's instructions.

Rules:
1. Maintain the HTML structure (<h2>, <h3>, <p>, <ul>, <ol>, <blockquote>, etc.)
2. Improve clarity, grammar, flow, and engagement
3. Follow the user's specific editing instructions carefully
4. Preserve the original meaning unless explicitly asked to change it
5. Return ONLY the edited HTML without any explanations
6. DO NOT wrap output in markdown code blocks - return raw HTML only

The context blocks below show the content to edit. Apply the requested changes and return the improved version.""",
    }

    def __init__(self):
        """Initialize AI Service with configuration from Django settings."""
        if not OPENAI_AVAILABLE:
            raise ImportError(
                "openai is required for AI features. "
                "Install it with: pip install openai"
            )

        # Get configuration from Django settings
        self.config = getattr(settings, "VISUAL_EDITOR_AI_CONFIG", {})

        # Use custom system prompts if provided, otherwise use defaults
        self.system_prompts = self.config.get("system_prompts", self.DEFAULT_PROMPTS)

        # Get default model ID
        self.default_model_id = self.config.get("default_model", "gpt-4o")

        # Build model configurations map
        self.models = {}
        for model_config in self.config.get("models", []):
            self.models[model_config["id"]] = model_config

    def _get_client_for_model(self, model_id: str) -> tuple:
        """
        Get OpenAI client and model name for a given model ID.

        Returns:
            Tuple of (client, model_name)
        """
        # Get model configuration
        model_config = self.models.get(model_id)
        if not model_config:
            raise ValueError(f"Model '{model_id}' not found in configuration")

        # Build client kwargs
        client_kwargs = {}

        if model_config.get("api_key"):
            client_kwargs["api_key"] = model_config["api_key"]

        if model_config.get("base_url"):
            client_kwargs["base_url"] = model_config["base_url"]

        if model_config.get("project"):
            client_kwargs["project"] = model_config["project"]

        # Create client
        client = openai.OpenAI(**client_kwargs)

        # Get model name
        model_name = model_config.get("model", model_id)

        return client, model_name

    def generate_content(
        self,
        prompt: str,
        context_blocks: Optional[List[str]] = None,
        model: Optional[str] = None,
        mode: str = "generate",
        additional_instructions: str = "",
    ) -> Dict[str, Any]:
        """
        Generate or edit content using AI.

        Args:
            prompt: The user's main request (e.g., "Write an introduction about Django")
            context_blocks: List of HTML strings from selected blocks (for context)
            model: AI model to use (e.g., 'gpt-4o', 'claude-3-5-sonnet-20241022')
                  If None, uses default_model from settings
            mode: 'generate' for new content or 'edit' for editing existing content
            additional_instructions: Extra instructions from UI (e.g., "Use formal tone")

        Returns:
            Dictionary with:
                - success: bool
                - content: str (generated HTML)
                - model: str (model used)
                - error: str (if failed)
        """
        if not prompt or not prompt.strip():
            return {"success": False, "error": "Prompt cannot be empty"}

        # Use provided model ID or fall back to default
        model_id = model or self.default_model_id

        try:
            # Get client and model name for this model
            client, model_name = self._get_client_for_model(model_id)

            # Build messages for the AI
            messages = self._build_messages(
                prompt=prompt,
                context_blocks=context_blocks or [],
                mode=mode,
                additional_instructions=additional_instructions,
            )

            # Log the request (useful for debugging)
            logger.info(
                f"AI request: model_id={model_id}, model_name={model_name}, mode={mode}, prompt_length={len(prompt)}"
            )

            # Get temperature and max_tokens from config or use defaults
            temperature = self.config.get("temperature", 0.7)
            max_tokens = self.config.get("max_tokens", 2000)

            # Call OpenAI API with the specific client and model
            response = client.chat.completions.create(
                model=model_name,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )

            # Extract content from response
            content = response.choices[0].message.content

            # Clean up the content (remove markdown code blocks if AI added them)
            content = self._clean_html_output(content)

            logger.info(f"AI response: success, content_length={len(content)}")

            return {"success": True, "content": content, "model": model_id}

        except Exception as e:
            logger.error(f"AI generation error: {str(e)}", exc_info=True)
            return {"success": False, "error": str(e), "model": model_id}

    def _build_messages(
        self,
        prompt: str,
        context_blocks: List[str],
        mode: str,
        additional_instructions: str,
    ) -> List[Dict[str, str]]:
        """
        Build the messages array for the AI model.

        Format:
        [
            {"role": "system", "content": "System prompt with instructions"},
            {"role": "user", "content": "User's request"}
        ]
        """
        # Get base system prompt for the mode
        system_prompt = self.system_prompts.get(
            mode, self.DEFAULT_PROMPTS.get(mode, self.DEFAULT_PROMPTS["generate"])
        )

        # Add additional instructions if provided
        if additional_instructions and additional_instructions.strip():
            system_prompt += (
                f"\n\nAdditional instructions:\n{additional_instructions.strip()}"
            )

        # Add context blocks if provided
        if context_blocks:
            context_text = "\n\n".join(
                [
                    f"<context-block>\n{block}\n</context-block>"
                    for block in context_blocks
                ]
            )
            system_prompt += f"\n\nContext blocks from the article:\n{context_text}"

        # Build messages array
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ]

        return messages

    def _clean_html_output(self, content: str) -> str:
        """
        Clean the AI output to ensure it's valid HTML.

        Sometimes AI wraps HTML in markdown code blocks like:
        ```html
        <h2>Title</h2>
        ```

        This method removes such wrapping.
        """
        content = content.strip()

        # Remove markdown code blocks
        if content.startswith("```html"):
            content = content[7:]  # Remove ```html
            if content.endswith("```"):
                content = content[:-3]  # Remove closing ```
        elif content.startswith("```"):
            content = content[3:]  # Remove ```
            if content.endswith("```"):
                content = content[:-3]  # Remove closing ```

        return content.strip()

    def get_available_models(self) -> List[Dict[str, str]]:
        """
        Get list of available AI models from configuration.

        Returns:
            List of dicts with 'id', 'name', 'provider' keys
        """
        return self.config.get(
            "models",
            [
                {"id": "gpt-4o", "name": "GPT-4o", "provider": "OpenAI"},
            ],
        )

    def is_enabled(self) -> bool:
        """Check if AI features are enabled in settings."""
        return self.config.get("enabled", False) and OPENAI_AVAILABLE
