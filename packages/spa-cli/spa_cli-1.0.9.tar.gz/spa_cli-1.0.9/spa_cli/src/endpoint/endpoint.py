from ...globals import load_config
from ..utils.folders import validate_path_not_exist
from ..utils.strings import camel_case
from ..utils.template_gen import copy_template_file

import os
import typer
from pathlib import Path

app = typer.Typer()

@app.command('add')
def new_endpoint(
        method: str = typer.Option(..., help='Metodo de la peticion. Valores permitidos [GET, POST, PUT, PATCH, DELETE]'),
        path: str = typer.Option(..., help='Path del endpoint.'),
        endpoint_name: str = typer.Option(help='Nombre de la funcion lambda.')
    ):
    
    if "-" in endpoint_name or " " in endpoint_name:
        typer.echo('El nombre de la lambda no debe contener espacios o guiones. Se modificará por guiones bajos.', color=typer.colors.YELLOW)
        endpoint_name = endpoint_name.replace("-", "_").replace(" ", "_")
    
    config = load_config()
    camel_name = camel_case(endpoint_name)
    
    lambda_template_path = Path(config.template.files.lambda_function)
    lambda_test_template_path = Path(config.template.files.test_lambda)
    lambda_conf_template_path = Path(config.template.files.lambda_conf)
    lambda_endpoint_template_path = Path(config.template.files.endpoint)
    
    lambda_output_folder_path = Path(config.project.folders.lambdas)

    try:
        model_exists = validate_path_not_exist(path=lambda_output_folder_path.joinpath(endpoint_name), custom_error_message=f'Ya existe una ruta con nombre: {endpoint_name}', abort=False)
    except Exception as e:
        typer.echo(str(e))
    
    if not model_exists:
        os.mkdir(lambda_output_folder_path.joinpath(endpoint_name))
    
    copy_template_file(
        template_path=lambda_template_path,
        destination_path=lambda_output_folder_path.joinpath(endpoint_name).joinpath('lambda_function.py'),
        code_format_override={}
    )
    
    copy_template_file(
        template_path=lambda_test_template_path,
        destination_path=lambda_output_folder_path.joinpath(endpoint_name).joinpath('test_lambda_function.py'),
        code_format_override={
            "camel_name": camel_name,
            "lambda_name": endpoint_name
        }
    )
    
    copy_template_file(
        template_path=lambda_conf_template_path,
        destination_path=lambda_output_folder_path.joinpath(endpoint_name).joinpath('infra_config.py'),
        code_format_override={
            "lambda_name": endpoint_name,
            "camel_name": camel_name
        }
    )
    
    copy_template_file(
        template_path=lambda_endpoint_template_path,
        destination_path=lambda_output_folder_path.joinpath(endpoint_name).joinpath('endpoint.yaml'),
        code_format_override={
            "endpoint_url": path,
            "endpoint_method": method.lower(),
        }
    )

    typer.echo(f'La ruta {path} [{method}] se agrego correctamente!', color=typer.colors.GREEN)

