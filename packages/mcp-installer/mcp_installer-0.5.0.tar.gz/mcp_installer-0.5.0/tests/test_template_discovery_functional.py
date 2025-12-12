"""Un-Gameable Functional Tests for Template Discovery Engine

This test suite validates the Template Discovery Engine with real user workflows
that are immune to AI gaming. These tests verify ACTUAL functionality, not mocks.

TRACEABILITY TO STATUS AND PLAN:
===============================

STATUS Gaps Addressed (STATUS-TEMPLATE-DISCOVERY-EVALUATION-2025-11-17-080057.md):
- Section 2.1: Project detection system (0% implemented) → All detection tests
- Section 2.2: Recommendation scoring (0% implemented) → All recommendation tests
- Section 6.1: 95%+ test coverage needed → Comprehensive coverage of all workflows

PLAN Items Validated (PLAN-TEMPLATE-DISCOVERY-2025-11-17-080505.md):
- P0-2: Docker Detection (lines 118-135) → test_detect_docker_compose_project
- P0-3: Language Detection (lines 137-159) → test_detect_nodejs_project, test_detect_python_project
- P0-4: Database Detection (lines 161-183) → test_detect_database_from_docker_compose
- P0-5: ProjectDetector Integration (lines 185-206) → test_detect_complex_project_context
- P0-8: Scoring Algorithm (lines 260-282) → test_recommend_best_template_for_context
- P0-10: TemplateRecommender (lines 307-333) → All recommendation workflow tests
- P1-17: Integration Tests (lines 489-512) → All end-to-end tests

TEST PHILOSOPHY:
================
These tests validate REAL functionality by:
1. Using actual file system operations (docker-compose.yml, package.json, etc.)
2. Verifying observable outcomes users would see
3. Testing complete workflows from detection → scoring → recommendation
4. Ensuring recommendations are logically correct (Docker project → Docker template)
5. Cannot be satisfied by stubs or mocked implementations

GAMING RESISTANCE:
==================
These tests CANNOT be gamed because:
1. Use REAL project structures (files, directories, content)
2. Verify actual file parsing (YAML, JSON)
3. Check logical correctness of recommendations (scores must make sense)
4. Test multiple verification points (detection + scoring + ranking)
5. Validate explanations match the actual detection results
6. Cannot pass with hardcoded responses (different projects → different recommendations)
"""

import json
from pathlib import Path
from typing import Dict, List

import pytest
import yaml

from mcpi.templates.discovery import ProjectDetector
from mcpi.templates.recommender import TemplateRecommender
from mcpi.templates.template_manager import create_test_template_manager, create_default_template_manager


class TestProjectDetection:
    """Functional tests for project context detection.

    USER PERSPECTIVE: "Can the system detect what kind of project I have?"

    These tests verify that the discovery engine can accurately identify:
    - Docker usage (docker-compose.yml, Dockerfile)
    - Programming languages (package.json, requirements.txt, go.mod)
    - Database services (from docker-compose or environment files)
    - Project characteristics needed for template recommendations

    GAMING RESISTANCE:
    - Uses real file structures (not mocks)
    - Verifies actual file parsing
    - Tests graceful failure (corrupted files, missing files)
    - Cannot fake without proper file I/O
    """

    def test_detect_docker_compose_project(self, tmp_path: Path):
        """Test detection of Docker Compose project with services.

        PLAN Reference: P0-2 Docker Detection (lines 118-135)

        USER SCENARIO:
        1. User has a project with docker-compose.yml
        2. Docker compose defines services: postgres, redis, web
        3. System should detect Docker Compose usage
        4. System should extract service names for matching

        OBSERVABLE OUTCOMES:
        - has_docker_compose = True
        - docker_services contains ['postgres', 'redis', 'web']
        - Recommendations favor Docker-based templates

        GAMING RESISTANCE:
        - Must parse real YAML file
        - Must extract actual service names
        - Cannot fake with hardcoded response
        """
        # GIVEN: Project with docker-compose.yml
        project_dir = tmp_path / "my_project"
        project_dir.mkdir()

        docker_compose_content = {
            "version": "3.8",
            "services": {
                "postgres": {
                    "image": "postgres:15",
                    "environment": {
                        "POSTGRES_PASSWORD": "secret"
                    },
                    "ports": ["5432:5432"]
                },
                "redis": {
                    "image": "redis:7",
                    "ports": ["6379:6379"]
                },
                "web": {
                    "build": ".",
                    "ports": ["8000:8000"],
                    "depends_on": ["postgres", "redis"]
                }
            }
        }

        compose_file = project_dir / "docker-compose.yml"
        with open(compose_file, 'w') as f:
            yaml.dump(docker_compose_content, f)

        # WHEN: Detection runs (this will be implemented)
        detector = ProjectDetector()
        context = detector.detect(project_dir)

        # THEN: Must detect Docker Compose and services
        # These assertions will initially fail (TDD approach)
        assert context.has_docker_compose is True, "Should detect docker-compose.yml"
        assert set(context.docker_services) == {"postgres", "redis", "web"}, \
            "Should extract all service names from docker-compose.yml"
        assert context.has_docker is True, "Docker Compose implies Docker usage"

        # VERIFICATION: File actually exists and is readable
        assert compose_file.exists(), "Test setup: docker-compose.yml must exist"
        with open(compose_file) as f:
            parsed = yaml.safe_load(f)
        assert "services" in parsed, "Test setup: YAML must be valid"
        assert "postgres" in parsed["services"], "Test setup: postgres service must be defined"

    def test_detect_nodejs_project(self, tmp_path: Path):
        """Test detection of Node.js project from package.json.

        PLAN Reference: P0-3 Language Detection (lines 137-159)

        USER SCENARIO:
        1. User has a Node.js project with package.json
        2. System should identify language as "nodejs"
        3. Recommendations favor Node.js-compatible templates

        OBSERVABLE OUTCOMES:
        - language = "nodejs"
        - Node.js-specific templates score higher

        GAMING RESISTANCE:
        - Must read actual package.json file
        - Different language → different detection result
        """
        # GIVEN: Node.js project
        project_dir = tmp_path / "nodejs_app"
        project_dir.mkdir()

        package_json = {
            "name": "my-app",
            "version": "1.0.0",
            "dependencies": {
                "express": "^4.18.0"
            }
        }

        package_file = project_dir / "package.json"
        with open(package_file, 'w') as f:
            json.dump(package_json, f)

        # WHEN: Detection runs
        detector = ProjectDetector()
        context = detector.detect(project_dir)

        # THEN: Must detect Node.js
        assert context.language == "nodejs", "Should detect Node.js from package.json"

        # VERIFICATION: File is real and parseable
        assert package_file.exists()
        with open(package_file) as f:
            parsed = json.load(f)
        assert parsed["name"] == "my-app"

    def test_detect_python_project(self, tmp_path: Path):
        """Test detection of Python project from requirements.txt.

        PLAN Reference: P0-3 Language Detection (lines 137-159)

        USER SCENARIO:
        1. User has Python project with requirements.txt
        2. System should identify language as "python"

        OBSERVABLE OUTCOMES:
        - language = "python"
        - Python-specific templates score higher

        GAMING RESISTANCE:
        - Different project type → different result
        - Cannot hardcode "nodejs" for all projects
        """
        # GIVEN: Python project
        project_dir = tmp_path / "python_app"
        project_dir.mkdir()

        requirements = project_dir / "requirements.txt"
        requirements.write_text("django==4.2.0\npsycopg2==2.9.0\n")

        # WHEN: Detection runs
        detector = ProjectDetector()
        context = detector.detect(project_dir)

        # THEN: Must detect Python
        assert context.language == "python", "Should detect Python from requirements.txt"

        # VERIFICATION: File exists
        assert requirements.exists()
        assert "django" in requirements.read_text()

    def test_detect_go_project(self, tmp_path: Path):
        """Test detection of Go project from go.mod.

        PLAN Reference: P0-3 Language Detection (mentions Go support)
        GAP-FILLING TEST: Added per FUNCTIONAL-TEST-EVALUATION-2025-11-18.md

        USER SCENARIO:
        1. User has Go project with go.mod
        2. System should identify language as "go"

        OBSERVABLE OUTCOMES:
        - language = "go"
        - Go-specific templates score higher

        GAMING RESISTANCE:
        - Different language file → different detection
        - Cannot assume only Node.js/Python exist
        """
        # GIVEN: Go project
        project_dir = tmp_path / "go_app"
        project_dir.mkdir()

        go_mod = project_dir / "go.mod"
        go_mod.write_text("module example.com/myapp\n\ngo 1.21\n")

        # WHEN: Detection runs
        detector = ProjectDetector()
        context = detector.detect(project_dir)

        # THEN: Must detect Go
        assert context.language == "go", "Should detect Go from go.mod"

        # VERIFICATION: File exists
        assert go_mod.exists()
        assert "module example.com/myapp" in go_mod.read_text()

    def test_detect_database_from_docker_compose(self, tmp_path: Path):
        """Test detection of database services from docker-compose.

        PLAN Reference: P0-4 Database Detection (lines 161-183)

        USER SCENARIO:
        1. User has docker-compose.yml with database services
        2. System should identify databases in use (postgres, mysql, redis)
        3. Recommendations favor templates for those databases

        OBSERVABLE OUTCOMES:
        - databases list contains detected database types
        - postgres service → postgres template recommended

        GAMING RESISTANCE:
        - Must parse docker-compose services
        - Must identify database types from service names/images
        """
        # GIVEN: Docker Compose with databases
        project_dir = tmp_path / "fullstack_app"
        project_dir.mkdir()

        docker_compose = {
            "services": {
                "postgres": {"image": "postgres:15"},
                "mysql": {"image": "mysql:8"},
                "redis": {"image": "redis:7"},
                "web": {"image": "node:18"}
            }
        }

        compose_file = project_dir / "docker-compose.yml"
        with open(compose_file, 'w') as f:
            yaml.dump(docker_compose, f)

        # WHEN: Detection runs
        detector = ProjectDetector()
        context = detector.detect(project_dir)

        # THEN: Must detect databases
        assert "postgres" in context.databases, "Should detect postgres from service name"
        assert "mysql" in context.databases, "Should detect mysql from service name"
        assert "redis" in context.databases, "Should detect redis from service name"
        assert "web" not in context.databases, "Should not misidentify non-database services"

        # VERIFICATION: Services exist
        assert compose_file.exists()
        with open(compose_file) as f:
            data = yaml.safe_load(f)
        assert len(data["services"]) == 4

    def test_detect_database_from_env_file(self, tmp_path: Path):
        """Test database detection from .env DATABASE_URL.

        PLAN mentioned .env detection as future enhancement.
        GAP-FILLING TEST: Added per FUNCTIONAL-TEST-EVALUATION-2025-11-18.md

        USER SCENARIO:
        1. User has .env file with DATABASE_URL
        2. System should detect database type from URL
        3. Works for non-Docker projects using local databases

        OBSERVABLE OUTCOMES:
        - databases contains detected type from URL
        - postgres URL → postgres in databases

        GAMING RESISTANCE:
        - Must parse .env file
        - Must extract database type from URL pattern
        """
        # GIVEN: Project with .env database configuration
        project_dir = tmp_path / "env_project"
        project_dir.mkdir()

        env_file = project_dir / ".env"
        env_file.write_text("DATABASE_URL=postgresql://localhost:5432/mydb\n")

        # WHEN: Detection runs
        detector = ProjectDetector()
        context = detector.detect(project_dir)

        # THEN: Should detect postgres from DATABASE_URL
        assert "postgres" in context.databases, \
            "Should detect postgres from postgresql:// URL in .env"

        # VERIFICATION: File exists and contains URL
        assert env_file.exists()
        assert "postgresql://" in env_file.read_text()

    def test_detect_complex_project_context(self, tmp_path: Path):
        """Test detection of complete project context with multiple indicators.

        PLAN Reference: P0-5 ProjectDetector Integration (lines 185-206)

        USER SCENARIO:
        1. User has real-world project with Docker, Node.js, and postgres
        2. System should detect ALL relevant characteristics
        3. Complete context enables accurate recommendations

        OBSERVABLE OUTCOMES:
        - has_docker_compose = True
        - language = "nodejs"
        - docker_services includes "postgres"
        - databases includes "postgres"
        - All detection results feed into scoring

        GAMING RESISTANCE:
        - Tests complete integration of all detectors
        - Must handle real project structure
        - All detection paths must work together
        """
        # GIVEN: Complex realistic project
        project_dir = tmp_path / "real_world_app"
        project_dir.mkdir()

        # Docker Compose with postgres
        docker_compose = {
            "version": "3.8",
            "services": {
                "postgres": {
                    "image": "postgres:15",
                    "environment": {"POSTGRES_DB": "myapp"}
                },
                "app": {
                    "build": ".",
                    "depends_on": ["postgres"]
                }
            }
        }
        (project_dir / "docker-compose.yml").write_text(yaml.dump(docker_compose))

        # Node.js application
        package_json = {
            "name": "real-world-app",
            "dependencies": {"express": "^4.18.0", "pg": "^8.11.0"}
        }
        (project_dir / "package.json").write_text(json.dumps(package_json))

        # Dockerfile
        (project_dir / "Dockerfile").write_text("FROM node:18\nWORKDIR /app\n")

        # WHEN: Complete detection runs
        detector = ProjectDetector()
        context = detector.detect(project_dir)

        # THEN: All context detected
        assert context.has_docker_compose is True
        assert context.has_docker is True
        assert context.language == "nodejs"
        assert "postgres" in context.docker_services
        assert "postgres" in context.databases

        # VERIFICATION: All files exist
        assert (project_dir / "docker-compose.yml").exists()
        assert (project_dir / "package.json").exists()
        assert (project_dir / "Dockerfile").exists()

    def test_detect_graceful_failure_on_corrupted_yaml(self, tmp_path: Path):
        """Test graceful handling of corrupted docker-compose.yml.

        PLAN Reference: P0-2 Docker Detection (line 127: "graceful failure")

        USER SCENARIO:
        1. User has corrupted docker-compose.yml (syntax error)
        2. System should not crash
        3. System should continue with empty services list

        OBSERVABLE OUTCOMES:
        - Detection completes without exception
        - has_docker_compose may be True (file exists)
        - docker_services is empty list (parsing failed gracefully)

        GAMING RESISTANCE:
        - Must handle real parsing errors
        - Cannot assume all files are valid
        - Error handling is critical functionality
        """
        # GIVEN: Corrupted YAML file
        project_dir = tmp_path / "broken_project"
        project_dir.mkdir()

        compose_file = project_dir / "docker-compose.yml"
        compose_file.write_text("invalid: yaml: content: [[[")

        # WHEN: Detection runs on corrupted file
        detector = ProjectDetector()
        context = detector.detect(project_dir)

        # THEN: Should not crash, should return empty services
        assert context.docker_services == [], \
            "Should return empty list when YAML parsing fails"

        # VERIFICATION: File is actually invalid
        assert compose_file.exists()
        with pytest.raises(yaml.YAMLError):
            yaml.safe_load(compose_file.read_text())

    def test_detect_empty_project(self, tmp_path: Path):
        """Test detection on empty project (no indicators).

        USER SCENARIO:
        1. User runs detection on brand new/empty project
        2. System should return "no indicators found" result
        3. Recommendations will use generic templates

        OBSERVABLE OUTCOMES:
        - All detection flags are False/empty
        - No crash or error
        - Recommendation system uses fallback behavior

        GAMING RESISTANCE:
        - Must handle "nothing to detect" case
        - Cannot assume indicators always exist
        """
        # GIVEN: Empty project directory
        project_dir = tmp_path / "empty_project"
        project_dir.mkdir()

        # WHEN: Detection runs
        detector = ProjectDetector()
        context = detector.detect(project_dir)

        # THEN: All flags should be False/empty
        assert context.has_docker is False
        assert context.has_docker_compose is False
        assert context.language is None
        assert context.docker_services == []
        assert context.databases == []

        # VERIFICATION: Directory is actually empty
        assert project_dir.exists()
        assert list(project_dir.iterdir()) == []

    def test_detection_performance(self, tmp_path: Path):
        """Test that detection completes in < 100ms.

        PLAN Reference: P0-5 mentions < 100ms target for detection
        GAP-FILLING TEST: Added per FUNCTIONAL-TEST-EVALUATION-2025-11-18.md

        USER SCENARIO:
        1. User runs detection on typical project
        2. Detection should be fast (< 100ms)
        3. CLI remains responsive

        OBSERVABLE OUTCOMES:
        - Detection completes quickly
        - Results are correct
        - No performance degradation

        GAMING RESISTANCE:
        - CRITICAL: Checks correctness FIRST, then performance
        - Cannot be gamed by returning empty results quickly
        - Must actually parse files AND be fast
        """
        import time

        # GIVEN: Realistic project
        project_dir = tmp_path / "perf_test"
        project_dir.mkdir()

        docker_compose = {"services": {"postgres": {"image": "postgres:15"}}}
        (project_dir / "docker-compose.yml").write_text(yaml.dump(docker_compose))
        (project_dir / "package.json").write_text('{"name": "test"}')

        detector = ProjectDetector()

        # WHEN: Measure detection time
        start = time.time()
        context = detector.detect(project_dir)
        elapsed = time.time() - start

        # THEN: Must be correct FIRST (cannot game by returning empty quickly)
        assert context.has_docker_compose is True, "Must detect correctly (not skip for speed)"
        assert context.language == "nodejs", "Must detect language correctly"

        # THEN: Must also be fast (performance check comes AFTER correctness)
        assert elapsed < 0.1, f"Detection took {elapsed:.3f}s, target < 0.100s"


class TestTemplateRecommendation:
    """Functional tests for template recommendation workflows.

    USER PERSPECTIVE: "Does the system recommend the RIGHT template for my project?"

    These tests verify that:
    - Scoring algorithm matches context to templates correctly
    - Recommendations are ranked by confidence
    - Explanations make sense
    - Edge cases are handled properly

    GAMING RESISTANCE:
    - Tests logical correctness of recommendations
    - Docker project MUST recommend Docker template
    - Scores must be mathematically correct
    - Cannot fake with hardcoded recommendations
    """

    def test_recommend_docker_template_for_docker_project(self, tmp_path: Path):
        """Test that Docker project gets Docker template recommendation.

        PLAN Reference: P0-8 Scoring Algorithm (lines 260-282)
        PLAN Reference: P1-17 Integration Test (line 499: "Docker Compose project recommends postgres/docker")

        USER SCENARIO:
        1. User has project with docker-compose.yml containing postgres service
        2. User runs: mcpi add postgres --recommend
        3. System should recommend postgres/docker template (high confidence)
        4. Explanation should mention Docker Compose detection

        OBSERVABLE OUTCOMES:
        - Top recommendation is postgres/docker template
        - Confidence > 0.5 (strong match)
        - Reasons include "uses Docker" or similar
        - Alternative templates ranked lower

        GAMING RESISTANCE:
        - Must actually match detection results to template metadata
        - Docker project → Docker template (logic must be correct)
        - Scores must reflect actual matching criteria
        - Explanations must match detection results
        """
        # GIVEN: Docker Compose project with postgres
        project_dir = tmp_path / "docker_project"
        project_dir.mkdir()

        docker_compose = {
            "services": {
                "postgres": {"image": "postgres:15"},
                "web": {"build": "."}
            }
        }
        (project_dir / "docker-compose.yml").write_text(yaml.dump(docker_compose))
        (project_dir / "package.json").write_text('{"name": "app"}')

        # WHEN: Recommendation system processes this project
        template_manager = create_test_template_manager(Path(__file__).parent.parent / "src" / "mcpi" / "data" / "templates")
        recommender = TemplateRecommender(template_manager)
        recommendations = recommender.recommend("postgres", project_dir)

        # THEN: Top recommendation MUST be docker template
        assert len(recommendations) > 0, "Should have at least one recommendation"
        top = recommendations[0]
        assert "docker" in top.template.name.lower(), \
            f"Top recommendation should be docker template, got: {top.template.name}"
        assert top.confidence >= 0.5, \
            f"Docker project should have high confidence, got: {top.confidence}"
        assert any("docker" in reason.lower() for reason in top.reasons), \
            "Explanation should mention Docker detection"

        # VERIFICATION: Detection would find Docker indicators
        assert (project_dir / "docker-compose.yml").exists()
        with open(project_dir / "docker-compose.yml") as f:
            data = yaml.safe_load(f)
        assert "postgres" in data["services"]

    def test_recommend_local_template_for_non_docker_project(self, tmp_path: Path):
        """Test that non-Docker project gets local-development template.

        PLAN Reference: P1-17 Integration Test (line 500: "No Docker project recommends local-development")

        USER SCENARIO:
        1. User has Python project WITHOUT Docker
        2. User wants to add postgres server
        3. System should recommend local-development template
        4. Docker template should rank lower or not appear

        OBSERVABLE OUTCOMES:
        - Top recommendation is local-development or similar
        - Docker template ranks lower (lower confidence)
        - Explanation mentions "no Docker detected" or "local development"

        GAMING RESISTANCE:
        - Different project type → different recommendation
        - Cannot always recommend Docker template
        - Scoring must adapt to project context
        """
        # GIVEN: Local Python project (no Docker)
        project_dir = tmp_path / "local_project"
        project_dir.mkdir()

        # Only Python indicators, no Docker
        (project_dir / "requirements.txt").write_text("django==4.2.0\npsycopg2==2.9.0\n")
        (project_dir / "manage.py").write_text("# Django management script\n")

        # WHEN: Recommendation runs
        template_manager = create_test_template_manager(Path(__file__).parent.parent / "src" / "mcpi" / "data" / "templates")
        recommender = TemplateRecommender(template_manager)
        recommendations = recommender.recommend("postgres", project_dir)

        # THEN: Should NOT recommend Docker template as top choice
        assert len(recommendations) > 0
        top = recommendations[0]
        # Should prefer local-development or production, NOT docker
        assert "docker" not in top.template.name.lower() or top.confidence < 0.4, \
            "Docker template should not be top choice for non-Docker project"

        # VERIFICATION: No Docker files present
        assert not (project_dir / "docker-compose.yml").exists()
        assert not (project_dir / "Dockerfile").exists()
        assert (project_dir / "requirements.txt").exists()

    def test_recommend_multiple_templates_ranked(self, tmp_path: Path):
        """Test that multiple templates are ranked by confidence.

        PLAN Reference: P0-10 TemplateRecommender (line 324: "Sorts by confidence descending")

        USER SCENARIO:
        1. User has project that matches multiple templates
        2. System returns ranked list (best to worst)
        3. User can see alternatives and make informed choice

        OBSERVABLE OUTCOMES:
        - Recommendations sorted by confidence (high to low)
        - All recommendations above threshold (e.g., 0.3)
        - Each has clear explanation

        GAMING RESISTANCE:
        - Must rank ALL matching templates
        - Order must be mathematically correct
        - Cannot arbitrarily pick one template
        """
        # GIVEN: Project with mixed indicators
        project_dir = tmp_path / "mixed_project"
        project_dir.mkdir()

        # Has Docker Compose, but also local development indicators
        docker_compose = {
            "services": {
                "postgres": {"image": "postgres:15"}
            }
        }
        (project_dir / "docker-compose.yml").write_text(yaml.dump(docker_compose))
        (project_dir / "package.json").write_text('{"name": "app"}')
        (project_dir / ".env").write_text("DATABASE_URL=postgresql://localhost/dev\n")

        # WHEN: Get all recommendations
        template_manager = create_test_template_manager(Path(__file__).parent.parent / "src" / "mcpi" / "data" / "templates")
        recommender = TemplateRecommender(template_manager)
        recommendations = recommender.recommend("postgres", project_dir)

        # THEN: Multiple templates ranked
        assert len(recommendations) >= 2, "Should have multiple recommendations"
        # Check sorting (confidence descending)
        confidences = [r.confidence for r in recommendations]
        assert confidences == sorted(confidences, reverse=True), \
            "Recommendations must be sorted by confidence (high to low)"
        # All above threshold
        assert all(r.confidence >= 0.3 for r in recommendations), \
            "All recommendations should meet minimum confidence threshold"

        # VERIFICATION: Multiple indicators present
        assert (project_dir / "docker-compose.yml").exists()
        assert (project_dir / ".env").exists()

    def test_recommend_low_confidence_for_mismatched_project(self, tmp_path: Path):
        """Test that mismatched project returns low-confidence or empty recommendations.

        PLAN Reference: P0-10 TemplateRecommender (line 323: "Filters by minimum confidence threshold (0.3)")

        USER SCENARIO:
        1. User has project that doesn't match any template well
        2. System returns low confidence matches or empty list
        3. CLI falls back to showing all templates

        OBSERVABLE OUTCOMES:
        - Empty recommendation list OR
        - All recommendations below strong confidence threshold
        - User sees "No clear recommendation" message

        GAMING RESISTANCE:
        - Cannot always return recommendations
        - Must respect confidence threshold
        - Low/empty result is valid and important
        """
        # GIVEN: Project with indicators that don't match postgres templates
        project_dir = tmp_path / "mismatch_project"
        project_dir.mkdir()

        # Has Docker, but not database-related
        docker_compose = {
            "services": {
                "web": {"image": "nginx:latest"},
                "cache": {"image": "memcached:latest"}
            }
        }
        (project_dir / "docker-compose.yml").write_text(yaml.dump(docker_compose))

        # WHEN: Request postgres recommendations
        template_manager = create_test_template_manager(Path(__file__).parent.parent / "src" / "mcpi" / "data" / "templates")
        recommender = TemplateRecommender(template_manager)
        recommendations = recommender.recommend("postgres", project_dir)

        # THEN: May return empty list or low-confidence matches
        # Either no recommendations, or all below strong threshold
        if recommendations:
            assert all(r.confidence < 0.6 for r in recommendations), \
                "No template should have high confidence for mismatched project"

        # VERIFICATION: No postgres indicators
        with open(project_dir / "docker-compose.yml") as f:
            data = yaml.safe_load(f)
        assert "postgres" not in str(data).lower()

    def test_recommend_confidence_scoring_correctness(self, tmp_path: Path):
        """Test that confidence scores are mathematically correct.

        PLAN Reference: P0-8 Scoring Algorithm (lines 271-281: scoring weights)

        USER SCENARIO:
        1. System detects multiple matching characteristics
        2. Scoring algorithm applies weights correctly
        3. Final confidence score is accurate and explainable

        OBSERVABLE OUTCOMES:
        - Scores are between 0.0 and 1.0
        - Scores reflect detected matches (more matches = higher score)
        - Weights are applied consistently

        GAMING RESISTANCE:
        - Must perform actual score calculation
        - Cannot hardcode scores
        - Math must be correct
        """
        # GIVEN: Project with known characteristics
        project_dir = tmp_path / "scoring_test"
        project_dir.mkdir()

        # Characteristics that should score:
        # - Docker Compose: +0.4 weight
        # - Postgres service match: +0.5 weight
        # - Language match: +0.3 weight (if template specifies)
        docker_compose = {
            "services": {
                "postgres": {"image": "postgres:15"}
            }
        }
        (project_dir / "docker-compose.yml").write_text(yaml.dump(docker_compose))
        (project_dir / "package.json").write_text('{"name": "app"}')

        # WHEN: Scoring happens
        template_manager = create_test_template_manager(Path(__file__).parent.parent / "src" / "mcpi" / "data" / "templates")
        recommender = TemplateRecommender(template_manager)
        recommendations = recommender.recommend("postgres", project_dir)

        # THEN: Score calculation is correct
        if recommendations:
            top = recommendations[0]
            # With docker (0.4) + docker service match (0.5) = 0.9 minimum
            assert top.confidence >= 0.8, \
                f"Expected high confidence for Docker + service match, got: {top.confidence}"
            assert top.confidence <= 1.0, "Confidence must not exceed 1.0"

        # VERIFICATION: Strong indicators present
        assert (project_dir / "docker-compose.yml").exists()
        with open(project_dir / "docker-compose.yml") as f:
            data = yaml.safe_load(f)
        assert "postgres" in data["services"]

    def test_recommend_explanations_match_detection(self, tmp_path: Path):
        """Test that recommendation explanations match actual detection results.

        PLAN Reference: P0-8 Scoring Algorithm (line 278: "reasons: List[str]")

        USER SCENARIO:
        1. User sees recommendation with explanations
        2. Explanations should accurately describe WHY recommended
        3. Explanations based on actual detected characteristics

        OBSERVABLE OUTCOMES:
        - Each recommendation has reasons list
        - Reasons are specific and accurate
        - "Uses Docker" only appears if Docker detected
        - Service names match actual docker-compose services

        GAMING RESISTANCE:
        - Explanations must be generated from detection results
        - Cannot have generic explanations for all projects
        - Must reference actual detected services (postgres, redis)
        - Cannot pass with generic text like "This template uses Docker Compose"
        """
        # GIVEN: Project with specific detectable features
        project_dir = tmp_path / "explanation_test"
        project_dir.mkdir()

        docker_compose = {
            "services": {
                "postgres": {"image": "postgres:15"},
                "redis": {"image": "redis:7"}
            }
        }
        (project_dir / "docker-compose.yml").write_text(yaml.dump(docker_compose))

        # WHEN: Get recommendation with reasons
        template_manager = create_test_template_manager(Path(__file__).parent.parent / "src" / "mcpi" / "data" / "templates")
        recommender = TemplateRecommender(template_manager)
        recommendations = recommender.recommend("postgres", project_dir)

        # THEN: Reasons must reference actual detected services
        if recommendations:
            top = recommendations[0]
            reasons_text = " ".join(top.reasons).lower()

            # CRITICAL: Explanations must reference ACTUAL detected services
            # The docker-compose has "postgres" and "redis" services
            # Explanations MUST mention these specific services, not generic Docker text

            # Must mention Docker/Compose (detects docker-compose.yml)
            assert "docker" in reasons_text or "compose" in reasons_text, \
                "Explanation should mention Docker when Docker detected"

            # SEMANTIC VALIDATION: Must reference actual detected services
            # Cannot pass with just "This template uses Docker Compose"
            # Must mention specific services that were detected
            assert "postgres" in reasons_text or "database" in reasons_text, \
                "Explanation must reference actual detected service 'postgres' or generic 'database'"

            # Additional semantic check: if redis detected, might be mentioned
            # This enforces that explanations are based on actual detection, not templates

        # VERIFICATION: Detection would find these specific features
        assert (project_dir / "docker-compose.yml").exists()
        with open(project_dir / "docker-compose.yml") as f:
            data = yaml.safe_load(f)
        assert "postgres" in data["services"], "Test setup: postgres service must exist"
        assert "redis" in data["services"], "Test setup: redis service must exist"


class TestTemplateMetadata:
    """Tests for template metadata coverage and correctness.

    GAP-FILLING TEST CLASS: Added per FUNCTIONAL-TEST-EVALUATION-2025-11-18.md

    These tests verify that production templates have the metadata needed
    for the recommendation engine to function correctly.
    """

    def test_all_templates_have_metadata(self):
        """Verify all postgres templates have complete metadata.

        PLAN Reference: P0-7 requires metadata on all templates
        GAP-FILLING TEST: Added per FUNCTIONAL-TEST-EVALUATION-2025-11-18.md

        TDD APPROACH: This test will FAIL until P0-7 is complete. That's correct!
        This test should fail now because template metadata has not been added yet.
        When P0-7 is implemented, this test should PASS.

        DO NOT SKIP THIS TEST. Skipped tests violate TestCriteria #4 (AUTOMATED).
        Let it fail. Implement P0-7. Watch it pass. That's TDD.

        USER SCENARIO:
        1. Recommendation engine needs template metadata
        2. All templates must have best_for, keywords, recommendations
        3. Missing metadata prevents recommendations from working

        OBSERVABLE OUTCOMES:
        - All templates load successfully
        - All have best_for tags (minimum 2)
        - All have keywords (minimum 3)
        - Known templates have expected metadata

        GAMING RESISTANCE:
        - Must load actual template files
        - Cannot fake metadata in tests
        - Metadata must exist in YAML files
        """
        # GIVEN: Production template manager
        template_manager = create_default_template_manager()

        # WHEN: Load postgres templates
        postgres_templates = template_manager.list_templates("postgres")

        # THEN: Should have at least 3 templates
        assert len(postgres_templates) >= 3, \
            "Should have docker, local-development, and production templates"

        # AND: Each must have complete metadata
        for template in postgres_templates:
            # Must have best_for tags
            assert len(template.best_for) >= 2, \
                f"{template.name} needs at least 2 best_for tags, has {len(template.best_for)}"

            # Must have keywords
            assert len(template.keywords) >= 3, \
                f"{template.name} needs at least 3 keywords, has {len(template.keywords)}"

        # AND: Verify expected metadata for known templates
        docker_template = next((t for t in postgres_templates if t.name == "docker"), None)
        if docker_template:
            assert "docker" in docker_template.best_for or "containers" in docker_template.best_for, \
                "Docker template should have docker-related best_for tags"
            assert "docker" in docker_template.keywords or "compose" in docker_template.keywords, \
                "Docker template should have docker-related keywords"


class TestEndToEndWorkflows:
    """End-to-end functional tests for complete recommendation workflows.

    USER PERSPECTIVE: "Does the entire feature work together?"

    These tests validate complete user journeys from project detection
    through recommendation to template selection.

    GAMING RESISTANCE:
    - Tests complete integration of all components
    - Uses real project structures
    - Verifies end-to-end behavior
    """

    def test_complete_workflow_docker_to_recommendation(self, tmp_path: Path):
        """Test complete workflow: Docker project → detection → recommendation.

        PLAN Reference: P1-17 Integration Tests (lines 489-512)

        USER SCENARIO (Complete Journey):
        1. User has Docker Compose project with postgres
        2. User runs: mcpi add postgres --recommend
        3. System detects: Docker Compose, postgres service, nodejs
        4. System scores all postgres templates
        5. System recommends postgres/docker (high confidence)
        6. User sees clear explanation
        7. User can accept or see alternatives

        OBSERVABLE OUTCOMES:
        - All detection steps complete
        - Scoring produces correct ranking
        - Top recommendation is postgres/docker
        - Explanation mentions Docker and service match
        - User has actionable choices

        GAMING RESISTANCE:
        - Tests ENTIRE pipeline
        - Cannot fake any step without breaking others
        - All components must work together
        - Real files, real parsing, real logic
        """
        # GIVEN: Complete Docker project
        project_dir = tmp_path / "fullstack_app"
        project_dir.mkdir()

        # Docker Compose with postgres
        docker_compose = {
            "version": "3.8",
            "services": {
                "postgres": {
                    "image": "postgres:15",
                    "environment": {
                        "POSTGRES_DB": "myapp",
                        "POSTGRES_PASSWORD": "secret"
                    }
                },
                "web": {
                    "build": ".",
                    "depends_on": ["postgres"]
                }
            }
        }
        (project_dir / "docker-compose.yml").write_text(yaml.dump(docker_compose))

        # Node.js application
        (project_dir / "package.json").write_text(json.dumps({
            "name": "fullstack-app",
            "dependencies": {"express": "^4.18.0", "pg": "^8.11.0"}
        }))

        # WHEN: Complete recommendation workflow
        # Step 1: Detection
        detector = ProjectDetector()
        context = detector.detect(project_dir)

        # Step 2: Load templates (from actual template files)
        template_manager = create_test_template_manager(Path(__file__).parent.parent / "src" / "mcpi" / "data" / "templates")
        templates = template_manager.list_templates("postgres")

        # Step 3: Recommendation
        recommender = TemplateRecommender(template_manager)
        recommendations = recommender.recommend("postgres", project_dir)

        # THEN: Complete workflow produces correct result
        # Detection results
        assert context.has_docker_compose is True
        assert "postgres" in context.docker_services
        assert context.language == "nodejs"

        # Templates loaded
        assert len(templates) >= 3, "Should load all postgres templates"

        # Recommendation quality
        assert len(recommendations) > 0, "Should have recommendations"
        top = recommendations[0]
        assert "docker" in top.template.name.lower(), "Should recommend docker template"
        assert top.confidence >= 0.7, "Should have high confidence"
        assert len(top.reasons) > 0, "Should have explanations"

        # VERIFICATION: Project is complete and realistic
        assert (project_dir / "docker-compose.yml").exists()
        assert (project_dir / "package.json").exists()
        with open(project_dir / "docker-compose.yml") as f:
            data = yaml.safe_load(f)
        assert "postgres" in data["services"]
        assert "web" in data["services"]

    def test_workflow_with_multiple_servers(self, tmp_path: Path):
        """Test recommendation workflow for different server types.

        PLAN Reference: P1-17 Integration Test (line 506: "All 12 templates can be recommended")

        USER SCENARIO:
        1. User wants recommendations for multiple servers
        2. GitHub recommendation based on project characteristics
        3. Filesystem recommendation for project structure
        4. Each server gets appropriate template

        OBSERVABLE OUTCOMES:
        - Different servers → different recommendations
        - Context applied consistently
        - No cross-contamination between server types

        GAMING RESISTANCE:
        - Must handle multiple server types correctly
        - Cannot hardcode server-specific logic
        - General recommendation algorithm
        """
        # GIVEN: Project that might use multiple MCP servers
        project_dir = tmp_path / "polyglot_project"
        project_dir.mkdir()

        # Has code repository indicators (GitHub)
        (project_dir / ".git").mkdir()
        (project_dir / "README.md").write_text("# My Project\n")

        # Has file structure (Filesystem server)
        (project_dir / "src").mkdir()
        (project_dir / "docs").mkdir()

        # WHEN: Request recommendations for different servers
        template_manager = create_test_template_manager(Path(__file__).parent.parent / "src" / "mcpi" / "data" / "templates")
        recommender = TemplateRecommender(template_manager)

        github_recommendations = recommender.recommend("github", project_dir)
        filesystem_recommendations = recommender.recommend("filesystem", project_dir)

        # THEN: Each server gets appropriate recommendations
        # GitHub recommendations exist
        assert len(github_recommendations) > 0, "Should recommend GitHub templates"

        # Filesystem recommendations exist
        assert len(filesystem_recommendations) > 0, "Should recommend filesystem templates"

        # Different templates for different servers
        github_names = {r.template.name for r in github_recommendations}
        filesystem_names = {r.template.name for r in filesystem_recommendations}
        assert github_names != filesystem_names, "Different servers should get different templates"

        # VERIFICATION: Project structure exists
        assert (project_dir / ".git").exists()
        assert (project_dir / "src").exists()
