from argparse import SUPPRESS
from argparse import ArgumentParser
from argparse import Namespace
from argparse import RawDescriptionHelpFormatter
from argparse import _SubParsersAction as SubParsers
from collections.abc import Callable
from os import environ
from pathlib import Path
from subprocess import run
from sys import exit
from sys import stderr
from sys import stdin
from sys import version_info
from tempfile import NamedTemporaryFile
from textwrap import dedent
from typing import Any

from .config import __metadata__
from .ezchlog import EzChLog


class ClapArgumentParser(ArgumentParser):
    def __init__(self, *args, metadata: dict | None = None, **kwargs):
        kwargs['formatter_class'] = RawDescriptionHelpFormatter
        if metadata:
            kwargs['description'] = dedent(
                f"""
                {metadata['summary']} ({metadata['name']} {metadata['version']})
                {metadata['author_email']}
                """,
            )
            kwargs['prog'] = metadata['name']
            kwargs['add_help'] = False
        super().__init__(*args, **kwargs)
        if metadata:
            self.add_argument('-h', '--help', action='help', default=SUPPRESS, help="Print help")
            self.add_argument('-V', '--version', action='version', version=f"{metadata['name']} {metadata['version']}", help="Print version")

    def format_help(self):
        formatter = self._get_formatter()
        formatter.add_text(self.description)
        formatter.add_usage(self.usage, self._actions, self._mutually_exclusive_groups)
        order = {  # builtin titles
            'positional arguments': '1',
            'options': '2',
        }
        for action_group in sorted(self._action_groups, key=lambda ag: order.get(ag.title, '0') + ag.title):
            formatter.start_section(action_group.title)
            formatter.add_text(action_group.description)
            formatter.add_arguments(action_group._group_actions)
            formatter.end_section()
        formatter.add_text(self.epilog)
        return formatter.format_help()


class Parser:
    def __init__(self, ezchlog: EzChLog) -> None:
        self.log = ezchlog
        self.parser = ClapArgumentParser(metadata=__metadata__)
        subparsers = self.parser.add_subparsers(required=True, dest='command', metavar='COMMAND', title='commands')
        parser_show_config = self._add_command(subparsers, 'showconfig', self.show_config_command, with_dry_run=False)
        parser_show_config.add_argument(
            dest='config_key',
            nargs='?',
            metavar='key',
            default='',
            help="Only show this config key value.",
        )
        parser_add = self._add_command(subparsers, 'add', self.add_command)
        parser_add.add_argument(
            '--no-git',
            action='store_true',
            help="Disable dealing with git index",
        )
        parser_add.add_argument(
            '-b',
            '--branch',
            dest='create_branch',
            action='store_true',
            help="Create the git branch along the changelog",
        )
        parser_add.add_argument(
            '-p',
            '--path',
            dest='use_paths',
            action='store_true',
            help="Output paths",
        )
        parser_add.add_argument(
            'message',
            help="Your message. Use '-' to open an editor instead.",
        )
        Category = self.log.cfg.category_class
        CategoryDef = Category[self.log.cfg.category_default]
        category_names = [cat.name for cat in Category]
        parser_add.add_argument(
            'cat',
            nargs='?',
            metavar='category',
            default=CategoryDef,
            type=lambda s: getattr(Category, s) if s else CategoryDef,
            choices=list(Category),
            help=f"Choose one of {', '.join(category_names)}. Defaut to {CategoryDef.name}.",
        )
        parser_add.add_argument(
            'ref',
            nargs='?',
            metavar='reference',
            default='',
            help="Reference for the log. Default is empty.",
        )
        parser_commit = self._add_command(subparsers, 'commit', self.commit_command)
        parser_commit.add_argument(
            'partlog_path',
            nargs='?',
            metavar='partlog',
            default=None,
            help="Main part log path if this is ambiguous",
        )
        parser_list = self._add_command(subparsers, 'list', self.list_command, with_dry_run=False)
        parser_list.add_argument(
            '-p',
            '--path',
            dest='use_paths',
            action='store_true',
            help="Output paths",
        )
        parser_merge = self._add_command(subparsers, 'merge', self.merge_command)
        parser_merge.add_argument(
            '--no-git',
            action='store_true',
            help="Disable dealing with git index",
        )
        parser_merge.add_argument(
            '-d',
            '--with-date',
            action='store_true',
            help="Add the current ISO date to the version title",
        )
        parser_merge.add_argument(
            '-l',
            '--link',
            dest='link',
            default='',
            help="Link to commits diff associated with the version",
        )
        parser_merge.add_argument(
            '-s',
            '--subtitle',
            dest='subtitle',
            default='',
            help="Add some markdown text under the version title",
        )
        parser_merge.add_argument(
            'version',
            metavar='next_ver',
            help="The next version",
        )

        def help_func(opts):
            """Print this message or the help of the given subcommand(s)"""
            self.parser.print_help()

        self._add_command(subparsers, 'help', help_func)

    def _add_command(self, subparsers: SubParsers, name: str, func: Callable, *, with_dry_run: bool = True) -> ArgumentParser:
        help_text = getattr(func, '__doc__', None)
        sub_parser = subparsers.add_parser(name, help=help_text, description=help_text)
        if with_dry_run:
            sub_parser.add_argument(
                '-n',
                '--dry-run',
                action='store_true',
                help="Dry-run the command",
            )
        sub_parser.set_defaults(func=func)
        return sub_parser

    def show_config_command(self, opts: Namespace) -> None:
        """Show configuration"""

        def format_value(value: Any | None, *, in_toml: bool = True) -> str:
            match value:
                case Path():
                    return format_value(
                        str(value.absolute().relative_to(self.log.cfg.root_dir.absolute())),
                        in_toml=in_toml,
                    )
                case str():
                    if in_toml:
                        return f'"""\n{value}\n"""' if '\n' in value else f'"{value}"'
                    else:
                        return value
                case list():  # assume items are strings
                    if in_toml:
                        return '[' + ', '.join(f'"{item}"' for item in value) + ']'
                    else:
                        return '\n'.join(str(item) for item in value)
                case bool():
                    return str(value).lower()
                case _:
                    return f'{value}'

        if opts.config_key:
            value = dict(self.log.cfg).get(opts.config_key)
            print(format_value(value, in_toml=False))  # noqa: T201
        else:
            for key, value in self.log.cfg:
                print(f'{key} = {format_value(value)}')  # noqa: T201

    def open_editor(self, file_ext: str, default_message: str) -> str:
        editor = environ.get('EZCHLOG_EDITOR', environ.get('EDITOR', environ.get('VISUAL', 'vim')))
        if not editor or not stdin.isatty():
            raise Exception(f"Cannot run editor '{editor}'")
        with NamedTemporaryFile(mode='w+', encoding='utf-8', suffix=f'.{file_ext}', delete=False) as f:
            f.write(default_message)
            f.flush()
            try:
                run([editor, f.name])
                f.seek(0)
                return '\n'.join(line for line in f.read().split('\n') if not line.startswith('#'))
            finally:
                Path(f.name).unlink()

    @staticmethod
    def _relative_to_walk_up(src_path: Path, dest_path: Path) -> Path:
        src_full_path = src_path.absolute()
        if list(version_info)[:2] >= [3, 12]:
            try:
                kwargs = dict(walk_up=True)  # split in two to please parsers/linters
                return src_full_path.relative_to(dest_path.absolute(), **kwargs)
            except ValueError:
                return src_full_path
        else:  # simulate walk_up for python < 3.12
            pp = Path()
            cur_path = dest_path.absolute()
            while not cur_path.is_mount():
                try:
                    return pp / src_full_path.relative_to(cur_path)
                except ValueError:
                    pp /= '..'
                    cur_path = cur_path.parent
            return src_full_path

    def add_command(self, opts: Namespace) -> None:
        """Add a changelog part file"""
        if opts.message == '-':
            opts.message = self.open_editor(
                'md',
                """
# This a markdown log file.
# Any comment will be removed.
# An empty file will abort.
""",
            )
        message = opts.message.strip()
        if not message:
            raise Exception("Aborted")
        no_git = self.log.cfg.no_git or opts.no_git
        create_branch = not no_git and opts.create_branch
        add_to_index = not no_git and bool(self.log.cfg.git_dir)
        p, md_message = self.log.add(dry_run=opts.dry_run, message=message, cat=opts.cat, ref=opts.ref, create_branch=create_branch, add_to_index=add_to_index)
        print(self._relative_to_walk_up(self.log.cfg.log_dir / p, Path.cwd()) if opts.use_paths else f'{p.parent!s: <20}{p.stem}')  # noqa: T201
        if opts.dry_run:
            print(md_message)  # noqa: T201

    def commit_command(self, opts: Namespace) -> None:
        """Commit using part changelog files content"""
        message = self.log.commit(dry_run=opts.dry_run, partlog_path=opts.partlog_path)
        if opts.dry_run:
            print(message, end='')  # noqa: T201

    def list_command(self, opts: Namespace) -> None:
        """List changelog files"""
        for p in self.log.list():
            print(self._relative_to_walk_up(self.log.cfg.log_dir / p, Path.cwd()) if opts.use_paths else f'{p.parent!s: <20}{p.stem}')  # noqa: T201

    def merge_command(self, opts: Namespace) -> None:
        """Merge changelog files into main changelog file under a version"""
        with_date = self.log.cfg.with_date or opts.with_date
        no_git = self.log.cfg.no_git or opts.no_git
        update_index = not no_git and bool(self.log.cfg.git_dir)
        changelog = self.log.merge(
            dry_run=opts.dry_run,
            next_version=opts.version,
            link=opts.link,
            subtitle=opts.subtitle,
            with_date=with_date,
            update_index=update_index,
        )
        if opts.dry_run:
            print(changelog)  # noqa: T201

    def parse(self, args: list[str] | None = None) -> None:
        try:
            opts = self.parser.parse_args(args=args)
            opts.func(opts)
        except Exception as e:
            if environ.get('DEBUG'):
                from traceback import print_exc

                print_exc()
            else:
                print(f"Error: {e}", file=stderr)  # noqa: T201
            exit(1)


def run_cli() -> None:
    Parser(EzChLog()).parse()
