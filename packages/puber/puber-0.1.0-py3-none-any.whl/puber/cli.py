from click import (
    group,
    argument,
    option,
    version_option,
    echo,
)

from .norm import norm_name
from .__version__ import __version__


@group(context_settings={"help_option_names": ["-h", "--help"]})
@version_option(__version__, "-v", "--version")
def cli():
    """
    puber - command-line tools for text normalization and publishing workflows.
    """
    pass


@cli.command("norm")
@argument("text", type=str, metavar="INPUT")
@option("-t", "--text", "mode", flag_value="text", default=True, help="Normalize as generic text.")
@option("-n", "--name", "mode", flag_value="name", help="Normalize as personal name.")
def cli_norm(text: str, mode):
    """
    Normalize input text.

    By default works in --text mode.
    """
    if mode == "text":
        result = norm_name(text.strip())
        echo(result)

    elif mode == "name":
        result = norm_name(text)
        echo(result)
