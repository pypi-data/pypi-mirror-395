from __future__ import annotations

import argparse
import asyncio
import logging
from abc import ABC, abstractmethod

from aristotlelib.api_request import get_api_key, set_api_key


class APIAction(ABC):
    def __init__(
        self, subparsers: argparse._SubParsersAction[argparse.ArgumentParser]
    ) -> None:
        self.parser = subparsers.add_parser(
            self.command_name,
            help=self.description,
            description=self.description,
        )

    @property
    def command_name(self) -> str:
        raise NotImplementedError()

    @property
    def description(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def add_action_arguments(self) -> None: ...

    @abstractmethod
    async def run_action(self, args: argparse.Namespace) -> None: ...

    def add_common_arguments(self) -> None:
        self.parser.add_argument(
            "--api-key",
            type=str,
            help="Aristotle API key (can also be set via ARISTOTLE_API_KEY environment variable)",
        )
        self.parser.add_argument(
            "--silent",
            action="store_true",
            help="Don't print any output to the console",
        )

    def add_arguments(self) -> None:
        self.add_common_arguments()
        self.add_action_arguments()
        self.parser.set_defaults(func=self.run)

    def validate(self) -> bool:
        try:
            get_api_key()
            return True
        except ValueError:
            logging.error(
                "API key not set. Please set the ARISTOTLE_API_KEY environment variable or use --api-key."
            )
            return False

    def run(self, args: argparse.Namespace) -> None:
        if args.silent:
            logging.basicConfig(
                level=logging.ERROR, format="%(levelname)s - %(message)s"
            )
        else:
            logging.basicConfig(
                level=logging.INFO, format="%(levelname)s - %(message)s"
            )
        
        # Completely disable httpx and httpcore logging
        logging.getLogger("httpx").disabled = True
        logging.getLogger("httpcore").disabled = True

        if args.api_key is not None:
            set_api_key(args.api_key)

        if not self.validate():
            return

        asyncio.run(self.run_action(args))
