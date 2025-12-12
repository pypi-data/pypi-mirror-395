import asyncio
import logging
import os
import pydantic  # type: ignore
from datetime import datetime
from pathlib import Path
from enum import Enum
from typing import cast, overload, Literal

from aristotlelib import api_request, local_file_utils
from aristotlelib.date_utils import format_relative_time

# Set up logger for this module
logger = logging.getLogger("aristotle")

MAX_FILES_PER_REQUEST = 10

# Polling and backoff constants for wait_for_completion
DEFAULT_MAX_FAILURE_TIME_SECONDS = 600  # 10 minutes
DEFAULT_MIN_BACKOFF_SECONDS = 15
DEFAULT_MAX_BACKOFF_SECONDS = 120  # 2 minutes


class ProjectStatus(Enum):
    NOT_STARTED = "NOT_STARTED"
    QUEUED = "QUEUED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"
    PENDING_RETRY = "PENDING_RETRY"


class ProjectInputType(Enum):
    FORMAL_LEAN = 2
    INFORMAL = 3


class Project(pydantic.BaseModel):
    project_id: str
    status: ProjectStatus
    created_at: datetime
    last_updated_at: datetime
    # if started, represents % processing complete (out of 100)
    percent_complete: int | None = None
    file_name: str | None = None
    description: str | None = None

    def __str__(self) -> str:
        ret = f"Project {self.project_id}"
        if self.file_name is not None:
            ret += f"\nfile name: {self.file_name}"
        if self.description is not None:
            ret += f"\ndescription: {self.description}"
        ret += f"\nstatus: {self.status.name}\ncreated: {format_relative_time(self.created_at)}\nlast updated: {format_relative_time(self.last_updated_at)}"
        if self.percent_complete is not None:
            ret += f"\npercent complete: {self.percent_complete}"
        return ret

    @classmethod
    async def from_id(cls, project_id: str) -> "Project":
        project = Project(
            project_id=project_id,
            status=ProjectStatus.NOT_STARTED,
            created_at=datetime.now(),
            last_updated_at=datetime.now(),
        )
        await project.refresh()
        return project

    @classmethod
    async def create(
        cls,
        context_file_paths: list[Path] | list[str] | None = None,
        validate_lean_project_root: bool = True,
        project_input_type: ProjectInputType = ProjectInputType.FORMAL_LEAN,
    ) -> "Project":
        """Create a new project.

        Args:
            context_file_paths: List of file paths to include in the project as context.
            validate_lean_project_root: Whether to validate that these files are part of a valid Lean project.
               Strongly recommended to set to True, but not required if you just want to reference a small number of
               other imported files but don't have a working Lean project.
        """
        context_file_paths = context_file_paths or []
        if len(context_file_paths) > MAX_FILES_PER_REQUEST:
            raise ValueError(
                f"Maximum number of files to upload per request is {MAX_FILES_PER_REQUEST}"
            )

        file_paths = local_file_utils.normalize_and_dedupe_paths(context_file_paths)
        project_root = None
        if validate_lean_project_root and file_paths:
            example_file = file_paths[0]
            project_root = local_file_utils.find_lean_project_root(example_file)

        local_file_utils.validate_local_file_paths(
            file_paths, project_root=project_root
        )

        files_for_upload = local_file_utils.get_files_for_upload(
            file_paths, project_root=project_root or Path(".")
        )
        async with api_request.AristotleRequestClient() as client:
            url = f"/project?project_type={project_input_type.value}"
            response = await client.post(
                url,
                files=[("context", file) for file in files_for_upload],
            )
            return cls.model_validate(response.json())

    async def add_context(
        self,
        context_file_paths: list[Path] | list[str],
        batch_size: int = MAX_FILES_PER_REQUEST,
        validate_lean_project_root: bool = True,
        project_root: Path | None = None,
    ) -> None:
        """Add context files to the project.

        Args:
            context_file_paths: List of context file paths (.lean, .md, .txt, .tex)
            batch_size: Number of files to upload per request
            validate_lean_project_root: Whether to validate files are in a Lean project.
                Set to False when uploading non-Lean context files.
            project_root: Project root directory. Required if validate_lean_project_root=False.
        """
        assert len(context_file_paths) > 0, "No context files provided"
        file_paths = local_file_utils.normalize_and_dedupe_paths(context_file_paths)

        if validate_lean_project_root:
            # Lean project mode - find and validate Lean project
            example_file = file_paths[0]
            project_root = local_file_utils.find_lean_project_root(example_file)
            # Validate as Lean files
            local_file_utils.validate_local_file_paths(
                file_paths, project_root=project_root
            )
        else:
            # Non-Lean context mode - just validate files exist
            assert project_root is not None, (
                "project_root must be provided if validate_lean_project_root is False"
            )
            # Validate each file exists and has allowed extension
            for file_path in file_paths:
                local_file_utils.validate_local_file_path(
                    file_path,
                    project_root=project_root,
                    require_lean=False,
                    allowed_extensions=local_file_utils.CONTEXT_EXTENSIONS,
                )

        async with api_request.AristotleRequestClient() as client:
            for i in range(0, len(file_paths), batch_size):
                batch = file_paths[i : i + batch_size]
                await self._add_context(client, batch, project_root=project_root)
                num_complete = min(i + batch_size, len(file_paths))
                logger.info(
                    f"{num_complete} of {len(file_paths)} context files uploaded"
                )

    async def _add_context(
        self,
        client: api_request.AristotleRequestClient,
        context_file_paths: list[Path],
        project_root: Path,
    ) -> None:
        if len(context_file_paths) > MAX_FILES_PER_REQUEST:
            raise ValueError(
                f"Cannot upload more than {MAX_FILES_PER_REQUEST} files at once. Got {len(context_file_paths)}"
            )
        if len(context_file_paths) == 0:
            logger.warning(f"No context files provided for project {self.project_id}")
            return

        # Note: Files are already validated in add_context() before calling this method
        # No need to re-validate here

        files_for_upload = local_file_utils.get_files_for_upload(
            context_file_paths, project_root=project_root
        )

        response = await client.post(
            f"/project/{self.project_id}/context",
            files=[("context", file) for file in files_for_upload],
        )
        self._update_from_response(response.json())

    @overload
    async def solve(
        self, *, input_file_path: Path | str, formal_input_context: Path | str | None = None
    ) -> None: ...

    @overload
    async def solve(
        self, *, input_content: str, formal_input_context: Path | str | None = None
    ) -> None: ...

    async def solve(
        self,
        input_file_path: Path | str | None = None,
        input_content: str | None = None,
        formal_input_context: Path | str | None = None,
    ) -> None:
        """Solve the project with either an input file or input text.

        Args:
            input_file_path: Path to a file to upload as input
            input_content: Text content to send as input
            formal_input_context: Path to a Lean file containing formal context for the problem.
                Supported in informal mode only.

        """
        assert self.status == ProjectStatus.NOT_STARTED, (
            "This project has already been attempted; create a new project instead."
        )
        assert input_file_path is not None or input_content is not None, (
            "Either input_file_path or input_content must be provided."
        )
        assert input_file_path is None or input_content is None, (
            "Only one of input_file_path or input_content must be provided."
        )

        async with api_request.AristotleRequestClient() as client:
            if input_file_path is not None:
                # Handle file upload case
                file_path = Path(input_file_path)
                file_content = local_file_utils.read_file_safely(file_path)
                files = [("input_file", (str(file_path), file_content, "text/plain"))]
                params = None
            else:
                # Handle text input case
                params = {"input_text": input_content}
                files = None


            # Add formal_input_context if provided (for informal mode)
            if formal_input_context is not None:
                context_path = Path(formal_input_context)
                context_content = local_file_utils.read_file_safely(context_path)
                if files is None:
                    files = []
                files.append(("formal_input_context", (str(context_path), context_content, "text/plain")))

            response = await client.post(
                f"/project/{self.project_id}/solve",
                params=params,
                files=files,
            )

            response_data = response.json()
            self._update_from_response(response_data)

    async def get_solution(self, output_path: Path | str | None = None) -> Path:
        """Download the solution file from the project result endpoint.

        Args:
            output_path: Path where to save the downloaded file. If None, uses filename from response headers.

        Returns:
            Path to the downloaded file
        """
        async with api_request.AristotleRequestClient() as client:
            response = await client.get(f"/project/{self.project_id}/result")

            if output_path is None:
                # Try to get filename from Content-Disposition header
                content_disposition = response.headers.get("content-disposition", "")
                if "filename=" in content_disposition:
                    filename = content_disposition.split("filename=")[1].strip('"')
                    output_path = Path(filename)
                else:
                    output_path = Path(f"{self.project_id}_solution.lean")
            else:
                output_path = Path(output_path)

            output_path.write_bytes(response.content)
            return output_path

    async def refresh(self) -> None:
        async with api_request.AristotleRequestClient() as client:
            response = await client.get(f"/project/{self.project_id}")
            response_data = response.json()
            self._update_from_response(response_data)

    def _update_from_response(self, response_data: dict) -> None:
        updated_project = cast(Project, self.model_validate(response_data))
        for field_name, field_value in updated_project.model_dump().items():
            setattr(self, field_name, field_value)

    @classmethod
    async def list_projects(
        cls,
        pagination_key: str | None = None,
        limit: int = 30,
        status: ProjectStatus | list[ProjectStatus] | None = None,
    ) -> tuple[list["Project"], str | None]:
        """List projects, ordered by creation date (most recent first).

        Args:
            pagination_key: Key to start from when paginating through projects.
            limit: Maximum number of projects to return. Must be between 1 and 100.
            status: Optional project status filter. Can be a single ProjectStatus,
                   a list of ProjectStatus values, or None for all projects.

        Returns:
            Tuple of list of projects and the new pagination key.
        """
        assert 1 <= limit <= 100, "Limit must be between 1 and 100"

        params = {"pagination_key": pagination_key, "limit": limit}
        if status is not None:
            if isinstance(status, list):
                # Convert list of ProjectStatus to list of status strings
                params["status"] = [s.value for s in status]
            else:
                # Single ProjectStatus
                params["status"] = status.value

        async with api_request.AristotleRequestClient() as client:
            response = await client.get("/project", params=params)
            response_data = response.json()
            projects: list["Project"] = [
                cast("Project", cls.model_validate(project))
                for project in response_data["projects"]
            ]
            pagination_key = response_data.get("pagination_key")
            assert pagination_key is None or isinstance(pagination_key, str)
            return projects, pagination_key

    @overload
    @classmethod
    async def prove_from_file(
        cls,
        *,
        input_file_path: Path | str,
        auto_add_imports: Literal[True],
        validate_lean_project: Literal[True] = True,
        polling_interval_seconds: int = 30,
        max_polling_failures: int = 3,
        output_file_path: Path | str | None = None,
        project_input_type: Literal[
            ProjectInputType.FORMAL_LEAN
        ] = ProjectInputType.FORMAL_LEAN,
        formal_input_context: Path | str | None = None,
    ) -> str: ...

    @overload
    @classmethod
    async def prove_from_file(
        cls,
        *,
        input_file_path: Path | str,
        auto_add_imports: Literal[False] = False,
        context_file_paths: list[Path] | list[str] | None = None,
        validate_lean_project: bool = True,
        polling_interval_seconds: int = 30,
        max_polling_failures: int = 3,
        output_file_path: Path | str | None = None,
        project_input_type: ProjectInputType = ProjectInputType.FORMAL_LEAN,
        formal_input_context: Literal[None] = None,
    ) -> str: ...

    @overload
    @classmethod
    async def prove_from_file(
        cls,
        *,
        input_content: str,
        auto_add_imports: Literal[False] = False,
        context_file_paths: list[Path] | list[str] | None = None,
        validate_lean_project: bool = True,
        polling_interval_seconds: int = 30,
        max_polling_failures: int = 3,
        output_file_path: Path | str | None = None,
        project_input_type: ProjectInputType = ProjectInputType.FORMAL_LEAN,
        formal_input_context: Path | str | None = None,
    ) -> str: ...

    @classmethod
    async def prove_from_file(
        cls,
        *,
        input_file_path: Path | str | None = None,
        input_content: str | None = None,
        auto_add_imports: bool = True,
        context_file_paths: list[Path] | list[str] | None = None,
        context_is_folder: bool = False,
        validate_lean_project: bool = True,
        wait_for_completion: bool = True,
        polling_interval_seconds: int = 30,
        max_polling_failures: int = 3,
        output_file_path: Path | str | None = None,
        project_input_type: ProjectInputType = ProjectInputType.FORMAL_LEAN,
        formal_input_context: Path | str | None = None,
    ) -> str:
        """Proves the input content.

        Args:
            input_file_path: Path to the input file
            auto_add_imports: Whether to automatically add imports from the input file as context to the project.
                              Requires that the input file is part of a valid Lean project.
            context_file_paths: List of file paths to add as context to the project, manually.
                Can include .lean, .md, .txt, .tex files.
            context_is_folder: If True, context_file_paths[0] is treated as a folder path
                and all allowed files within are gathered.
            validate_lean_project: Whether to validate that the input file is part of a valid Lean project.
            wait_for_completion: Whether to wait for the project to complete before returning. If False, the project id is returned.
            polling_interval_seconds: Interval in seconds to poll for the project status.
            max_polling_failures: Maximum number of polling failures before raising an error.
            output_file_path: Path to save the solution file. If None, uses names the file based on the input file name with _aristotle appended.
            project_input_type: Type of project input to create.
            formal_input_context: Path to a Lean file containing formal context for the problem. Supported in informal mode only.

        Returns:
            The file path to the solution, or the project id if wait_for_completion is False
        """
        assert formal_input_context is None or project_input_type == ProjectInputType.INFORMAL, (
            "formal_input_context can only be provided in informal mode"
        )
        project_root = None
        if input_file_path is not None:
            assert input_content is None, (
                "input_content cannot be provided when input_file_path is provided"
            )
            logger.info("Validating input...")
            input_file_path = Path(input_file_path)
            if validate_lean_project and project_input_type == ProjectInputType.FORMAL_LEAN:
                project_root = local_file_utils.find_lean_project_root(input_file_path)
            # Validate file extension based on input type
            # Formal Lean: require .lean files
            # Informal: allow .txt, .tex, and .md files
            require_lean = project_input_type == ProjectInputType.FORMAL_LEAN
            allowed_extensions = (
                [".lean"]
                if require_lean
                else [".txt", ".tex", ".md"]
            )
            local_file_utils.validate_local_file_path(
                input_file_path,
                project_root=project_root,
                require_lean=require_lean,
                allowed_extensions=allowed_extensions,
            )
            logger.info("Input Validated.")
        else:
            assert input_content, "input_file_path or input_content must be provided"
        
        # If auto_add_imports is enabled and we have a formal_input_context, we need to find the project root
        # even if validate_lean_project is False (for informal input with Lean context)
        if project_root is None and formal_input_context and auto_add_imports:
            formal_input_context = Path(formal_input_context)
            project_root = local_file_utils.find_lean_project_root(formal_input_context)

        logger.info("Creating project...")
        project = await cls.create(
            validate_lean_project_root=validate_lean_project,
            project_input_type=project_input_type,
        )
        logger.info(f"Created project {project.project_id}")

        if auto_add_imports:
            # Auto-imports: gather Lean imports from the input file
            # Note: context_file_paths (natural language context) can still be provided separately
            lean_context_file_paths = []

            # Gather imports based on input type
            if input_file_path is not None and project_input_type == ProjectInputType.FORMAL_LEAN:
                # Formal Lean input: gather imports from the input file
                assert validate_lean_project, (
                    "validate_lean_project must be True when auto_add_imports is True for formal Lean input"
                )
                assert project_root is not None, (
                    "project_root must be set for formal Lean input with auto_add_imports"
                )
                logger.info("Adding imports to project...")
                lean_context_file_paths = list(
                    local_file_utils.gather_file_imports(input_file_path, project_root)
                )
            elif formal_input_context is not None:
                # Informal input with formal context: gather imports from the context file
                assert project_root is not None, (
                    "project_root must be set when formal_input_context is provided with auto_add_imports"
                )
                logger.info("Adding imports from formal context to project...")
                formal_input_context_path = Path(formal_input_context)
                # Gather imports from the formal_input_context file
                # Note: The formal_input_context file itself will be sent separately to the solve endpoint
                imports = local_file_utils.gather_file_imports(formal_input_context_path, project_root)
                lean_context_file_paths = list(imports)
            # else: Informal input without formal context - no imports to gather

            if lean_context_file_paths:
                await project.add_context(
                    lean_context_file_paths, validate_lean_project_root=True
                )
                logger.info(f"Added {len(lean_context_file_paths)} imports to project")
            else:
                logger.info("No imports to add")

        # Process natural language context files (separate from auto-imports)
        if context_file_paths is not None and len(context_file_paths) > 0:
            # Process context_file_paths (may be folder or individual files)
            if context_is_folder:
                # Expect single path (folder)
                assert len(context_file_paths) == 1, (
                    "When context_is_folder=True, context_file_paths must contain a single folder path"
                )
                folder_path = Path(context_file_paths[0])
                logger.info(f"Gathering context files from folder: {folder_path}")

                # Gather files from folder
                context_file_paths = local_file_utils.gather_context_files_from_folder(
                    folder_path,
                    allowed_extensions=local_file_utils.CONTEXT_EXTENSIONS,
                )
                logger.info(f"Gathered {len(context_file_paths)} context files from folder")

                # Filter out the input file itself (and formal_input_context if provided)
                # We don't want to include the main input file as context
                files_to_exclude = set()
                if input_file_path is not None:
                    files_to_exclude.add(Path(input_file_path).resolve())
                if formal_input_context is not None:
                    files_to_exclude.add(Path(formal_input_context).resolve())

                context_file_paths = [
                    f for f in context_file_paths
                    if f.resolve() not in files_to_exclude
                ]
                logger.info(f"After filtering, {len(context_file_paths)} context files remain")

            # Validate all context files (allow any context extension)
            for ctx_file in context_file_paths:
                local_file_utils.validate_local_file_path(
                    Path(ctx_file),
                    project_root=None,
                    require_lean=False,
                    allowed_extensions=local_file_utils.CONTEXT_EXTENSIONS,
                )

            logger.info("Adding context files to project...")
            # For natural language context files, we need a project root that contains all of them
            # Find the common parent directory of all context files
            resolved_paths = [Path(f).resolve() for f in context_file_paths]

            # Find common parent by going up from each file until we find a common ancestor
            # Start with the parent of the first file
            if resolved_paths:
                common_parent = resolved_paths[0].parent
                # Keep going up until we find a directory that contains all files
                while not all(
                    str(p).startswith(str(common_parent) + os.sep) or p.parent == common_parent
                    for p in resolved_paths
                ):
                    if common_parent.parent == common_parent:
                        # Reached filesystem root, use root
                        break
                    common_parent = common_parent.parent

                project_root_for_context = common_parent
            else:
                project_root_for_context = Path(".")

            await project.add_context(
                context_file_paths,
                validate_lean_project_root=False,  # Don't require Lean project for context
                project_root=project_root_for_context,
            )
            logger.info(f"Added {len(context_file_paths)} context files to project")

        if input_file_path is not None:
            await project.solve(
                input_file_path=input_file_path,
                formal_input_context=formal_input_context
            )
        else:
            assert input_content is not None
            await project.solve(
                input_content=input_content,
                formal_input_context=formal_input_context
            )

        if not wait_for_completion:
            logger.info(
                "Not waiting for completion. Returning project id. You can manually check on it any time with Project.from_id('{project.project_id}')"
            )
            return project.project_id

        if output_file_path is None:
            if input_file_path is not None:
                output_file_path = local_file_utils.get_default_output_path(
                    input_file_path
                )
            else:
                output_file_path = Path(f"{project.project_id}_solution.lean")

        return await project.wait_for_completion(
            output_file_path,
            polling_interval_seconds=polling_interval_seconds,
            max_polling_failures=max_polling_failures,
        )

    async def wait_for_completion(
        self,
        output_file_path: Path | str,
        polling_interval_seconds: int = 30,
        max_polling_failures: int = 3,
    ) -> str:
        try:
            num_polling_failures = 0
            total_failure_time = 0

            while self.status not in (ProjectStatus.COMPLETE, ProjectStatus.FAILED):
                try:
                    msg = str(self)
                    logger.info(
                        msg + f"\nSleeping for {polling_interval_seconds} seconds..."
                    )
                    await asyncio.sleep(polling_interval_seconds)
                    await self.refresh()
                    # Reset failure tracking on successful refresh
                    num_polling_failures = 0
                    total_failure_time = 0
                except api_request.AristotleAPIError:
                    num_polling_failures += 1
                    # Calculate exponential backoff: 15s, 30s, 60s, 120s, 120s...
                    backoff_seconds = min(
                        DEFAULT_MIN_BACKOFF_SECONDS * (2 ** (num_polling_failures - 1)),
                        DEFAULT_MAX_BACKOFF_SECONDS
                    )
                    total_failure_time += backoff_seconds

                    if total_failure_time >= DEFAULT_MAX_FAILURE_TIME_SECONDS:
                        raise api_request.AristotleAPIError(
                            "Connection interrupted - Aristotle is still at work. You will be able to reconnect and retrieve results via the history as normal."
                        )

                    logger.warning(
                        f"We haven't been able to check on your project {num_polling_failures} time(s). Don't worry; we're still working on it. Trying again in {backoff_seconds} seconds."
                    )
                    await asyncio.sleep(backoff_seconds)

            if self.status != ProjectStatus.COMPLETE:
                raise api_request.AristotleAPIError(
                    "Project failed due to an internal error. The team at Harmonic has been notified; please try again."
                )

            logger.info("Solve complete! Getting solution...")
            solution_file_path = await self.get_solution(output_path=output_file_path)
            logger.info(f"Solution saved to {solution_file_path}")
            return str(solution_file_path)
        finally:
            if self.status not in (ProjectStatus.FAILED, ProjectStatus.COMPLETE):
                logger.info(
                    f"Project {self.project_id} is still running. You can manually check on it any time by typing `aristotle` in a shell or with Project.from_id('{self.project_id}')"
                )
