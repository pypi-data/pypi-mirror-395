import os
import json
import shutil
from typing import cast
from cookiecutter.main import cookiecutter
from functools import wraps
from typing import Any, Callable, Dict
from pathlib import Path
from ...globals import Constants

def generate_project_template(project_name: str,
                            author_name: str,
                            author_email: str,
                            db_engine: str,
                            db_driver: str,
                            aws_region: str,
                            secret_name: str,
                            pattern_version = 'main',
                            project_description: str = 'Autogenerado por SPA-CLI'):
    """Descarga y configura el template de patron para Serverless

    Args:
        project_name (str): Nombre del proyecto
        author_name (str): Nombre del autor
        author_email (str): Email del autor
        db_engine (str): Motor de base de datos
        db_driver (str): Driver de base de datos
        aws_region (str): Región de AWS para el proyecto
        secret_name (str): Nombre del secreto en AWS Secret Manager
        pattern_version (str, optional): Rama o tag de github a utilizar del template. Lates utiliza la rama main.
        project_description (str, optional): Descripción del proyecto. Defaults to 'Autogenerado por SPA-CLI'.
    """
    config_override = {
        "directory_name": project_name,
        "develop_branch": "main",
        "dbDialect": db_engine,
        "_dbDriver": db_driver,
        "project_short_description": project_description,
        "aws_region": aws_region,
        "author_name": author_name,
        "author_email": author_email,
        "db_secret_name": secret_name
    }

    cookiecutter_kwargs = {
        "directory": "code",
        "overwrite_if_exists": True,
        "no_input": True,
        "extra_context": config_override
    }
    if pattern_version != 'latest':
        cookiecutter_kwargs.update({"checkout": pattern_version})
    
    template_url = Constants.PROJECT_TEMPLATE.value
    cookiecutter(template_url, **cookiecutter_kwargs)

def add_code_to_module(template_path: Path, module_path: Path, modelName: str, code_format_override: dict):
    module_code = template_path.read_text().format(**code_format_override)
    module_path.joinpath(f'{modelName}.py').write_text(module_code)

def add_file_to_module(module_path: Path, modelName: str, replace_import: str = None):
    module_text = module_path.joinpath('__init__.py').read_text()
    module_text += f"\nfrom .{modelName} import {modelName}" if replace_import is None else f"\nfrom .{modelName} import {replace_import}"
    module_path.joinpath('__init__.py').write_text(module_text)

def copy_template_file(template_path: Path, destination_path: Path, code_format_override: dict):
    module_code = template_path.read_text().format(**code_format_override)
    destination_path.write_text(module_code)


def read_project_config():
    local_project_dir = Path(os.getcwd()).joinpath('.spa')

    try:
        with open(local_project_dir.joinpath('project.json'), 'r') as f:
            project_config = cast(dict, json.load(f))
    except Exception as e:
        raise e
    
    return project_config


