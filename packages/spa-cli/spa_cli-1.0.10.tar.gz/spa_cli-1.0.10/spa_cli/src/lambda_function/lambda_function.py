from ...globals import load_config
from ..utils.folders import validate_path_not_exist
from ..utils.strings import camel_case
from ..utils.template_gen import copy_template_file

import os
import typer
from pathlib import Path

app = typer.Typer()

@app.command('add')
def new_lambda(
        lambda_name: str = typer.Option(help='Nombre de la funcion lambda.')
    ):
    config = load_config()
    
    if "-" in lambda_name or " " in lambda_name:
        typer.echo('El nombre de la lambda no debe contener espacios o guiones. Se modificará por guiones bajos.', color=typer.colors.YELLOW)
        lambda_name = lambda_name.replace("-", "_").replace(" ", "_")
    camel_name = camel_case(lambda_name)
    
    lambda_template_path = Path(config.template.files.lambda_function)
    lambda_test_template_path = Path(config.template.files.test_lambda)
    lambda_conf_template_path = Path(config.template.files.lambda_conf)
    
    lambda_output_folder_path = Path(config.project.folders.lambdas)

    try:
        model_exists = validate_path_not_exist(path=lambda_output_folder_path.joinpath(lambda_name), custom_error_message=f'Ya existe una ruta con nombre: {lambda_name}', abort=False)
    except Exception as e:
        typer.echo(str(e))
    
    if not model_exists:
        os.mkdir(lambda_output_folder_path.joinpath(lambda_name))
    
    copy_template_file(
        template_path=lambda_template_path,
        destination_path=lambda_output_folder_path.joinpath(lambda_name).joinpath('lambda_function.py'),
        code_format_override={}
    )
    
    copy_template_file(
        template_path=lambda_test_template_path,
        destination_path=lambda_output_folder_path.joinpath(lambda_name).joinpath('test_lambda_function.py'),
        code_format_override={
            "camel_name": camel_name,
            "lambda_name": lambda_name
        }
    )
    
    copy_template_file(
        template_path=lambda_conf_template_path,
        destination_path=lambda_output_folder_path.joinpath(lambda_name).joinpath('infra_config.py'),
        code_format_override={
            "lambda_name": lambda_name,
            "camel_name": camel_name
        }
    )

    typer.echo(f'La lambda {lambda_name} se agrego correctamente!', color=typer.colors.GREEN)

