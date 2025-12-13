import argparse
import ast
import json
import logging
import os
import pathlib
import re
import subprocess
import sys
import yaml


# regexp pattern for isolating base package names
NAME_RE = re.compile(r"^[A-Za-z0-9_.-]+")


# class definition to enable color refs for logging
class Color:
    RESET = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"


class ColorFormatter(logging.Formatter):
    # pairs log severity levels with colors
    COLORS = {
        logging.DEBUG: Color.BLUE,
        logging.INFO: Color.GREEN,
        logging.WARNING: Color.YELLOW,
        logging.ERROR: Color.RED,
        logging.CRITICAL: Color.RED,
    }

    # displays the message in the right color
    def format(self, record):
        color = self.COLORS.get(record.levelno, Color.RESET)
        msg = super().format(record)
        return f"{color}{msg}{Color.RESET}"


def make_logger(name="vforge", level=logging.INFO):
    # initializes the logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(ColorFormatter("%(levelname)s: %(message)s"))
        logger.addHandler(handler)
    return logger


def validate_directory(path, is_venv=False):
    # ensures path exists and is a directory
    log = make_logger()
    log.debug(f"Checking {path}")
    path = pathlib.Path(path)
    if not path.exists():
        log.error(f"Directory {path} does not exist.")
        sys.exit(1)

    if not path.is_dir():
        log.error(f"Path {path} is not a directory.")
        sys.exit(1)

    # additional validation: ensure venv_path is a true virtual env
    if is_venv:
        pip = program_path(path, "pip")
        if not pip.exists():
            log.critical(f"Invalid virtual environment: pip not found at {pip}. Try re-running vforge init!")
            sys.exit(1)


def _extract_python_source_from_ipynb(path):
    # read Jupyter Notebooks and extract Python code
    # fails gracefully by skipping cell if an error is hit
    try:
        raw = path.read_text(encoding="utf8")
    except Exception:
        return ""  # unreadable file

    try:
        data = json.loads(raw)
    except Exception:
        return ""  # malformed JSON

    chunks = []
    for cell in data.get("cells", []):
        try:
            # exclude markdown and raw cells
            if cell.get("cell_type") != "code":
                continue
            src = cell.get("source", [])
            # handle both types of formatting
            if isinstance(src, list):
                chunks.append("".join(src))
            elif isinstance(src, str):
                chunks.append(src)
        except Exception:
            continue  # ignore malformed cell

    return "\n".join(chunks)


def _find_imports_in_file(path: pathlib.Path):
    # AST parses python file to locate all package imports
    if path.suffix == ".py":
        source = path.read_text(encoding="utf8")
    elif path.suffix == ".ipynb":
        source = _extract_python_source_from_ipynb(path)
    else:
        return []


    try:
        tree = ast.parse(source)
    except SyntaxError:
        # source code contains syntax errors, skip it
        log = make_logger()
        log.critical(f"Python script {path} contains SyntaxErrors. vforge cannot parse for dependencies unless you fix the error or comment it out!")
        return []

    imports = list()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                # covers import matplotlib.pyplot -> matplotlib
                imports.append(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.level > 0:
                continue  # relative import -> skip
            if node.module:  # filters out empty string
                root = node.module.split(".")[0]
                imports.append(root)

    return imports


def normalize_name(name: str) -> str:
    # Lowercase and normalize simple dash/underscore variants for matching
    if not name:
        return ""
    n = name.lower().strip()
    return n.replace("-", "_")


def scan_directory(project_path):
    """
    Recursively scan project for import roots in .py and .ipynb files.
    Skips .vforge, .git, and the venv directory (if present in project).
    Returns a deduplicated list of import root names (not starting with '_').
    """
    project_path = pathlib.Path(project_path).resolve()
    imports = set()

    # always exclude .vforge and .git
    exclude_dirs = {".vforge", ".git"}

    # also exclude venv dir if vforge_config points to it and it's inside project
    try:
        venv_candidate = get_venv_path(project_path)
        # if venv inside project, exclude its name
        try:
            if venv_candidate.exists() and venv_candidate.resolve().is_relative_to(project_path):
                exclude_dirs.add(venv_candidate.name)
        except Exception:
            # Python <3.9 doesn't have is_relative_to — fallback
            try:
                if str(venv_candidate.resolve()).startswith(str(project_path) + os.sep):
                    exclude_dirs.add(venv_candidate.name)
            except Exception:
                pass
    except Exception:
        # try anyway
        pass

    for file in project_path.rglob("*"):
        # skip anything under excluded directories
        if any(part in exclude_dirs for part in file.parts):
            continue
        if file.suffix not in (".py", ".ipynb"):
            # _find_imports_in_file also excludes non py/ipynb, but better to be defensive
            continue
        for imp in _find_imports_in_file(file):
            if not imp or imp.startswith("_"):
                continue
            imports.add(normalize_name(imp))

    return sorted(imports)


def program_path(venv_path: pathlib.Path, program: str) -> pathlib.Path:
    # Retrieves pip or python path depending on OS
    venv_path = pathlib.Path(venv_path)
    if sys.platform == "win32":
        return venv_path / "Scripts" / f"{program}.exe"
    else:
        return venv_path / "bin" / f"{program}"


def extract_base_package(requirement_line: str) -> str:
    # isolate the base package name from the user config file
    m = NAME_RE.match(requirement_line.strip())
    return normalize_name(m.group(0)) if m else ""


def load_vforge_config(project_dir):
    # locates the vforge config file and returns it as dictionary
    # helper function to get_venv_path as venv_path currently only parameter in here
    config_path = pathlib.Path(project_dir) / ".vforge" / "vforge_config.yaml"
    log = make_logger()
    try:
        # read the file and return dictionary (healthy case)
        with open(config_path, 'r') as file:
            config_data = yaml.safe_load(file)
            return config_data
    except FileNotFoundError:
        log.error(f"Error: '{config_path}' not found. Re-run vforge init.")
        sys.exit(1)
    except yaml.YAMLError as e:
        # corrupt or improper yaml file. can't proceed, must error out
        log.error(f"Error parsing YAML file: {e}. Fix the file or re-run vforge init.")
        sys.exit(1)


def get_venv_path(project_dir):
    # reads the vforge config file and returns the path to the venv

    log = make_logger()
    # find the virtual environment
    vforge_config = load_vforge_config(project_dir)
    venv_path = pathlib.Path(vforge_config["venv_path"])

    # validate virtual environment path
    validate_directory(venv_path, True)
    venv_name = venv_path.name
    log.info(f"Found the {venv_name} virtual environment")

    return venv_path


def parse_args(args: list):
    # helper function used by all scripts to read in the arguments provided
    parser = argparse.ArgumentParser()
    for arg in args:
        parser.add_argument(f"--{arg}", type=str)
    return vars(parser.parse_args())


def list_installed_packages(pip_path: pathlib.Path) -> list:
    """
    Return dict of {package_name_lower: [dependency_name_lower, ...]} for all
    packages in the venv, using venv's pip. Works across pip versions.
    """
    log = make_logger()
    # get installed packages via pip list --format=json
    try:
        out = subprocess.check_output([str(pip_path), "list", "--format=json"], text=True)
        pkg_list = json.loads(out)
    except subprocess.CalledProcessError as e:
        log.critical(f"Error parsing YAML file: {e}. Fix the file or re-run vforge init.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        log.critical(f"Invalid JSON from pip list: {e}")
        sys.exit(1)

    # pip list returns list of {"name":..., "version":...}
    names = list(set([normalize_name(p["name"]) for p in pkg_list]))
    return names


def get_installed_packages_and_deps(pip_path: pathlib.Path, names=None):
    """
    Return dict of {package_name_lower: [dependency_name_lower, ...]} for all
    packages in the venv, using venv's pip. Works across pip versions.
    Tells us: 
        1) which distributions are installed
        2) which distributions depend on which others.
    Goal: distribution → [its dependency distributions]
    Reads the Requires output of pip show to determine these dependencies
    """
    if not names:  # use pip_path
        # get installed packages via pip list
        names = list_installed_packages(pip_path)

    # For each package request pip show to get Requires field
    installed = {}
    for name in names:
        deps = []
        try:
            out = subprocess.check_output([str(pip_path), "show", name], text=True)

            # pip show returns lines like "Requires: pkg1, pkg2"
            req_line = next((ln for ln in out.splitlines() if ln.startswith("Requires:")), "")
            if req_line:
                reqs = req_line.partition(":")[2].strip()
                if reqs:
                    # split by comma, strip spaces, lower-case
                    deps = [normalize_name(r.strip().split()[0]) for r in reqs.split(",") if r.strip()]
        except subprocess.CalledProcessError:
            # pip show failed for this package; treat as no deps
            deps = []
        installed[name] = deps

    return installed


def map_imports_to_dists(pip_path: pathlib.Path):
    """
    Reads Files output of pip show to match import name to package name, see below
    Goal: import_name → distribution_name (ex. yaml -> PyYAML; bs4 -> beautifulsoup4)
    """
# helpers.py — add this function (requires existing program_path)
import json
from pathlib import Path
import subprocess
from typing import Dict, Set, List

def _venv_site_packages(venv_python: Path) -> List[str]:
    """
    Ask the venv Python for an authoritative site-packages path.
    Returns a list (ordered) of candidate site-packages paths; caller takes the first that exists.
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
            "print(json.dumps(paths))\n"
        ),
    ]
    out = subprocess.check_output(cmd, text=True).strip()
    try:
        paths = json.loads(out)
        return paths if isinstance(paths, list) else []
    except Exception:
        return []

def map_imports_to_dists_from_venv(project_dir: Path) -> Dict[str, str]:
    """
    Build a mapping import_root -> distribution name for the given venv.
    Returns a dict mapping top-level import names (lowercase) to distribution names (lowercase).
    """
    log = make_logger()
    # Resolve venv python
    venv_path = get_venv_path(project_dir)
    venv_python = program_path(venv_path, "python")
    if not venv_python.exists():
        # defensive: try to use venv_path if caller passed python already
        log.error(f"venv python not found at {venv_python!s}. Re-run vforge init.")
        sys.exit(1)

    # Ask venv python for site-packages candidates
    site_candidates = _venv_site_packages(venv_python)

    site_pkg = None
    for p in site_candidates:
        if p and Path(p).exists():
            site_pkg = Path(p)
            break
    if site_pkg is None:
        # Last-ditch fallback: try common layout using sys.version_info from venv python
        # Query minor/major
        try:
            ver_out = subprocess.check_output([str(venv_python), "-c", "import sys; print(f'{sys.version_info[0]}.{sys.version_info[1]}')"], text=True).strip()
            guess = venv_path / "lib" / f"python{ver_out}" / "site-packages"
            if guess.exists():
                site_pkg = guess
        except Exception:
            pass

    if site_pkg is None:
        raise SystemExit("Could not find site-packages for venv. Aborting mapping.")

    mapping: Dict[str, str] = {}
    # iterate dist-info directories
    for distinfo in site_pkg.glob("*.dist-info"):
        distname = None
        top_levels: Set[str] = set()
        # read top_level.txt if present (preferred)
        top_path = distinfo / "top_level.txt"
        if top_path.exists():
            try:
                raw = top_path.read_text(encoding="utf8")
                for ln in raw.splitlines():
                    ln = ln.strip()
                    if ln:
                        top_levels.add(ln.lower())
            except Exception:
                pass

        # parse METADATA / PKG-INFO to get canonical distribution name if needed
        metadata_name = None
        for meta_file in ("METADATA", "PKG-INFO"):
            mf = distinfo / meta_file
            if mf.exists():
                try:
                    for ln in mf.read_text(encoding="utf8").splitlines():
                        if ln.startswith("Name:"):
                            metadata_name = ln.partition(":")[2].strip().lower()
                            break
                except Exception:
                    pass
                if metadata_name:
                    break

        # fallback: attempt to infer distribution "directory name" from dist-info filename
        if metadata_name:
            distname = metadata_name
        else:
            # distinfo name like 'snowflake_connector_python-2.9.0.dist-info'
            name_part = distinfo.name.rsplit("-", 1)[0]
            distname = name_part.replace("_", "-").lower()

        # If top_level.txt was missing, try to infer top-level package directories
        if not top_levels:
            # Many wheels include package directories right next to dist-info
            # gather candidate roots by scanning site-packages for dirs/files with same prefix
            # Heuristic: list entries that share the same normalized prefix as distinfo name
            candidate_roots = set()
            # scan immediate children of site-packages for folders/files
            for entry in site_pkg.iterdir():
                if entry.name.endswith(".dist-info"):
                    continue
                if entry.name.endswith(".egg-info"):
                    continue
                # package folder (pkg/) or single-file module (pkg.py)
                if entry.is_dir():
                    candidate_roots.add(entry.name.lower())
                elif entry.is_file() and entry.suffix == ".py":
                    candidate_roots.add(entry.stem.lower())

            # attempt to match reasonable candidates to the distribution name
            # e.g. distname 'snowflake-connector-python' → try 'snowflake', 'connector', 'python'
            tokens = set(distname.replace("-", " ").replace("_", " ").split())
            for cand in candidate_roots:
                # if any token of distname is prefix of candidate or vice-versa, accept it
                if any(tok and (cand == tok or cand.startswith(tok) or tok.startswith(cand)) for tok in tokens):
                    top_levels.add(cand)

        # finally populate mapping
        for t in top_levels:
            mapping[t] = distname

    return mapping


def load_user_config(project_path):
    # read user config and return lists of requirements and exclusions

    log = make_logger()
    config_path = pathlib.Path(project_path) / ".vforge" / "user_config.txt"
    explicit = []
    exclude = []

    # strategy: iterate over lines and determine which of the 2 sections we're in
    # then, read in that respective info
    current = None  # "explicit" or "exclude"

    try:
        lines = config_path.read_text(encoding="utf8").splitlines()
    except FileNotFoundError:
        log.warning("user_config.txt is missing from .vforge. This is probably fine unless accidentally deleted. If so, re-run vforge init.")
        return explicit, exclude

    for line in lines:
        stripped = line.strip()

        if not stripped:
            continue  # skip blank lines

        if stripped.startswith("#"):
            # comment
            header = stripped.lstrip("#").strip().lower()
            if header.startswith("explicit"):
                # explicit requirement section
                current = "explicit"
            elif header.startswith("exclude"):
                # package exclusion section
                current = "exclude"
            else:
                current = None
            continue

        if current == "explicit":
            explicit.append(stripped)

        elif current == "exclude":
            base = extract_base_package(stripped)
            if base:
                exclude.append(base)

    return explicit, exclude