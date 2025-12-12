"""CLI interface for CCswitcher."""

import os
import shutil
import sys
from pathlib import Path

import click

from .config import Config


class CustomGroup(click.Group):
    """Custom group that treats unknown commands as profile names."""

    def invoke(self, ctx):
        # Get the subcommand name from arguments
        if len(sys.argv) > 1:
            subcommand_name = sys.argv[1]
            # If it's not a registered subcommand, treat it as a profile switch
            if subcommand_name not in self.commands:
                return switch_profile(subcommand_name)
        return super().invoke(ctx)


@click.command(cls=CustomGroup)
@click.pass_context
def main(ctx):
    """
    CCswitcher - Switch between different Claude Code API settings.

    Usage:
        ccswitcher deepseek    # Switch to deepseek settings
        ccswitcher claude      # Switch to default Claude (removes settings.json)
        ccswitcher new <name> --path=<path>  # Register a new profile
    """
    if not ctx.invoked_subcommand:
        click.echo(ctx.get_help())


@main.command()
@click.argument('name')
@click.option('--path', required=True, help='Path to the settings file')
def new(name, path):
    """Register a new profile with a settings file path."""
    config = Config()

    expanded_path = os.path.expanduser(path)

    if not Path(expanded_path).parent.exists():
        click.echo(f"Error: Parent directory of '{expanded_path}' does not exist.", err=True)
        return

    config.add_profile(name, expanded_path)
    click.echo(f"✓ Profile '{name}' registered with path: {expanded_path}")


@main.command()
def list():
    """List all registered profiles."""
    config = Config()
    profiles = config.list_profiles()

    if not profiles:
        click.echo("No profiles registered yet.")
        click.echo("Use 'ccswitcher new <name> --path=<path>' to register a profile.")
        return

    click.echo("Registered profiles:")
    for name, path in profiles.items():
        exists = "✓" if Path(path).exists() else "✗"
        click.echo(f"  {exists} {name}: {path}")


def switch_profile(profile: str):
    """Switch to a specific profile."""
    config = Config()

    if profile.lower() == 'claude':
        if config.claude_settings.exists():
            config.claude_settings.unlink()
            click.echo("✓ Switched to default Claude (removed settings.json)")
        else:
            click.echo("✓ Already using default Claude (no settings.json)")
        return

    profile_path = config.get_profile_path(profile)

    if not profile_path:
        click.echo(f"Error: Profile '{profile}' not found.", err=True)
        click.echo(f"Use 'ccswitcher new {profile} --path=<path>' to register it.", err=True)
        return

    source_path = Path(profile_path)

    if not source_path.exists():
        click.echo(f"Error: Settings file not found at: {profile_path}", err=True)
        return

    config.claude_dir.mkdir(parents=True, exist_ok=True)

    shutil.copy2(source_path, config.claude_settings)
    click.echo(f"✓ Switched to '{profile}' profile")
    click.echo(f"  Copied: {profile_path} → {config.claude_settings}")


if __name__ == '__main__':
    main()
