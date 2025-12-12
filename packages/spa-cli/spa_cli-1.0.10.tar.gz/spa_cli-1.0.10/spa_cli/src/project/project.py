from ...globals import Constants, DRIVERS, load_config
from ..utils.template_gen import generate_project_template
from ..utils.install_local_layers import install_layers, build_layers
from ..utils.up_local_server import main as up_local_server
from ..utils.build import build_lambdas, build_lambda_stack, build_api

import os
import re
import json
import typer
from typing import cast
from click.types import Choice
from pathlib import Path
from shutil import copytree, rmtree, copy2

app = typer.Typer()

@app.command('init')
def init_project(
        pattern_version: str = typer.Option(help='Version del patron.', default='latest')
    ):
    """
    Genera un nuevo proyecto con template
    """
    db_config = {
        "db_engine": None,
        "db_driver": None,
        "secret_name": '',
    }
    project_name = typer.prompt("Nombre del proyecto")
    project_description = typer.prompt("Descripción del proyecto")
    
    author_name = typer.prompt("Nombre del autor", default=os.getlogin())
    author_email = typer.prompt("Email del autor", default="")

    dbChoices = Choice([
        Constants.MYSQL_ENGINE.value,
        Constants.POSTGRESQL_ENGINE.value
    ])
    db_config['db_engine'] = typer.prompt(
        "Elija su motor de base de datos",
        Constants.MYSQL_ENGINE.value,
        show_choices=True,
        type=dbChoices
    )
    
    aws_region = typer.prompt("Región de AWS", default="us-east-1")
    
    db_config['db_driver'] = DRIVERS[Constants.MYSQL_ENGINE.value]
    db_config['secret_name'] = typer.prompt("Escriba el nombre del secreto para las credenciales de la base de datos - Revise la documentación para el formato correcto")
    
    generate_project_template(
        project_name,
        author_name=author_name,
        author_email=author_email,
        **db_config,
        aws_region=aws_region,
        pattern_version=pattern_version,
        project_description=project_description
    )
        
    
    local_project_dir = Path(os.getcwd()).joinpath(project_name).joinpath('.spa')
    if not local_project_dir.exists():
        os.mkdir(local_project_dir)
    
    with open(local_project_dir.joinpath('project.json'), 'w') as f:
        json.dump({
            "project_name": project_name,
            "dbDialect": db_config['db_engine'],
            "pattern_version": pattern_version
        }, f)
    

@app.command('install')
def install_project():
    try:
        project_config = load_config()
    except:
        typer.echo('No se puedo leer la configuracion del proyecto', color=typer.colors.RED)
        raise typer.Abort()
    install_layers(project_config)

@app.command('run-api')
def run_app():
    try:
        project_config = load_config()
    except:
        typer.echo('No se puedo leer la configuracion del proyecto', color=typer.colors.RED)
        raise typer.Abort()
    
    typer.echo('Iniciando servidor local')
    up_local_server(project_config)
    

@app.command('build')
def build_project():
    try:
        project_config = load_config()
    except:
        typer.echo('No se puedo leer la configuracion del proyecto', color=typer.colors.RED)
        raise typer.Abort()
    
    typer.echo('Construyendo proyecto')
    build_path = Path(os.getcwd()).joinpath('build')
    if build_path.exists():
        for item in os.listdir(build_path):
            item_path = os.path.join(build_path, item)
            if os.path.isdir(item_path):
                try:
                    rmtree(item_path)
                    typer.echo(f"Deleted directory: {item_path}")
                except OSError as e:
                    typer.echo(f"Error deleting directory '{item_path}': {e}")
        
        rmtree(build_path)
        typer.echo(f"Deleted directory: {build_path}")
    os.mkdir(build_path)

    copytree(
        Path(os.getcwd()).joinpath('infra'),
        build_path.joinpath('infra'),
        dirs_exist_ok=True
    )
    
    for filename in os.listdir(Path(os.getcwd())):
        if re.compile(r'Pulumi.*').match(filename):
            source_path = os.path.join(Path(os.getcwd()), filename)
            destination_path = os.path.join(build_path, filename)
            try:
                copy2(source_path, destination_path)
                typer.echo(f"Copied '{filename}' to '{build_path}'")
            except Exception as e:
                typer.echo(f"Error copying '{filename}': {e}", color=typer.colors.RED)
    
    copy2(Path().cwd() / 'pyproject.toml', build_path / 'pyproject.toml')

    layers_path = Path(os.getcwd()) / project_config.project.folders.layers
    lambdas_path = Path(os.getcwd()) / project_config.project.folders.lambdas
    output_layers_path = build_path / 'tmp_build_layer'

    typer.echo(f'Building layers from {layers_path} into {output_layers_path}...')
    build_layers(layers_path, output_layers_path)

    typer.echo(f'Building lambdas from {lambdas_path}...')
    build_lambdas(lambdas_path, build_path.joinpath('infra') / 'components' / 'lambdas')

    typer.echo('Building lambda stack...')
    build_lambda_stack(
        build_lambdas_path=build_path.joinpath('infra') / "components" / "lambdas",
        environment=os.getenv("ENVIRONMENT") or "dev",
        app_name=os.getenv("APP_NAME") or cast(str, project_config.project.definition.name)
    )

    typer.echo('Building API definition...')
    build_api(
        api_path=Path(project_config.project.definition.base_api),
        lambdas_path=build_path.joinpath('infra') / "components" / "lambdas",
        output_file=build_path.joinpath('infra') / "components" / "openapi.json"
    )

    typer.echo('Build completed.')
