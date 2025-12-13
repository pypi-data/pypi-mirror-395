#!/usr/bin/env python3
"""
Paved CLI - SDK+CLI (remote‑only): build, deploy, invoke, logs, list.
VM execution commands are stubbed out in this package.
"""
import io
import os
import sys
import json
import yaml
import click
import tarfile
import tempfile
from pathlib import Path
from typing import Optional

from .config import config
from .api import api_client, PlatformAPIError


@click.group()
@click.version_option(version="0.1.0")
@click.option('--platform', envvar='PAVED_PLATFORM_URL', help='Platform URL (default: https://app.hipaved.com)')
def cli(platform):
    """Paved CLI (remote‑only)."""
    if platform:
        config.platform_url = platform


@cli.command()
@click.argument('agent_dir', type=click.Path(exists=True, file_okay=False))
@click.option('--output', '-o', default=None, help='Output image file path (default: <name>.tar.gz)')
@click.option('--tag', '-t', default=None, help='Tag for the agent image (metadata only)')
def build(agent_dir: str, output: Optional[str], tag: Optional[str]):
    """Build an agent tar.gz from a directory (for deploy)."""
    agent_path = Path(agent_dir)

    if not (agent_path / "main.py").exists() and not (agent_path / "agent.py").exists():
        click.echo("Error: Agent directory must contain main.py or agent.py", err=True)
        sys.exit(1)

    # Load metadata (optional)
    metadata = {}
    metadata_file = agent_path / "agent.yaml"
    if metadata_file.exists():
        with open(metadata_file) as f:
            metadata = yaml.safe_load(f) or {}

    agent_name = metadata.get('name', agent_path.name)
    if not tag:
        tag = f"{agent_name}:latest"
    if not output:
        output = f"{agent_name}.tar.gz"

    click.echo(f"Building agent image: {tag}")

    with tempfile.NamedTemporaryFile(suffix='.tar.gz', delete=False) as tmp_file:
        with tarfile.open(tmp_file.name, 'w:gz') as tar:
            # Add all files from agent directory
            for file_path in agent_path.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(agent_path)
                    tar.add(file_path, arcname=arcname)

            # If no agent.yaml present, inject minimal metadata
            if not metadata_file.exists():
                metadata_info = tarfile.TarInfo(name='agent.yaml')
                metadata_content = yaml.dump({"name": agent_name, "tag": tag}).encode('utf-8')
                metadata_info.size = len(metadata_content)
                tar.addfile(metadata_info, fileobj=io.BytesIO(metadata_content))

    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    os.replace(tmp_file.name, output_path)
    click.echo(f"Agent image built: {output_path}")


@cli.command()
@click.option('--email', prompt=True, help='Your email address')
@click.option('--password', prompt=True, hide_input=True, help='Your password')
@click.option('--platform-url', envvar='PAVED_PLATFORM_URL', help='Platform URL')
def login(email, password, platform_url):
    """Authenticate with the Paved Platform."""
    click.echo("🔐 Logging in to Paved Platform...")
    if platform_url:
        config.platform_url = platform_url
    try:
        auth_response = api_client.login(email, password)
        access_token = auth_response.get('access_token')
        if not access_token:
            click.echo("Error: No access token received", err=True)
            sys.exit(1)
        api_client.api_key = access_token
        user_info = api_client.get_current_user()
        config.api_key = access_token
        config.user_email = user_info['email']
        config.user_id = user_info['id']
        click.echo()
        click.secho("✓ Successfully logged in!", fg="green")
        click.echo(f"  User: {user_info['name']} ({user_info['email']})")
        click.echo(f"  Platform: {config.platform_url}")
        click.echo(f"  Token: {access_token[:20]}...")
        click.echo()
        click.echo("Note: JWT tokens may expire. Use API keys for long‑lived auth where available.")
    except PlatformAPIError as e:
        click.echo(f"Login failed: {e}", err=True)
        sys.exit(1)


@cli.command()
def logout():
    """Log out from Paved Platform."""
    if not config.is_authenticated():
        click.echo("You are not logged in.")
        return
    email = config.user_email
    config.clear()
    click.secho("✓ Logged out successfully!", fg="green")
    if email:
        click.echo(f"  User: {email}")


@cli.command()
@click.argument('agent_tar', type=click.Path(exists=True))
@click.option('--name', prompt=True, help='Agent name')
@click.option('--description', default='', help='Agent description')
@click.option('--policies', multiple=True, help='Policies for the agent')
def deploy(agent_tar, name, description, policies):
    """Deploy an agent tarball to the Paved Platform."""
    if not config.is_authenticated():
        click.echo("Error: Not authenticated. Run 'pvd login' first.", err=True)
        sys.exit(1)
    agent_path = Path(agent_tar)
    if not agent_path.exists():
        click.echo(f"Error: Agent tar not found: {agent_tar}", err=True)
        sys.exit(1)
    click.echo(f"🚀 Deploying agent: {name}")
    click.echo(f"   File: {agent_path.name} ({agent_path.stat().st_size} bytes)")
    click.echo(f"   Platform: {config.platform_url}")
    click.echo()
    try:
        with click.progressbar(length=100, label='Uploading') as bar:
            bar.update(30)
            result = api_client.upload_agent(name=name, agent_tar_path=agent_path, description=description, policies=list(policies))
            bar.update(70)
        click.echo()
        click.secho("✓ Agent deployed successfully!", fg="green")
        click.echo(f"  Agent ID: {result['agent']['id']}")
        click.echo(f"  Version: {result['version']['version']}")
        click.echo(f"  Status: {result['agent']['status']}")
        click.echo()
        click.echo("Invoke your agent:")
        click.echo("  pvd invoke <agent-id> --payload '{""message"": ""Hello!""}'")
    except PlatformAPIError as e:
        click.echo(f"Deploy failed: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('agent_id')
@click.option('--payload', required=True, help='JSON payload for the agent')
@click.option('--sync/--async', 'sync_mode', default=False, help='Run synchronously (default: async)')
@click.option('--timeout', default=None, type=int, help='Timeout seconds for sync execution')
def invoke(agent_id, payload, sync_mode, timeout):
    """Invoke a deployed agent."""
    if not config.is_authenticated():
        click.echo("Error: Not authenticated. Run 'pvd login' first.", err=True)
        sys.exit(1)
    try:
        payload_obj = json.loads(payload)
    except json.JSONDecodeError:
        click.echo("Error: --payload must be valid JSON", err=True)
        sys.exit(1)
    try:
        result = api_client.invoke_agent(agent_id, payload=payload_obj, async_execution=not sync_mode, timeout_seconds=timeout)
        if sync_mode:
            click.secho("✓ Invocation completed", fg="green")
            click.echo(json.dumps(result, indent=2))
        else:
            inv_id = result.get('invocation', {}).get('id') or result.get('invocation_id')
            click.secho("✓ Invocation started", fg="green")
            click.echo(f"  Invocation ID: {inv_id}")
            click.echo("Use: pvd logs <invocation-id> --follow")
    except PlatformAPIError as e:
        click.echo(f"\nInvocation failed: {e}", err=True)
        sys.exit(1)


@cli.command(name='logs')
@click.argument('invocation_id')
@click.option('--follow', '-f', is_flag=True, help='Follow logs in real-time')
def logs_command(invocation_id, follow):
    """Get logs for an invocation."""
    if not config.is_authenticated():
        click.echo("Error: Not authenticated. Run 'pvd login' first.", err=True)
        sys.exit(1)
    if follow:
        _follow_logs(invocation_id)
    else:
        _show_logs(invocation_id)


def _show_logs(invocation_id: str):
    try:
        invocation = api_client.get_invocation(invocation_id)
        click.echo(f"📋 Invocation: {invocation_id}")
        click.echo(f"   Agent: {invocation.get('agent_id')}")
        click.echo(f"   Status: {invocation.get('status')}")
        click.echo(f"   Started: {invocation.get('queued_at', 'N/A')}")
        if invocation.get('duration_ms'):
            click.echo(f"   Duration: {invocation['duration_ms']}ms")
        logs_response = api_client.get_invocation_logs(invocation_id)
        logs = logs_response.get('logs', '')
        if logs:
            click.echo()
            click.echo("=== LOGS ===")
            click.echo(logs)
        if invocation.get('status') == 'completed' and invocation.get('result'):
            click.echo()
            click.echo("=== RESULT ===")
            click.echo(json.dumps(invocation['result'], indent=2))
        elif invocation.get('status') == 'failed' and invocation.get('error'):
            click.echo()
            click.secho("=== ERROR ===", fg="red")
            click.echo(invocation['error'])
    except PlatformAPIError as e:
        click.echo(f"Failed to get logs: {e}", err=True)
        sys.exit(1)


def _follow_logs(invocation_id: str):
    import time
    try:
        click.echo(f"Following invocation: {invocation_id}")
        click.echo("Press Ctrl+C to stop")
        click.echo()
        last_status = None
        while True:
            invocation = api_client.get_invocation(invocation_id)
            status = invocation.get('status')
            if status != last_status:
                click.echo(f"Status: {status}")
                last_status = status
            if status in ['completed', 'failed', 'cancelled']:
                if status == 'completed' and invocation.get('result'):
                    click.echo()
                    click.secho("✓ Completed!", fg="green")
                    click.echo(f"Duration: {invocation.get('duration_ms', 0)}ms")
                    click.echo()
                    click.echo("Result:")
                    click.echo(json.dumps(invocation['result'], indent=2))
                elif status == 'failed':
                    click.echo()
                    click.secho("✗ Failed!", fg="red")
                    if invocation.get('error'):
                        click.echo(f"Error: {invocation['error']}")
                break
            time.sleep(2)
    except KeyboardInterrupt:
        click.echo("\nStopped following logs")
    except PlatformAPIError as e:
        click.echo(f"\nFailed to follow logs: {e}", err=True)
        sys.exit(1)


@cli.command(name='list')
@click.option('--page', default=1, help='Page number')
@click.option('--per-page', default=20, help='Items per page')
def list_command(page, per_page):
    """List your deployed agents."""
    if not config.is_authenticated():
        click.echo("Error: Not authenticated. Run 'pvd login' first.", err=True)
        sys.exit(1)
    try:
        result = api_client.list_agents(page=page, per_page=per_page)
        agents = result.get('agents', [])
        pagination = result.get('pagination', {'page': 1, 'total_pages': 1, 'total': len(agents)})
        if not agents:
            click.echo("No agents deployed yet.")
            click.echo()
            click.echo("Deploy your first agent:")
            click.echo("  pvd build ./my-agent")
            click.echo("  pvd deploy my-agent.tar.gz --name my-agent")
            return
        click.echo(f"📦 Your Agents (Page {pagination['page']} of {pagination.get('total_pages', 1)})")
        click.echo()
        click.echo(f"{'ID':<38} {'NAME':<20} {'STATUS':<12} {'VERSIONS'}")
        click.echo("-" * 90)
        for agent in agents:
            click.echo(
                f"{agent['id']:<38} "
                f"{agent['name']:<20} "
                f"{agent['status']:<12} "
                f"{agent.get('version_count', 0)}"
            )
        click.echo()
        click.echo(f"Total: {pagination.get('total', len(agents))} agents")
    except PlatformAPIError as e:
        click.echo(f"Failed to list agents: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('name')
@click.option('--template', default='simple', type=click.Choice(['simple', 'llm', 'api']), help='Agent template')
def init(name, template):
    """Initialize a new agent project in NAME directory."""
    agent_dir = Path(name)
    if agent_dir.exists():
        click.echo(f"Error: Directory '{name}' already exists", err=True)
        sys.exit(1)
    agent_dir.mkdir(parents=True)

    if template == 'simple':
        main_content = '''#!/usr/bin/env python3
"""
Simple Paved agent.
"""
import sys
import json


def main(agent):
    """Agent main function.

    Args:
        agent: Agent object with SDK capabilities (for SDK-remote mode)
               In platform-hosted mode, this is None - use stdin/stdout instead
    """
    if agent is None:
        # Platform-hosted mode: read from stdin
        input_data = json.load(sys.stdin)
    else:
        # SDK-remote mode: agent invocation context available
        input_data = getattr(agent, '_invocation_payload', {})

    message = input_data.get('message', 'Hello, Paved!')
    result = {'status': 'success', 'message': message, 'echo': f'You said: {message}'}

    if agent is None:
        # Platform-hosted: write to stdout
        print(json.dumps(result))

    return result


if __name__ == '__main__':
    main(None)
'''
    elif template == 'llm':
        main_content = '''#!/usr/bin/env python3
"""
LLM-powered Paved agent.
"""
import sys
import json
import os


def main(agent):
    """Agent main function.

    Args:
        agent: Agent object with SDK capabilities (for SDK-remote mode)
               In platform-hosted mode, this is None - use stdin/stdout instead
    """
    if agent is None:
        # Platform-hosted mode: read from stdin
        input_data = json.load(sys.stdin)
    else:
        # SDK-remote mode: can use agent.llm() for policy-enforced LLM calls
        input_data = getattr(agent, '_invocation_payload', {})

    prompt = input_data.get('prompt', 'Hello!')
    # TODO: integrate your LLM
    result = {'status': 'success', 'prompt': prompt, 'response': 'LLM response would go here', 'model': 'gpt-4'}

    if agent is None:
        # Platform-hosted: write to stdout
        print(json.dumps(result))

    return result


if __name__ == '__main__':
    main(None)
'''
    else:  # api
        main_content = '''#!/usr/bin/env python3
"""
API-calling Paved agent.
"""
import sys
import json
import requests


def main(agent):
    """Agent main function.

    Args:
        agent: Agent object with SDK capabilities (for SDK-remote mode)
               In platform-hosted mode, this is None - use stdin/stdout instead
    """
    if agent is None:
        # Platform-hosted mode: read from stdin
        input_data = json.load(sys.stdin)
    else:
        # SDK-remote mode: can use agent.http_request() for policy-enforced HTTP calls
        input_data = getattr(agent, '_invocation_payload', {})

    url = input_data.get('url', 'https://api.example.com/data')
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        result = {'status': 'success', 'url': url, 'data': response.json(), 'status_code': response.status_code}
    except Exception as e:
        result = {'status': 'error', 'error': str(e)}

    if agent is None:
        # Platform-hosted: write to stdout
        print(json.dumps(result))

    return result


if __name__ == '__main__':
    main(None)
'''

    (agent_dir / 'main.py').write_text(main_content)
    (agent_dir / 'main.py').chmod(0o755)

    agent_yaml = f'''name: {name}
description: A new Paved agent
version: 1.0.0
template: {template}

policies:
  - {template}
'''
    (agent_dir / 'agent.yaml').write_text(agent_yaml)

    if template == 'api':
        (agent_dir / 'requirements.txt').write_text('requests\n')
    elif template == 'llm':
        (agent_dir / 'requirements.txt').write_text('openai\n')
    else:
        (agent_dir / 'requirements.txt').write_text('')

    readme = f'''# {name}

A Paved agent created with the {template} template.

## Development

Test locally:
```bash
echo '{{"message": "test"}}' | python3 main.py
```

Build agent:
```bash
pvd build .
```

Deploy to platform:
```bash
pvd deploy {name}.tar.gz --name {name}
```

## Usage

Invoke the agent:
```bash
pvd invoke <agent-id> --payload '{{"message": "Hello!"}}'
```
'''
    (agent_dir / 'README.md').write_text(readme)

    click.secho(f"✓ Agent project created: {name}/", fg="green")
    click.echo()
    click.echo("Next steps:")
    click.echo(f"  cd {name}")
    click.echo("  # Edit main.py with your agent logic")
    click.echo("  pvd build .")
    click.echo(f"  pvd deploy {name}.tar.gz --name {name}")


# ---- Stubbed VM commands (disabled in this package) ----

def _vm_stub(cmd: str):
    click.echo(f"'{cmd}' is not available in the pvd package. Use platform remote workflow.", err=True)
    sys.exit(1)


@cli.command()
def version():
    """Show Paved SDK/CLI version."""
    click.echo("Paved SDK/CLI (remote‑only)")
    click.echo("Route: Platform policies endpoint (/v1/policies/check)")


@cli.command()
def run():  # noqa: D401 - stub
    _vm_stub('run')


@cli.command(name='runtime-logs')
def runtime_logs():  # noqa: D401 - stub
    _vm_stub('runtime-logs')


@cli.command()
def ps():  # noqa: D401 - stub
    _vm_stub('ps')


@cli.command()
def stop():  # noqa: D401 - stub
    _vm_stub('stop')


if __name__ == '__main__':
    cli()
