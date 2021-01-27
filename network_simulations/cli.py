"""Console script for network_simulations."""
import sys
import click

from network_simulations.network_simulations import sim


@click.command()
def main(args=None):
    """Console script for network_simulations."""
    sim()


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
