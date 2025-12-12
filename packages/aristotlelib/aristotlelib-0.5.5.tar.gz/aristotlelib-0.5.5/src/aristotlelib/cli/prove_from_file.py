import argparse
from aristotlelib.cli.api_action import APIAction
from aristotlelib.project import Project, ProjectInputType


class ProveFromFileAction(APIAction):
    @property
    def command_name(self) -> str:
        return "prove-from-file"

    @property
    def description(self) -> str:
        return "Prove theorems from a Lean file"

    def add_action_arguments(self) -> None:
        self.parser.add_argument(
            "input_file", type=str, help="Path to the Lean file to prove"
        )

        # Commonly used options
        self.parser.add_argument(
            "--output-file",
            type=str,
            help="Path to save the solution file (default: [input-file-name]_aristotle.lean)",
        )

        # Advanced options
        self.parser.add_argument(
            "--no-auto-add-imports",
            action="store_true",
            help="Disable automatic import resolution (default: enabled)",
        )

        self.parser.add_argument(
            "--context-files",
            type=str,
            nargs="*",
            help="Additional context files to include (cannot be used with auto-add-imports)",
        )

        self.parser.add_argument(
            "--no-validate-lean-project",
            action="store_true",
            help="Skip Lean project validation (default: validate)",
        )

        self.parser.add_argument(
            "--no-wait",
            action="store_true",
            help="Don't wait for completion; just kick it off (default: wait)",
        )

        self.parser.add_argument(
            "--polling-interval",
            type=int,
            default=30,
            help="Polling interval in seconds when waiting for completion (default: 30)",
        )

        self.parser.add_argument(
            "--max-polling-failures",
            type=int,
            default=3,
            help="Max polling failures before exiting early. Proof might still be working in the background. (default: 3)",
        )

        self.parser.add_argument(
            "--informal",
            action="store_true",
            help="Use informal input mode instead of formal Lean (default: formal Lean)",
        )

        self.parser.add_argument(
            "--formal-input-context",
            type=str,
            help="Path to a Lean file containing formal context for the problem (works with --informal mode)",
        )

        self.parser.add_argument(
            "--context-folder",
            type=str,
            help="Path to a folder containing context files. All .lean, .md, .txt, .tex files will be included.",
        )

    async def run_action(self, args: argparse.Namespace) -> None:
        auto_add_imports = not args.no_auto_add_imports
        validate_lean_project = not args.no_validate_lean_project

        kwargs = {
            "auto_add_imports": auto_add_imports,
            "validate_lean_project": validate_lean_project,
            "wait_for_completion": not args.no_wait,
            "polling_interval_seconds": args.polling_interval,
            "max_polling_failures": args.max_polling_failures,
            "project_input_type": ProjectInputType.INFORMAL if args.informal else ProjectInputType.FORMAL_LEAN,
        }

        # Handle context files or folder
        if args.context_folder and args.context_files:
            raise ValueError("Cannot specify both --context-folder and --context-files")

        if args.context_folder:
            kwargs["context_file_paths"] = [args.context_folder]
            kwargs["context_is_folder"] = True
        elif args.context_files:
            kwargs["context_file_paths"] = args.context_files

        if args.output_file:
            kwargs["output_file_path"] = args.output_file

        if args.formal_input_context:
            kwargs["formal_input_context"] = args.formal_input_context

        await Project.prove_from_file(input_file_path=args.input_file, **kwargs)
