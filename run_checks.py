#!/usr/bin/env python3

import subprocess
import textwrap
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from collections.abc import Mapping, Sequence


def _extract_actions(args: Mapping[str, bool]) -> list[str]:
    """Return specified actions if any or all avialable actions if script called without args."""

    all_actions = [action for action in args.keys()]
    selected_actions = [action for action, selected in args.items() if selected]
    return selected_actions or all_actions


def _output(command: Sequence[str]) -> None:
    """Helper function. Prints start/finish and runs the command inbetween."""

    print(f'========== {command[0]} starting ==========')
    subprocess.run(command)
    print(f'========== {command[0]} finished ==========')


def run_checks(args: Mapping[str, bool]):
    """Run specified checks or all checks, if script called without arguments"""

    for action in _extract_actions(args):
        eval(action)()


def gitlint() -> None:
    """Check style of all local git commit messages."""

    _output(['gitlint', '--commits', 'origin..HEAD'])


def flake8() -> None:
    """Check Python code style"""

    _output(['flake8', '.'])


def mypy() -> None:
    """Check type annotations."""

    _output(['mypy', '.', '--exclude', 'environment/vendor/'])


def unittest() -> None:
    """Run unittests."""

    _output(['coverage', 'run', '--source=.', '-m', 'unittest', 'discover'])


def coverage() -> None:
    """Show coverage report."""

    _output(['coverage', 'report'])


def main() -> None:
    """Define available arguments and run the checks"""

    parser = ArgumentParser(
        formatter_class=RawDescriptionHelpFormatter,
        description=textwrap.dedent("""
        Run linters and test suits.

        Running the script without arguments is the same as running it with all of them.
        """),
    )

    parser.add_argument('--gitlint', action='store_true', help='Run gitlint on all local commits.')
    parser.add_argument('--flake8', action='store_true', help='Run flake8.')
    parser.add_argument('--mypy', action='store_true', help='Check type annotations.')
    parser.add_argument('--unittest', action='store_true',
                        help='Run tests and write down the coverage report.')
    parser.add_argument('--coverage', action='store_true', help='Show coverage report.')
    args = parser.parse_args()
    run_checks(vars(args))


if __name__ == '__main__':
    main()
