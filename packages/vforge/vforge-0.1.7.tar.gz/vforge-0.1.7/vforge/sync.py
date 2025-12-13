from vforge import helpers
import pathlib
from stdlib_list import stdlib_list
import subprocess
import sys


def main():
    log = helpers.make_logger()

    # fetch arguments
    args_dict = helpers.parse_args(["project-dir"])

    # directory validation
    project_dir = pathlib.Path(args_dict["project_dir"])
    helpers.validate_directory(project_dir, False)

    # find the virtual environment
    venv_path = helpers.get_venv_path(project_dir)

    # check for explicit requirements and excluded packages
    explicit, exclude = helpers.load_user_config(project_dir)

    # normalize exclude and stdlib to comparison set
    exclude_set = {helpers.normalize_name(e) for e in exclude}

    # determine set of builtins
    major, minor, *_ = sys.version_info
    log.debug(f"Detected Python verson {major}.{minor}")
    if (major, minor) < (3, 10):
        stdlib_set = set(stdlib_list(f"{major}.{minor}"))
    else:
        # only available for >= 3.10
        stdlib_set = set(sys.stdlib_module_names)

    # upgrade pip
    pip = helpers.program_path(venv_path, "pip")
    subprocess.check_call([str(pip), "install", "--upgrade", "pip"])

    # install explicit (one-by-one so failures are isolated)
    for requirement in explicit:
        subprocess.run([str(pip), "install", "--no-deps", requirement], check=True)

    # include explicit's dependencies if not excluded
    dependencies = fetch_deps_minus_exclude(pip, explicit, exclude_set)
        
    log.info(f"Installed {len(explicit)} explicitly defined requirements.")

    # discover imports but exclude stdlib and project-state dirs (scan_directory avoids venv & .vforge)
    import_to_dist = helpers.map_imports_to_dists_from_venv(project_dir)
    unique_imports = helpers.scan_directory(project_dir)
    log.debug(f"Scanned project directory for imports: {len(unique_imports)} roots found.")

    if exclude_set:
        log.warning("Will install dependencies directly to avoid accidentally installing any packages in your exclude list. This will be slower.")

        # grab all dependencies and eliminate the excludes
        dependencies += fetch_deps_minus_exclude(pip, unique_imports, exclude_set)

    dependencies = list(set(dependencies))
    candidates = []
    for pkg in unique_imports + dependencies:
        n = helpers.normalize_name(pkg)
        if any([n in exclude_set, pkg in exclude_set, n in stdlib_set, pkg in stdlib_set, pkg in import_to_dist]):
            continue

        # final is_installable check using pip path
        if is_installable(pkg, pip):
            candidates.append(pkg)

    # install auto candidates
    failed_packages = []

    if exclude_set:
        # download but manually supply dependencies
        for pkg in candidates:
            try:
                subprocess.run([str(pip), "install", "--no-deps", pkg], check=True)
            except subprocess.CalledProcessError as e:
                # Log the failure
                log.error(f"Failed to install package {pkg}: {e}")
                failed_packages.append(pkg)
    else:
        # simpler case, let pip resolve dependencies
        for pkg in candidates:
            try:
                subprocess.run([str(pip), "install", pkg], check=True)
            except subprocess.CalledProcessError as e:
                # Log the failure
                log.error(f"Failed to install package {pkg}: {e}")
                failed_packages.append(pkg)

    if failed_packages:
        log.warning(f"Some packages failed to install: {failed_packages}")
    log.info(f"Installed {len(candidates)} auto-detected packages.")

    log.info("Sync complete!")


def is_installable(package_name: str, pip_path) -> bool:
    # checks if a package is installable via pip
    pip_str = str(pip_path)

    # prefer `pip index versions <pkg>` (does not install) when supported
    try:
        res = subprocess.run([pip_str, "index", "versions", package_name],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return res.returncode == 0
    except Exception:
        # fallback to pip install --dry-run if supported; otherwise assume installable
        try:
            subprocess.run([pip_str, "install", "--dry-run", package_name],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            return True
        except subprocess.CalledProcessError:
            return False
        except Exception:
            # unknown pip; optimistically allow installation
            return True


def fetch_deps_minus_exclude(pip, root_pkgs: list[str], exclude = set):
    # installs root package/requirement plus all deps, as long as none are in exclude
    # root_pkgs can be just package names or requirements, doesn't matter

    # get base package names for all roots and screen them
    root_bases = [helpers.extract_base_package(root.strip()) for root in root_pkgs if root not in exclude]

    # now pull dependencies for roots
    dependencies = list()
    packages_and_deps_dict = helpers.get_installed_packages_and_deps(pip, root_bases)

    # screen dependencies
    for dep_list in packages_and_deps_dict.values():
        dependencies += dep_list
    dependencies = [dep for dep in set(dependencies) if dep not in exclude]
    return dependencies


if __name__ == "__main__":
    main()