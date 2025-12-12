# Union Flyte Plugin

Proprietary extensions and features for Flyte, providing Union-specific functionality.

## Installation

```bash
uv pip install flyteplugins-union
```

For development:
```bash
uv pip install -e .
```

## Features

### API Key Management

Create and manage API keys for headless authentication with Union.

### Create an API Key

```bash
flyte create api-key admin --name my-api-key
```

This will create OAuth application credentials and output an API key that can be used for headless authentication.

Example output:
```
Client ID: serverless-1-myorg-my-api-key
The following API key will only be shown once. Be sure to keep it safe!
Configure your headless CLI by setting the following environment variable:

export FLYTE_API_KEY="<base64-encoded-credentials>"
```

### Using the API Key

Set the generated API key as an environment variable:

```bash
export FLYTE_API_KEY="<your-api-key>"
```

Then use the Flyte CLI as normal - it will authenticate using the API key instead of prompting for interactive login.

## Architecture

The Union SDK is structured as follows:

- `flyteplugins/union/internal/` - Proprietary protobuf definitions and generated code
- `flyteplugins/union/cli/` - CLI command plugins that extend the Flyte CLI
- `flyteplugins/union/utils/` - Shared utility functions
- `flyteplugins/union/remote/` - Union-specific remote objects

### Plugin System

The SDK registers CLI plugins via entry points in `pyproject.toml`:

```toml
[project.entry-points."flyte.plugins.cli.commands"]
"create.api-key" = "flyteplugins.union.cli.api_key:create_api_key"
"delete.api-key" = "flyteplugins.union.cli.api_key:delete_api_key"
"get.api-key" = "flyteplugins.union.cli.api_key:get_api_key"
```

This makes Union commands available seamlessly through the Flyte CLI.

## Dependencies

- flyte>=2.0.0b26 - The Flyte SDK v2
- rich-click>=1.8.0 - For CLI formatting

## Development

To add a new CLI plugin:

1. Create a new file in `src/flyteplugins/union/cli/`
2. Define your click commands
3. Register the entry point in `pyproject.toml`
4. Shared resources (protobufs, utilities) are available in `flyteplugins.union.internal.*` and `flyteplugins.union.utils.*`

## Iterating
Commands to rebuild and reinstall this plugin (into the flyte-sdk venv presumably).
From this folder:
```bash
python -m build --wheel
```

From your flyte-sdk venv:
```bash
uv pip install --prerelease=allow --force-reinstall --no-deps --no-index --find-links /Users/ytong/go/src/github.com/unionai/flyteplugins-union/dist flyteplugins-union
```