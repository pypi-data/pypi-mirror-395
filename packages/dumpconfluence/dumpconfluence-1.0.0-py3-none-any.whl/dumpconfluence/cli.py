#!/usr/bin/env python3
"""Command-line interface for DumpConfluence"""

import click
import sys
import os
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn
import json

from .core import ConfluenceBackup
from .config import ConfigManager
from .exceptions import (
    AuthenticationError,
    ConfluenceBackupError,
    NetworkError,
    ValidationError,
)
from . import __version__

console = Console()


@click.group(invoke_without_command=True)
@click.version_option(version=__version__, prog_name="DumpConfluence")
@click.pass_context
def cli(ctx):
    """DumpConfluence - Backup Confluence pages with images and attachments"""
    if ctx.invoked_subcommand is None:
        # ASCII art banner with dynamic version
        version_line = f"Confluence Backup Tool v{__version__} - by Dani Lipari"
        # Center the version line in the banner (56 chars width)
        centered_version = version_line.center(56)

        console.print(f"""[bold cyan]
╔════════════════════════════════════════════════════════╗
║                                                        ║
║    ____                         ____             __    ║
║   |  _ \ _   _ _ __ ___  _ __  / ___|___  _ __  / _|   ║
║   | | | | | | | '_ ` _ \| '_ \| |   / _ \| '_ \| |_    ║
║   | |_| | |_| | | | | | | |_) | |__| (_) | | | |  _|   ║
║   |____/ \__,_|_| |_| |_| .__/ \____\___/|_| |_|_|     ║
║                         |_|                            ║
║                                                        ║
║{centered_version}║
║                                                        ║
╚════════════════════════════════════════════════════════╝
        [/bold cyan]""")

        # Show saved profiles
        config = ConfigManager()
        profiles = config.list_profiles()

        if profiles:
            console.print("\n[bold green] Saved Profiles:[/bold green]")
            default_profile = config.get_default_profile()

            for profile in profiles:
                data = config.load_profile(profile)
                is_default = profile == default_profile

                # Show (auto) for single profile, (default) for default when multiple profiles
                if len(profiles) == 1:
                    status_mark = " [green](auto)[/green]"
                elif is_default:
                    status_mark = " [yellow](default)[/yellow]"
                else:
                    status_mark = ""

                console.print(f"   • [cyan]{profile}[/cyan]: {data['email']} @ {data['url']}{status_mark}")

            if len(profiles) == 1:
                console.print(f"\n   [dim]Auto-selected profile:[/dim] [yellow]dumpconfluence backup URL[/yellow]")
            elif default_profile:
                console.print(f"\n   [dim]Default profile active:[/dim] [yellow]dumpconfluence backup URL[/yellow]")
            else:
                console.print(f"\n   [dim]Set default:[/dim] [yellow]dumpconfluence config default {profiles[0]}[/yellow]")
        else:
            console.print("\n[yellow]  No profiles configured yet[/yellow]")
            console.print("   [dim]Create one with:[/dim] [cyan]dumpconfluence backup URL --save-profile myprofile[/cyan]")

        console.print("\n[bold]Quick Start:[/bold]")
        console.print("   • Backup page:     [cyan]dumpconfluence backup URL[/cyan]")
        console.print("   • Batch backup:    [cyan]dumpconfluence batch urls.txt --profile NAME[/cyan]")
        console.print("   • Manage profiles: [cyan]dumpconfluence config --help[/cyan]")
        console.print("\nFor detailed help: [yellow]dumpconfluence COMMAND --help[/yellow]\n")


@cli.command()
@click.argument('page_url')
@click.option('--url', '-u', help='Confluence base URL (e.g., https://company.atlassian.net)')
@click.option('--email', '-e', help='Confluence account email')
@click.option('--token', '-t', help='Confluence API token')
@click.option('--output-dir', '-o', default='.', help='Output directory (default: current directory)')
@click.option('--profile', '-p', help='Use saved profile')
@click.option('--save-profile', help='Save credentials as profile')
def backup(page_url: str, url: Optional[str], email: Optional[str], token: Optional[str],
          output_dir: str, profile: Optional[str], save_profile: Optional[str]):
    """Backup a single Confluence page"""

    config = ConfigManager()

    # Auto-use profile if available and none specified
    if not profile and not any([url, email, token]):
        auto_profile = config.get_auto_profile()
        if auto_profile:
            url = auto_profile.get('url')
            email = auto_profile.get('email')
            token = auto_profile.get('token')

            profiles = config.list_profiles()
            if len(profiles) == 1:
                console.print(f"[green]✓ Auto-using profile '[cyan]{profiles[0]}[/cyan]' ({email})[/green]")
            else:
                default_name = config.get_default_profile()
                console.print(f"[green]✓ Using default profile '[cyan]{default_name}[/cyan]' ({email})[/green]")

    # Load profile if specified
    elif profile:
        profile_config = config.load_profile(profile)
        if profile_config:
            url = url or profile_config.get('url')
            email = email or profile_config.get('email')
            token = token or profile_config.get('token')
            console.print(f"[green]✓ Using profile '[cyan]{profile}[/cyan]' ({email})[/green]")
        else:
            console.print(f"[red]Profile '{profile}' not found[/red]")
            return

    # Interactive prompts for missing values
    if not url:
        url = Prompt.ask("Confluence URL", default="https://company.atlassian.net")

    if not email:
        email = Prompt.ask("Email")

    if not token:
        token = Prompt.ask("API Token", password=True)

    # Save profile if requested
    if save_profile:
        config.save_profile(save_profile, url, email, token)
        console.print(f"[green]✓ Profile '{save_profile}' saved[/green]")

    # Create output directory
    output_path = Path(output_dir).resolve()

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Backing up page...", total=None)

            backup_client = ConfluenceBackup(url, email, token, str(output_path))
            result = backup_client.backup_page(page_url)

            if result:
                console.print(f"[green]✓ Successfully backed up to {result}[/green]")
            else:
                console.print("[red]✗ Backup failed[/red]")
                sys.exit(1)

    except ValidationError as e:
        console.print(f"[red]Validation Error:[/red] {str(e)}")
        console.print("[yellow]Tip:[/yellow] Check the page URL format and credentials")
        sys.exit(1)
    except AuthenticationError as e:
        console.print(f"[red]Authentication Error:[/red] {str(e)}")
        console.print("[yellow]Tip:[/yellow] Verify your email and API token in the profile")
        sys.exit(1)
    except NetworkError as e:
        console.print(f"[red]Network Error:[/red] {str(e)}")
        console.print("[yellow]Tip:[/yellow] Check your internet connection and Confluence URL")
        sys.exit(1)
    except ConfluenceBackupError as e:
        console.print(f"[red]Backup Error:[/red] {str(e)}")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Unexpected Error:[/red] {str(e)}")
        console.print("[dim]If this persists, please report it at: https://github.com/danilipari/dumpconfluence/issues[/dim]")
        sys.exit(1)


@cli.command()
@click.argument('file_path')
@click.option('--profile', '-p', help='Use saved profile')
@click.option('--output-dir', '-o', default='.', help='Output directory (default: current directory)')
def batch(file_path: str, profile: Optional[str], output_dir: str):
    """Backup multiple pages from a file with URLs"""

    config = ConfigManager()

    # Load profile
    if profile:
        profile_config = config.load_profile(profile)
        if not profile_config:
            console.print(f"[red]Profile '{profile}' not found[/red]")
            return
    else:
        console.print("[red]Profile required for batch operations[/red]")
        return

    # Read URLs from file
    try:
        with open(file_path, 'r') as f:
            urls = [line.strip() for line in f if line.strip()]
    except Exception as e:
        console.print(f"[red]Error reading file: {str(e)}[/red]")
        return

    console.print(f"[cyan]Found {len(urls)} URLs to backup[/cyan]")

    backup_client = ConfluenceBackup(
        profile_config['url'],
        profile_config['email'],
        profile_config['token'],
        output_dir
    )

    # Backup each URL
    for i, url in enumerate(urls, 1):
        console.print(f"\n[cyan][{i}/{len(urls)}] Processing: {url}[/cyan]")
        try:
            result = backup_client.backup_page(url)
            if result:
                console.print(f"[green]✓ Success: {result}[/green]")
            else:
                console.print(f"[yellow]⚠ Skipped: {url}[/yellow]")
        except Exception as e:
            console.print(f"[red]✗ Failed: {str(e)}[/red]")


@cli.group()
def config():
    """Manage configuration and profiles"""
    pass


@config.command()
@click.argument('name')
@click.option('--url', '-u', help='Confluence base URL')
@click.option('--email', '-e', help='Confluence account email')
@click.option('--token', '-t', help='Confluence API token')
def add(name: str, url: Optional[str], email: Optional[str], token: Optional[str]):
    """Add a new profile"""

    # Interactive prompts
    if not url:
        url = Prompt.ask("Confluence URL", default="https://company.atlassian.net")
    if not email:
        email = Prompt.ask("Email")
    if not token:
        token = Prompt.ask("API Token", password=True)

    config_mgr = ConfigManager()
    config_mgr.save_profile(name, url, email, token)
    console.print(f"[green]✓ Profile '{name}' created[/green]")


@config.command()
def list():
    """List all saved profiles"""
    config_mgr = ConfigManager()
    profiles = config_mgr.list_profiles()

    if not profiles:
        console.print("[yellow]No profiles found[/yellow]")
        return

    console.print("\n[bold cyan]Saved Profiles:[/bold cyan]")
    for profile in profiles:
        data = config_mgr.load_profile(profile)
        console.print(f"  • [bold]{profile}[/bold]: {data['email']} @ {data['url']}")


@config.command()
@click.argument('name')
def remove(name: str):
    """Remove a profile"""
    config_mgr = ConfigManager()
    if config_mgr.remove_profile(name):
        console.print(f"[green]✓ Profile '{name}' removed[/green]")
    else:
        console.print(f"[red]Profile '{name}' not found[/red]")


@config.command()
@click.argument('name')
def default(name: str):
    """Set a profile as default"""
    config_mgr = ConfigManager()
    if config_mgr.set_default_profile(name):
        console.print(f"[green]✓ Profile '{name}' set as default[/green]")
    else:
        console.print(f"[red]Profile '{name}' not found[/red]")


def main():
    cli()


if __name__ == "__main__":
    main()