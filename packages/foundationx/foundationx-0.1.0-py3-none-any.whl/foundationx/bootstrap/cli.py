"""FoundationX Bootstrap CLI."""
import click


@click.group()
@click.version_option()
def main():
    """FoundationX Bootstrap CLI."""
    pass


if __name__ == "__main__":
    main()
