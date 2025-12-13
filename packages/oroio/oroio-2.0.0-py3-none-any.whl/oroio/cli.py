#!/usr/bin/env python3
"""
oroio CLI - Command-line tool for oroio Factory Droid API Key Manager
"""

import click
import requests
import sys
from rich.console import Console
from rich.table import Table
from rich import box
from datetime import datetime
from typing import Optional

from .config import config

console = Console()


def get_headers() -> dict:
    """Get request headers with auth token"""
    token = config.get_access_token()
    if not token:
        console.print("[red]Not authenticated. Please run 'oroio login' first.[/red]")
        sys.exit(1)
    return {"Authorization": f"Bearer {token}"}


def handle_auth_error(response):
    """Handle authentication errors"""
    if response.status_code == 401:
        console.print("[red]Authentication failed. Please run 'oroio login' again.[/red]")
        config.clear_tokens()
        sys.exit(1)


@click.group()
def cli():
    """oroio - Factory Droid API Key Manager
    
    Manage your Factory Droid API keys through oroio microservice.
    """
    pass


# ===== Configuration Commands =====

@cli.group()
def config_cmd():
    """Configuration management"""
    pass


@config_cmd.command("set-server")
@click.argument('url')
def set_server(url: str):
    """Set API server URL
    
    Examples:
        oroio config set-server https://api.oroio.io
        oroio config set-server http://localhost:8000
    """
    config.set_api_endpoint(url)
    console.print(f"[green]✓ Server set to: {url}[/green]")


@config_cmd.command("show")
def show_config():
    """Show current configuration"""
    endpoint = config.get_api_endpoint()
    authenticated = config.is_authenticated()
    
    console.print("\n[cyan]Current Configuration:[/cyan]")
    console.print(f"[dim]Server:[/dim]        {endpoint}")
    console.print(f"[dim]Authenticated:[/dim] {'Yes' if authenticated else 'No'}")
    console.print(f"[dim]Config file:[/dim]   {config.config_file}\n")


# Legacy command for backward compatibility
@cli.command("config-endpoint", hidden=True)
@click.option('--endpoint', default='http://localhost:8000', help='API endpoint URL')
def config_endpoint_legacy(endpoint: str):
    """[DEPRECATED] Use 'oroio config set-server' instead"""
    config.set_api_endpoint(endpoint)
    console.print(f"[yellow]Warning: This command is deprecated. Use 'oroio config set-server' instead.[/yellow]")
    console.print(f"[green]API endpoint set to: {endpoint}[/green]")


@cli.command()
def version():
    """Show version information"""
    from .__version__ import __version__
    console.print(f"[cyan]oroio CLI version {__version__}[/cyan]")
    console.print(f"[dim]API endpoint: {config.get_api_endpoint()}[/dim]")


# ===== Authentication Commands =====

@cli.command()
@click.option('--username', prompt=True, help='Username')
@click.option('--password', prompt=True, hide_input=True, help='Password')
def login(username: str, password: str):
    """Login to oroio service"""
    api_endpoint = config.get_api_endpoint()
    
    try:
        response = requests.post(
            f"{api_endpoint}/api/auth/login",
            json={"username": username, "password": password},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            config.set_tokens(data['access_token'], data['refresh_token'])
            console.print(f"[green]✓ Logged in successfully as {username}[/green]")
        elif response.status_code == 401:
            console.print("[red]✗ Invalid username or password[/red]")
            sys.exit(1)
        else:
            console.print(f"[red]✗ Login failed: {response.text}[/red]")
            sys.exit(1)
    
    except requests.exceptions.RequestException as e:
        console.print(f"[red]✗ Connection error: {e}[/red]")
        console.print(f"[yellow]Make sure API server is running at {api_endpoint}[/yellow]")
        sys.exit(1)


@cli.command()
@click.option('--username', prompt=True, help='Username')
@click.option('--email', prompt=True, help='Email')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='Password')
def register(username: str, email: str, password: str):
    """Register new account"""
    api_endpoint = config.get_api_endpoint()
    
    try:
        response = requests.post(
            f"{api_endpoint}/api/auth/register",
            json={"username": username, "email": email, "password": password},
            timeout=10
        )
        
        if response.status_code == 201:
            console.print(f"[green]✓ Account created successfully![/green]")
            console.print(f"[cyan]Please run 'oroio login' to authenticate.[/cyan]")
        elif response.status_code == 400:
            error = response.json().get('detail', 'Registration failed')
            console.print(f"[red]✗ {error}[/red]")
            sys.exit(1)
        else:
            console.print(f"[red]✗ Registration failed: {response.text}[/red]")
            sys.exit(1)
    
    except requests.exceptions.RequestException as e:
        console.print(f"[red]✗ Connection error: {e}[/red]")
        sys.exit(1)


@cli.command()
def logout():
    """Logout from oroio service"""
    config.clear_tokens()
    console.print("[green]✓ Logged out successfully[/green]")


# ===== Key Management Commands =====

@cli.command()
@click.argument('key')
def add(key: str):
    """Add a new API key
    
    Example:
        oroio add fk-your-factory-api-key
    """
    api_endpoint = config.get_api_endpoint()
    
    try:
        response = requests.post(
            f"{api_endpoint}/api/keys",
            json={"key": key},
            headers=get_headers(),
            timeout=10
        )
        
        handle_auth_error(response)
        
        if response.status_code == 201:
            data = response.json()
            console.print(f"[green]✓ {data['message']}[/green]")
        else:
            error = response.json().get('detail', 'Failed to add key')
            console.print(f"[red]✗ {error}[/red]")
            sys.exit(1)
    
    except requests.exceptions.RequestException as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        sys.exit(1)


@cli.command()
def list():
    """List all API keys with usage information"""
    api_endpoint = config.get_api_endpoint()
    
    try:
        response = requests.get(
            f"{api_endpoint}/api/keys",
            headers=get_headers(),
            timeout=10
        )
        
        handle_auth_error(response)
        
        if response.status_code == 200:
            data = response.json()
            keys = data['keys']
            
            if not keys:
                console.print("[yellow]No keys found. Add one with 'oroio add <key>'[/yellow]")
                return
            
            # Create table
            table = Table(box=box.ROUNDED, show_header=True, header_style="bold cyan")
            table.add_column("#", style="dim", width=3)
            table.add_column("Key", style="cyan", width=20)
            table.add_column("Balance", justify="right", width=12)
            table.add_column("Used / Total", justify="right", width=20)
            table.add_column("Expires", width=12)
            table.add_column("Status", width=10)
            
            for idx, key_info in enumerate(keys, 1):
                usage = key_info.get('usage')
                
                if usage and usage.get('total'):
                    balance = usage.get('balance', 0)
                    total = usage.get('total', 0)
                    used = usage.get('used', 0)
                    expires = usage.get('expires_at', '?')
                    
                    # Format balance
                    if balance is not None:
                        if balance <= 0:
                            balance_str = f"[red]{format_number(balance)}[/red]"
                        elif balance / total <= 0.1:
                            balance_str = f"[yellow]{format_number(balance)}[/yellow]"
                        else:
                            balance_str = f"[green]{format_number(balance)}[/green]"
                    else:
                        balance_str = "[dim]?[/dim]"
                    
                    usage_str = f"{format_number(used)} / {format_number(total)}"
                else:
                    balance_str = "[dim]?[/dim]"
                    usage_str = "[dim]? / ?[/dim]"
                    expires = "[dim]?[/dim]"
                
                status = "[green]●[/green] Active" if key_info['is_active'] else "[dim]○[/dim] Inactive"
                
                table.add_row(
                    str(idx),
                    key_info['key_prefix'],
                    balance_str,
                    usage_str,
                    str(expires),
                    status
                )
            
            console.print(table)
            console.print(f"\n[dim]Total: {len(keys)} keys[/dim]")
        
        else:
            console.print(f"[red]✗ Failed to list keys: {response.text}[/red]")
            sys.exit(1)
    
    except requests.exceptions.RequestException as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        sys.exit(1)


@cli.command()
@click.argument('index', type=int)
def use(index: int):
    """Switch to key by index (from 'oroio list')
    
    Example:
        oroio use 2
    """
    api_endpoint = config.get_api_endpoint()
    
    try:
        # Get all keys first
        response = requests.get(
            f"{api_endpoint}/api/keys",
            headers=get_headers(),
            timeout=10
        )
        
        handle_auth_error(response)
        
        if response.status_code == 200:
            data = response.json()
            keys = data['keys']
            
            if index < 1 or index > len(keys):
                console.print(f"[red]✗ Index out of range. Must be 1-{len(keys)}[/red]")
                sys.exit(1)
            
            key_id = keys[index - 1]['id']
            
            # Activate key
            response = requests.put(
                f"{api_endpoint}/api/keys/{key_id}/activate",
                headers=get_headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                console.print(f"[green]✓ Switched to key #{index}[/green]")
            else:
                console.print(f"[red]✗ Failed to switch key[/red]")
                sys.exit(1)
        
    except requests.exceptions.RequestException as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        sys.exit(1)


@cli.command()
@click.argument('index', type=int)
def rm(index: int):
    """Remove key by index
    
    Example:
        oroio rm 2
    """
    api_endpoint = config.get_api_endpoint()
    
    try:
        # Get all keys first
        response = requests.get(
            f"{api_endpoint}/api/keys",
            headers=get_headers(),
            timeout=10
        )
        
        handle_auth_error(response)
        
        if response.status_code == 200:
            data = response.json()
            keys = data['keys']
            
            if index < 1 or index > len(keys):
                console.print(f"[red]✗ Index out of range. Must be 1-{len(keys)}[/red]")
                sys.exit(1)
            
            key_id = keys[index - 1]['id']
            
            # Delete key
            response = requests.delete(
                f"{api_endpoint}/api/keys/{key_id}",
                headers=get_headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                console.print(f"[green]✓ {data['message']}[/green]")
            else:
                console.print(f"[red]✗ Failed to delete key[/red]")
                sys.exit(1)
        
    except requests.exceptions.RequestException as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        sys.exit(1)


@cli.command()
def current():
    """Get current active key"""
    api_endpoint = config.get_api_endpoint()
    
    try:
        response = requests.get(
            f"{api_endpoint}/api/keys/current",
            headers=get_headers(),
            timeout=10
        )
        
        handle_auth_error(response)
        
        if response.status_code == 200:
            data = response.json()
            key = data['key']
            
            console.print(f"\n[cyan]Current key:[/cyan] [bold]{key}[/bold]")
            console.print(f"\n[dim]Export command:[/dim]")
            console.print(f"[green]export FACTORY_API_KEY={key}[/green]")
            console.print(f"[dim]# Or for v1 compatibility:[/dim]")
            console.print(f"[green]export DROID_API_KEY={key}[/green]\n")
            
            usage = data.get('usage')
            if usage and usage.get('total'):
                console.print(f"[dim]Balance:[/dim] {format_number(usage.get('balance', 0))} / {format_number(usage.get('total', 0))}")
                console.print(f"[dim]Expires:[/dim] {usage.get('expires_at', '?')}")
        
        elif response.status_code == 404:
            console.print("[yellow]No keys available. Add one with 'oroio add <key>'[/yellow]")
        else:
            console.print(f"[red]✗ Failed to get current key[/red]")
            sys.exit(1)
    
    except requests.exceptions.RequestException as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        sys.exit(1)


@cli.command()
def refresh():
    """Refresh usage information for all keys"""
    api_endpoint = config.get_api_endpoint()
    
    console.print("[cyan]Refreshing usage data...[/cyan]")
    
    try:
        response = requests.post(
            f"{api_endpoint}/api/usage/refresh",
            headers=get_headers(),
            timeout=30
        )
        
        handle_auth_error(response)
        
        if response.status_code == 200:
            data = response.json()
            console.print(f"[green]✓ {data['message']}[/green]")
        else:
            console.print(f"[red]✗ Failed to refresh usage[/red]")
            sys.exit(1)
    
    except requests.exceptions.RequestException as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        sys.exit(1)


@cli.command()
@click.argument('command', nargs=-1, required=True)
def run(command):
    """Run command with current API key (auto-set FACTORY_API_KEY and DROID_API_KEY)
    
    Example:
        oroio run droid
        oroio run python script.py
    """
    import subprocess
    import os
    
    api_endpoint = config.get_api_endpoint()
    
    try:
        response = requests.get(
            f"{api_endpoint}/api/keys/current",
            headers=get_headers(),
            timeout=10
        )
        
        handle_auth_error(response)
        
        if response.status_code == 200:
            data = response.json()
            key = data['key']
            
            # Show masked key
            masked_key = key[:10] + "..." if len(key) > 10 else key
            console.print(f"[dim]Using key: {masked_key}[/dim]")
            
            # Set environment variables (both for compatibility)
            env = os.environ.copy()
            env['FACTORY_API_KEY'] = key  # v2 standard
            env['DROID_API_KEY'] = key    # v1 compatibility
            
            # Run command
            cmd = ' '.join(command)
            console.print(f"[dim]Running: {cmd}[/dim]\n")
            
            # Use shell=True to support pipes, redirects, etc.
            result = subprocess.run(cmd, shell=True, env=env)
            sys.exit(result.returncode)
        
        elif response.status_code == 404:
            console.print("[yellow]No keys available. Add one with 'oroio add <key>'[/yellow]")
            sys.exit(1)
        else:
            console.print(f"[red]✗ Failed to get current key[/red]")
            sys.exit(1)
    
    except requests.exceptions.RequestException as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        sys.exit(1)


# ===== Helper Functions =====

def format_number(n: Optional[float]) -> str:
    """Format large numbers with K/M/B suffixes"""
    if n is None:
        return "?"
    
    if abs(n) >= 1e9:
        return f"{n / 1e9:.1f}B"
    elif abs(n) >= 1e6:
        return f"{n / 1e6:.1f}M"
    elif abs(n) >= 1e3:
        return f"{n / 1e3:.1f}K"
    else:
        return str(int(n))


# Entry point
if __name__ == '__main__':
    cli()
