# purge.py
import json
import pathlib
import subprocess
import sys
from typing import Dict, List, Set
from vforge import helpers


# packages which never get uninstalled
ALWAYS_KEEP = {"pip", "setuptools", "wheel"}


def main():
    # fetch arguments
    args_dict = helpers.parse_args(["project-dir"])
    log = helpers.make_logger()

    # directory validation
    project_dir = pathlib.Path(args_dict["project_dir"])
    helpers.validate_directory(project_dir, False)

    # find the virtual environment
    venv_path = helpers.get_venv_path(project_dir)

    # scan project for imports (roots)
    # check for excluded packages
    root_packages = {helpers.normalize_name(p) for p in helpers.scan_directory(project_dir)}
    log.info(f"Scan found {len(root_packages)} root package candidates.")

    # Keep packages which user explicitly requested, even if they're not actively being used.
    explicit, _ = helpers.load_user_config(project_dir)
    for pkg in explicit:
        root_packages.add(pkg)
    log.info(f"Scan found {len(root_packages)} explicitly requested packages to keep.")

    # get installed packages and dependency mapping from venv pip
    pip_exe = helpers.program_path(venv_path, "pip")
    log.debug("Checking for installed packages now.")
    installed = helpers.get_installed_packages_and_deps(pip_exe)
    log.debug(f"Found {len(installed)} packages in venv.")

    # compute dependency closure
    import_to_dist = helpers.map_imports_to_dists(pip_exe)
    root_dists = {import_to_dist.get(imp, imp) for imp in root_packages}
    retain = dependency_closure(root_dists, installed)

    log.debug(f"Packages to retain (roots + deps): {len(retain)}")

    # site-packages path for size measurement (ask venv python)
    venv_python = helpers.program_path(venv_path, "python")
    site_pkgs = get_site_packages_path(venv_python)
    size_before = dir_size(pathlib.Path(site_pkgs)) if site_pkgs else 0

    # determine packages to remove (installed names are lower-case)
    _, exclude = helpers.load_user_config(project_dir)
    to_remove = list()
    for pkg in list(installed.keys()) + list(exclude):
        if pkg in ALWAYS_KEEP:
            # critical package that user should not exclude
            continue
        elif pkg in exclude or pkg not in retain:
            # either manually excluded or not a root/dependency
            to_remove.append(pkg)

    if to_remove:
        log.debug(f"Uninstalling {len(to_remove)} packages: {to_remove}")
        subprocess.run([str(pip_exe), "uninstall", "-y", *to_remove], check=True)
        log.debug(f"Removed {len(to_remove)} packages.")
    else:
        log.warning("No packages to remove.")

    # size after uninstall
    size_after = dir_size(pathlib.Path(site_pkgs)) if site_pkgs else 0
    log.info(f"Freed space: {format_bytes(size_before - size_after)}")


def dependency_closure(roots: Set[str], installed: Dict[str, List[str]]) -> Set[str]:
    """Return set of packages to retain (roots + all recursive dependencies)."""
    retain = {"pip"}
    queue = [r for r in roots if r in installed]
    # include roots not present in installed? if root not installed, ignore it.
    while queue:
        pkg = queue.pop()
        if pkg in retain:
            continue
        retain.add(pkg)
        for dep in installed.get(pkg, []):
            if dep not in retain:
                queue.append(dep)
    return retain


def get_site_packages_path(venv_python: pathlib.Path) -> str:
    """
    Return the path to site-packages for the venv by asking its python.
    Falls back to scanning sys.path if site.getsitepackages() is unavailable.
    """
    cmd = [
        str(venv_python),
        "-c",
        (
            "import site, sys, json\n"
            "paths = []\n"
            "try:\n"
            "    paths = site.getsitepackages()\n"
            "except Exception:\n"
            "    paths = [p for p in sys.path if 'site-packages' in p]\n"
            "print(json.dumps(paths[0] if paths else ''))\n"
        ),
    ]
    try:
        out = subprocess.check_output(cmd, text=True).strip()
        # out is a JSON string
        path = json.loads(out)
        return path
    except Exception:
        return ""


def dir_size(path: pathlib.Path) -> int:
    total = 0
    if not path.exists():
        return 0
    for p in path.rglob("*"):
        try:
            if p.is_file():
                total += p.stat().st_size
        except (OSError, PermissionError):
            # skip entries we can't stat
            continue
    return total


def format_bytes(n: float) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while n >= 1000 and i < len(units) - 1:
        n /= 1000.0
        i += 1
    return f"{n:.2f}{units[i]}"


if __name__ == "__main__":
    main()
