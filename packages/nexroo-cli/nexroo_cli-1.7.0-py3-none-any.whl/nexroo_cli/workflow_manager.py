import json
import re
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple
import aiohttp
from loguru import logger
from .config import Config


class WorkflowManager:
    WORKFLOW_DIR = Path.home() / ".nexroo" / "workflows"
    DEFAULT_REPO = "nexroo-ai/workflow-example"
    DEFAULT_BRANCH = "main"

    def __init__(self):
        self.WORKFLOW_DIR.mkdir(parents=True, exist_ok=True)
        self.config = Config()

    def _parse_workflow_spec(self, workflow_spec: str) -> tuple[str, str, str, str]:
        if workflow_spec.startswith('@'):
            workflow_spec = workflow_spec[1:]

            if ':' in workflow_spec:
                repo_part, workflow_name = workflow_spec.split(':', 1)
            else:
                repo_part = workflow_spec
                workflow_name = None

            if '/' in repo_part:
                parts = repo_part.split('/')
                if len(parts) == 2:
                    owner, repo = parts
                    branch = self.DEFAULT_BRANCH
                else:
                    owner = parts[0]
                    repo = parts[1]
                    branch = '/'.join(parts[2:]) if len(parts) > 2 else self.DEFAULT_BRANCH
            else:
                owner = "nexroo-ai"
                repo = "workflow-example"
                branch = self.DEFAULT_BRANCH
                workflow_name = repo_part

            if workflow_name is None:
                workflow_name = repo

            return owner, repo, branch, workflow_name
        else:
            return "nexroo-ai", "demo-workflows", self.DEFAULT_BRANCH, workflow_spec

    def _get_workflow_path(self, name: str) -> Path:
        safe_name = re.sub(r'[^\w\-.]', '_', name)
        return self.WORKFLOW_DIR / f"{safe_name}.json"

    def _get_workflow_config_path(self, name: str) -> Path:
        safe_name = re.sub(r'[^\w\-.]', '_', name)
        return self.WORKFLOW_DIR / f"{safe_name}.config.json"

    def _get_auth_headers(self) -> Dict[str, str]:
        headers = {}
        token = self.config.get_github_token()
        if token:
            headers['Authorization'] = f'token {token}'
        return headers

    async def _check_repo_access(self, owner: str, repo: str) -> tuple[bool, int]:
        api_url = f"https://api.github.com/repos/{owner}/{repo}"
        headers = self._get_auth_headers()

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url, headers=headers) as response:
                    return response.status == 200, response.status
        except Exception:
            return False, 0

    async def _fetch_workflow_from_github(self, owner: str, repo: str, branch: str, workflow_name: str) -> Optional[Dict[str, Any]]:
        url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{workflow_name}.json"
        headers = self._get_auth_headers()
        has_token = bool(self.config.get_github_token())

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        text = await response.text()
                        try:
                            return json.loads(text)
                        except json.JSONDecodeError as e:
                            print(f"\n✗ Invalid JSON in workflow file: {e}")
                            print(f"The workflow file may be corrupted or not valid JSON\n")
                            return None
                    elif response.status == 404:
                        repo_accessible, repo_status = await self._check_repo_access(owner, repo)

                        if not repo_accessible and repo_status == 404:
                            if not has_token:
                                print(f"\n✗ Repository '{owner}/{repo}' not found or is private.\n")
                                print("If this is a private repository, set your GitHub Personal Access Token:")
                                print(f"  Option 1 (Recommended): export {self.config.GITHUB_TOKEN_ENV_VAR}=YOUR_TOKEN")
                                print(f"  Option 2: nexroo config set github_token YOUR_TOKEN")
                                print(f"\nCreate a token at: https://github.com/settings/tokens")
                                print(f"Required scopes: 'repo' (for private repos) or 'public_repo' (for public repos)\n")
                            else:
                                print(f"\n✗ Repository '{owner}/{repo}' not found or you don't have access.\n")
                                print("Possible reasons:")
                                print(f"  - Repository doesn't exist")
                                print(f"  - Your token doesn't have access to this repository")
                                print(f"  - Token has expired or been revoked\n")
                        else:
                            print(f"\n✗ Workflow '{workflow_name}.json' not found in {owner}/{repo} (branch: {branch})")
                            print(f"\nPossible reasons:")
                            print(f"  - Workflow file doesn't exist at the root of the repository")
                            print(f"  - Branch name is incorrect")
                            print(f"  - File name is misspelled\n")
                            print(f"List available workflows from this repository:")
                            print(f"  nexroo workflow list --available\n")

                        print(f"Browse public Nexroo examples:")
                        print(f"  https://github.com/nexroo-ai/workflow-example\n")
                        return None
                    elif response.status == 401 or response.status == 403:
                        print(f"\n✗ Authentication failed. Repository may be private.\n")
                        print("To access private repositories, set your GitHub Personal Access Token:")
                        print(f"  Option 1 (Recommended): export {self.config.GITHUB_TOKEN_ENV_VAR}=YOUR_TOKEN")
                        print(f"  Option 2: nexroo config set github_token YOUR_TOKEN")
                        print(f"\nCreate a token at: https://github.com/settings/tokens")
                        print(f"Required scopes: 'repo' (for private repos) or 'public_repo' (for public repos)\n")
                        return None
                    else:
                        print(f"\n✗ Failed to fetch workflow: HTTP {response.status}")
                        print(f"Repository: https://github.com/{owner}/{repo}\n")
                        return None
        except aiohttp.ClientError as e:
            print(f"\n✗ Network error: {e}")
            print(f"Check your internet connection or repository URL\n")
            return None
        except Exception as e:
            print(f"\n✗ Unexpected error: {e}\n")
            return None

    async def _list_available_workflows(self, owner: str = None, repo: str = None) -> List[str]:
        if not owner:
            owner = "nexroo-ai"
        if not repo:
            repo = "workflow-example"

        api_url = f"https://api.github.com/repos/{owner}/{repo}/contents"
        headers = self._get_auth_headers()

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url, headers=headers) as response:
                    if response.status == 200:
                        files = await response.json()
                        workflows = [
                            f['name'][:-5]
                            for f in files
                            if f['type'] == 'file' and f['name'].endswith('.json')
                        ]
                        return workflows
                    else:
                        logger.error(f"Failed to list workflows: HTTP {response.status}")
                        print(f"Browse workflows at: https://github.com/{owner}/{repo}")
                        return []
        except Exception as e:
            logger.error(f"Error listing workflows: {e}")
            print(f"Browse workflows at: https://github.com/{owner}/{repo}")
            return []

    async def pull(self, workflow_spec: str, custom_name: Optional[str] = None, skip_config: bool = False) -> bool:
        owner, repo, branch, workflow_name = self._parse_workflow_spec(workflow_spec)

        print(f"\nPulling workflow '{workflow_name}' from {owner}/{repo}...")
        print(f"Repository: https://github.com/{owner}/{repo} (branch: {branch})\n")

        workflow_data = await self._fetch_workflow_from_github(owner, repo, branch, workflow_name)

        if not workflow_data:
            return False

        save_name = custom_name if custom_name else workflow_name
        workflow_path = self._get_workflow_path(save_name)

        if workflow_path.exists():
            response = input(f"\nWorkflow '{save_name}' already exists. Overwrite? (y/n): ").strip().lower()
            if response not in ['y', 'yes']:
                print(f"\nPull cancelled")
                print(f"You can pull with a different name using:")
                print(f"  nexroo workflow pull {workflow_spec} <custom-name>\n")
                return False
            print()

        try:
            workflow_path.write_text(json.dumps(workflow_data, indent=2))
            print(f"✓ Workflow saved as '{save_name}'")

            if not skip_config:
                await self._run_setup(save_name, workflow_data)

            print(f"\nWorkflow ready! Run it with:")
            print(f"  nexroo run {save_name}")
            if skip_config:
                print(f"\nTo configure this workflow later, run:")
                print(f"  nexroo workflow config {save_name}")
            print()

            return True

        except Exception as e:
            logger.error(f"Failed to save workflow: {e}")
            print(f"\n✗ Failed to save workflow: {e}\n")
            return False

    def _is_template_field(self, obj: Any) -> bool:
        if not isinstance(obj, dict):
            return False
        return '__type' in obj

    def _is_secret_path(self, path: str) -> bool:
        """Check if a path is in the secrets section of addon config."""
        return '.secrets.' in path or path.startswith('addons') and 'secrets' in path.split('.')

    def _find_template_fields(self, obj: Any, path: str = "") -> List[Dict[str, Any]]:
        """Recursively find all template fields in a workflow structure."""
        templates = []

        if isinstance(obj, dict):
            if self._is_template_field(obj):
                is_secret = obj.get('__secret', False) or self._is_secret_path(path)
                templates.append({
                    'path': path,
                    'type': obj.get('__type'),
                    'description': obj.get('__description', 'No description provided'),
                    'required': obj.get('__required', True),
                    'default': obj.get('__default'),
                    'is_secret': is_secret
                })
            else:
                for key, value in obj.items():
                    new_path = f"{path}.{key}" if path else key
                    templates.extend(self._find_template_fields(value, new_path))
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                new_path = f"{path}[{i}]"
                templates.extend(self._find_template_fields(item, new_path))

        return templates

    def _set_nested_value(self, obj: Dict[str, Any], path: str, value: Any) -> None:
        """Set a value in a nested dictionary using a path string."""
        keys = re.findall(r'[^\.\[\]]+', path)
        current = obj

        for i, key in enumerate(keys[:-1]):
            if key.isdigit():
                key = int(key)
                current = current[key]
            else:
                if key not in current:
                    current[key] = {}
                current = current[key]

        final_key = keys[-1]
        if final_key.isdigit():
            current[int(final_key)] = value
        else:
            current[final_key] = value

    def _convert_value(self, value_str: str, expected_type: str) -> Any:
        """Convert string input to the expected type."""
        if expected_type == "number":
            try:
                if '.' in value_str:
                    return float(value_str)
                return int(value_str)
            except ValueError:
                raise ValueError(f"Invalid number: {value_str}")
        elif expected_type == "boolean":
            return value_str.lower() in ('true', 'yes', '1', 'y')
        elif expected_type == "object":
            try:
                return json.loads(value_str)
            except json.JSONDecodeError:
                raise ValueError(f"Invalid JSON object: {value_str}")
        elif expected_type == "array":
            try:
                return json.loads(value_str)
            except json.JSONDecodeError:
                raise ValueError(f"Invalid JSON array: {value_str}")
        else:
            return value_str

    def _suggest_env_var_name(self, path: str, description: str) -> str:
        parts = re.findall(r'[^\.\[\]]+', path)

        meaningful_parts = []
        for part in parts:
            if not part.isdigit() and part not in ['addons', 'secrets', 'config', 'workflow', 'steps', 'parameters']:
                meaningful_parts.append(part)

        if meaningful_parts:
            suggestion = '_'.join(meaningful_parts).upper()
        else:
            desc_words = re.findall(r'\w+', description.lower())
            suggestion = '_'.join(desc_words[:3]).upper() if desc_words else 'SECRET_VALUE'

        return suggestion

    async def _configure_template_fields(self, workflow_data: Dict[str, Any], name: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        templates = self._find_template_fields(workflow_data)

        if not templates:
            return workflow_data, {}

        secret_templates = [t for t in templates if t['is_secret']]
        regular_templates = [t for t in templates if not t['is_secret']]

        print(f"Found {len(templates)} template field(s) to configure:")
        if secret_templates:
            print(f"  - {len(secret_templates)} secret field(s)")
        if regular_templates:
            print(f"  - {len(regular_templates)} regular field(s)")
        print()

        setup_config = {
            'version': '1.0',
            'workflow_name': name,
            'templates': {}
        }

        configured_data = json.loads(json.dumps(workflow_data))

        if secret_templates:
            print(f"{'='*60}")
            print(f"STEP 1: Configure Secret Fields")
            print(f"{'='*60}\n")
            print("Secret fields will be stored as environment variable references.")
            print("You'll need to set these environment variables before running the workflow.\n")

            for template in secret_templates:
                path = template['path']
                field_type = template['type']
                description = template['description']
                required = template['required']

                suggested_env_var = self._suggest_env_var_name(path, description)

                print(f"Secret Field: {path}")
                print(f"  Type: {field_type}")
                print(f"  Description: {description}")
                print(f"  Required: {'Yes' if required else 'No'}")

                while True:
                    env_var_name = input(f"  Environment variable name [{suggested_env_var}]: ").strip()

                    if not env_var_name:
                        env_var_name = suggested_env_var

                    if not re.match(r'^[A-Z][A-Z0-9_]*$', env_var_name):
                        print("  ✗ Invalid format. Use uppercase letters, numbers, and underscores (e.g., MY_API_KEY)")
                        continue

                    break

                self._set_nested_value(configured_data, path, env_var_name)

                setup_config['templates'][path] = {
                    'type': 'secret',
                    'env_var': env_var_name,
                    'description': description,
                    'field_type': field_type,
                    'required': required
                }

                print(f"  ✓ Will use environment variable: {env_var_name}")
                print(f"  Set it with: export {env_var_name}=your_secret_value\n")

        if regular_templates:
            print(f"{'='*60}")
            print(f"STEP 2: Configure Regular Fields")
            print(f"{'='*60}\n")

            for template in regular_templates:
                path = template['path']
                field_type = template['type']
                description = template['description']
                required = template['required']
                default = template.get('default')

                print(f"Field: {path}")
                print(f"  Type: {field_type}")
                print(f"  Description: {description}")

                if not required:
                    if default is not None:
                        print(f"  Optional (default: {default})")
                    else:
                        print(f"  Optional (no default)")

                while True:
                    if not required and default is not None:
                        prompt = f"  Value [press Enter to use default: {default}]: "
                    elif not required:
                        prompt = f"  Value [press Enter to skip]: "
                    else:
                        prompt = f"  Value: "

                    value_str = input(prompt).strip()

                    if not value_str:
                        if not required:
                            if default is not None:
                                print(f"  ✓ Will use default value (handled by engine)\n")
                            else:
                                print(f"  ✓ Skipped (field will be omitted)\n")
                            break
                        else:
                            print("  ✗ This field is required. Please provide a value.")
                            continue

                    try:
                        value = self._convert_value(value_str, field_type)
                        self._set_nested_value(configured_data, path, value)

                        setup_config['templates'][path] = {
                            'type': 'regular',
                            'value': value,
                            'description': description,
                            'field_type': field_type
                        }

                        print(f"  ✓ Set to: {value}\n")
                        break
                    except ValueError as e:
                        print(f"  ✗ {e}. Please try again.")

        return configured_data, setup_config

    def _display_entrypoints_info(self, workflow_data: Dict[str, Any]) -> None:
        """Display information about entrypoints and their expected content."""
        entrypoints = workflow_data.get('entrypoints', [])

        if not entrypoints:
            return

        print(f"\n{'='*60}")
        print("Entrypoint Information")
        print(f"{'='*60}\n")

        for entrypoint in entrypoints:
            ep_id = entrypoint.get('id', 'unknown')
            ep_name = entrypoint.get('name', ep_id)
            expected_content = entrypoint.get('expectedContent', [])

            print(f"Entrypoint: {ep_name} (id: {ep_id})")

            if expected_content:
                print(f"  Expected payload content fields ({len(expected_content)}):")
                for field in expected_content:
                    field_name = field.get('name', 'unknown')
                    field_type = field.get('type', 'any')
                    field_desc = field.get('description', '')

                    if field_desc:
                        print(f"    • {field_name} ({field_type}) - {field_desc}")
                    else:
                        print(f"    • {field_name} ({field_type})")

                print(f"\n  Example payload structure:")
                example_payload = {
                    "type": "application/json",
                    "content": {}
                }
                for field in expected_content:
                    field_name = field.get('name', 'unknown')
                    field_type = field.get('type', 'any')

                    if field_type == "string":
                        example_payload["content"][field_name] = "example_value"
                    elif field_type == "number":
                        example_payload["content"][field_name] = 0
                    elif field_type == "boolean":
                        example_payload["content"][field_name] = True
                    elif field_type == "object":
                        example_payload["content"][field_name] = {}
                    elif field_type == "array":
                        example_payload["content"][field_name] = []
                    else:
                        example_payload["content"][field_name] = None

                print(f"  {json.dumps(example_payload, indent=4)}")
            else:
                print("  No payload expected (or not documented)")

            print()

    async def _run_setup(self, name: str, workflow_data: Dict[str, Any]):
        workflow_info = workflow_data.get('workflow', {})
        workflow_name = workflow_info.get('name', name)

        print(f"\n{'='*60}")
        print(f"Setup: {workflow_name}")
        print(f"{'='*60}\n")

        templates = self._find_template_fields(workflow_data)

        if templates:
            print(f"This workflow has {len(templates)} configurable parameter(s).")
            print("Let's configure them now:\n")

            configured_data, setup_config = await self._configure_template_fields(workflow_data, name)

            config_path = self._get_workflow_config_path(name)
            config_path.write_text(json.dumps(setup_config, indent=2))

            print(f"\n{'='*60}")
            print(f"✓ Configuration Complete")
            print(f"{'='*60}\n")
            print(f"Setup configuration saved to: {config_path.name}")
        else:
            print("No template fields to configure.")

        self._display_entrypoints_info(workflow_data)

        print(f"You can reconfigure this workflow anytime with:")
        print(f"  nexroo workflow config {name}\n")

    async def config(self, workflow_spec: str) -> bool:
        _, _, _, workflow_name = self._parse_workflow_spec(workflow_spec)
        workflow_path = self._get_workflow_path(workflow_name)

        if not workflow_path.exists():
            print(f"\n✗ Workflow '{workflow_name}' not found")
            print(f"  Run 'nexroo workflow pull @nexroo/{workflow_name}' first\n")
            return False

        try:
            workflow_data = json.loads(workflow_path.read_text())
            await self._run_setup(workflow_name, workflow_data)
            return True
        except Exception as e:
            logger.error(f"Failed to configure workflow: {e}")
            print(f"\n✗ Failed to configure workflow: {e}\n")
            return False

    def get_workflow_path(self, workflow_spec: str) -> Optional[Path]:
        if workflow_spec.startswith('@'):
            _, _, _, workflow_name = self._parse_workflow_spec(workflow_spec)
            workflow_path = self._get_workflow_path(workflow_name)

            if workflow_path.exists():
                return workflow_path
            else:
                return None
        else:
            workflow_path = self._get_workflow_path(workflow_spec)
            if workflow_path.exists():
                return workflow_path

            path = Path(workflow_spec)
            return path if path.exists() else None

    def list_local(self) -> List[Dict[str, Any]]:
        workflows = []

        for workflow_file in self.WORKFLOW_DIR.glob("*.json"):
            if workflow_file.stem.endswith('.config'):
                continue

            try:
                data = json.loads(workflow_file.read_text())
                workflow_info = data.get('workflow', {})

                workflows.append({
                    'name': workflow_file.stem,
                    'title': workflow_info.get('name', workflow_file.stem),
                    'version': workflow_info.get('version', 'unknown'),
                    'path': str(workflow_file)
                })
            except Exception as e:
                logger.warning(f"Failed to read workflow {workflow_file}: {e}")

        return workflows

    async def list_available(self) -> List[str]:
        return await self._list_available_workflows()

    def delete(self, workflow_spec: str) -> bool:
        _, _, _, workflow_name = self._parse_workflow_spec(workflow_spec)
        workflow_path = self._get_workflow_path(workflow_name)
        config_path = self._get_workflow_config_path(workflow_name)

        if not workflow_path.exists():
            return False

        try:
            workflow_path.unlink()
            if config_path.exists():
                config_path.unlink()
            return True
        except Exception as e:
            logger.error(f"Failed to delete workflow: {e}")
            return False

    def resolve_workflow_for_runtime(self, workflow_path: Path) -> Optional[Dict[str, Any]]:
        try:
            workflow_data = json.loads(workflow_path.read_text())

            workflow_name = workflow_path.stem
            config_path = self._get_workflow_config_path(workflow_name)

            if not config_path.exists():
                return workflow_data

            setup_config = json.loads(config_path.read_text())
            templates = setup_config.get('templates', {})

            if not templates:
                return workflow_data

            resolved_data = json.loads(json.dumps(workflow_data))

            for path, config in templates.items():
                if config['type'] == 'secret':
                    env_var = config['env_var']
                    self._set_nested_value(resolved_data, path, env_var)
                elif config['type'] == 'regular':
                    value = config['value']
                    self._set_nested_value(resolved_data, path, value)

            return resolved_data

        except Exception as e:
            logger.error(f"Failed to resolve workflow: {e}")
            return None

    def show_config(self, workflow_spec: str) -> bool:
        _, _, _, workflow_name = self._parse_workflow_spec(workflow_spec)
        workflow_path = self._get_workflow_path(workflow_name)
        config_path = self._get_workflow_config_path(workflow_name)

        if not workflow_path.exists():
            print(f"\n✗ Workflow '{workflow_name}' not found")
            print(f"  Run 'nexroo workflow pull @nexroo/{workflow_name}' first\n")
            return False

        if not config_path.exists():
            print(f"\n✗ No configuration found for workflow '{workflow_name}'")
            print(f"  Run 'nexroo workflow config {workflow_name}' to configure it\n")
            return False

        try:
            setup_config = json.loads(config_path.read_text())
            templates = setup_config.get('templates', {})

            if not templates:
                print(f"\nWorkflow '{workflow_name}' has no configured template fields\n")
                return True

            workflow_display_name = setup_config.get('workflow_name', workflow_name)
            print(f"\n{'='*60}")
            print(f"Configuration for: {workflow_display_name}")
            print(f"{'='*60}\n")

            secret_fields = {k: v for k, v in templates.items() if v['type'] == 'secret'}
            regular_fields = {k: v for k, v in templates.items() if v['type'] == 'regular'}

            if secret_fields:
                print(f"Secret Fields ({len(secret_fields)}):\n")
                for path, config in secret_fields.items():
                    print(f"  Field: {path}")
                    print(f"    Description: {config['description']}")
                    print(f"    Type: {config['field_type']}")
                    print(f"    Environment Variable: {config['env_var']}")
                    print(f"    Required: {'Yes' if config.get('required', True) else 'No'}")
                    print()

            if regular_fields:
                print(f"Regular Fields ({len(regular_fields)}):\n")
                for path, config in regular_fields.items():
                    print(f"  Field: {path}")
                    print(f"    Description: {config['description']}")
                    print(f"    Type: {config['field_type']}")
                    print(f"    Value: {config['value']}")
                    if config.get('used_default'):
                        print(f"    (using default value)")
                    print()

            print(f"Configuration file: {config_path}\n")
            return True

        except Exception as e:
            logger.error(f"Failed to show config: {e}")
            print(f"\n✗ Failed to read configuration: {e}\n")
            return False

    async def load(self, file_path: str, custom_name: Optional[str] = None, skip_config: bool = False) -> bool:
        source_path = Path(file_path)

        if not source_path.exists():
            print(f"\n✗ File not found: {file_path}\n")
            return False

        if not source_path.suffix == '.json':
            print(f"\n✗ File must be a JSON file: {file_path}\n")
            return False

        try:
            workflow_data = json.loads(source_path.read_text())

            if 'workflow' not in workflow_data:
                print(f"\n✗ Invalid workflow file: missing 'workflow' section\n")
                return False

            workflow_info = workflow_data.get('workflow', {})
            workflow_id = workflow_info.get('id', source_path.stem)

            save_name = custom_name if custom_name else workflow_id
            workflow_path = self._get_workflow_path(save_name)

            if workflow_path.exists():
                print(f"\n✗ Workflow '{save_name}' already exists")
                print(f"  Delete it first with: nexroo workflow delete {save_name}\n")
                return False

            workflow_path.write_text(json.dumps(workflow_data, indent=2))
            print(f"\n✓ Workflow loaded as '{save_name}'")
            print(f"  Source: {file_path}")

            if not skip_config:
                await self._run_setup(save_name, workflow_data)

            print(f"\nWorkflow ready! Run it with:")
            print(f"  nexroo run {save_name}")
            if skip_config:
                print(f"\nTo configure this workflow later, run:")
                print(f"  nexroo workflow config {save_name}")
            print()

            return True

        except json.JSONDecodeError as e:
            print(f"\n✗ Invalid JSON file: {e}\n")
            return False
        except Exception as e:
            logger.error(f"Failed to load workflow: {e}")
            print(f"\n✗ Failed to load workflow: {e}\n")
            return False
