from vforge import helpers
import pathlib
import shutil
import subprocess
import sys
import venv
import yaml


def main():
    log = helpers.make_logger()

    # fetch arguments
    args_dict = helpers.parse_args([
        "venv-name", "target-dir", "project-dir", "sync"
    ])

    # directory validation
    directories = dict()
    dir_list = ["target_dir", "project_dir"]
    for dir_key in dir_list:
        # retrieve the dir
        directories[dir_key] = pathlib.Path(args_dict[dir_key])

        # directory validation
        helpers.validate_directory(directories[dir_key])

    # prompt if venv would overwrite an existing directory
    venv_path = directories["target_dir"] / args_dict["venv_name"]
    if venv_path.exists():
        reply = input(f"{venv_path} already exists. Overwrite? [y/N]: ").strip().lower()
        if reply != "y":
            raise SystemExit("Aborted: directory already exists.")
        # user approved overwrite
        log.warning(f"Overwriting contents of {venv_path}")
        if venv_path.is_dir():
            # it's a directory -> delete it
            shutil.rmtree(venv_path)
        else:
            # it's a file -> delete it
            venv_path.unlink()

    # build the environment
    log.debug("Building your environment now!")
    try:
        builder = venv.EnvBuilder(
            system_site_packages=False,
            clear=True,
            with_pip=True
        )
        builder.create(str(venv_path))
    except (PermissionError, FileExistsError, OSError) as e:
        # delete the half-baked environment and log error
        shutil.rmtree(venv_path)
        log.error(f"Failed to create virtual environment at {venv_path}: {e}")
        sys.exit(1)
    except Exception as e:
        # delete the half-baked environment and log error
        shutil.rmtree(venv_path)
        log.error(f"Unexpected error during virtual environment creation: {e}")
        sys.exit(1)

    # create config file
    config_dir = directories["project_dir"] / ".vforge"
    config_dir.mkdir(exist_ok=True)

    # vforge config
    vforge_config_path = config_dir / "vforge_config.yaml"
    with open(vforge_config_path, "w") as file:
        config_data = {
            "venv_path": str(venv_path)
        }
        yaml.dump(config_data, file, default_flow_style=False, sort_keys=False)
    log.warning(f"Created vforge config file at {vforge_config_path}. DO NOT ALTER THIS FILE.")

    # user config file
    user_config_path = config_dir / "user_config.txt"
    with open(user_config_path, "w") as file:
        file.write("# explicit\n")
        file.write("# Add explicit requirements here (e.g., pandas==2.1.0)\n")
        file.write("# One per line\n\n")

        file.write("# exclude\n")
        file.write("# Add packages to exclude from auto install\n")
        file.write("# One per line\n")

    log.info(f"Created user config file at {user_config_path}.")

    # run vforge sync to scan for packages + install them
    if (args_dict["sync"]).lower() == "y":
        log.info("running sync")
        command = ["vforge", "sync", "--project-dir", str(directories["project_dir"])]
        subprocess.run(command)


if __name__ == "__main__":
    main()