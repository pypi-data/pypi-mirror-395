import click
from portableenv.env_manager import create_env

@click.command()
@click.argument('env_name')
@click.option('-v', '--version', default='3.10.9', help='Python version to use')
def main(env_name, version):
    """Create a virtual environment with the given name using embedded Python."""
    create_env(env_name, version)

if __name__ == "__main__":
    main()