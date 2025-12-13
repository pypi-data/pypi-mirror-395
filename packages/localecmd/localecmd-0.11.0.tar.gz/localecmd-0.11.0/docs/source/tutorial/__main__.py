import functions
from functions import DOMAIN, _

from localecmd import start_cli


def main():
    modules = [functions]
    greeting = _("Welcome to the turtle shell. Type help to list commands.")
    cli = start_cli(modules, greeting=greeting, gettext_domains=[DOMAIN])
    cli.cmdloop()
    cli.close()


main()
