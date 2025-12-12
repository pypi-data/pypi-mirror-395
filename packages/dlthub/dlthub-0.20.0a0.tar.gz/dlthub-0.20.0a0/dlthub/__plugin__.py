import os
from typing import Any, Dict, Optional, Type

from dlt.common.configuration import plugins as _plugins
from dlt.common.configuration.specs.pluggable_run_context import RunContextBase

from dlt._workspace.cli import SupportsCliCommand

from dlthub.project.exceptions import ProjectRunContextNotAvailable
from dlthub.project.project_context import is_project_dir
from dlthub.common.license.decorators import is_scope_active


@_plugins.hookimpl(specname="plug_run_context", tryfirst=True)
def _plug_run_context_impl(
    run_dir: Optional[str], runtime_kwargs: Optional[Dict[str, Any]]
) -> Optional[RunContextBase]:
    """Called when run new context is created"""

    from dlthub.project.project_context import (
        create_project_context,
        find_project_dir,
    )

    # use explicit dir or find one starting from cwd
    project_dir = (
        run_dir
        if run_dir and is_project_dir(run_dir)
        else find_project_dir()
        if not run_dir
        else None
    )
    runtime_kwargs = runtime_kwargs or {}
    profile = runtime_kwargs.get("profile")
    if project_dir:
        # TODO: get local_dir, data_dir, and verify settings_dir. allow them to override
        #   settings in project config
        return create_project_context(
            project_dir, profile=profile, validate=runtime_kwargs.get("_validate", False)
        )
    else:
        if runtime_kwargs.get("_required") == "ProjectRunContext":
            raise ProjectRunContextNotAvailable(project_dir or run_dir or os.getcwd())

    # no run dir pass through to next plugin
    return None


#
# legacy transformation commands
#
if is_scope_active("dlthub.project"):

    @_plugins.hookimpl(specname="plug_cli")
    def _plug_cli_transformation() -> Type[SupportsCliCommand]:
        from dlt.common.exceptions import MissingDependencyException

        try:
            from dlthub.legacy.transformations.cli import TransformationCommand

            return TransformationCommand
        except (MissingDependencyException, ImportError):
            # TODO: we need a better mechanism to plug in placeholder commands for non installed
            # packages
            from dlt._workspace.cli import SupportsCliCommand

            class _PondCommand(SupportsCliCommand):
                command = "transformation"
                help_string = "Please install dlthub[cache] to enable transformations"

            return _PondCommand

    @_plugins.hookimpl(specname="plug_cli")
    def _plug_cli_cache() -> Type[SupportsCliCommand]:
        from dlthub.cache.cli import CacheCommand
        from dlt.common.exceptions import MissingDependencyException

        try:
            from dlthub.cache.cli import CacheCommand

            return CacheCommand
        except (MissingDependencyException, ImportError):
            from dlt._workspace.cli import SupportsCliCommand

            class _CacheCommand(SupportsCliCommand):
                command = "cache"
                help_string = "Please install dlthub[cache] to use local transformation cache"

            return _CacheCommand


if is_scope_active("dlthub.project"):

    @_plugins.hookimpl(specname="plug_cli")
    def _plug_cli_project() -> Type[SupportsCliCommand]:
        from dlthub.project.cli.project_command import ProjectCommand

        return ProjectCommand

    @_plugins.hookimpl(specname="plug_cli", tryfirst=True)
    def _plug_cli_pipeline() -> Type[SupportsCliCommand]:
        # should be executed before dlt command got plugged in (tryfirst) to override it
        from dlthub.project.cli.pipeline_command import ProjectPipelineCommand

        return ProjectPipelineCommand

    @_plugins.hookimpl(specname="plug_cli")
    def _plug_cli_dataset() -> Type[SupportsCliCommand]:
        from dlthub.project.cli.dataset_command import DatasetCommand

        return DatasetCommand

    @_plugins.hookimpl(specname="plug_cli")
    def _plug_cli_source() -> Type[SupportsCliCommand]:
        from dlthub.project.cli.source_command import SourceCommand

        return SourceCommand

    @_plugins.hookimpl(specname="plug_cli")
    def _plug_cli_destination() -> Type[SupportsCliCommand]:
        from dlthub.project.cli.destination_command import DestinationCommand

        return DestinationCommand

    @_plugins.hookimpl(specname="plug_cli")
    def _plug_cli_profile() -> Type[SupportsCliCommand]:
        from dlthub.project.cli.profile_command import ProfileCommand

        return ProfileCommand


@_plugins.hookimpl(specname="plug_cli")
def _plug_cli_license() -> Type[SupportsCliCommand]:
    from dlthub.common.license.cli import LicenseCommand

    return LicenseCommand


if is_scope_active("dlthub.dbt_generator"):

    @_plugins.hookimpl(specname="plug_cli")
    def _plug_cli_dbt() -> Type[SupportsCliCommand]:
        from dlthub.dbt_generator.cli import DbtCommand

        return DbtCommand
