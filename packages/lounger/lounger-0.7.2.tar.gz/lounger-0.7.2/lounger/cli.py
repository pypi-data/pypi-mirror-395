"""
lounger CLI
"""
import os
from pathlib import Path

import click
from pytest_req.log import log

from lounger import __version__


@click.command()
@click.version_option(version=__version__, help="Show version.")
@click.option("-pw", "--project-web", help="Create an Web automation test project.")
@click.option("-pa", "--project-api", help="Create an API automation test project.")
def main(project_web, project_api):
    """
    lounger CLI.
    """

    if project_web:
        create_scaffold(project_web, "web")
        return 0

    if project_api:
        create_scaffold(project_api, "api")
        return 0

    return None


def create_scaffold(project_name: str, type: str) -> None:
    """
    Create a project scaffold with the specified name and type.

    :param project_name: Name of the project (folder)
    :param type: Project type, one of "api", "web", "yapi"
    """
    project_root = Path(project_name)

    # Check if project already exists
    if project_root.exists():
        log.info(f"Folder {project_name} already exists. Please specify a new folder name.")
        return

    log.info(f"Start to create new test project: {project_name}")
    log.info(f"CWD: {os.getcwd()}\n")

    # Shared paths
    current_file = Path(__file__).resolve()
    template_base = current_file.parent / "project_temp"

    # Ensure project root exists
    project_root.mkdir(parents=True, exist_ok=True)

    # Create reports folder
    (project_root / "reports").mkdir(exist_ok=True)
    log.info("📁 created folder: reports")

    # Define Add conftest.py (shared)
    file_mappings = [(template_base / "conftest.py", "conftest.py")]

    if type == "web":
        file_mappings.extend([
            (template_base / "web" / "pytest.ini", "pytest.ini"),
            (template_base / "__init__.py", "test_dir/__init__.py"),
            (template_base / "web" / "test_dir" / "test_sample.py", "test_dir/test_sample.py")
        ])

    elif type == "api":
        file_mappings.extend([
            (template_base / "api" / "pytest.ini", "pytest.ini"),
            (template_base / "api" / "test_api.py", "test_api.py"),
            (template_base / "api" / "config" / "config.yaml", "config/config.yaml"),
            (template_base / "api" / "datas" / "sample" / "test_sample.yaml", "datas/sample/test_sample.yaml"),
            (template_base / "__init__.py", "test_dir/__init__.py"),
            (template_base / "api" / "test_dir" / "test_sample.py", "test_dir/test_sample.py"),
        ])
    else:
        log.error(f"Unsupported project type: {type}. Choose from 'api', 'web'.")
        return

    # Copy all template files
    for src_path, dest_rel in file_mappings:
        try:
            content = src_path.read_text(encoding="utf-8")
            dest_path = project_root / dest_rel

            # Ensure parent dir exists
            dest_path.parent.mkdir(parents=True, exist_ok=True)

            dest_path.write_text(content, encoding="utf-8")
            log.info(f"📄 created file: {dest_rel}")
        except Exception as e:
            log.error(f"Failed to create {dest_rel}: {e}")

    log.info(f"🎉 Project '{project_name}' created successfully.")
    log.info(f"👉 Go to the project folder and run 'pytest' to start testing.")


if __name__ == '__main__':
    main()
