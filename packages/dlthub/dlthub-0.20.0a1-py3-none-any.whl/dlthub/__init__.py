"""dlthub is a plugin to OSS `dlt` adding projects, packages a runner and new cli commands."""

from dlthub.version import __version__, ensure_dlt_version as _ensure_dlt

_ensure_dlt()

from dlt import hub as _hub

from dlthub._runner import PipelineRunner as _PipelineRunner
from dlthub import destinations, sources, current, data_quality
from dlthub.transformations import transformation
from dlthub.common.license import self_issue_trial_license

runner = _PipelineRunner

# dlt.hub is causing circular dependency if dlthub is imported first. reload
if not _hub.__found__:
    from importlib import reload as _reload

    _reload(_hub)

__all__ = [
    "__version__",
    "data_quality",
    "current",
    "runner",
    "destinations",
    "sources",
    "transformation",
    "self_issue_trial_license",
]
