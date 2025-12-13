#!/usr/bin/env python3
"""DebugTwin Copilot CLI - AI-powered firmware debugging assistant.

This is a standalone CLI that communicates with the DebugTwin API.
"""

import click
import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Optional
import aiohttp
from datetime import datetime

from . import __version__

# Default production API URL
DEFAULT_API_URL = "https://web-production-5988.up.railway.app"


class DebugTwinClient:
    """Client for DebugTwin API."""
    
    def __init__(self, api_url: str, api_key: Optional[str] = None):
        self.api_url = api_url.rstrip('/')
        self.api_key = api_key
        self.session_id: Optional[str] = None
        self.user_id = f"cli_user_{int(datetime.now().timestamp())}"
    
    def _get_headers(self) -> dict:
        """Get request headers with authentication."""
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers
    
    async def start_session(self, project_name: str = "cli_project") -> bool:
        """Start a new conversation session."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.api_url}/copilot/start",
                    json={
                        "user_id": self.user_id,
                        "project_name": project_name,
                        "platform": "cortex-m"
                    },
                    headers=self._get_headers()
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        self.session_id = data["session_id"]
                        click.echo(f"\n🤖 {data['message']}\n")
                        return True
                    else:
                        error = await response.text()
                        click.echo(f"❌ Failed to start session: {error}", err=True)
                        return False
        except aiohttp.ClientError as e:
            click.echo(f"❌ Connection error: {e}", err=True)
            return False
    
    async def send_message(self, message: str) -> Optional[str]:
        """Send a message and get response."""
        if not self.session_id:
            click.echo("❌ No active session", err=True)
            return None
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.api_url}/copilot/message",
                    json={
                        "session_id": self.session_id,
                        "message": message,
                        "attachments": []
                    },
                    headers=self._get_headers()
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("message", "")
                    else:
                        error = await response.text()
                        click.echo(f"❌ Error: {error}", err=True)
                        return None
        except aiohttp.ClientError as e:
            click.echo(f"❌ Connection error: {e}", err=True)
            return None
    
    async def analyze_file(self, file_path: Path) -> Optional[str]:
        """Analyze a firmware log file using the dedicated analyze endpoint."""
        try:
            content = file_path.read_bytes()
            # Use a longer timeout for analysis (120 seconds)
            timeout = aiohttp.ClientTimeout(total=120)
            
            # Use multipart form data for file upload
            form_data = aiohttp.FormData()
            form_data.add_field('log_file', content, 
                               filename=file_path.name,
                               content_type='text/plain')
            form_data.add_field('platform', 'cortex-m')
            form_data.add_field('confidence_threshold', '0.5')
            
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(
                    f"{self.api_url}/analyze/log",
                    data=form_data,
                    headers={"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        # Extract the markdown report from the response
                        return data.get("markdown_report") or self._format_analysis_result(data)
                    else:
                        error = await response.text()
                        click.echo(f"❌ Analysis error: {error}", err=True)
                        return None
        except asyncio.TimeoutError:
            click.echo(f"❌ Timeout: Analysis took too long. Try a smaller file.", err=True)
            return None
        except Exception as e:
            click.echo(f"❌ Analyze error: {e}", err=True)
            return None
    
    def _format_analysis_result(self, data: dict) -> str:
        """Format analysis result when markdown_report is not available."""
        lines = [
            "# Firmware Log Analysis",
            "",
            f"**Platform:** {data.get('platform', 'Unknown')}",
            f"**Primary Fault:** {data.get('primary_fault', 'Unknown')}",
            f"**Confidence:** {data.get('confidence', 0):.1%}",
            f"**Criticality:** {data.get('criticality', 'Unknown')}",
            "",
            "## Root Cause",
            data.get('root_cause', 'Unknown'),
            "",
            "## Suggested Fix",
            data.get('suggested_fix', 'No suggestions available'),
            ""
        ]
        
        # Add evidence
        evidence = data.get('evidence_lines', [])
        if evidence:
            lines.append("## Evidence from Logs")
            for e in evidence[:10]:
                lines.append(f"- {e}")
            lines.append("")
        
        return "\n".join(lines)


def get_config_path() -> Path:
    """Get path to config file."""
    config_dir = Path.home() / ".debugtwin"
    config_dir.mkdir(exist_ok=True)
    return config_dir / "config.json"


def load_config() -> dict:
    """Load configuration from file."""
    config_path = get_config_path()
    if config_path.exists():
        try:
            return json.loads(config_path.read_text())
        except Exception:
            pass
    return {}


def save_config(config: dict) -> None:
    """Save configuration to file."""
    config_path = get_config_path()
    config_path.write_text(json.dumps(config, indent=2))


@click.group()
@click.option('--api-url', envvar='DEBUGTWIN_API_URL', help='API URL (default: production)')
@click.pass_context
def cli(ctx, api_url):
    """DebugTwin Copilot CLI - AI-powered firmware debugging assistant."""
    ctx.ensure_object(dict)
    
    config = load_config()
    
    # Priority: CLI flag > env var > config file > default
    final_url = api_url or config.get('api_url') or DEFAULT_API_URL
    auth_token = config.get('auth_token')
    
    ctx.obj['api_url'] = final_url
    ctx.obj['auth_token'] = auth_token
    ctx.obj['config'] = config


@cli.command()
def version():
    """Show version information."""
    click.echo(f"DebugTwin CLI v{__version__}")


@cli.command(name='help')
@click.pass_context
def show_help(ctx):
    """Show detailed help and usage examples."""
    help_text = f"""
╔══════════════════════════════════════════════════════════════════╗
║                    DebugTwin CLI v{__version__}                        ║
║            AI-Powered Firmware Debugging Assistant               ║
╚══════════════════════════════════════════════════════════════════╝

📚 COMMANDS:
  login      Authenticate with your API key
  logout     Remove saved authentication
  chat       Start an interactive debugging session
  ask        Ask a quick one-off question
  analyze    Analyze a firmware log file
  configure  Set custom API URL (for self-hosted)
  version    Show version information
  help       Show this help message

🚀 QUICK START:
  1. Get an API key from: https://embedded-frontend-production.up.railway.app
  2. Login:    debugtwin login --key YOUR_API_KEY
  3. Chat:     debugtwin chat

📖 EXAMPLES:
  debugtwin login --key dt_live_xxx...
  debugtwin chat
  debugtwin ask "What causes a HardFault on STM32?"
  debugtwin analyze crash_dump.log
  debugtwin configure --url https://your-server.com

💡 TIPS:
  • In chat mode, type 'exit', 'quit', or press Ctrl+C to leave
  • Use 'analyze' to upload and analyze log files
  • API keys can be generated from the web dashboard

📬 SUPPORT:
  Issues: https://github.com/ashish-frozo/embedded-client
"""
    click.echo(help_text)


@cli.command()
@click.option('--url', required=True, help='API URL to configure')
@click.pass_context
def configure(ctx, url):
    """Configure API URL (for self-hosted deployments)."""
    config = ctx.obj['config']
    config['api_url'] = url
    save_config(config)
    click.echo(f"✅ API URL configured: {url}")


@cli.command()
@click.option('--key', required=True, help='Your API key from the dashboard')
@click.pass_context
def login(ctx, key):
    """Authenticate with your API key."""
    api_url = ctx.obj.get('api_url') or DEFAULT_API_URL
    
    # Validate basic format
    if not key.startswith('dt_live_'):
        click.echo("❌ Invalid API key format. Keys should start with 'dt_live_'", err=True)
        sys.exit(1)
    
    click.echo(f"🔐 Validating API key with {api_url}...")
    
    async def validate_key():
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{api_url}/copilot/start",
                    json={
                        "user_id": "cli_validation",
                        "project_name": "key_validation",
                        "platform": "cortex-m"
                    },
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {key}"
                    }
                ) as response:
                    if response.status == 200:
                        return True
                    elif response.status == 401:
                        click.echo("❌ Invalid API key. Please check your key and try again.", err=True)
                        return False
                    else:
                        error = await response.text()
                        click.echo(f"❌ Server error: {error}", err=True)
                        return False
        except aiohttp.ClientError as e:
            click.echo(f"❌ Connection error: {e}", err=True)
            return False
    
    if asyncio.run(validate_key()):
        config = ctx.obj['config']
        config['auth_token'] = key
        save_config(config)
        click.echo("✅ API key validated and saved.")
        click.echo("🔓 You are now logged in.")


@cli.command()
@click.pass_context
def logout(ctx):
    """Remove saved authentication."""
    config = ctx.obj['config']
    if 'auth_token' in config:
        del config['auth_token']
        save_config(config)
    click.echo("👋 Logged out successfully.")


@cli.command()
@click.pass_context
def chat(ctx):
    """Start an interactive debugging session."""
    api_url = ctx.obj['api_url']
    auth_token = ctx.obj['auth_token']
    
    if not auth_token:
        click.echo("❌ Not logged in. Run: debugtwin login --key YOUR_KEY", err=True)
        sys.exit(1)
    
    click.echo("🚀 Starting DebugTwin Copilot CLI...")
    click.echo(f"🔌 Connecting to: {api_url}")
    
    client = DebugTwinClient(api_url, auth_token)
    
    async def run_chat():
        if not await client.start_session():
            sys.exit(1)
        
        click.echo("Type 'exit' or 'quit' to end the session.\n")
        
        while True:
            try:
                user_input = click.prompt("You", prompt_suffix=": ")
                
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    click.echo("\n👋 Goodbye! Happy debugging!")
                    break
                
                response = await client.send_message(user_input)
                if response:
                    click.echo(f"\n🤖 {response}\n")
                    
            except (KeyboardInterrupt, EOFError):
                click.echo("\n👋 Session ended.")
                break
    
    asyncio.run(run_chat())


@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.pass_context
def analyze(ctx, file_path):
    """Analyze a firmware log file."""
    api_url = ctx.obj['api_url']
    auth_token = ctx.obj['auth_token']
    
    if not auth_token:
        click.echo("❌ Not logged in. Run: debugtwin login --key YOUR_KEY", err=True)
        sys.exit(1)
    
    file_path = Path(file_path)
    click.echo(f"🔍 Analyzing {file_path.name}...")
    click.echo(f"🔌 Using API: {api_url}")
    click.echo("⏳ This may take up to 2 minutes for complex logs...")
    
    client = DebugTwinClient(api_url, auth_token)
    
    async def run_analyze():
        # Use dedicated analyze endpoint (no copilot session needed)
        analysis = await client.analyze_file(file_path)
        if analysis:
            click.echo(f"\n📊 ANALYSIS RESULTS:\n{analysis}")
        else:
            click.echo("❌ Analysis failed. Please try again.", err=True)
            sys.exit(1)
    
    asyncio.run(run_analyze())


@cli.command()
@click.argument('question')
@click.pass_context
def ask(ctx, question):
    """Ask a quick question about firmware debugging."""
    api_url = ctx.obj['api_url']
    auth_token = ctx.obj['auth_token']
    
    if not auth_token:
        click.echo("❌ Not logged in. Run: debugtwin login --key YOUR_KEY", err=True)
        sys.exit(1)
    
    client = DebugTwinClient(api_url, auth_token)
    
    async def run_ask():
        if not await client.start_session():
            sys.exit(1)
        
        response = await client.send_message(question)
        if response:
            click.echo(f"\n🤖 {response}\n")
    
    asyncio.run(run_ask())


def main():
    """Entry point for the CLI."""
    cli(obj={})


if __name__ == '__main__':
    main()
