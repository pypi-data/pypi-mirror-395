import click
from .ui.app import StatsManApp


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
@click.option(
    "--bg-color",
    default="black",
    help="Terminal background color (default: black)",
)
@click.version_option(version="0.1.3", prog_name="statsman")
def main(refresh_rate: float, no_color: bool, bg_color: str) -> None:
    """StatsMan - Terminal System Monitor with Manual UI"""
    app = StatsManApp(refresh_rate=refresh_rate, no_color=no_color, bg_color=bg_color)
    app.run()


if __name__ == "__main__":
    main()