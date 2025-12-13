from vforge import helpers
import pathlib
import subprocess
import sys


def main():
    # fetch arguments
    args_dict = helpers.parse_args([
        "out-dir", "project-dir"
    ])
    log = helpers.make_logger()

    # directory validation
    directories = dict()
    dir_list = ["project_dir", "out_dir"]
    for dir_key in dir_list:
        # retrieve the dir
        directories[dir_key] = pathlib.Path(args_dict[dir_key])

        # directory validation
        helpers.validate_directory(directories[dir_key])

    # find the virtual environment
    venv_path = helpers.get_venv_path(directories["project_dir"])
    
    # get pip
    pip = helpers.program_path(venv_path, "pip")

    # run pip freeze and send to target directory
    try:
        result = subprocess.run([pip, "freeze"], check=True, capture_output=True, text=True)
        out_path = directories["out_dir"] / "requirements.txt"
        out_path.write_text(result.stdout)
        log.info("requirements.txt created successfully.")
        log.warning("NOTE: This is for documentation only. Updating requirements.txt will not impact any vforge operations.")
    except subprocess.CalledProcessError as e:
        log.error(f"Error executing command: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()