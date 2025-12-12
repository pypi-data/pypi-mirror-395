from typing import TYPE_CHECKING, Dict, Optional

from .config import config
from .telemetry_client import TelemetryClient

if TYPE_CHECKING:
    from .git_wrapper import GitWorkflow

_telemetry_client: Optional[TelemetryClient] = None
_git_workflow_cache: Dict[str, "GitWorkflow"] = {}


def get_telemetry_client() -> Optional[TelemetryClient]:
    return _telemetry_client


def set_telemetry_client(client: TelemetryClient):
    global _telemetry_client
    _telemetry_client = client


def _get_cached_git_workflow(repo_path: str) -> Optional["GitWorkflow"]:
    if repo_path not in _git_workflow_cache:
        try:
            from .git_wrapper import GitWorkflow
            _git_workflow_cache[repo_path] = GitWorkflow(repo_path)
        except Exception:
            return None
    return _git_workflow_cache.get(repo_path)


def track_event(*args, **kwargs):
    client = get_telemetry_client()
    if client:
        if 'repository_path' not in kwargs:
            try:
                if config.is_configured() and hasattr(config, 'repository_path'):
                    repo_path = config.repository_path
                    if repo_path:
                        kwargs['repository_path'] = repo_path
            except Exception:
                pass

        try:
            parameters = kwargs.get('parameters')
            if parameters is None:
                parameters = {}

            if 'current_branch' not in parameters:
                repo_path = kwargs.get('repository_path')
                if repo_path:
                    git = _get_cached_git_workflow(str(repo_path))
                    if git:
                        try:
                            current_branch = git.get_current_branch()
                            parameters = {**parameters, 'current_branch': current_branch}
                            kwargs['parameters'] = parameters
                        except Exception:
                            pass
        except Exception:
            pass

        client.track_event(*args, **kwargs)
