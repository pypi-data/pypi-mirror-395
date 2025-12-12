# Nexroo CLI

A command-line interface for running Nexroo Engine anywhere and interacting with the Nexroo SaaS automation platform.

> **CLI & Engine Documentation:** [docs.nexroo.ai](https://docs.nexroo.ai)

> **Website**: [nexroo.ai](https://nexroo.ai/)
---

Automate your processes, deploy micro-SaaS products, and scale seamless.

Nexroo platform is divided in four components, the engine and CLI, the SaaS platform, the micro-saas package and the addons.

Engine, CLI and micro-saas renderer are all free to use, all can be easily managed from our SaaS to edit with no-code editor, versionning, environments, and push multiples workflows to the deployed engine or micro-saas you are managing for your clients. 

Engine Addons are open source, all viewable in nexroo-ai github repository.

## Screenshots

### Nexro Engine standalone usage
Standalone engine to run in any environment, most lightweight
![Nexroo Engine CLI screenshot](./assets/demo_cli.png)

### Micro-SaaS usage
Render and deploy micro-SaaS on-premise for your clients
![Micro-SaaS screenshot](./assets/demo_user.png)

### SaaS usage
Manage and publish client-ready revisions (no-code)
![SaaS screenshot](./assets/demo_editor.png)

### Deploy only what your client really need, manage all from one place
![Escalidraw Nexroo Components](./assets/nexroo_components_escalidraw.png)


---

## Prerequisites

**Python 3.11+** is required for addon packages to work. The engine itself is a standalone binary, but addons are installed to your system Python.

- **Windows:** [Download Python](https://www.python.org/downloads/)
- **Linux:** `apt install python3` or `yum install python3`
- **macOS:** `brew install python3`

## Installation

### Quick Install (Recommended)

```bash
# install CLI
pip install nexroo-cli
# use CLI to install engine
nexroo install
```

or

**Linux/macOS:**
```bash
curl -fsSL https://raw.githubusercontent.com/nexroo-ai/nexroo-cli/main/install.sh | bash
```

**Windows (PowerShell):**
```powershell
irm https://raw.githubusercontent.com/nexroo-ai/nexroo-cli/main/install.ps1 | iex
```


## Quick Start

After installation, authenticate and run your first workflow:

(optionnal, for SaaS features like pulling/pushing workflows revisions)
```bash
# Authenticate with Nexroo
nexroo login
```

# Run a workflow
```bash
nexroo run workflow.json
```

## Usage

### Authentication Commands

#### Login
```bash
nexroo login
```

Opens browser for Zitadel authentication.

#### Logout
```bash
nexroo logout
```

Clears saved credentials.

#### Status
```bash
nexroo status
```

Shows authentication status and token expiration.

### Workflow Management

#### Pull Workflow from Repository

```bash
# Pull from default Nexroo repository
nexroo workflow pull @nexroo/workflow-name

# Pull from custom repository
nexroo workflow pull @owner/repo:workflow-name

# Pull with custom name
nexroo workflow pull @nexroo/workflow-name my-custom-name

# Skip configuration during pull
nexroo workflow pull @nexroo/workflow-name --no-config
```

#### Load Local Workflow

```bash
# Load workflow from local file
nexroo workflow load ./my-workflow.json

# Load with custom name
nexroo workflow load ./my-workflow.json my-workflow

# Skip configuration
nexroo workflow load ./my-workflow.json --no-config
```

#### Configure Workflow

```bash
# Configure workflow (interactive guided process)
nexroo workflow config set my-workflow

# Show current configuration
nexroo workflow config show my-workflow
```

#### List Workflows

```bash
# List installed workflows
nexroo workflow list

# List available workflows from repository
nexroo workflow list --available
```

#### Delete Workflow

```bash
nexroo workflow delete my-workflow
```

### Running Workflows

```bash
# Set required environment variables for secrets
export OPENAI_API_KEY=sk-...

# Run installed workflow
nexroo run my-workflow

# Run local workflow file
nexroo run workflow.json [entrypoint]

# Without authentication (local-only mode)
nexroo run workflow.json --no-auth
```

### Additional Options

Refer to [Nexroo Documentation](https://docs.nexroo.ai) for all available options.

### Update

```bash
pip install --upgrade nexroo-cli
nexroo update
```

### Uninstall

```bash
# Uninstall engine, addons, and all data
nexroo uninstall

# Remove the CLI package
pip uninstall nexroo-cli
```

## Addon Packages

### Installing Addons

Addons extend the engine with additional capabilities (AI providers, databases, storage, etc.).

```bash
# Install an addon
nexroo addon install redis

# List available addons
nexroo addon list --available

# List installed addons
nexroo addon list
```

### Troubleshooting Addon Issues

**If the engine can't find an addon:**

1. Verify Python 3.11+ is installed:
   ```bash
   python3 --version
   ```

2. Check addon installation:
   ```bash
   nexroo addon list
   python3 -m pip list | grep rooms-pkg
   ```

3. Reinstall addon:
   ```bash
   nexroo addon install <addon_name> --upgrade
   ```

## Storage Locations

- Engine: Installed via pip to Python's site-packages (available as `nexroo-engine` or `nexroo run`)
- Addon packages: System Python's site-packages
- Workflows: `~/.nexroo/workflows/`
- Workflow configurations: `~/.nexroo/workflows/*.config.json`
- Encrypted tokens: `~/.nexroo/auth_token.enc`
- Encryption key: `~/.nexroo/.key`
- Addon metadata: `~/.nexroo/installed_packages.json`
- Engine version: `~/.nexroo/.engine_version`
- Download cache: `~/.nexroo/cache/`

## Troubleshooting

For debug use '--verbose'

### Authentication fails
```bash
nexroo logout
nexroo login
```

### Token expired
```bash
nexroo status
nexroo login   # Re-authenticate
```

## Documentation

See [Nexroo Engine Documentation](https://docs.nexroo.ai) to know how to use Nexroo workflow engine.

## License

Nexroo Engine Free Use License v1.0 - see [LICENSE](./LICENSE) file for details.

## Support

- GitHub Issues: https://github.com/nexroo-ai/nexroo-cli/issues

## Contact

Adrien EPPLING </br>
mail: adrien.eppling@nexroo.ai </br>
linkedin: https://www.linkedin.com/in/adrien-eppling/

Romain MICHAUX </br>
mail: romain.michaux@nexroo.ai </br>
linkedin: https://www.linkedin.com/in/romain-michaux/