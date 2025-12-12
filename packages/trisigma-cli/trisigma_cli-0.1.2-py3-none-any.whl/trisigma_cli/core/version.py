import importlib.metadata


def get_current_version() -> str:
    try:
        return importlib.metadata.version("trisigma-cli")
    except importlib.metadata.PackageNotFoundError:
        try:
            from trisigma_cli import __version__ as pkg_version

            return pkg_version
        except ImportError:
            return "0.0.0"


__version__ = get_current_version()
