"""Configuration templates for MCP servers with interactive prompts."""

from .discovery import ProjectContext, ProjectDetector
from .models import PromptDefinition, ServerTemplate
from .prompt_handler import collect_template_values, prompt_for_value
from .recommender import TemplateRecommendation, TemplateRecommender
from .template_manager import (
    TemplateManager,
    create_default_template_manager,
    create_test_template_manager,
)

__all__ = [
    # Models
    "PromptDefinition",
    "ServerTemplate",
    # Template Management
    "TemplateManager",
    "create_default_template_manager",
    "create_test_template_manager",
    # Interactive Prompts
    "prompt_for_value",
    "collect_template_values",
    # Discovery
    "ProjectContext",
    "ProjectDetector",
    # Recommendation
    "TemplateRecommendation",
    "TemplateRecommender",
]
