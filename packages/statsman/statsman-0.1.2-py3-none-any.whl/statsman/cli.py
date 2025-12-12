import click
from .app import StatsManApp


@click.command()
@click.option(
    "--refresh-rate",
    "-r",
    default=1.0,
    type=float,
    help="Refresh rate in seconds (default: 1.0)",
)
@click.option(
    "--no-color",
    is_flag=True,
    default=False,
    help="Disable colored output",
)
@click.version_option(version="0.1.0", prog_name="statsman")
def main(refresh_rate: float, no_color: bool) -> None:
    app = StatsManApp(refresh_rate=refresh_rate, no_color=no_color)
    app.run()


if __name__ == "__main__":
    main()