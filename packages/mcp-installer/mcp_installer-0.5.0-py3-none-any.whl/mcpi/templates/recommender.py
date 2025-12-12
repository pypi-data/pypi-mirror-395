"""Template recommendation engine using project context scoring.

This module provides functionality to recommend the most appropriate template
for a given server based on detected project characteristics.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from .discovery import ProjectContext, ProjectDetector
from .models import ServerTemplate
from .template_manager import TemplateManager


@dataclass
class TemplateRecommendation:
    """A template recommendation with confidence score and explanation.

    Represents a single template recommendation with a confidence score
    indicating how well it matches the project context, plus human-readable
    reasons explaining why it was recommended.

    Attributes:
        template: The recommended ServerTemplate
        confidence: Confidence score between 0.0 and 1.0 (higher = better match)
        reasons: List of human-readable reasons for this recommendation
    """

    template: ServerTemplate
    confidence: float
    reasons: list[str]


class TemplateRecommender:
    """Recommends templates based on project context analysis.

    Uses a scoring algorithm to match detected project characteristics
    (from ProjectDetector) against template metadata to produce ranked
    recommendations.

    Scoring considers:
    - Docker usage (matches docker-based templates)
    - Language compatibility (nodejs project → nodejs-compatible templates)
    - Database service matches (postgres service → postgres templates)
    - Best-for metadata in templates
    - Keywords and tags

    Example:
        ```python
        manager = create_default_template_manager()
        recommender = TemplateRecommender(manager)

        recommendations = recommender.recommend("postgres", Path("/path/to/project"))

        if recommendations:
            top = recommendations[0]
            print(f"Recommend: {top.template.name} (confidence: {top.confidence:.0%})")
            for reason in top.reasons:
                print(f"  - {reason}")
        ```

    Attributes:
        template_manager: TemplateManager for loading available templates
        detector: ProjectDetector for analyzing project directories
        min_confidence: Minimum confidence threshold for recommendations (default: 0.3)
    """

    def __init__(
        self,
        template_manager: TemplateManager,
        detector: Optional[ProjectDetector] = None,
        min_confidence: float = 0.3,
    ):
        """Initialize the template recommender.

        Args:
            template_manager: TemplateManager for loading templates
            detector: Optional ProjectDetector (creates default if not provided)
            min_confidence: Minimum confidence threshold for recommendations (0.0-1.0)
        """
        self.template_manager = template_manager
        self.detector = detector if detector is not None else ProjectDetector()
        self.min_confidence = min_confidence

    def recommend(
        self,
        server_id: str,
        project_path: Optional[Path] = None,
        top_n: int = 3,
    ) -> list[TemplateRecommendation]:
        """Recommend templates for a server based on project context.

        Analyzes the project directory (if provided), loads all templates for
        the specified server, scores each template against the project context,
        and returns ranked recommendations.

        Args:
            server_id: Server ID to get recommendations for (e.g., "postgres")
            project_path: Path to project directory to analyze (uses cwd if None)
            top_n: Maximum number of recommendations to return

        Returns:
            List of TemplateRecommendation objects, sorted by confidence (high to low).
            Empty list if no templates meet the minimum confidence threshold.

        Note:
            The scoring algorithm:
            1. Detects project context using ProjectDetector
            2. Loads all templates for the server
            3. Scores each template against context:
               - Docker usage: +0.4 weight if has_docker_compose AND service matches
               - Service match: +0.5 weight if docker service matches server_id
               - Language match: +0.3 weight if language matches template metadata
            4. Filters by min_confidence threshold
            5. Sorts by confidence descending
            6. Returns top N recommendations with explanations
        """
        # Use current directory if no path provided
        if project_path is None:
            project_path = Path.cwd()

        # Detect project context
        context = self.detector.detect(project_path)

        # Load templates for server
        templates = self.template_manager.list_templates(server_id)

        if not templates:
            return []

        # Score each template
        recommendations = []
        for template in templates:
            confidence, reasons = self._score_template(template, context)

            # Filter by minimum confidence
            if confidence >= self.min_confidence:
                recommendations.append(
                    TemplateRecommendation(
                        template=template,
                        confidence=confidence,
                        reasons=reasons,
                    )
                )

        # Sort by confidence descending
        recommendations.sort(key=lambda r: r.confidence, reverse=True)

        # Return top N
        return recommendations[:top_n]

    def _score_template(
        self,
        template: ServerTemplate,
        context: ProjectContext,
    ) -> tuple[float, list[str]]:
        """Score a single template against project context.

        Args:
            template: Template to score
            context: Detected project context

        Returns:
            Tuple of (confidence_score, reasons_list)

        Note:
            Scoring weights:
            - Docker match with service: +0.4 (only if service matches)
            - docker_service matches server_id: +0.5
            - language matches template metadata: +0.3
            - database in context matches template: +0.3
            - Baseline score: 0.35 (ensures all templates are considered)
        """
        score = 0.35  # Baseline score for all templates
        reasons = []

        # Track if template is docker-based or anti-docker
        template_is_docker = any(
            keyword in template.best_for or keyword in template.keywords
            for keyword in ["docker", "docker-compose", "containers"]
        )
        template_is_local = any(
            keyword in template.best_for or keyword in template.keywords
            for keyword in ["local", "local-development", "native", "no-docker"]
        )

        # Check if docker service name matches server_id (weight: 0.5)
        has_service_match = context.docker_services and template.server_id in context.docker_services

        # Check for database match in services (weight: 0.3)
        has_database_match = context.databases and template.server_id in context.databases

        # Docker + Service Match (weight: 0.4)
        # Only give docker bonus if there's actually a matching service
        if context.has_docker_compose and template_is_docker:
            if has_service_match or has_database_match:
                score += 0.4
                reasons.append("Project uses Docker Compose")
            # No bonus if docker exists but service doesn't match

        # Service name match (weight: 0.5)
        if has_service_match:
            score += 0.5
            reasons.append(
                f"Detected '{template.server_id}' service in docker-compose.yml"
            )

        # Database match (weight: 0.3)
        if has_database_match:
            score += 0.3
            reasons.append(f"Project uses {template.server_id} database")

        # Check language compatibility (weight: 0.3)
        if context.language:
            if context.language in template.keywords or context.language in template.best_for:
                score += 0.3
                reasons.append(f"Compatible with {context.language} projects")

        # No Docker - favor local templates (weight: 0.3)
        if not context.has_docker_compose and not context.has_docker:
            if template_is_local:
                score += 0.3
                reasons.append("No Docker detected - local development setup")

        # Penalize mismatches
        if context.has_docker_compose and template_is_local:
            score -= 0.25  # Docker project but local template - always penalize
        if not context.has_docker_compose and template_is_docker:
            score -= 0.1  # No docker but docker template

        # Normalize score to 0.0-1.0 range
        # Maximum possible score: 0.35 (baseline) + 0.4 (docker) + 0.5 (service) + 0.3 (database) + 0.3 (language) = 1.85
        # Cap at 1.0, floor at 0.0
        score = max(0.0, min(score, 1.0))

        # If no specific matches, provide generic reason
        if not reasons:
            reasons.append(f"General-purpose {template.server_id} template")

        return score, reasons
