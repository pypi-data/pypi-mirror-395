"""Performance optimization utilities for MCPI CLI."""

import functools
import time
from contextlib import contextmanager
from typing import Any, Callable, Dict


class PerformanceOptimizer:
    """Performance optimization utilities for MCPI operations."""

    def __init__(self):
        self._cache: Dict[str, Any] = {}
        self._cache_ttl: Dict[str, float] = {}
        self.default_ttl = 300  # 5 minutes

    def cached_operation(self, key: str, ttl: int = None) -> Callable:
        """Decorator for caching expensive operations.

        Args:
            key: Cache key
            ttl: Time to live in seconds (default: 5 minutes)
        """

        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                cache_key = f"{key}:{hash(str(args) + str(kwargs))}"
                current_time = time.time()

                # Check if cached value exists and is still valid
                if (
                    cache_key in self._cache
                    and cache_key in self._cache_ttl
                    and current_time < self._cache_ttl[cache_key]
                ):
                    return self._cache[cache_key]

                # Execute function and cache result
                result = func(*args, **kwargs)
                self._cache[cache_key] = result
                self._cache_ttl[cache_key] = current_time + (ttl or self.default_ttl)

                return result

            return wrapper

        return decorator

    def clear_cache(self, pattern: str = None) -> None:
        """Clear cache entries.

        Args:
            pattern: Clear only keys containing this pattern (default: clear all)
        """
        if pattern is None:
            self._cache.clear()
            self._cache_ttl.clear()
        else:
            keys_to_remove = [k for k in self._cache.keys() if pattern in k]
            for key in keys_to_remove:
                self._cache.pop(key, None)
                self._cache_ttl.pop(key, None)

    @contextmanager
    def timer(self, operation_name: str, threshold: float = 1.0):
        """Context manager for timing operations and warning on slow operations.

        Args:
            operation_name: Name of the operation being timed
            threshold: Warning threshold in seconds
        """
        start_time = time.time()
        try:
            yield
        finally:
            elapsed = time.time() - start_time
            if elapsed > threshold:
                print(f"⚠️  Slow operation: {operation_name} took {elapsed:.2f}s")


# Global performance optimizer instance
perf_optimizer = PerformanceOptimizer()


def optimize_cli_startup():
    """Optimization strategies for CLI startup performance."""

    # 1. Defer heavy imports until needed
    def lazy_import_yaml():
        """Lazy import of YAML library."""
        try:
            import yaml

            return yaml
        except ImportError:
            return None

    def lazy_import_httpx():
        """Lazy import of HTTP client."""
        try:
            import httpx

            return httpx
        except ImportError:
            return None

    # 2. Registry loading optimizations
    def optimize_registry_loading():
        """Optimize registry file loading."""
        # Use faster JSON parsing when possible
        # Implement streaming for large registries
        # Cache parsed registry data
        pass

    # 3. Config loading optimizations
    def optimize_config_loading():
        """Optimize configuration loading."""
        # Cache config data with modification time checks
        # Use faster TOML parsing
        # Lazy load profile-specific settings
        pass

    return {
        "lazy_yaml": lazy_import_yaml,
        "lazy_httpx": lazy_import_httpx,
        "registry_optimizer": optimize_registry_loading,
        "config_optimizer": optimize_config_loading,
    }


def profile_cli_commands():
    """Profiling utilities for CLI commands."""

    def profile_command(func: Callable) -> Callable:
        """Decorator to profile CLI command execution."""

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with perf_optimizer.timer(func.__name__, threshold=0.5):
                return func(*args, **kwargs)

        return wrapper

    return profile_command


class CLIPerformanceMonitor:
    """Monitor CLI performance and suggest optimizations."""

    def __init__(self):
        self.command_times: Dict[str, list] = {}
        self.slow_commands: Dict[str, float] = {}

    def record_command_time(self, command: str, execution_time: float):
        """Record command execution time."""
        if command not in self.command_times:
            self.command_times[command] = []

        self.command_times[command].append(execution_time)

        # Track slow commands (>2 seconds)
        if execution_time > 2.0:
            self.slow_commands[command] = execution_time

    def get_performance_report(self) -> Dict[str, Any]:
        """Generate performance report."""
        report = {
            "command_stats": {},
            "slow_commands": self.slow_commands,
            "optimization_suggestions": [],
        }

        for command, times in self.command_times.items():
            avg_time = sum(times) / len(times)
            max_time = max(times)
            min_time = min(times)

            report["command_stats"][command] = {
                "average_time": avg_time,
                "max_time": max_time,
                "min_time": min_time,
                "execution_count": len(times),
            }

            # Add optimization suggestions
            if avg_time > 1.0:
                report["optimization_suggestions"].append(
                    {
                        "command": command,
                        "suggestion": "Consider adding caching or lazy loading",
                        "current_avg_time": avg_time,
                    }
                )

        return report

    def suggest_optimizations(self) -> list:
        """Suggest performance optimizations based on usage patterns."""
        suggestions = []

        # Check for frequently used commands
        frequent_commands = {
            cmd: len(times)
            for cmd, times in self.command_times.items()
            if len(times) > 10
        }

        for command, count in frequent_commands.items():
            avg_time = sum(self.command_times[command]) / count
            if avg_time > 0.5:
                suggestions.append(
                    {
                        "type": "caching",
                        "command": command,
                        "reason": f"Frequently used ({count} times) with avg time {avg_time:.2f}s",
                    }
                )

        # Check for registry-heavy operations
        registry_commands = [
            cmd
            for cmd in self.command_times.keys()
            if "list" in cmd or "search" in cmd or "info" in cmd
        ]

        for command in registry_commands:
            if command in self.command_times:
                avg_time = sum(self.command_times[command]) / len(
                    self.command_times[command]
                )
                if avg_time > 0.3:
                    suggestions.append(
                        {
                            "type": "registry_optimization",
                            "command": command,
                            "reason": f"Registry operation taking {avg_time:.2f}s average",
                        }
                    )

        return suggestions


# Global performance monitor
performance_monitor = CLIPerformanceMonitor()
