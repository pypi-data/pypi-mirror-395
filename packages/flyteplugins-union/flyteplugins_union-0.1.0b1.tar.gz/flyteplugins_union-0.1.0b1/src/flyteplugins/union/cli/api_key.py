import rich_click as click
from flyte.cli._common import initialize_config

from flyteplugins.union.remote import ApiKey


@click.command("api-key")
@click.option("--name", type=str, help="Name for API key", required=True)
@click.pass_context
def create_api_key(ctx: click.Context, name: str):
    """
    Create an API key for headless authentication.

    This creates OAuth application credentials that can be used to authenticate
    with Union without interactive login. The generated API key should be set
    as the FLYTE_API_KEY environment variable. Oauth applications should not be
    confused with Union Apps, which are a different construct entirely.

    Examples:

        # Create an API key named "ci-pipeline"
        $ flyte create api-key --name ci-pipeline

        # The output will include an export command like:
        # export FLYTE_API_KEY="<base64-encoded-credentials>"
    """
    # Api keys (aka oauth apps) are not scoped to project/domain.
    initialize_config(ctx, "", "")

    try:
        api_key = ApiKey.create(name=name)

        click.echo(f"Client ID: {api_key.client_id}")
        click.echo("The following API key will only be shown once. Be sure to keep it safe!")
        click.echo("Configure your headless CLI by setting the following environment variable:")
        click.echo()
        click.echo(f'export FLYTE_API_KEY="{api_key.encoded_credentials}"')

    except Exception as e:
        raise click.ClickException(f"Unable to create api-key with name: {name}\n{e}") from e


@click.command("api-key")
@click.argument("client-id", type=str, required=False)
@click.option("--limit", type=int, default=100, help="Maximum number of keys to list")
@click.pass_context
def get_api_key(ctx, client_id: str | None, limit: int):
    """
    Get or list API keys.

    If CLIENT-ID is provided, gets a specific API key.
    Otherwise, lists all API keys.

    Examples:

        # List all API keys
        $ flyte get api-key

        # List with a limit
        $ flyte get api-key --limit 10

        # Get a specific API key
        $ flyte get api-key my-client-id
    """
    initialize_config(ctx, "", "")

    try:
        if client_id:
            # Get specific key
            key = ApiKey.get(client_id=client_id)
            click.echo(f"Client ID: {key.client_id}")
            click.echo(f"Name: {key.client_name}")
            if key.organization:
                click.echo(f"Organization: {key.organization}")
        else:
            # List all keys
            keys = list(ApiKey.listall(limit=limit))
            if not keys:
                click.echo("No API keys found.")
                return

            click.echo(f"Found {len(keys)} API key(s):")
            click.echo()
            for key in keys:
                click.echo(f"  • {key.client_id}")
                click.echo(f"    Name: {key.client_name}")
                if key.organization:
                    click.echo(f"    Organization: {key.organization}")
                click.echo()

    except Exception as e:
        raise click.ClickException(f"Unable to get api-key(s): {e}") from e


@click.command("api-key")
@click.argument("client-id", type=str)
@click.option("--yes", is_flag=True, help="Skip confirmation prompt")
@click.pass_context
def delete_api_key(ctx, client_id: str, yes: bool):
    """
    Delete an API key.

    Examples:

        # Delete an API key (with confirmation)
        $ flyte delete api-key my-client-id

        # Delete without confirmation
        $ flyte delete api-key my-client-id --yes
    """
    initialize_config(ctx, "", "")

    if not yes:
        click.confirm(f"Are you sure you want to delete API key '{client_id}'?", abort=True)

    try:
        ApiKey.delete(client_id=client_id)
        click.echo(f"Successfully deleted API key: {client_id}")

    except Exception as e:
        raise click.ClickException(f"Unable to delete api-key: {e}") from e
