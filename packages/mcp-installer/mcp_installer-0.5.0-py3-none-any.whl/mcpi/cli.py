"""New CLI implementation using the plugin architecture."""

import sys
from collections import defaultdict
from pathlib import Path
from typing import List, Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.text import Text

from mcpi.bundles import create_default_bundle_catalog
from mcpi.bundles.catalog import BundleCatalog
from mcpi.bundles.installer import BundleInstaller
from mcpi.clients import ServerConfig, ServerState
from mcpi.clients.manager import MCPManager, create_default_manager
from mcpi.registry.catalog import ServerCatalog, create_default_catalog
from mcpi.registry.catalog_manager import CatalogManager, create_default_catalog_manager

console = Console()


def shorten_path(path: Optional[str]) -> str:
    """Shorten a path for display by replacing home and current directory.

    Args:
        path: The path to shorten

    Returns:
        Shortened path with ~ for home and . for current directory
    """
    if not path:
        return "N/A"

    path_obj = Path(path)
    home = Path.home()
    cwd = Path.cwd()

    try:
        # Try to make it relative to current directory first
        relative_to_cwd = path_obj.relative_to(cwd)
        # If it's the current directory itself, return "."
        if str(relative_to_cwd) == ".":
            return "."
        return f"./{relative_to_cwd}"
    except ValueError:
        # Not relative to cwd, try home directory
        try:
            relative_to_home = path_obj.relative_to(home)
            return f"~/{relative_to_home}"
        except ValueError:
            # Not relative to home either, return as-is
            return str(path)


def get_user_config(ctx: click.Context):
    """Lazy initialization of user configuration."""
    if "user_config" not in ctx.obj:
        from mcpi.user_config import create_default_config

        ctx.obj["user_config"] = create_default_config()
    return ctx.obj["user_config"]


def get_default_scope(ctx: click.Context, provided_scope: Optional[str]) -> Optional[str]:
    """Get scope with fallback to config default.

    Args:
        ctx: Click context
        provided_scope: Scope explicitly provided by user (or None)

    Returns:
        Provided scope, or default from config, or None
    """
    if provided_scope:
        return provided_scope

    config = get_user_config(ctx)
    return config.default_scope


def get_default_client(ctx: click.Context, provided_client: Optional[str]) -> Optional[str]:
    """Get client with fallback to config default.

    Args:
        ctx: Click context
        provided_client: Client explicitly provided by user (or None)

    Returns:
        Provided client, or default from config, or None
    """
    if provided_client:
        return provided_client

    config = get_user_config(ctx)
    return config.default_client


def get_mcp_manager(ctx: click.Context):
    """Lazy initialization of MCPManager using factory function."""
    if "mcp_manager" not in ctx.obj:
        try:
            ctx.obj["mcp_manager"] = create_default_manager()
        except Exception as e:
            if ctx.obj.get("verbose", False):
                console.print(f"[red]MCP manager initialization error: {e}[/red]")
                import traceback

                console.print(traceback.format_exc())
            else:
                console.print(f"[red]Failed to initialize MCP manager: {e}[/red]")
            sys.exit(1)
    return ctx.obj["mcp_manager"]


def get_catalog_manager(ctx: click.Context) -> CatalogManager:
    """Lazy initialization of CatalogManager using factory function.

    Returns:
        CatalogManager instance for managing multiple catalogs
    """
    if "catalog_manager" not in ctx.obj:
        try:
            ctx.obj["catalog_manager"] = create_default_catalog_manager()
        except Exception as e:
            if ctx.obj.get("verbose", False):
                console.print(f"[red]Catalog manager initialization error: {e}[/red]")
                import traceback

                console.print(traceback.format_exc())
            else:
                console.print(f"[red]Failed to initialize catalog manager: {e}[/red]")
            sys.exit(1)
    return ctx.obj["catalog_manager"]


def get_catalog(
    ctx: click.Context, catalog_name: Optional[str] = None
) -> ServerCatalog:
    """Get catalog by name (defaults to official catalog).

    Args:
        ctx: Click context
        catalog_name: Catalog name ("official" or "local"), or None for default

    Returns:
        ServerCatalog instance

    Raises:
        click.ClickException: If catalog_name is invalid
    """
    manager = get_catalog_manager(ctx)

    if catalog_name is None:
        # Default behavior: return official catalog
        return manager.get_default_catalog()

    # Lookup specific catalog
    catalog = manager.get_catalog(catalog_name)
    if catalog is None:
        raise click.ClickException(
            f"Unknown catalog: '{catalog_name}'. Available catalogs: official, local"
        )

    return catalog


def get_bundle_catalog(ctx: click.Context):
    """Lazy initialization of BundleCatalog using factory function."""
    if "bundle_catalog" not in ctx.obj:
        try:
            # Use factory function for default bundles directory
            ctx.obj["bundle_catalog"] = create_default_bundle_catalog()
        except Exception as e:
            if ctx.obj.get("verbose", False):
                console.print(f"[red]Bundle catalog initialization error: {e}[/red]")
                import traceback

                console.print(traceback.format_exc())
            else:
                console.print(f"[red]Failed to initialize bundle catalog: {e}[/red]")
            sys.exit(1)
    return ctx.obj["bundle_catalog"]


def get_template_manager(ctx: click.Context):
    """Lazy initialization of TemplateManager using factory function.

    This is lazy-loaded to avoid performance penalty on CLI startup.
    Only imported and initialized when template-related operations are used.
    """
    if "template_manager" not in ctx.obj:
        try:
            # Import here to avoid import cost on CLI startup
            from mcpi.templates.template_manager import create_default_template_manager

            ctx.obj["template_manager"] = create_default_template_manager()
        except Exception as e:
            if ctx.obj.get("verbose", False):
                console.print(f"[red]Template manager initialization error: {e}[/red]")
                import traceback

                console.print(traceback.format_exc())
            else:
                console.print(f"[red]Failed to initialize template manager: {e}[/red]")
            sys.exit(1)
    return ctx.obj["template_manager"]


def get_available_scopes(
    ctx: click.Context, client_name: Optional[str] = None
) -> List[str]:
    """Get available scope names for a client.

    Args:
        ctx: Click context
        client_name: Optional client name (uses default if not specified)

    Returns:
        List of available scope names
    """
    try:
        manager = get_mcp_manager(ctx)
        scopes_info = manager.get_scopes_for_client(client_name)
        return [scope["name"] for scope in scopes_info]
    except Exception:
        # Return common default scopes if we can't get them dynamically
        return ["user", "user-internal", "project", "project-mcp"]


class DynamicScopeType(click.ParamType):
    """Dynamic parameter type for scopes that validates based on the client."""

    name = "scope"

    def get_metavar(self, param, ctx=None):
        """Get metavar for help text."""
        # Show common examples, but indicate it varies by client
        return "[varies by client: e.g., user|project|workspace]"

    def convert(self, value, param, ctx):
        """Convert and validate the scope value."""
        if value is None:
            return None

        # Try to get the client from context or command parameters
        client_name = None
        if ctx and ctx.params:
            client_name = ctx.params.get("client")

        # If we have a client, validate against its available scopes
        if ctx and ctx.obj:
            try:
                # Try to get available scopes for validation
                manager = ctx.obj.get("mcp_manager")
                if manager:
                    # If no client specified, use the default
                    if not client_name:
                        client_name = manager.default_client

                    scopes_info = manager.get_scopes_for_client(client_name)
                    available_scopes = [scope["name"] for scope in scopes_info]

                    if available_scopes and value not in available_scopes:
                        self.fail(
                            f"'{value}' is not a valid scope for client '{client_name}'. "
                            f"Available scopes: {', '.join(available_scopes)}",
                            param,
                            ctx,
                        )
            except click.exceptions.BadParameter:
                # Re-raise validation errors
                raise
            except Exception:
                # If we can't validate due to other errors, just accept the value
                pass

        return value

    def shell_complete(self, ctx, param, incomplete):
        """Provide shell completion for scopes."""
        from click.shell_completion import CompletionItem
        from mcpi.utils.completion_debug import log_completion, CompletionLogger

        completions = []

        try:
            log_completion(
                "DynamicScopeType.shell_complete called",
                ctx=ctx,
                param_name=param.name if param else None,
                incomplete=incomplete,
            )

            # Try to get available scopes for the current client
            if ctx and ctx.obj:
                # Initialize manager if not present
                if "mcp_manager" not in ctx.obj:
                    log_completion("Initializing MCPManager", ctx=ctx)
                    ctx.obj["mcp_manager"] = create_default_manager()

                manager = ctx.obj.get("mcp_manager")
                client_name = ctx.params.get("client") if ctx.params else None

                log_completion(
                    "Getting scopes for client", ctx=ctx, client_name=client_name
                )

                if manager:
                    scopes_info = manager.get_scopes_for_client(client_name)

                    # For rescope command: filter out the --from scope when completing --to
                    exclude_scope = None
                    if param and param.name == "to_scope" and ctx.params:
                        # If completing --to parameter, exclude the --from scope
                        exclude_scope = ctx.params.get("from_scope")
                    elif param and param.name == "from_scope" and ctx.params:
                        # If completing --from parameter, exclude the --to scope (if already set)
                        exclude_scope = ctx.params.get("to_scope")

                    log_completion(
                        "Scope filtering",
                        ctx=ctx,
                        param_name=param.name if param else None,
                        exclude_scope=exclude_scope,
                        available_scopes=len(scopes_info),
                    )

                    # Show file paths for each scope
                    completions = [
                        CompletionItem(scope["name"], help=scope.get("path", "No path"))
                        for scope in scopes_info
                        if scope["name"].startswith(incomplete)
                        and scope["name"] != exclude_scope
                    ]

                    log_completion(
                        "Returning scope completions",
                        ctx=ctx,
                        result_count=len(completions),
                    )
            else:
                log_completion("No context available, using defaults", ctx=ctx)
                # No context available, use default scopes
                default_scopes = [
                    "user",
                    "user-internal",
                    "project",
                    "project-mcp",
                    "workspace",
                    "global",
                ]
                completions = [
                    CompletionItem(scope)
                    for scope in default_scopes
                    if scope.startswith(incomplete)
                ]

        except Exception as e:
            logger = CompletionLogger.get_logger()
            logger.log_error(
                e,
                ctx=ctx,
                function="DynamicScopeType.shell_complete",
                param_name=param.name if param else None,
                incomplete=incomplete,
            )

            # Fallback: If we can't get scopes from manager, use defaults
            default_scopes = [
                "user",
                "user-internal",
                "project",
                "project-mcp",
                "workspace",
                "global",
            ]
            completions = [
                CompletionItem(scope)
                for scope in default_scopes
                if scope.startswith(incomplete)
            ]

        return completions


# Tab completion functions


def complete_client_names(
    ctx: click.Context, param: click.Parameter, incomplete: str
) -> List:
    """Complete MCP client names from available clients.

    Args:
        ctx: Click context with mcp_manager in obj
        param: Parameter being completed
        incomplete: Partial text entered by user

    Returns:
        List of CompletionItem objects matching the prefix
    """
    from click.shell_completion import CompletionItem

    if not ctx or not ctx.obj:
        return []

    try:
        from mcpi.utils.completion_debug import log_completion

        log_completion("complete_client_names called", ctx=ctx, incomplete=incomplete)

        # Initialize manager if not present
        if "mcp_manager" not in ctx.obj:
            log_completion("Initializing MCPManager", ctx=ctx)
            ctx.obj["mcp_manager"] = create_default_manager()

        manager = ctx.obj["mcp_manager"]

        # Check if we need to filter by scope
        scope_param = (
            ctx.params.get("scope") if hasattr(ctx, "params") and ctx.params else None
        )

        log_completion("Getting client info", ctx=ctx, scope_filter=scope_param)

        client_info = manager.get_client_info()

        # If scope is specified, filter clients that support that scope
        if scope_param:
            filtered_clients = {}
            for name, info in client_info.items():
                scopes_info = manager.get_scopes_for_client(name)
                scope_names = [s["name"] for s in scopes_info]
                if scope_param in scope_names:
                    filtered_clients[name] = info
            client_info = filtered_clients if filtered_clients else client_info
            log_completion(
                "Filtered by scope",
                ctx=ctx,
                original_count=len(manager.get_client_info()),
                filtered_count=len(client_info),
            )

        results = [
            CompletionItem(name, help=f"{info.get('server_count', 0)} servers")
            for name, info in client_info.items()
            if name.startswith(incomplete)
        ]

        log_completion("Returning completions", ctx=ctx, result_count=len(results))

        return results
    except Exception as e:
        from mcpi.utils.completion_debug import CompletionLogger

        logger = CompletionLogger.get_logger()
        logger.log_error(
            e, ctx=ctx, function="complete_client_names", incomplete=incomplete
        )

        # Fallback to common client names if initialization fails
        default_clients = ["claude-code", "cursor", "vscode"]
        return [
            CompletionItem(name)
            for name in default_clients
            if name.startswith(incomplete)
        ]


def complete_server_ids(
    ctx: click.Context, param: click.Parameter, incomplete: str
) -> List:
    """Complete server IDs from registry or installed servers.

    This function provides context-aware completion:
    - For 'add' command: shows servers from registry
    - For 'remove', 'enable', 'disable' commands: shows installed servers filtered by state
    - Other commands: shows all registry servers

    Args:
        ctx: Click context with catalog/mcp_manager in obj
        param: Parameter being completed
        incomplete: Partial text entered by user

    Returns:
        List of CompletionItem objects matching the prefix (max 50)
    """
    from click.shell_completion import CompletionItem

    # Initialize context object if needed
    if not ctx:
        return []

    if ctx.obj is None:
        ctx.obj = {}

    try:
        from mcpi.utils.completion_debug import log_completion

        log_completion(
            "complete_server_ids called",
            ctx=ctx,
            incomplete=incomplete,
            has_ctx_obj=ctx.obj is not None,
        )

        # Get command name for context-aware filtering
        # Click context always has info_name (may be None) and parent attributes
        command_name = ctx.info_name or (ctx.parent.info_name if ctx.parent else None)

        log_completion("Command context", ctx=ctx, command_name=command_name)

        # For remove/enable/disable commands, show only installed servers
        if command_name in ["remove", "enable", "disable"]:
            log_completion(
                f"Using installed servers for '{command_name}' command", ctx=ctx
            )

            # Initialize manager if not present
            if "mcp_manager" not in ctx.obj:
                log_completion("Initializing MCPManager", ctx=ctx)
                ctx.obj["mcp_manager"] = create_default_manager()

            manager = ctx.obj["mcp_manager"]

            # Filter by state for enable/disable
            state_filter = None
            if command_name == "enable":
                state_filter = ServerState.DISABLED
            elif command_name == "disable":
                state_filter = ServerState.ENABLED

            log_completion("Querying servers", ctx=ctx, state_filter=state_filter)

            servers = manager.list_servers(state_filter=state_filter)

            log_completion("Retrieved servers", ctx=ctx, server_count=len(servers))

            # Create completions with scope information
            # Note: If a server is in multiple scopes, it will appear multiple times
            # IMPORTANT: Include server ID in help text to make each entry unique and prevent
            # zsh from grouping multiple servers together
            completions = []
            for qualified_id, info in servers.items():
                if info.id.startswith(incomplete):
                    # Use qualified ID format to ensure uniqueness
                    # Format: server-name in client:scope (enabled/disabled/unapproved)
                    # Add colors for better readability:
                    # - Dim gray for server name (to de-emphasize since it's already in the completion)
                    # - Cyan for scope (most important for user to see)
                    # - Green for enabled, Yellow for disabled, Cyan for unapproved
                    state_labels = {
                        ServerState.ENABLED: "enabled",
                        ServerState.DISABLED: "disabled",
                        ServerState.UNAPPROVED: "unapproved",
                        ServerState.NOT_INSTALLED: "not installed",
                    }
                    state_colors = {
                        ServerState.ENABLED: "\033[32m",    # green
                        ServerState.DISABLED: "\033[33m",   # yellow
                        ServerState.UNAPPROVED: "\033[36m", # cyan
                        ServerState.NOT_INSTALLED: "\033[31m",  # red
                    }
                    state_label = state_labels.get(info.state, info.state.name.lower())
                    state_color = state_colors.get(info.state, "\033[37m")  # default white
                    reset = "\033[0m"
                    dim = "\033[2m"
                    cyan = "\033[36m"

                    help_text = (
                        f"{dim}{info.id}{reset} in "
                        f"{cyan}{info.client}:{info.scope}{reset} "
                        f"({state_color}{state_label}{reset})"
                    )
                    completions.append(CompletionItem(info.id, help=help_text))

            # Sort by server ID, then by scope for consistent ordering
            completions.sort(key=lambda c: (c.value, c.help or ""))

            log_completion(
                "Returning completions",
                ctx=ctx,
                completion_count=len(completions),
                sample=[(c.value, c.help) for c in completions[:5]],
            )

            return completions[:50]

        # For add and other commands, show servers from registry
        # Initialize catalog manager if not present (use new multi-catalog context)
        catalog = get_catalog(ctx)
        servers = catalog.list_servers()

        # Filter and limit results
        matches = [
            CompletionItem(
                server_id,
                help=(
                    server.description[:50] + "..."
                    if len(server.description) > 50
                    else server.description
                ),
            )
            for server_id, server in servers
            if server_id.startswith(incomplete)
        ]

        # Limit to 50 results to avoid overwhelming user
        return matches[:50]
    except Exception as e:
        from mcpi.utils.completion_debug import CompletionLogger

        logger = CompletionLogger.get_logger()
        logger.log_error(
            e,
            ctx=ctx,
            function="complete_server_ids",
            command_name=command_name if "command_name" in locals() else "unknown",
            incomplete=incomplete,
        )

        # Fallback to empty list if we can't load servers
        return []


def complete_rescope_server_name(
    ctx: click.Context, param: click.Parameter, incomplete: str
) -> List:
    """Complete server names for rescope command.

    Shows all installed MCP servers. If --from scope is specified, filters to only
    servers in that scope. Otherwise shows all installed servers across all scopes.

    Args:
        ctx: Click context with mcp_manager
        param: Parameter being completed
        incomplete: Partial text entered by user

    Returns:
        List of CompletionItem objects for installed servers
    """
    from click.shell_completion import CompletionItem

    if not ctx or not ctx.obj:
        return []

    try:
        from mcpi.utils.completion_debug import log_completion

        log_completion(
            "complete_rescope_server_name called", ctx=ctx, incomplete=incomplete
        )

        # Initialize manager if needed
        if "mcp_manager" not in ctx.obj:
            manager = get_mcp_manager(ctx)
        else:
            manager = ctx.obj["mcp_manager"]

        # Get client (use default if not specified)
        client_name = ctx.params.get("client")
        if not client_name:
            client_name = manager.get_default_client()

        # Get the --from scope if specified
        from_scope = ctx.params.get("from_scope")

        log_completion(
            "Rescope parameters",
            ctx=ctx,
            client_name=client_name,
            from_scope=from_scope,
        )

        if from_scope:
            # List servers from the specified source scope only
            servers = manager.list_servers(client=client_name, scope=from_scope)
        else:
            # No scope specified - show all installed servers across all scopes
            servers = manager.list_servers(client=client_name)

        log_completion("Retrieved servers", ctx=ctx, server_count=len(servers))

        # Return matching server IDs
        results = [
            CompletionItem(server_id)
            for server_id in sorted(servers.keys())
            if server_id.startswith(incomplete)
        ][:50]

        log_completion("Returning completions", ctx=ctx, result_count=len(results))

        return results

    except Exception as e:
        from mcpi.utils.completion_debug import CompletionLogger

        logger = CompletionLogger.get_logger()
        logger.log_error(
            e,
            ctx=ctx,
            function="complete_rescope_server_name",
            incomplete=incomplete,
        )
        return []


@click.group()
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
@click.option(
    "--dry-run", is_flag=True, help="Show what would be done without making changes"
)
@click.option(
    "--debug",
    is_flag=True,
    help="Enable debug logging (writes to ~/.mcpi_completion_debug.log)",
)
@click.version_option()
@click.pass_context
def main(ctx: click.Context, verbose: bool, dry_run: bool, debug: bool) -> None:
    """MCPI - MCP Server Package Installer (New Plugin Architecture)."""
    # Ensure context object exists
    ctx.ensure_object(dict)

    # Store options in context
    ctx.obj["verbose"] = verbose
    ctx.obj["dry_run"] = dry_run
    ctx.obj["debug"] = debug

    # Set environment variable for debug mode (used by completion)
    if debug:
        import os

        os.environ["MCPI_DEBUG"] = "1"


# CLIENT MANAGEMENT COMMANDS


@main.group()
@click.pass_context
def client(ctx: click.Context) -> None:
    """Manage MCP clients and their configurations."""
    pass


@client.command("list")
@click.pass_context
def list_clients(ctx: click.Context) -> None:
    """List available MCP clients."""
    try:
        manager = get_mcp_manager(ctx)
        client_info = manager.get_client_info()

        if not client_info:
            console.print("[yellow]No MCP clients available[/yellow]")
            return

        table = Table(title="Available MCP Clients")
        table.add_column("Client", style="cyan", no_wrap=True)
        table.add_column("Default", style="green")
        table.add_column("Scopes", style="blue")
        table.add_column("Servers", style="magenta")
        table.add_column("Status", style="yellow")

        for name, info in client_info.items():
            is_default = "✓" if name == manager.default_client else ""
            scope_count = str(len(info.get("scopes", [])))
            server_count = str(info.get("server_count", 0))

            # Determine status
            if "error" in info:
                status = f"Error: {info['error']}"
            elif info.get("installed", False):
                status = "Installed"
            else:
                status = "Available"

            table.add_row(name, is_default, scope_count, server_count, status)

        console.print(table)

    except Exception as e:
        console.print(f"[red]Error listing clients: {e}[/red]")


@client.command("info")
@click.argument("client_name", required=False, shell_complete=complete_client_names)
@click.pass_context
def client_info(ctx: click.Context, client_name: Optional[str]) -> None:
    """Show detailed information about a client."""
    try:
        manager = get_mcp_manager(ctx)

        if client_name is None:
            client_name = manager.default_client
            if not client_name:
                console.print(
                    "[red]No default client set and no client specified[/red]"
                )
                return

        info = manager.get_client_info(client_name)
        if not info or client_name not in info:
            console.print(f"[red]Client '{client_name}' not found[/red]")
            return

        client_data = info[client_name]

        # Create info panel
        info_text = f"[bold]Client:[/bold] {client_name}\n"
        if client_name == manager.default_client:
            info_text += "[bold]Default:[/bold] Yes\n"

        if "error" in client_data:
            info_text += f"[bold]Error:[/bold] {client_data['error']}\n"
        else:
            info_text += f"[bold]Servers:[/bold] {client_data.get('server_count', 0)}\n"

            # Show scopes
            scopes = client_data.get("scopes", [])
            if scopes:
                info_text += "[bold]Scopes:[/bold]\n"
                for scope in scopes:
                    scope_type = "User" if scope.get("is_user_level") else "Project"
                    info_text += (
                        f"  • {scope['name']} ({scope_type}) - {scope['description']}\n"
                    )
                    if scope.get("path"):
                        info_text += f"    Path: {scope['path']}\n"

        console.print(Panel(info_text, title=f"Client Information: {client_name}"))

    except Exception as e:
        console.print(f"[red]Error getting client info: {e}[/red]")


@client.command("set-default")
@click.argument("client_name", shell_complete=complete_client_names)
@click.pass_context
def set_default_client(ctx: click.Context, client_name: str) -> None:
    """Set the default client for MCPI operations."""
    try:
        manager = get_mcp_manager(ctx)
        result = manager.set_default_client(client_name)

        if result.success:
            console.print(f"[green]✓ {result.message}[/green]")
        else:
            console.print(f"[red]✗ {result.message}[/red]")

    except Exception as e:
        console.print(f"[red]Error setting default client: {e}[/red]")


# SCOPE MANAGEMENT COMMANDS


@main.group()
@click.pass_context
def scope(ctx: click.Context) -> None:
    """Manage configuration scopes."""
    pass


@scope.command("list")
@click.option(
    "--client",
    shell_complete=complete_client_names,
    help="Filter by client (uses default if not specified)",
)
@click.pass_context
def list_scopes(ctx: click.Context, client: Optional[str]) -> None:
    """List available configuration scopes."""
    try:
        manager = get_mcp_manager(ctx)
        scopes = manager.get_scopes_for_client(client)

        if not scopes:
            client_name = client or manager.default_client
            console.print(
                f"[yellow]No scopes available for client '{client_name}'[/yellow]"
            )
            return

        # Build caption with current directory
        cwd = Path.cwd()
        caption_text = Text()
        caption_text.append("Current Directory: ", style="cyan bold")
        caption_text.append(str(cwd), style="yellow")

        table = Table(
            title=f"Configuration Scopes: {client or manager.default_client}",
            caption=caption_text,
            caption_justify="left",
        )
        table.add_column("Name", style="cyan", no_wrap=True)
        table.add_column("Type", style="blue")
        table.add_column("Priority", style="magenta")
        table.add_column("Path", style="yellow")
        table.add_column("Exists", style="green")
        table.add_column("Description", style="white")

        for scope in scopes:
            scope_type = "User" if scope["is_user_level"] else "Project"
            exists = "✓" if scope["exists"] else "✗"
            path = shorten_path(scope["path"])

            table.add_row(
                scope["name"],
                scope_type,
                str(scope["priority"]),
                path,
                exists,
                scope["description"],
            )

        console.print(table)

    except Exception as e:
        console.print(f"[red]Error listing scopes: {e}[/red]")


# CONFIG MANAGEMENT COMMANDS


@main.group()
@click.pass_context
def config(ctx: click.Context) -> None:
    """Manage MCPI configuration."""
    pass


@config.command("show")
@click.pass_context
def config_show(ctx: click.Context) -> None:
    """Show current configuration."""
    from mcpi.user_config import create_default_config

    console = Console()
    cfg = create_default_config()

    if not cfg.is_loaded:
        console.print(f"[yellow]No configuration file found at {cfg.config_path}[/yellow]")
        console.print("\n[dim]Use 'mcpi config set' to create configuration.[/dim]")
        return

    console.print(f"[bold]Configuration:[/bold] {cfg.config_path}\n")

    config_dict = cfg.to_dict()
    if not config_dict:
        console.print("[dim]Configuration file is empty[/dim]")
        return

    for section, values in config_dict.items():
        console.print(f"[cyan][{section}][/cyan]")
        for key, value in values.items():
            console.print(f"  {key} = {value}")
        console.print()


@config.command("get")
@click.argument("key")
@click.pass_context
def config_get(ctx: click.Context, key: str) -> None:
    """Get a configuration value.

    KEY format: section.key (e.g., defaults.scope)
    """
    from mcpi.user_config import create_default_config

    console = Console()
    cfg = create_default_config()

    try:
        section, key_name = key.split(".", 1)
    except ValueError:
        console.print(f"[red]Error: KEY must be in format 'section.key' (e.g., 'defaults.scope')[/red]")
        sys.exit(1)

    value = cfg.get(section, key_name)
    if value is None:
        console.print(f"[yellow]No value set for '{key}'[/yellow]")
        sys.exit(1)

    console.print(value)


@config.command("set")
@click.argument("key")
@click.argument("value")
@click.pass_context
def config_set(ctx: click.Context, key: str, value: str) -> None:
    """Set a configuration value.

    KEY format: section.key (e.g., defaults.scope)

    Examples:
        mcpi config set defaults.scope user-global
        mcpi config set defaults.client claude-code
    """
    from mcpi.user_config import create_default_config

    console = Console()
    cfg = create_default_config()

    try:
        section, key_name = key.split(".", 1)
    except ValueError:
        console.print(f"[red]Error: KEY must be in format 'section.key' (e.g., 'defaults.scope')[/red]")
        sys.exit(1)

    cfg.set(section, key_name, value)
    cfg.save()

    console.print(f"[green]✓[/green] Set {key} = {value}")
    console.print(f"[dim]Config saved to {cfg.config_path}[/dim]")


# SERVER MANAGEMENT COMMANDS


@main.command()
@click.option(
    "--client",
    shell_complete=complete_client_names,
    help="Filter by client (uses default if not specified)",
)
@click.option(
    "--scope",
    type=DynamicScopeType(),
    help="Filter by specific scope (default: show all scopes)",
)
@click.option(
    "--state",
    type=click.Choice(["enabled", "disabled", "unapproved", "not_installed"]),
    help="Filter by state",
)
@click.option("--verbose", "-v", is_flag=True, help="Show detailed information")
@click.pass_context
def list(
    ctx: click.Context,
    client: Optional[str],
    scope: Optional[str],
    state: Optional[str],
    verbose: bool,
) -> None:
    """List MCP servers with optional filtering.

    By default, shows servers from all scopes. Use --scope to filter to a specific scope.
    """
    try:
        manager = get_mcp_manager(ctx)

        # Apply config defaults if not explicitly provided
        client = get_default_client(ctx, client)
        # Note: Don't apply scope default - show all scopes by default
        # Users can explicitly pass --scope to filter

        # Convert state string to enum
        state_filter = None
        if state:
            state_filter = ServerState[state.upper()]

        servers = manager.list_servers(
            client_name=client, scope=scope, state_filter=state_filter
        )

        if not servers:
            console.print("[yellow]No servers found[/yellow]")
            return

        if verbose:
            # Detailed view
            for qualified_id, info in servers.items():
                server_text = f"[bold]ID:[/bold] {info.id}\n"
                server_text += f"[bold]Client:[/bold] {info.client}\n"
                server_text += f"[bold]Scope:[/bold] {info.scope}\n"
                server_text += f"[bold]State:[/bold] {info.state.name}\n"
                server_text += f"[bold]Command:[/bold] {info.command}\n"
                if info.args:
                    server_text += f"[bold]Args:[/bold] {' '.join(info.args)}\n"
                if info.env:
                    server_text += (
                        f"[bold]Environment:[/bold] {len(info.env)} variables\n"
                    )

                console.print(Panel(server_text, title=qualified_id))
        else:
            # Table view
            table = Table(title="MCP Servers")
            table.add_column("ID", style="cyan", no_wrap=True)
            table.add_column("Client", style="blue")
            table.add_column("Scope", style="magenta")
            table.add_column("State", style="green")
            table.add_column("Command", style="yellow")

            for qualified_id, info in servers.items():
                state_color = {
                    ServerState.ENABLED: "green",
                    ServerState.DISABLED: "yellow",
                    ServerState.UNAPPROVED: "cyan",
                    ServerState.NOT_INSTALLED: "red",
                }.get(info.state, "white")

                table.add_row(
                    info.id,
                    info.client,
                    info.scope,
                    f"[{state_color}]{info.state.name}[/{state_color}]",
                    info.command or "N/A",
                )

            console.print(table)

    except Exception as e:
        console.print(f"[red]Error listing servers: {e}[/red]")


@main.command()
@click.argument("server_id", shell_complete=complete_server_ids)
@click.option(
    "--catalog",
    type=click.Choice(["official", "local"], case_sensitive=False),
    help="Search in specific catalog (default: official)",
)
@click.option(
    "--client",
    shell_complete=complete_client_names,
    help="Target client (uses default if not specified)",
)
@click.option(
    "--scope",
    type=DynamicScopeType(),
    help="Target scope (available scopes depend on client, uses primary scope if not specified)",
)
@click.option(
    "--template",
    help="Use a configuration template (e.g., 'production', 'development')",
)
@click.option(
    "--list-templates",
    is_flag=True,
    help="List available templates for this server",
)
@click.option(
    "--dry-run", is_flag=True, help="Show what would be done without making changes"
)
@click.pass_context
def add(
    ctx: click.Context,
    server_id: str,
    catalog: Optional[str],
    client: Optional[str],
    scope: Optional[str],
    template: Optional[str],
    list_templates: bool,
    dry_run: bool,
) -> None:
    """Add an MCP server from the registry.

    Examples:
        mcpi add filesystem
        mcpi add my-server --catalog local
        mcpi add filesystem --scope project-mcp
        mcpi add postgres --list-templates
        mcpi add postgres --template production
    """
    verbose = ctx.obj.get("verbose", False)

    # Update dry_run if passed as command option
    if dry_run:
        ctx.obj["dry_run"] = True

    try:
        # Get components
        manager = get_mcp_manager(ctx)
        cat = get_catalog(ctx, catalog)

        # Get server info from catalog
        server = cat.get_server(server_id)
        if not server:
            console.print(
                f"[red]Server '{server_id}' not found in {catalog or 'official'} catalog[/red]"
            )
            return

        # Handle --list-templates flag
        if list_templates:
            template_manager = get_template_manager(ctx)
            templates = template_manager.list_templates(server_id)

            if not templates:
                console.print(
                    f"[yellow]No templates available for '{server_id}'[/yellow]"
                )
                console.print(
                    f"[dim]Use 'mcpi add {server_id}' to install with default configuration[/dim]"
                )
                return

            # Display templates in a Rich table
            table = Table(title=f"Available Templates for '{server_id}'")
            table.add_column("Name", style="cyan", no_wrap=True)
            table.add_column("Priority", style="magenta")
            table.add_column("Scope", style="blue")
            table.add_column("Description", style="white")

            for tmpl in templates:
                table.add_row(tmpl.name, tmpl.priority, tmpl.scope, tmpl.description)

            console.print(table)
            console.print(
                f"\n[dim]Use --template <name> to install with a template[/dim]"
            )
            return

        # Handle --template flag
        if template:
            # Validate template exists
            template_manager = get_template_manager(ctx)
            template_obj = template_manager.get_template(server_id, template)

            if not template_obj:
                console.print(
                    f"[red]Template '{template}' not found for server '{server_id}'[/red]"
                )
                console.print(
                    f"[dim]Run 'mcpi add {server_id} --list-templates' to see available templates[/dim]"
                )
                return

            # Collect template values via interactive prompts
            try:
                from mcpi.templates.prompt_handler import collect_template_values

                # Collect user input for template parameters
                user_values = collect_template_values(template_obj)

                # Apply template with user values to create configuration
                config = template_manager.apply_template(template_obj, user_values)

                # Use template's recommended scope if none specified
                if not scope:
                    scope = template_obj.scope
                    console.print(
                        f"[dim]Using template's recommended scope: {scope}[/dim]\n"
                    )

                # Skip default config creation - we have config from template

            except KeyboardInterrupt:
                console.print("\n[yellow]Setup cancelled by user[/yellow]")
                return
            except Exception as e:
                console.print(f"[red]Error collecting template values: {e}[/red]")
                if verbose:
                    import traceback

                    console.print(traceback.format_exc())
                return
        else:
            # No template - flag to create default config below
            config = None

        # If no scope specified, show interactive menu (unless in dry-run mode)
        if not scope:
            # Get available scopes for the target client
            target_client = client or manager.default_client
            scopes_info = manager.get_scopes_for_client(target_client)

            if not scopes_info:
                console.print(
                    f"[red]No scopes available for client '{target_client}'[/red]"
                )
                ctx.exit(1)

            # In dry-run mode, just use the first available scope
            if ctx.obj.get("dry_run", False):
                scope = scopes_info[0]["name"]
                console.print(f"[dim]Dry-run: Would use scope '{scope}'[/dim]")
            else:
                # Build a list of scope choices with descriptions
                console.print(
                    f"\n[bold cyan]Select a scope for '{server_id}':[/bold cyan]"
                )
                console.print(f"[dim]Client: {target_client}[/dim]\n")

                # Display scope options
                scope_choices = []
                for i, scope_info in enumerate(scopes_info, 1):
                    scope_name = scope_info["name"]
                    scope_desc = scope_info["description"]
                    scope_type = "User" if scope_info["is_user_level"] else "Project"
                    exists = "✓" if scope_info["exists"] else "✗"

                    # Show the option
                    console.print(
                        f"  [{i}] [cyan]{scope_name}[/cyan] - {scope_type} scope {exists}"
                    )
                    console.print(f"      [dim]{scope_desc}[/dim]")
                    scope_choices.append(scope_name)

                # Get user's choice
                console.print()
                choice = Prompt.ask(
                    "Enter the number of your choice",
                    choices=[str(i) for i in range(1, len(scope_choices) + 1)],
                    default="1",
                )

                scope = scope_choices[int(choice) - 1]
                console.print(f"[green]Selected scope: {scope}[/green]\n")

        # Check if server already exists
        existing_info = manager.get_server_info(server_id, client)
        if existing_info:
            console.print(
                f"[yellow]Server '{server_id}' already exists (state: {existing_info.state.name})[/yellow]"
            )
            return

        # Create server configuration (if not already created by template)
        if config is None:
            config = ServerConfig(
                command=server.command, args=server.args, env={}, type="stdio"
            )

        # Show server info
        if not ctx.obj.get("dry_run", False):
            console.print(f"\n[bold]Server ID:[/bold] {server_id}")
            console.print(f"[bold]Description:[/bold] {server.description}")
            console.print(f"[bold]Command:[/bold] {server.command}")
            console.print(
                f"[bold]Target Client:[/bold] {client or manager.default_client}"
            )
            console.print(f"[bold]Target Scope:[/bold] {scope}")

        # Add the server
        if ctx.obj.get("dry_run", False):
            console.print(f"[blue]Would add: {server_id}[/blue]")
            console.print(f"  Client: {client or manager.default_client}")
            console.print(f"  Scope: {scope}")
            console.print(f"  Command: {config.command}")
        else:
            console.print(f"[blue]Adding {server_id} to {scope}...[/blue]")
            result = manager.add_server(server_id, config, scope, client)

            if result.success:
                console.print(f"[green]✓ Successfully added {server_id}[/green]")
            else:
                console.print(
                    f"[red]✗ Failed to add {server_id}: {result.message}[/red]"
                )
                if result.errors and verbose:
                    for error in result.errors:
                        console.print(f"  [red]{error}[/red]")

    except (SystemExit, click.exceptions.Exit):
        # Re-raise exit exceptions to preserve exit codes
        raise
    except Exception as e:
        if verbose:
            console.print(f"[red]Error adding {server_id}: {e}[/red]")
            import traceback

            console.print(traceback.format_exc())
        else:
            console.print(f"[red]Failed to add {server_id}: {e}[/red]")


@main.command()
@click.argument("server_id", shell_complete=complete_server_ids)
@click.option(
    "--client",
    shell_complete=complete_client_names,
    help="Target client (uses default if not specified)",
)
@click.option(
    "--scope",
    type=DynamicScopeType(),
    help="Source scope (available scopes depend on client, auto-detected if not specified)",
)
@click.option(
    "--dry-run", is_flag=True, help="Show what would be done without making changes"
)
@click.pass_context
def remove(
    ctx: click.Context,
    server_id: str,
    client: Optional[str],
    scope: Optional[str],
    dry_run: bool,
) -> None:
    """Remove an MCP server completely."""
    verbose = ctx.obj.get("verbose", False)

    # Update dry_run if passed as command option
    if dry_run:
        ctx.obj["dry_run"] = True

    try:
        manager = get_mcp_manager(ctx)

        # Find server if scope not specified
        if not scope:
            server_info = manager.get_server_info(server_id, client)
            if server_info:
                scope = server_info.scope
            else:
                console.print(f"[red]Server '{server_id}' not found[/red]")
                return

        # Remove the server
        if ctx.obj.get("dry_run", False):
            console.print(f"[blue]Would remove: {server_id} from {scope}[/blue]")
        else:
            console.print(f"[blue]Removing {server_id} from {scope}...[/blue]")
            result = manager.remove_server(server_id, scope, client)

            if result.success:
                console.print(f"[green]✓ Successfully removed {server_id}[/green]")
            else:
                console.print(
                    f"[red]✗ Failed to remove {server_id}: {result.message}[/red]"
                )

    except Exception as e:
        if verbose:
            console.print(f"[red]Error removing {server_id}: {e}[/red]")
            import traceback

            console.print(traceback.format_exc())
        else:
            console.print(f"[red]Failed to remove {server_id}: {e}[/red]")


@main.command()
@click.argument("server_id", shell_complete=complete_server_ids)
@click.option(
    "--client",
    shell_complete=complete_client_names,
    help="Target client (uses default if not specified)",
)
@click.option(
    "--dry-run", is_flag=True, help="Show what would be done without making changes"
)
@click.pass_context
def enable(
    ctx: click.Context, server_id: str, client: Optional[str], dry_run: bool
) -> None:
    """Enable a disabled MCP server."""
    verbose = ctx.obj.get("verbose", False)

    # Update dry_run if passed as command option
    if dry_run:
        ctx.obj["dry_run"] = True

    try:
        manager = get_mcp_manager(ctx)

        # Check current state
        current_state = manager.get_server_state(server_id, client)
        if current_state == ServerState.NOT_INSTALLED:
            console.print(f"[red]Server '{server_id}' is not installed[/red]")
            return

        if current_state == ServerState.ENABLED:
            console.print(f"[yellow]Server '{server_id}' is already enabled[/yellow]")
            return

        # Enable the server
        if ctx.obj.get("dry_run", False):
            console.print(f"[blue]Would enable: {server_id}[/blue]")
        else:
            console.print(f"[blue]Enabling {server_id}...[/blue]")
            result = manager.enable_server(server_id, client)

            if result.success:
                console.print(f"[green]✓ Successfully enabled {server_id}[/green]")
            else:
                console.print(
                    f"[red]✗ Failed to enable {server_id}: {result.message}[/red]"
                )

    except Exception as e:
        if verbose:
            console.print(f"[red]Error enabling {server_id}: {e}[/red]")
            import traceback

            console.print(traceback.format_exc())
        else:
            console.print(f"[red]Failed to enable {server_id}: {e}[/red]")


@main.command()
@click.argument("server_id", shell_complete=complete_server_ids)
@click.option(
    "--client",
    shell_complete=complete_client_names,
    help="Target client (uses default if not specified)",
)
@click.option(
    "--dry-run", is_flag=True, help="Show what would be done without making changes"
)
@click.pass_context
def disable(
    ctx: click.Context, server_id: str, client: Optional[str], dry_run: bool
) -> None:
    """Disable an enabled MCP server."""
    verbose = ctx.obj.get("verbose", False)

    # Update dry_run if passed as command option
    if dry_run:
        ctx.obj["dry_run"] = True

    try:
        manager = get_mcp_manager(ctx)

        # Check current state
        current_state = manager.get_server_state(server_id, client)
        if current_state == ServerState.NOT_INSTALLED:
            console.print(f"[red]Server '{server_id}' is not installed[/red]")
            return

        if current_state == ServerState.DISABLED:
            console.print(f"[yellow]Server '{server_id}' is already disabled[/yellow]")
            return

        # Disable the server
        if ctx.obj.get("dry_run", False):
            console.print(f"[blue]Would disable: {server_id}[/blue]")
        else:
            console.print(f"[blue]Disabling {server_id}...[/blue]")
            result = manager.disable_server(server_id, client)

            if result.success:
                console.print(f"[green]✓ Successfully disabled {server_id}[/green]")
            else:
                console.print(
                    f"[red]✗ Failed to disable {server_id}: {result.message}[/red]"
                )

    except Exception as e:
        if verbose:
            console.print(f"[red]Error disabling {server_id}: {e}[/red]")
            import traceback

            console.print(traceback.format_exc())
        else:
            console.print(f"[red]Failed to disable {server_id}: {e}[/red]")


@main.command()
@click.argument("server_name", shell_complete=complete_rescope_server_name)
@click.option(
    "--to",
    "to_scope",
    required=True,
    type=DynamicScopeType(),
    help="Destination scope to move to",
)
@click.option(
    "--client",
    default=None,
    shell_complete=complete_client_names,
    help="MCP client to use (auto-detected if not specified)",
)
@click.option(
    "--dry-run", is_flag=True, help="Show what would happen without making changes"
)
@click.pass_context
def rescope(
    ctx: click.Context,
    server_name: str,
    to_scope: str,
    client: Optional[str],
    dry_run: bool,
) -> None:
    """Move an MCP server configuration to a target scope (OPTION A: AGGRESSIVE).

    This command automatically detects ALL scopes where the server is defined and
    moves it to the target scope. The operation is atomic with ADD-FIRST, REMOVE-SECOND
    ordering to prevent data loss.

    IMPORTANT: This command does NOT require --from parameter. It automatically finds
    the server in all scopes.

    Examples:
        mcpi rescope my-server --to user-global

        mcpi rescope my-server --to project-mcp --client claude-code

        mcpi rescope my-server --to user-global --dry-run
    """
    verbose = ctx.obj.get("verbose", False)

    # Update dry_run if passed as command option
    if dry_run:
        ctx.obj["dry_run"] = True

    try:
        # Step 1: Get manager and determine client
        manager = get_mcp_manager(ctx)
        client_name = client or manager.default_client

        if not client_name:
            console.print(
                "[red]Error: No client specified and no default client available[/red]"
            )
            ctx.exit(1)

        # Step 2: Get client plugin to access scope handlers
        try:
            client_plugin = manager.registry.get_client(client_name)
        except Exception as e:
            console.print(
                f"[red]Error: Failed to get client '{client_name}': {e}[/red]"
            )
            ctx.exit(1)

        # Step 3: Validate target scope exists
        try:
            dest_handler = client_plugin.get_scope_handler(to_scope)
        except Exception as e:
            console.print(f"[red]Error: Invalid target scope '{to_scope}': {e}[/red]")
            if verbose:
                import traceback

                console.print(traceback.format_exc())
            ctx.exit(1)

        # Step 4: Find ALL scopes where server currently exists
        source_scopes = manager.find_all_server_scopes(server_name, client_name)

        if not source_scopes:
            console.print(
                f"[red]Error: Server '{server_name}' not found in any scope[/red]"
            )
            ctx.exit(1)

        # Extract scope names from tuples
        source_scope_names = [scope_name for _, scope_name in source_scopes]

        # Step 5: Get server configuration from any source scope
        first_source_scope = source_scope_names[0]
        servers_in_first_source = manager.list_servers(
            client_name=client_name, scope=first_source_scope
        )

        source_server_info = None
        for qualified_id, server_info in servers_in_first_source.items():
            if server_info.id == server_name:
                source_server_info = server_info
                break

        if source_server_info is None:
            console.print(
                f"[red]Error: Failed to get server configuration from '{first_source_scope}'[/red]"
            )
            ctx.exit(1)

        server_config = ServerConfig.from_dict(source_server_info.config)

        # Step 6: Dry-run mode
        if ctx.obj.get("dry_run", False):
            console.print(
                f"[cyan]Dry-run mode: Would rescope server '{server_name}'[/cyan]"
            )
            console.print(f"  Would add to: {to_scope}")
            console.print(
                f"  Would remove from: {', '.join(s for s in source_scope_names if s != to_scope)}"
            )
            console.print(f"  Client: {client_name}")
            console.print("\n[yellow]No changes made (dry-run mode)[/yellow]")
            ctx.exit(0)

        # Step 7: Execute rescope with ADD-FIRST, REMOVE-SECOND ordering
        # This is the critical safety property: if add fails, sources remain unchanged
        try:
            # ADD to destination first (even if it might already be there)
            # If it's already there, add will fail with "already exists" which we handle below
            add_result = dest_handler.add_server(server_name, server_config)

            # Determine which scopes to remove from
            scopes_to_remove_from = []

            if add_result.success:
                # Add succeeded - remove from ALL source scopes (they're all "old" now)
                scopes_to_remove_from = source_scope_names
            elif "already exists" in add_result.message.lower():
                # Idempotent case: server already in destination
                # Remove from all OTHER scopes (not the destination)
                scopes_to_remove_from = [s for s in source_scope_names if s != to_scope]

                # If server is ONLY in target scope, we're done
                if not scopes_to_remove_from:
                    # No scopes to remove from, just skip to success output
                    pass
            else:
                # Real failure: abort without touching sources
                console.print(
                    f"[red]Error: Failed to add server to '{to_scope}': {add_result.message}[/red]"
                )
                ctx.exit(1)

            # REMOVE from determined scopes (only after successful add or idempotent case)
            failed_removals = []
            for source_scope in scopes_to_remove_from:
                try:
                    source_handler = client_plugin.get_scope_handler(source_scope)
                    remove_result = source_handler.remove_server(server_name)
                    if not remove_result.success:
                        failed_removals.append((source_scope, remove_result.message))
                except Exception as e:
                    failed_removals.append((source_scope, str(e)))

            # Check if any removals failed
            if failed_removals:
                console.print(
                    f"[yellow]Warning: Server added to '{to_scope}' but failed to remove from some scopes:[/yellow]"
                )
                for scope, error in failed_removals:
                    console.print(f"  - {scope}: {error}")

                console.print(
                    "\n[yellow]Server is now in multiple scopes. Run command again to clean up.[/yellow]"
                )
                ctx.exit(1)

        except Exception as e:
            # If we failed during add (before any removes), sources are unchanged
            console.print(f"[red]Error during rescope: {str(e)}[/red]")
            if verbose:
                import traceback

                console.print(traceback.format_exc())
            ctx.exit(1)

        # Step 9: Success output
        console.print(f"[green]✓[/green] Successfully rescoped server '{server_name}'")
        if scopes_to_remove_from:
            console.print(f"  Removed from: {', '.join(scopes_to_remove_from)}")
        console.print(f"  Now in: {to_scope}")
        console.print(f"  Client: {client_name}")

    except (SystemExit, click.exceptions.Exit):
        # Re-raise exit exceptions to preserve exit codes
        raise
    except Exception as e:
        if verbose:
            console.print(f"[red]Error rescoping {server_name}: {e}[/red]")
            import traceback

            console.print(traceback.format_exc())
        else:
            console.print(f"[red]Failed to rescope {server_name}: {e}[/red]")
        ctx.exit(1)


@main.command()
@click.argument("server_id", required=False, shell_complete=complete_server_ids)
@click.option(
    "--catalog",
    type=click.Choice(["official", "local"], case_sensitive=False),
    help="Search in specific catalog (default: search official first, then local)",
)
@click.option(
    "--client",
    shell_complete=complete_client_names,
    help="Target client (uses default if not specified)",
)
@click.option(
    "--plain",
    is_flag=True,
    help="Plain text output (no box characters)",
)
@click.option("--json", "output_json", is_flag=True, help="Output in JSON format")
@click.pass_context
def info(
    ctx: click.Context,
    server_id: Optional[str],
    catalog: Optional[str],
    client: Optional[str],
    plain: bool,
    output_json: bool,
) -> None:
    """Show detailed information about a server or system status.

    Examples:
        mcpi info filesystem
        mcpi info my-server --catalog local
        mcpi info
    """
    try:
        if server_id:
            # Get registry info
            cat = get_catalog(ctx, catalog)
            registry_info = cat.get_server(server_id)

            if not registry_info:
                error_msg = (
                    f"Server '{server_id}' not found in {catalog or 'official'} catalog"
                )
                if plain:
                    console.print(error_msg)
                else:
                    console.print(f"[red]{error_msg}[/red]")
                ctx.exit(1)

            # Output JSON if requested
            if output_json:
                import json

                print(json.dumps(registry_info.model_dump(), indent=2, default=str))
                return

            # Build registry section
            if plain:
                # Plain text output (no Rich markup)
                info_text = "Registry Information:\n"
                info_text += f"ID: {server_id}\n"
                info_text += f"Description: {registry_info.description}\n"
                info_text += f"Command: {registry_info.command}\n"
            else:
                # Rich formatted output
                info_text = "[bold cyan]Registry Information:[/bold cyan]\n"
                info_text += f"[bold]ID:[/bold] {server_id}\n"
                info_text += f"[bold]Description:[/bold] {registry_info.description}\n"
                info_text += f"[bold]Command:[/bold] {registry_info.command}\n"

            if registry_info.args:
                if plain:
                    info_text += f"Arguments: {' '.join(registry_info.args)}\n"
                else:
                    info_text += (
                        f"[bold]Arguments:[/bold] {' '.join(registry_info.args)}\n"
                    )

            if registry_info.repository:
                if plain:
                    info_text += f"Repository: {registry_info.repository}\n"
                else:
                    info_text += (
                        f"[bold]Repository:[/bold] {registry_info.repository}\n"
                    )

            # Get installation info
            if plain:
                info_text += "\nLocal Installation:\n"
            else:
                info_text += "\n[bold cyan]Local Installation:[/bold cyan]\n"

            manager = get_mcp_manager(ctx)
            server_info = manager.get_server_info(server_id, client)

            if server_info:
                if plain:
                    info_text += f"Status: Installed\n"
                    info_text += f"Client: {server_info.client}\n"
                    info_text += f"Scope: {server_info.scope}\n"
                    info_text += f"State: {server_info.state.name}\n"
                else:
                    info_text += f"[bold]Status:[/bold] [green]Installed[/green]\n"
                    info_text += f"[bold]Client:[/bold] {server_info.client}\n"
                    info_text += f"[bold]Scope:[/bold] {server_info.scope}\n"
                    info_text += f"[bold]State:[/bold] {server_info.state.name}\n"

                if server_info.env:
                    if plain:
                        info_text += "Environment Variables:\n"
                    else:
                        info_text += "[bold]Environment Variables:[/bold]\n"
                    for key, value in server_info.env.items():
                        info_text += f"  {key}={value}\n"
            else:
                if plain:
                    info_text += f"Status: Not Installed\n"
                else:
                    info_text += (
                        f"[bold]Status:[/bold] [yellow]Not Installed[/yellow]\n"
                    )

            # Output result
            if plain:
                console.print(info_text)
            else:
                console.print(
                    Panel(info_text, title=f"Server Information: {server_id}")
                )
        else:
            # Show system status
            manager = get_mcp_manager(ctx)
            status = manager.get_status_summary()

            if plain:
                # Plain text system status
                status_text = (
                    f"Default Client: {status.get('default_client', 'None')}\n"
                )
                status_text += f"Available Clients: {', '.join(status.get('available_clients', []))}\n"
                status_text += f"Total Servers: {status.get('total_servers', 0)}\n"
            else:
                # Rich formatted system status
                status_text = f"[bold]Default Client:[/bold] {status.get('default_client', 'None')}\n"
                status_text += f"[bold]Available Clients:[/bold] {', '.join(status.get('available_clients', []))}\n"
                status_text += (
                    f"[bold]Total Servers:[/bold] {status.get('total_servers', 0)}\n"
                )

            # Server states
            states = status.get("server_states", {})
            if states:
                if plain:
                    status_text += "Server States:\n"
                else:
                    status_text += "[bold]Server States:[/bold]\n"
                for state, count in states.items():
                    if count > 0:
                        status_text += f"  {state}: {count}\n"

            # Registry stats
            registry_stats = status.get("registry_stats", {})
            if registry_stats:
                if plain:
                    status_text += "Registry:\n"
                else:
                    status_text += "[bold]Registry:[/bold]\n"
                status_text += f"  Clients: {registry_stats.get('total_clients', 0)}\n"
                status_text += (
                    f"  Loaded: {registry_stats.get('loaded_instances', 0)}\n"
                )

            # Output result
            if plain:
                console.print(status_text)
            else:
                console.print(Panel(status_text, title="MCPI Status"))

    except Exception as e:
        error_msg = f"Error getting information: {e}"
        plain_flag = plain if "plain" in locals() else False
        if plain_flag:
            console.print(error_msg)
        else:
            console.print(f"[red]{error_msg}[/red]")
        ctx.exit(1)


@main.command()
@click.option(
    "--query",
    "-q",
    required=True,
    help="Search query (term to search for in server descriptions)",
)
@click.option(
    "--catalog",
    type=click.Choice(["official", "local"], case_sensitive=False),
    help="Search in specific catalog (default: official)",
)
@click.option("--limit", default=20, help="Maximum number of results to show")
@click.option("--json", "output_json", is_flag=True, help="Output in JSON format")
@click.pass_context
def search(
    ctx: click.Context,
    query: str,
    catalog: Optional[str],
    limit: int,
    output_json: bool,
) -> None:
    """Search for MCP servers in the registry.

    Examples:
        mcpi search --query filesystem
        mcpi search -q database --catalog local
        mcpi search --query git --catalog official
    """
    try:
        # Search single catalog (default: official)
        cat = get_catalog(ctx, catalog)

        # Search servers (returns list of (server_id, MCPServer) tuples)
        servers = cat.search_servers(query)

        # Limit results
        servers = servers[:limit]

        if not servers:
            if output_json:
                import json

                print(json.dumps([]))
            else:
                console.print("[yellow]No servers found matching criteria[/yellow]")
            return

        # Output JSON if requested
        if output_json:
            import json

            # Build JSON output - handle both tuple and plain server results
            json_results = []
            for item in servers:
                # Check if it's a tuple (server, score, matches) or just (server_id, server)
                if isinstance(item, tuple):
                    if len(item) == 3:
                        # Tuple result with score and matches
                        server, score, matches = item
                        result = server.model_dump()
                        result["score"] = score
                        result["matches"] = matches
                        json_results.append(result)
                    elif len(item) == 2:
                        # Plain (server_id, server) tuple
                        server_id, server = item
                        json_results.append(server.model_dump())
                else:
                    # Single server object
                    json_results.append(item.model_dump())

            print(json.dumps(json_results, indent=2, default=str))
            return

        # Table output
        catalog_name = catalog or "official"
        table = Table(title=f"{catalog_name.upper()} CATALOG ({len(servers)} found)")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Command", style="magenta")
        table.add_column("Description", style="white")

        for server_id, server in servers:
            table.add_row(
                server_id,
                server.command,
                (
                    server.description[:80] + "..."
                    if len(server.description) > 80
                    else server.description
                ),
            )

        console.print(table)

    except Exception as e:
        console.print(f"[red]Error searching registry: {e}[/red]")


# STATUS COMMAND


@main.command()
@click.option("--json", "output_json", is_flag=True, help="Output in JSON format")
@click.pass_context
def status(ctx: click.Context, output_json: bool) -> None:
    """Show system status and summary information."""
    try:
        manager = get_mcp_manager(ctx)

        # Get system status
        status_summary = manager.get_status_summary()

        if output_json:
            # Output as JSON
            import json

            print(json.dumps(status_summary, indent=2, default=str))
            return

        status_text = f"[bold]Default Client:[/bold] {status_summary.get('default_client', 'None')}\n"
        status_text += f"[bold]Available Clients:[/bold] {', '.join(status_summary.get('available_clients', []))}\n"
        status_text += (
            f"[bold]Total Servers:[/bold] {status_summary.get('total_servers', 0)}\n"
        )

        # Server states
        states = status_summary.get("server_states", {})
        if states:
            status_text += "[bold]Server States:[/bold]\n"
            for state, count in states.items():
                if count > 0:
                    status_text += f"  {state}: {count}\n"

        # Registry stats
        registry_stats = status_summary.get("registry_stats", {})
        if registry_stats:
            status_text += "[bold]Registry:[/bold]\n"
            status_text += f"  Clients: {registry_stats.get('total_clients', 0)}\n"
            status_text += f"  Loaded: {registry_stats.get('loaded_instances', 0)}\n"

        console.print(Panel(status_text, title="MCPI Status"))

    except Exception as e:
        console.print(f"[red]Error getting status: {e}[/red]")


# CATALOG MANAGEMENT COMMANDS


@main.group()
@click.pass_context
def catalog(ctx: click.Context) -> None:
    """Manage MCP server catalogs.

    MCPI supports multiple server catalogs:
    - official: Built-in catalog of MCP servers
    - local: Your custom servers
    """
    pass


@catalog.command("list")
@click.option(
    "--catalog",
    "-c",
    type=click.Choice(["official", "local", "all"], case_sensitive=False),
    default="all",
    help="Which catalog to list servers from (default: all)",
)
@click.option(
    "--summary",
    is_flag=True,
    help="Show catalog summary instead of servers",
)
@click.pass_context
def catalog_list(ctx: click.Context, catalog: str, summary: bool) -> None:
    """List all MCP servers from catalogs.

    Examples:
        mcpi catalog list              # List all servers from all catalogs
        mcpi catalog list -c official  # List servers from official catalog only
        mcpi catalog list --summary    # Show catalog summary
    """
    try:
        manager = get_catalog_manager(ctx)

        if summary:
            # Show catalog summary (old behavior)
            catalogs = manager.list_catalogs()
            if not catalogs:
                console.print("[yellow]No catalogs available[/yellow]")
                return

            table = Table(title="Available Catalogs", show_header=True)
            table.add_column("Name", style="cyan", no_wrap=True)
            table.add_column("Type", style="magenta")
            table.add_column("Servers", justify="right", style="green")
            table.add_column("Description", style="white")

            for cat in catalogs:
                table.add_row(cat.name, cat.type, str(cat.server_count), cat.description)

            console.print(table)
            console.print(f"\nUse [cyan]mcpi catalog info <name>[/cyan] for details")
            return

        # List all servers from catalogs
        all_servers: list[tuple[str, str, str]] = []  # (id, description, catalog_name)

        if catalog.lower() == "all":
            catalog_names = ["official", "local"]
        else:
            catalog_names = [catalog.lower()]

        for cat_name in catalog_names:
            cat = manager.get_catalog(cat_name)
            if cat:
                for server_id, server in cat.list_servers():
                    all_servers.append(
                        (server_id, server.description or "", cat_name)
                    )

        if not all_servers:
            console.print("[yellow]No servers found in catalogs[/yellow]")
            return

        # Sort by server ID
        all_servers.sort(key=lambda x: x[0].lower())

        table = Table(title="Available MCP Servers", show_header=True)
        table.add_column("Server ID", style="cyan", no_wrap=True)
        table.add_column("Description", style="white")
        table.add_column("Catalog", style="magenta")

        for server_id, description, cat_name in all_servers:
            # Truncate description if too long
            desc = description[:60] + "..." if len(description) > 60 else description
            table.add_row(server_id, desc, cat_name)

        console.print(table)
        console.print(f"\n[dim]{len(all_servers)} servers available[/dim]")
        console.print(
            f"Use [cyan]mcpi info <server-id>[/cyan] for details, "
            f"[cyan]mcpi add <server-id>[/cyan] to install"
        )

    except Exception as e:
        console.print(f"[red]Error listing catalogs: {e}[/red]")


@catalog.command("info")
@click.argument("name", type=click.Choice(["official", "local"], case_sensitive=False))
@click.pass_context
def catalog_info(ctx: click.Context, name: str) -> None:
    """Show detailed information about a catalog.

    Examples:
        mcpi catalog info official
        mcpi catalog info local
    """
    try:
        manager = get_catalog_manager(ctx)
        cat = manager.get_catalog(name)

        if not cat:
            console.print(f"[red]Catalog '{name}' not found[/red]")
            ctx.exit(1)

        # Get catalog metadata
        servers = cat.list_servers()
        categories = cat.list_categories()

        # Display using Rich
        # Catalog header
        console.print(
            Panel(
                f"[bold cyan]{name}[/bold cyan] catalog\n{cat.catalog_path}",
                title="Catalog Information",
            )
        )

        # Stats
        console.print(f"\n[bold]Statistics:[/bold]")
        console.print(f"  Servers: {len(servers)}")
        console.print(f"  Categories: {len(categories)}")

        # Top categories
        if categories:
            console.print(f"\n[bold]Top Categories:[/bold]")
            sorted_cats = sorted(categories.items(), key=lambda x: x[1], reverse=True)
            for category, count in sorted_cats[:10]:
                console.print(f"  {category}: {count}")

        # Sample servers
        if servers:
            console.print(f"\n[bold]Sample Servers:[/bold]")
            for server_id, server in servers[:5]:
                console.print(f"  {server_id}: {server.description}")

            if len(servers) > 5:
                console.print(f"  ... and {len(servers) - 5} more")

        console.print(
            f"\nUse [cyan]mcpi search --query <term> --catalog {name}[/cyan] to search this catalog"
        )

    except (SystemExit, click.exceptions.Exit):
        # Re-raise exit exceptions to preserve exit codes
        raise
    except Exception as e:
        console.print(f"[red]Error getting catalog info: {e}[/red]")


@catalog.command("add")
@click.argument("source", nargs=-1, required=True)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Show what would be done without making changes",
)
@click.pass_context
def catalog_add(ctx: click.Context, source: tuple, dry_run: bool) -> None:
    """Add an MCP server to the local catalog using Claude.

    SOURCE can be any of:
    - URL to a GitHub repository
    - Git clone URL (https or ssh)
    - npx/npm package name
    - JSON configuration blob
    - Any text describing the MCP server

    This command uses Claude in non-interactive mode to discover information
    about the MCP server and add it to the local catalog.

    Examples:

        mcpi catalog add https://github.com/anthropics/mcp-filesystem-server

        mcpi catalog add git@github.com:user/mcp-server.git

        mcpi catalog add npx @modelcontextprotocol/server-postgres

        mcpi catalog add "A filesystem MCP server for managing local files"

        mcpi catalog add --dry-run https://github.com/some/mcp-server
    """
    import subprocess

    # Join all source arguments into a single string
    source_str = " ".join(source)

    if not source_str.strip():
        console.print("[red]Error: No source provided[/red]")
        ctx.exit(1)

    # Get paths for the prompt
    package_dir = Path(__file__).parent.parent.parent
    catalog_path = package_dir / "data" / "catalog.json"

    # Build the prompt for Claude
    prompt = f"""Discover the information about this MCP server and add it to the catalog.

Source: {source_str}

Instructions:
1. Analyze the provided source (URL, git repo, package name, JSON, or description)
2. Discover the MCP server's:
   - Unique server ID (following the pattern: owner/name or @scope/name)
   - Description of what the server does
   - Command to run it (e.g., npx, python, node)
   - Arguments for the command
   - Repository URL if available
   - Categories (e.g., "filesystem", "database", "ai", "tools")
3. Add the server to the catalog at: {catalog_path}

The catalog format is JSON with entries like:
{{
  "server-id": {{
    "description": "Brief description of functionality",
    "command": "npx",
    "args": ["-y", "@package/server-name"],
    "repository": "https://github.com/owner/repo",
    "categories": ["category1", "category2"]
  }}
}}

IMPORTANT:
- Use the existing catalog.json file format exactly
- Do NOT duplicate existing entries
- Validate the server information is accurate
- If you cannot determine the server details, explain why

{"DRY RUN MODE: Show what would be added but do not modify any files." if dry_run else "Add the server to the catalog file."}"""

    console.print(f"[blue]Analyzing source: {source_str}[/blue]")

    if dry_run:
        console.print("[yellow]Dry run mode - no changes will be made[/yellow]")

    # Check if Claude CLI is available
    try:
        version_result = subprocess.run(
            ["claude", "--version"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if version_result.returncode != 0:
            console.print(
                "[red]Error: Claude CLI not found or not working properly[/red]"
            )
            console.print(
                "[dim]Install Claude CLI: https://docs.anthropic.com/en/docs/claude-code[/dim]"
            )
            ctx.exit(1)
    except FileNotFoundError:
        console.print("[red]Error: Claude CLI not found[/red]")
        console.print(
            "[dim]Install Claude CLI: https://docs.anthropic.com/en/docs/claude-code[/dim]"
        )
        ctx.exit(1)
    except subprocess.TimeoutExpired:
        console.print("[red]Error: Claude CLI check timed out[/red]")
        ctx.exit(1)

    # Run Claude in non-interactive mode
    try:
        console.print("[dim]Running Claude to discover server information...[/dim]")

        result = subprocess.run(
            [
                "claude",
                "--print",  # Non-interactive mode, print response
                prompt,
            ],
            capture_output=True,
            text=True,
            cwd=str(package_dir),  # Run in the package directory
            timeout=120,  # 2 minute timeout
        )

        if result.returncode != 0:
            console.print(f"[red]Error: Claude failed with code {result.returncode}[/red]")
            if result.stderr:
                console.print(f"[red]{result.stderr}[/red]")
            ctx.exit(1)

        # Display Claude's response
        if result.stdout:
            console.print("\n[bold]Claude's response:[/bold]")
            console.print(result.stdout)

        if not dry_run:
            console.print(
                f"\n[green]✓ Server catalog may have been updated at:[/green] {catalog_path}"
            )
            console.print(
                "[dim]Use 'mcpi catalog list -c official' to verify the changes[/dim]"
            )
        else:
            console.print("\n[yellow]Dry run complete - no changes were made[/yellow]")

    except subprocess.TimeoutExpired:
        console.print("[red]Error: Claude command timed out after 2 minutes[/red]")
        ctx.exit(1)
    except Exception as e:
        console.print(f"[red]Error running Claude: {e}[/red]")
        ctx.exit(1)


# BUNDLE MANAGEMENT COMMANDS


@main.group()
@click.pass_context
def bundle(ctx: click.Context) -> None:
    """Manage MCP server bundles."""
    pass


@bundle.command("list")
@click.pass_context
def list_bundles(ctx: click.Context) -> None:
    """List available server bundles."""
    try:
        catalog = get_bundle_catalog(ctx)
        bundles = catalog.list_bundles()

        if not bundles:
            console.print("[yellow]No bundles available[/yellow]")
            return

        table = Table(title="Available Server Bundles")
        table.add_column("Name", style="cyan", no_wrap=True)
        table.add_column("Description", style="white")
        table.add_column("Servers", style="magenta")
        table.add_column("Suggested Scope", style="blue")

        for bundle_name, bundle in bundles:
            server_count = len(bundle.servers)
            table.add_row(
                bundle_name,
                (
                    bundle.description[:60] + "..."
                    if len(bundle.description) > 60
                    else bundle.description
                ),
                str(server_count),
                bundle.suggested_scope,
            )

        console.print(table)

    except Exception as e:
        console.print(f"[red]Error listing bundles: {e}[/red]")


@bundle.command("info")
@click.argument("bundle_id")
@click.pass_context
def bundle_info(ctx: click.Context, bundle_id: str) -> None:
    """Show detailed information about a bundle."""
    try:
        catalog = get_bundle_catalog(ctx)
        bundle = catalog.get_bundle(bundle_id)

        if not bundle:
            console.print(f"[red]Bundle '{bundle_id}' not found[/red]")
            console.print(
                "\n[dim]Run 'mcpi bundle list' to see available bundles[/dim]"
            )
            ctx.exit(1)

        # Build info panel
        info_text = f"[bold]Name:[/bold] {bundle.name}\n"
        info_text += f"[bold]Description:[/bold] {bundle.description}\n"
        info_text += f"[bold]Version:[/bold] {bundle.version}\n"
        if bundle.author:
            info_text += f"[bold]Author:[/bold] {bundle.author}\n"
        info_text += f"[bold]Suggested Scope:[/bold] {bundle.suggested_scope}\n"
        info_text += f"\n[bold]Servers ({len(bundle.servers)}):[/bold]\n"

        for server in bundle.servers:
            info_text += f"  • {server.id}"
            if server.config:
                info_text += " [dim](custom config)[/dim]"
            info_text += "\n"

        console.print(Panel(info_text, title=f"Bundle: {bundle_id}"))

    except (SystemExit, click.exceptions.Exit):
        # Re-raise exit exceptions to preserve exit codes
        raise
    except Exception as e:
        console.print(f"[red]Error getting bundle info: {e}[/red]")


@bundle.command("install")
@click.argument("bundle_id")
@click.option(
    "--scope",
    type=DynamicScopeType(),
    help="Target scope (uses bundle's suggested scope if not specified)",
)
@click.option(
    "--client",
    shell_complete=complete_client_names,
    help="Target client (uses default if not specified)",
)
@click.option(
    "--dry-run", is_flag=True, help="Show what would be installed without installing"
)
@click.pass_context
def install_bundle(
    ctx: click.Context,
    bundle_id: str,
    scope: Optional[str],
    client: Optional[str],
    dry_run: bool,
) -> None:
    """Install all servers from a bundle."""
    verbose = ctx.obj.get("verbose", False)

    try:
        # Get components
        bundle_catalog = get_bundle_catalog(ctx)
        server_catalog = get_catalog(ctx)
        manager = get_mcp_manager(ctx)

        # Get bundle
        bundle = bundle_catalog.get_bundle(bundle_id)
        if not bundle:
            console.print(f"[red]Bundle '{bundle_id}' not found[/red]")
            console.print(
                "\n[dim]Run 'mcpi bundle list' to see available bundles[/dim]"
            )
            ctx.exit(1)

        # Determine target scope
        target_scope = scope or bundle.suggested_scope
        target_client = client or manager.default_client

        # Show bundle info
        console.print(f"\n[bold]Bundle:[/bold] {bundle.name}")
        console.print(f"[bold]Description:[/bold] {bundle.description}")
        console.print(f"[bold]Servers:[/bold] {len(bundle.servers)}")
        console.print(f"[bold]Target Client:[/bold] {target_client}")
        console.print(f"[bold]Target Scope:[/bold] {target_scope}\n")

        # Create installer
        installer = BundleInstaller(manager=manager, catalog=server_catalog)

        # Install bundle
        console.print(
            f"[blue]{'[DRY-RUN] ' if dry_run else ''}Installing bundle '{bundle_id}'...[/blue]\n"
        )

        results = installer.install_bundle(
            bundle=bundle,
            scope=target_scope,
            client_name=target_client,
            dry_run=dry_run,
        )

        # Display results
        success_count = sum(1 for r in results if r.success)
        failure_count = len(results) - success_count

        for result in results:
            if result.success:
                console.print(f"[green]✓[/green] {result.message}")
            else:
                console.print(f"[red]✗[/red] {result.message}")

        console.print()
        if dry_run:
            console.print(f"[yellow]Dry-run complete. No changes made.[/yellow]")
        elif failure_count == 0:
            console.print(
                f"[green]Successfully installed all {success_count} servers![/green]"
            )
        else:
            console.print(
                f"[yellow]Installed {success_count} servers, {failure_count} failed[/yellow]"
            )

    except Exception as e:
        if verbose:
            console.print(f"[red]Error installing bundle: {e}[/red]")
            import traceback

            console.print(traceback.format_exc())
        else:
            console.print(f"[red]Failed to install bundle: {e}[/red]")
        ctx.exit(1)


# FZF TUI COMMAND


@main.command()
@click.pass_context
def fzf(ctx: click.Context) -> None:
    """Interactive fuzzy finder for managing MCP servers.

    Launches an fzf-based TUI that allows you to:
    - Browse all available MCP servers
    - View installed servers (highlighted in green/yellow)
    - Add, remove, enable, disable servers with keyboard shortcuts
    - View detailed server information

    Keyboard shortcuts:
        ctrl-a: Add server (interactive scope selection)
        ctrl-r: Remove server
        ctrl-e: Enable server
        ctrl-d: Disable server
        ctrl-i/enter: Show detailed server info
        esc: Exit

    Requirements:
        fzf must be installed (brew install fzf)
    """
    try:
        # Import here to avoid circular dependency
        from mcpi.tui import launch_fzf_interface

        manager = get_mcp_manager(ctx)
        catalog = get_catalog(ctx)

        launch_fzf_interface(manager, catalog)

    except RuntimeError as e:
        # Handle fzf not installed error
        console.print(f"[red]{e}[/red]")
        ctx.exit(1)
    except Exception as e:
        if ctx.obj.get("verbose", False):
            console.print(f"[red]Error launching fzf interface: {e}[/red]")
            import traceback

            console.print(traceback.format_exc())
        else:
            console.print(f"[red]Failed to launch fzf interface: {e}[/red]")
        ctx.exit(1)


# TUI RELOAD COMMAND (hidden, used by fzf bindings)


@main.command("tui-reload", hidden=True)
@click.pass_context
def tui_reload(ctx: click.Context) -> None:
    """Reload server list for fzf TUI (internal command).

    This command is used by fzf bindings to refresh the server list
    after operations like add/remove/enable/disable. It's hidden from
    help output as it's not intended for direct user invocation.
    """
    from mcpi.tui import reload_server_list

    try:
        manager = get_mcp_manager(ctx)
        catalog = get_catalog(ctx)
        reload_server_list(catalog, manager)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        ctx.exit(1)


# COMPLETION COMMAND


@main.command()
@click.option(
    "--shell",
    type=click.Choice(["bash", "zsh", "fish"]),
    help="Shell type (auto-detect if not specified)",
)
@click.pass_context
def completion(ctx: click.Context, shell: Optional[str]) -> None:
    """Generate shell completion script for mcpi.

    Tab completion provides intelligent suggestions for:
    - Command names (list, add, remove, etc.)
    - Option flags (--client, --scope, --help)
    - Client names (based on detected MCP clients)
    - Scope names (filtered by selected client)
    - Server IDs (from the registry)

    Examples:
        mcpi completion --shell bash > mcpi-completion.bash
        mcpi completion --shell zsh >> ~/.zshrc
    """
    import os

    # Auto-detect shell if not specified
    if not shell:
        shell_env = os.environ.get("SHELL", "").split("/")[-1]
        if shell_env in ["bash", "zsh", "fish"]:
            shell = shell_env
        else:
            console.print(
                "[yellow]Could not auto-detect shell. Please specify with --shell[/yellow]"
            )
            console.print("[dim]Examples:[/dim]")
            console.print("  mcpi completion --shell bash")
            console.print("  mcpi completion --shell zsh")
            console.print("  mcpi completion --shell fish")
            ctx.exit(1)

    # Show installation instructions
    console.print(f"\n[cyan]# Tab completion setup for {shell}[/cyan]\n")

    if shell == "bash":
        console.print("[bold]To enable completion, add to ~/.bashrc:[/bold]")
        console.print('[yellow]eval "$(_MCPI_COMPLETE=bash_source mcpi)"[/yellow]\n')
        console.print("[dim]Then run: source ~/.bashrc[/dim]\n")
    elif shell == "zsh":
        console.print("[bold]To enable completion, add to ~/.zshrc:[/bold]")
        console.print('[yellow]eval "$(_MCPI_COMPLETE=zsh_source mcpi)"[/yellow]\n')
        console.print("[dim]Then run: source ~/.zshrc[/dim]\n")
    elif shell == "fish":
        console.print(
            "[bold]To enable completion, add to ~/.config/fish/config.fish:[/bold]"
        )
        console.print("[yellow]eval (env _MCPI_COMPLETE=fish_source mcpi)[/yellow]\n")
        console.print("[dim]Then restart your shell[/dim]\n")


# TUI RELOAD ENTRY POINT (for mcpi-tui-reload console script)


def tui_reload_entry() -> None:
    """Entry point for mcpi-tui-reload console script.

    This function is called when the user runs `mcpi-tui-reload` directly.
    It creates a Click context and invokes the tui-reload command.
    """
    from mcpi.tui import reload_server_list

    try:
        # Create a minimal Click context for initialization
        ctx = click.Context(main)
        ctx.ensure_object(dict)
        ctx.obj["verbose"] = False
        ctx.obj["dry_run"] = False
        ctx.obj["debug"] = False

        # Initialize manager and catalog
        manager = get_mcp_manager(ctx)
        catalog = get_catalog(ctx)

        # Call reload function
        reload_server_list(catalog, manager)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
