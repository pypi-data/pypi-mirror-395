"""
CLI Adapter for ForgeBase.

Provides command-line interface for executing UseCases and interacting
with ForgeBase applications.

:author: ForgeBase Development Team
:since: 2025-11-03
"""

import argparse
import json
import sys
from typing import Any

from forgebase.adapters.adapter_base import AdapterBase


class CLIAdapter(AdapterBase):
    """
    Command-line interface adapter.

    Provides CLI commands for executing UseCases, viewing metrics,
    and managing configuration.

    Example::

        cli = CLIAdapter(usecases={'create_user': CreateUserUseCase()})
        cli.run(['create_user', '--email', 'test@example.com'])
    """

    def __init__(self, usecases: dict[str, Any] | None = None):
        """
        Initialize CLI adapter.

        :param usecases: Dictionary mapping names to UseCase instances
        :type usecases: Optional[Dict[str, Any]]
        """
        self.usecases = usecases or {}
        self.parser = self._build_parser()

    def _build_parser(self) -> argparse.ArgumentParser:
        """Build argument parser."""
        parser = argparse.ArgumentParser(
            prog='forgebase',
            description='ForgeBase CLI - Cognitive Framework'
        )

        subparsers = parser.add_subparsers(dest='command', help='Commands')

        # Execute command
        exec_parser = subparsers.add_parser('exec', help='Execute a UseCase')
        exec_parser.add_argument('usecase', help='UseCase name')
        exec_parser.add_argument('--json', help='JSON input data')
        exec_parser.add_argument('--output', default='json', choices=['json', 'text'])

        # List command
        subparsers.add_parser('list', help='List available UseCases')

        return parser

    def run(self, argv: list[str] | None = None) -> int:
        """
        Run CLI with arguments.

        :param argv: Command-line arguments
        :type argv: Optional[List[str]]
        :return: Exit code
        :rtype: int
        """
        args = self.parser.parse_args(argv)

        if args.command == 'exec':
            return self._execute_usecase(args)
        if args.command == 'list':
            return self._list_usecases()
        self.parser.print_help()
        return 1

    def _execute_usecase(self, args) -> int:
        """Execute a UseCase."""
        if args.usecase not in self.usecases:
            print(f"Error: UseCase '{args.usecase}' not found", file=sys.stderr)
            return 1

        try:
            data = json.loads(args.json) if args.json else {}
            usecase = self.usecases[args.usecase]
            result = usecase.execute(**data)

            if args.output == 'json':
                print(json.dumps({'result': str(result)}, indent=2))
            else:
                print(result)

            return 0
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1

    def _list_usecases(self) -> int:
        """List available UseCases."""
        print("Available UseCases:")
        for name in sorted(self.usecases.keys()):
            print(f"  - {name}")
        return 0

    def name(self) -> str:
        """Get adapter name."""
        return "CLIAdapter"

    def module(self) -> str:
        """Get module name."""
        return "forgebase.adapters.cli"

    def _instrument(self) -> None:
        """Instrument adapter."""
        pass  # CLI doesn't need special instrumentation
