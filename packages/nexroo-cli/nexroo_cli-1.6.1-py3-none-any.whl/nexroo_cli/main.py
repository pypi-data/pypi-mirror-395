import sys
import os
import asyncio
import argparse
import subprocess
import shutil
import json
import tempfile
from pathlib import Path
from loguru import logger
from .auth.manager import AuthManager
from .installer import BinaryInstaller
from .package_manager import PackageManager
from .config import Config
from .workflow_manager import WorkflowManager


def setup_logging(verbose: bool = False):
    logger.remove()
    level = "DEBUG" if verbose else "INFO"
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=level
    )


async def login_command():
    print("\nLogin feature not yet available")
    print("  This feature will be available with the SaaS release in Q1 2026 after the end of the open beta phase.")
    print("  Stay tuned for updates: https://www.linkedin.com/company/nexroo\n")


async def logout_command():
    try:
        auth_manager = AuthManager()
        await auth_manager.logout()
        print("\n✓ Logged out successfully\n")
    except Exception as e:
        print(f"\n✗ Logout failed: {e}\n")
        sys.exit(1)


async def status_command():
    try:
        auth_manager = AuthManager()

        if not auth_manager.is_authenticated():
            print("\n✗ Not authenticated")
            print("  Run 'nexroo login' to authenticate\n")
            return

        is_valid = await auth_manager.verify_authentication()
        token_data = auth_manager.storage.load_token()

        if is_valid:
            print("\n✓ Authenticated")
            if token_data:
                print(f"  Token expires: {token_data.get('expires_at')}")
            print("  Synvex SaaS features available\n")
        else:
            print("\n⚠ Token expired")
            print("  Run 'nexroo login' to re-authenticate\n")

    except FileNotFoundError:
        print("\n✗ No authentication configuration found")
        print("  Create .zitadel-config.json in project root or ~/.nexroo/\n")
    except Exception as e:
        print(f"\n⚠ Status check failed: {e}\n")


async def ensure_binary_installed():
    installer = BinaryInstaller()

    if not installer.is_installed():
        logger.info("nexroo-engine not found. Installing...")
        try:
            await installer.install()
        except Exception as e:
            logger.error(f"Failed to install nexroo-engine: {e}")
            sys.exit(1)


async def install_command(args):
    try:
        installer = BinaryInstaller()

        if installer.is_installed():
            print("\n✓ nexroo-engine already installed")
            print("\n  Run 'nexroo update' to update to latest version\n")
            return

        print("\nInstalling nexroo-engine...")
        await installer.install()
        print("\n✓ nexroo-engine installed successfully!\n")

    except Exception as e:
        print(f"\n✗ Installation failed: {e}\n")
        sys.exit(1)


async def update_command():
    try:
        installer = BinaryInstaller()
        current_version = installer._get_installed_version()
        await installer.update()
        new_version = installer._get_installed_version()

        if current_version == new_version and current_version:
            print(f"\n✓ Already up to date ({current_version})\n")
        else:
            print("\n✓ nexroo-engine updated successfully\n")
    except Exception as e:
        print(f"\n✗ Update failed: {e}\n")
        sys.exit(1)


def uninstall_command(args):
    try:
        from pathlib import Path
        import shutil

        installer = BinaryInstaller()
        nexroo_dir = Path.home() / ".nexroo"

        if not nexroo_dir.exists() and not installer.is_installed():
            print("\n✓ Nothing to uninstall\n")
            return

        print("\nThis will remove:")
        print(f"  - nexroo-engine package")
        print(f"  - All addons")
        print(f"  - Authentication tokens")
        print(f"  - All data in {nexroo_dir}")
        print()

        if not args.yes:
            response = input("Continue? [y/N]: ").strip().lower()
            if response != 'y':
                print("\n✗ Uninstall cancelled\n")
                return

        installer.uninstall()

        if nexroo_dir.exists():
            shutil.rmtree(nexroo_dir)

        print("\n✓ Uninstalled successfully")
        print("\nTo remove the CLI package, run:")
        print("  pip uninstall nexroo-cli\n")

    except Exception as e:
        print(f"\n✗ Uninstall failed: {e}\n")
        sys.exit(1)


async def addon_list_command(args):
    try:
        pkg_manager = PackageManager()

        if args.available:
            packages = pkg_manager.registry.get_packages(refresh=args.refresh)
            if not packages:
                print("\nNo packages found\n")
                return

            print(f"\nAvailable addons ({len(packages)}):\n")
            names = sorted([pkg['name'].replace('-rooms-pkg', '') for pkg in packages])
            for name in names:
                print(f"  {name}")
            print()
        else:
            installed = pkg_manager.list_installed()
            if not installed:
                print("\nNo addons installed\n")
                print("  Run 'nexroo addon list --available' to see available packages")
                print("  Run 'nexroo addon install <name>' to install\n")
                return

            print(f"\nInstalled addons ({len(installed)}):\n")
            for pkg in installed:
                short_name = pkg['name'].replace('-rooms-pkg', '')
                if pkg["location"] == "bundled":
                    print(f"  {short_name} v{pkg['version']} [bundled]")
                else:
                    print(f"  {short_name} v{pkg['version']}")
                if pkg.get("description"):
                    print(f"    {pkg['description']}")
            print()

    except Exception as e:
        print(f"\nFailed to list packages: {e}\n")
        sys.exit(1)


async def addon_search_command(args):
    try:
        pkg_manager = PackageManager()
        results = pkg_manager.registry.search_packages(args.query)

        if not results:
            print(f"\nNo packages found matching '{args.query}'\n")
            return

        print(f"\nSearch results for '{args.query}' ({len(results)}):\n")
        for pkg in results:
            short_name = pkg['name'].replace('-rooms-pkg', '')
            print(f"  {short_name}")
            if pkg.get("description"):
                print(f"    {pkg['description']}")
        print()

    except Exception as e:
        print(f"\nSearch failed: {e}\n")
        sys.exit(1)


async def addon_install_command(args):
    try:
        pkg_manager = PackageManager()
        success = await pkg_manager.install(
            args.package,
            version=args.version,
            url=args.url,
            upgrade=args.upgrade
        )
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\nInstallation failed: {e}\n")
        sys.exit(1)


async def addon_uninstall_command(args):
    try:
        pkg_manager = PackageManager()
        success = await pkg_manager.uninstall(args.package, force=args.yes)
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\nUninstallation failed: {e}\n")
        sys.exit(1)


async def addon_update_command(args):
    try:
        pkg_manager = PackageManager()

        if args.all:
            results = await pkg_manager.update_all()
            successes = sum(1 for v in results.values() if v)
            print(f"\nUpdated {successes}/{len(results)} packages\n")
            sys.exit(0 if successes == len(results) else 1)
        else:
            success = await pkg_manager.update(args.package)
            sys.exit(0 if success else 1)

    except Exception as e:
        print(f"\nUpdate failed: {e}\n")
        sys.exit(1)


def config_command(args):
    try:
        config = Config()

        if args.config_command == 'set':
            config.set(args.key, args.value)
            if args.key == 'github_token':
                print(f"\n✓ GitHub token has been set securely\n")
                print(f"Note: Using {config.GITHUB_TOKEN_ENV_VAR} environment variable is recommended for better security\n")
            else:
                print(f"\n✓ Set {args.key} = {args.value}\n")
        elif args.config_command == 'get':
            if args.key == 'github_token':
                print(f"\n✗ Cannot display github_token for security reasons\n")
                print(f"Token is read from {config.GITHUB_TOKEN_ENV_VAR} env var or config file\n")
                sys.exit(1)
            value = config.get(args.key)
            if value is not None:
                print(f"\n{args.key} = {value}\n")
            else:
                print(f"\n✗ {args.key} not set\n")
                sys.exit(1)
        elif args.config_command == 'delete':
            if config.delete(args.key):
                print(f"\n✓ Deleted {args.key}\n")
            else:
                print(f"\n✗ {args.key} not found\n")
                sys.exit(1)
        elif args.config_command == 'list':
            cfg = config.all()
            if cfg:
                print("\nConfiguration:\n")
                for key, value in cfg.items():
                    if key == 'github_token':
                        print(f"  {key} = [hidden]")
                    else:
                        print(f"  {key} = {value}")
                print()
            else:
                print("\nNo configuration set\n")
        else:
            print("\nUsage: nexroo config <set|get|delete|list> [key] [value]\n")
            sys.exit(1)

    except Exception as e:
        print(f"\nConfig operation failed: {e}\n")
        sys.exit(1)


async def workflow_pull_command(args):
    try:
        workflow_manager = WorkflowManager()
        success = await workflow_manager.pull(args.workflow, args.name, skip_config=args.no_config)
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\nPull failed: {e}\n")
        sys.exit(1)


async def workflow_list_command(args):
    try:
        workflow_manager = WorkflowManager()

        if args.available:
            workflows = await workflow_manager.list_available()
            if not workflows:
                print("\nNo workflows found\n")
                return

            print(f"\nAvailable workflows ({len(workflows)}):\n")
            for name in sorted(workflows):
                print(f"  @nexroo/{name}")
            print()
        else:
            workflows = workflow_manager.list_local()
            if not workflows:
                print("\nNo workflows installed\n")
                print("  Run 'nexroo workflow list --available' to see available workflows")
                print("  Run 'nexroo workflow pull @nexroo/<name>' to install\n")
                return

            print(f"\nInstalled workflows ({len(workflows)}):\n")
            for wf in workflows:
                print(f"  {wf['name']}")
                print(f"    {wf['title']} v{wf['version']}")
            print()

    except Exception as e:
        print(f"\nList failed: {e}\n")
        sys.exit(1)


async def workflow_config_command(args):
    try:
        workflow_manager = WorkflowManager()

        if args.config_action == 'set':
            success = await workflow_manager.config(args.workflow)
        elif args.config_action == 'show':
            success = workflow_manager.show_config(args.workflow)
        else:
            success = await workflow_manager.config(args.workflow)

        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\nConfig failed: {e}\n")
        sys.exit(1)


async def workflow_load_command(args):
    try:
        workflow_manager = WorkflowManager()
        success = await workflow_manager.load(args.file, args.name, skip_config=args.no_config)
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\nLoad failed: {e}\n")
        sys.exit(1)


async def workflow_delete_command(args):
    try:
        workflow_manager = WorkflowManager()
        workflow_id = args.workflow.replace('@nexroo/', '')

        if not args.yes:
            response = input(f"Delete workflow '{workflow_id}'? [y/N]: ").strip().lower()
            if response != 'y':
                print("\n✗ Delete cancelled\n")
                return

        success = workflow_manager.delete(args.workflow)
        if success:
            print(f"\n✓ Workflow '{workflow_id}' deleted\n")
        else:
            print(f"\n✗ Workflow '{workflow_id}' not found\n")
            sys.exit(1)

    except Exception as e:
        print(f"\nDelete failed: {e}\n")
        sys.exit(1)


async def run_command(args):
    is_authenticated = False
    auth_token = None

    await ensure_binary_installed()

    if not args.no_auth:
        try:
            auth_manager = AuthManager()

            if auth_manager.is_authenticated():
                is_valid = await auth_manager.verify_authentication()

                if is_valid:
                    logger.info("✓ Authenticated - SaaS features enabled")
                    is_authenticated = True
                    auth_token = auth_manager.get_token()
                else:
                    logger.warning("⚠ Authentication expired")
                    logger.info("  Run 'nexroo login' to re-authenticate")
                    logger.info("  Continuing without SaaS features...")
            else:
                logger.info("ℹ Not authenticated")
                logger.info("  Run 'nexroo login' to access SaaS features")

        except FileNotFoundError:
            logger.debug("No auth configuration found")
        except Exception as e:
            logger.warning(f"Auth check failed: {e}")

    config = Config()
    engine_path = config.get_engine_path()

    if not engine_path:
        engine_path = shutil.which("nexroo-engine")

    if not engine_path:
        bin_dir = Path(sys.executable).parent
        possible_path = bin_dir / "nexroo-engine"
        if possible_path.exists():
            engine_path = str(possible_path)

    if not engine_path:
        logger.error("nexroo-engine not found")
        print("\nCannot find nexroo-engine binary.")
        print("\nOptions to fix this:")
        print("  1. Add the Python bin directory to your PATH")
        print("  2. Set the engine path manually:")
        print("     nexroo config set engine_path /path/to/nexroo-engine")
        print(f"\nHint: Try looking in {bin_dir}\n")
        sys.exit(1)

    workflow_path = args.workflow
    runtime_workflow_path = None

    if isinstance(args.workflow, str):
        workflow_manager = WorkflowManager()
        resolved_path = workflow_manager.get_workflow_path(args.workflow)
        if resolved_path:
            workflow_path = resolved_path

            resolved_data = workflow_manager.resolve_workflow_for_runtime(workflow_path)
            if resolved_data:
                runtime_fd, runtime_workflow_path = tempfile.mkstemp(suffix='.json', prefix='nexroo_runtime_')
                with os.fdopen(runtime_fd, 'w') as f:
                    json.dump(resolved_data, f, indent=2)
                workflow_path = runtime_workflow_path
        elif not Path(args.workflow).exists():
            workflow_spec = f"@nexroo/{args.workflow}" if not args.workflow.startswith('@nexroo/') else args.workflow
            print(f"\n✗ Workflow '{args.workflow}' not found")
            print(f"  Run 'nexroo workflow pull {workflow_spec}' to install it\n")
            sys.exit(1)

    env = os.environ.copy()
    if is_authenticated and auth_token:
        env['SYNVEX_AUTH_TOKEN'] = auth_token
        env['SYNVEX_SAAS_ENABLED'] = 'true'

    cmd = [engine_path, str(workflow_path)]

    if args.entrypoint:
        cmd.append(args.entrypoint)

    if args.verbose:
        cmd.append('-v')
    if args.mock:
        cmd.append('--mock')
    if args.dry_run:
        cmd.append('--dry-run')
    if args.mock_config:
        cmd.extend(['--mock-config', args.mock_config])
    if args.payload:
        cmd.extend(['--payload', args.payload])
    if args.payload_file:
        cmd.extend(['--payload-file', args.payload_file])

    try:
        result = subprocess.run(cmd, env=env)
        sys.exit(result.returncode)
    except Exception as e:
        logger.error(f"Failed to run workflow: {e}")
        sys.exit(1)
    finally:
        if runtime_workflow_path and os.path.exists(runtime_workflow_path):
            try:
                os.unlink(runtime_workflow_path)
            except:
                pass


def main():
    parser = argparse.ArgumentParser(
        prog='nexroo',
        description='Nexroo CLI - Workflow orchestration with Zitadel authentication',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(
        dest='command',
        title='commands',
        metavar=''
    )

    install_parser = subparsers.add_parser('install', help='Install nexroo-engine')

    subparsers.add_parser('login', help='Authenticate with Zitadel to access SaaS features')
    subparsers.add_parser('logout', help='Clear saved authentication credentials')
    subparsers.add_parser('status', help='Show authentication status')
    subparsers.add_parser('update', help='Update nexroo-engine to latest version')

    uninstall_parser = subparsers.add_parser('uninstall', help='Uninstall nexroo-engine, addons, and all data')
    uninstall_parser.add_argument('-y', '--yes', action='store_true', help='Skip confirmation')

    addon_parser = subparsers.add_parser('addon', help='Manage addon packages')
    addon_subparsers = addon_parser.add_subparsers(
        dest='addon_command',
        title='addon commands',
        metavar=''
    )

    addon_list_parser = addon_subparsers.add_parser('list', help='List installed or available addons')
    addon_list_parser.add_argument('--available', action='store_true', help='List available packages')
    addon_list_parser.add_argument('--refresh', action='store_true', help='Refresh package cache')

    addon_search_parser = addon_subparsers.add_parser('search', help='Search for addon packages')
    addon_search_parser.add_argument('query', help='Search query')

    addon_install_parser = addon_subparsers.add_parser('install', help='Install an addon package')
    addon_install_parser.add_argument('package', help='Package name')
    addon_install_parser.add_argument('--version', help='Specific version to install')
    addon_install_parser.add_argument('--url', help='Custom URL to install from')
    addon_install_parser.add_argument('--upgrade', action='store_true', help='Upgrade if already installed')

    addon_uninstall_parser = addon_subparsers.add_parser('uninstall', help='Uninstall an addon package')
    addon_uninstall_parser.add_argument('package', help='Package name')
    addon_uninstall_parser.add_argument('-y', '--yes', action='store_true', help='Skip confirmation')

    addon_update_parser = addon_subparsers.add_parser('update', help='Update addon package(s)')
    addon_update_parser.add_argument('package', nargs='?', help='Package name (optional)')
    addon_update_parser.add_argument('--all', action='store_true', help='Update all packages')

    config_parser = subparsers.add_parser('config', help='Manage CLI configuration')
    config_subparsers = config_parser.add_subparsers(
        dest='config_command',
        title='config commands',
        metavar=''
    )

    config_set_parser = config_subparsers.add_parser('set', help='Set a configuration value')
    config_set_parser.add_argument('key', help='Configuration key')
    config_set_parser.add_argument('value', help='Configuration value')

    config_get_parser = config_subparsers.add_parser('get', help='Get a configuration value')
    config_get_parser.add_argument('key', help='Configuration key')

    config_delete_parser = config_subparsers.add_parser('delete', help='Delete a configuration value')
    config_delete_parser.add_argument('key', help='Configuration key')

    config_subparsers.add_parser('list', help='List all configuration')

    workflow_parser = subparsers.add_parser('workflow', help='Manage workflows from GitHub repositories')
    workflow_subparsers = workflow_parser.add_subparsers(
        dest='workflow_command',
        title='workflow commands',
        metavar=''
    )

    workflow_pull_parser = workflow_subparsers.add_parser('pull', help='Pull a workflow from a GitHub repository')
    workflow_pull_parser.add_argument('workflow', help='Workflow spec: @nexroo/name, @owner/repo:name, or @owner/repo/branch:name')
    workflow_pull_parser.add_argument('name', nargs='?', help='Custom name for the workflow (optional)')
    workflow_pull_parser.add_argument('--no-config', action='store_true', help='Skip configuration setup')

    workflow_list_parser = workflow_subparsers.add_parser('list', help='List installed or available workflows')
    workflow_list_parser.add_argument('--available', action='store_true', help='List available workflows from repository')

    workflow_config_parser = workflow_subparsers.add_parser('config', help='Configure or show workflow configuration')
    workflow_config_parser.add_argument('workflow', help='Workflow name (e.g., basic-rag-api)')
    workflow_config_parser.add_argument('config_action', nargs='?', default='set', choices=['set', 'show'], help='Action: set (configure) or show (display config)')

    workflow_load_parser = workflow_subparsers.add_parser('load', help='Load a workflow from a local file')
    workflow_load_parser.add_argument('file', help='Path to workflow JSON file')
    workflow_load_parser.add_argument('name', nargs='?', help='Custom name for the workflow (optional)')
    workflow_load_parser.add_argument('--no-config', action='store_true', help='Skip configuration setup')

    workflow_delete_parser = workflow_subparsers.add_parser('delete', help='Delete an installed workflow')
    workflow_delete_parser.add_argument('workflow', help='Workflow name (e.g., basic-rag-api)')
    workflow_delete_parser.add_argument('-y', '--yes', action='store_true', help='Skip confirmation')

    run_parser = subparsers.add_parser('run', help='Run a workflow')
    run_parser.add_argument('workflow', help='Workflow name or path to JSON file (e.g., basic-rag-api or ./workflow.json)')
    run_parser.add_argument('entrypoint', nargs='?', help='Entrypoint ID (optional)')
    run_parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose logging')
    run_parser.add_argument('--mock', action='store_true', help='Run in mock mode')
    run_parser.add_argument('--dry-run', action='store_true', help='Run in dry-run mode')
    run_parser.add_argument('--mock-config', help='Path to mock configuration file')
    run_parser.add_argument('--payload', help='JSON payload string')
    run_parser.add_argument('--payload-file', help='Path to JSON payload file')
    run_parser.add_argument('--no-auth', action='store_true', help='Skip authentication (no SaaS features)')

    args = parser.parse_args()

    setup_logging(verbose=getattr(args, 'verbose', False))

    if args.command == 'install':
        asyncio.run(install_command(args))
    elif args.command == 'login':
        asyncio.run(login_command())
    elif args.command == 'logout':
        asyncio.run(logout_command())
    elif args.command == 'status':
        asyncio.run(status_command())
    elif args.command == 'update':
        asyncio.run(update_command())
    elif args.command == 'uninstall':
        uninstall_command(args)
    elif args.command == 'addon':
        if args.addon_command == 'list':
            asyncio.run(addon_list_command(args))
        elif args.addon_command == 'search':
            asyncio.run(addon_search_command(args))
        elif args.addon_command == 'install':
            asyncio.run(addon_install_command(args))
        elif args.addon_command == 'uninstall':
            asyncio.run(addon_uninstall_command(args))
        elif args.addon_command == 'update':
            asyncio.run(addon_update_command(args))
        else:
            addon_parser.print_help()
            sys.exit(1)
    elif args.command == 'config':
        config_command(args)
    elif args.command == 'workflow':
        if args.workflow_command == 'pull':
            asyncio.run(workflow_pull_command(args))
        elif args.workflow_command == 'list':
            asyncio.run(workflow_list_command(args))
        elif args.workflow_command == 'config':
            asyncio.run(workflow_config_command(args))
        elif args.workflow_command == 'load':
            asyncio.run(workflow_load_command(args))
        elif args.workflow_command == 'delete':
            asyncio.run(workflow_delete_command(args))
        else:
            workflow_parser.print_help()
            sys.exit(1)
    elif args.command == 'run':
        asyncio.run(run_command(args))
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
