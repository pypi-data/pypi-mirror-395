# Wrapper around tenant commands for backward compatibility in docs. (shall be removed later after deprecation period)

import click

from day2_cli.commands.tenant import tenant as full_tenant


# Create a new Click group that includes only certain commands
@click.group(name="tenant", help="Tenant commands")
def tenant() -> None:
    """Docs-only CLI for tenant commands"""


# Add only selected subcommands
tenant.add_command(full_tenant.commands["create"])
tenant.add_command(full_tenant.commands["list"])
tenant.add_command(full_tenant.commands["get"])
tenant.add_command(full_tenant.commands["list-categories"])
