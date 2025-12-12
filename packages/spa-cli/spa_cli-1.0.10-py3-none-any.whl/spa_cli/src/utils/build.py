import os
import json
import tqdm
import yaml
import typer
from pathlib import Path
from typing import List
from shutil import copytree
from typing import cast

from ...globals import load_config

def get_lambda_dirs_with_endpoint(base_path: Path) -> List[str]:
    result = []
    if not os.path.exists(base_path):
        raise FileNotFoundError(f"La ruta base no existe: {base_path}")

    for entry in os.listdir(base_path):
        dir_path = os.path.join(base_path, entry)
        endpoint_file = os.path.join(dir_path, "endpoint.yaml")
        if os.path.isdir(dir_path) and os.path.isfile(endpoint_file):
            result.append(entry)

    return result

def get_api_initial_definition(dir_name: Path):
    with open(dir_name, 'r', encoding="utf-8") as f:
        return yaml.safe_load(f)

def get_api_config(lambdas_path: Path):
    endpoint_dirs = get_lambda_dirs_with_endpoint(lambdas_path)
    import_lambdas = []
    endpoint_list = []
    for dir_name in endpoint_dirs:
        import_lambdas.append(f"from src.lambdas.{dir_name}.lambda_function import lambda_handler as {dir_name}_handler")

        with open(Path(lambdas_path / dir_name / "endpoint.yaml"), 'r', encoding="utf-8") as f:
            endpoint_list.append({"definition": yaml.safe_load(f), "name": dir_name})

    return import_lambdas, endpoint_list

def build_api_config(lambdas_path: Path, environment: str = None, app_name: str = None, aws_account: str = None, aws_region: str = None):
    endpoint_dirs = get_lambda_dirs_with_endpoint(lambdas_path)
    endpoint_list = []
    for dir_name in endpoint_dirs:

        with open(Path(lambdas_path / dir_name / "endpoint.yaml"), 'r', encoding="utf-8") as f:
            endpoint_node = cast(dict, yaml.safe_load(f))
            for endpoint_name in endpoint_node.keys():
                for method in endpoint_node[endpoint_name]:
                    if 'x-amazon-apigateway-integration' in endpoint_node[endpoint_name][method]:
                        integration = endpoint_node[endpoint_name][method]['x-amazon-apigateway-integration']
                        if 'uri' in integration and environment is not None:
                            integration['uri'] = f'arn:aws:apigateway:{aws_region}:lambda:path/2015-03-31/functions/arn:aws:lambda:{aws_region}:{aws_account}:function:{environment}-{app_name}-{dir_name}/invocations'
                        if 'credentials' in integration and environment is not None:
                            integration['credentials'] = f'arn:aws:iam::{aws_account}:role/{environment}-{app_name}-apigw-invoke-lambda-role'
            endpoint_list.append(endpoint_node)

    return endpoint_list

def build_lambdas(lambdas_path: Path, build_path: Path):
    """
    Copia toda la estructura de src/lambdas a infra/components/lambdas,
    manteniendo la jerarquía de carpetas.
    """

    # Crear destino si no existe
    build_path.mkdir(parents=True, exist_ok=True)

    # Iterar sobre cada subcarpeta dentro de src/lambdas
    for lambda_dir in tqdm.tqdm(lambdas_path.iterdir()):
        if lambda_dir.is_dir():
            target = build_path / lambda_dir.name
            # copytree falla si ya existe el destino → usamos dirs_exist_ok
            copytree(lambda_dir, target, dirs_exist_ok=True)
            typer.echo(f"Copiado {lambda_dir} → {target}")


def build_lambda_stack(build_lambdas_path: Path, environment: str, app_name: str):
    lambdas_init = build_lambdas_path / "__init__.py"

    excluded_dirs = [
        "__pycache__"
    ]

    for lambda_dir in tqdm.tqdm(build_lambdas_path.iterdir()):
        if lambda_dir.is_dir() and lambda_dir.name not in excluded_dirs:
            typer.echo(f"Procesando {lambda_dir.name} para __init__.py")

            lambda_camel_case = lambda_dir.name.replace("-", "_").title().replace("_", "")

            infra_config = ""
            with open(lambdas_init, "r") as f:
                infra_config = f.read()

            with open(lambdas_init, "a") as f:
                header = f"############ Lambda{lambda_camel_case}Stack ############"
                if header in infra_config:
                    typer.echo(f"Sección {header} ya existe en __init__.py, se omite.")
                    continue
                f.write(f"""
        {header}
        from .{lambda_dir.name}.infra_config import Lambda{lambda_camel_case}Stack

        Lambda{lambda_camel_case}Stack(
            name="{environment}-{app_name}-{lambda_camel_case}Stack",
            environment="{environment}",
            app_name="{app_name}",
            lambda_execution_role_arn=lambda_execution_role_arn,
            layers=layers,
            sg_ids=sg_ids,
            subnets_ids=subnets_ids,
            tags=DEFAULT_TAGS
        )\n\n""")

def build_api(api_path: Path, lambdas_path: Path, output_file: Path):

    config = load_config()
    api_definition = get_api_initial_definition(api_path)

    environment = os.getenv("ENVIRONMENT") or "dev"
    app_name = os.getenv("APP_NAME") or "myapp"
    aws_account = os.getenv("AWS_ACCOUNT_ID") or "123456789012"
    aws_region = os.getenv("AWS_REGION") or "us-east-1"

    endpoint_list = build_api_config(
        lambdas_path,
        environment=environment,
        app_name=app_name,
        aws_account=aws_account,
        aws_region=aws_region
    )

    for ep in endpoint_list:
        cast(dict, api_definition['paths']).update(ep)

    # Replace authorizer placeholders in securityDefinitions (Swagger 2.0)
    # Support both 'securityDefinitions' (Swagger 2.0) and 'components.securitySchemes' (OpenAPI 3.0) for compatibility
    security_schemes = None
    if 'securityDefinitions' in api_definition:
        security_schemes = api_definition['securityDefinitions']
    elif 'components' in api_definition and 'securitySchemes' in api_definition['components']:
        security_schemes = api_definition['components']['securitySchemes']

    if security_schemes:
        for scheme_name, scheme_config in security_schemes.items():
            if 'x-amazon-apigateway-authorizer' in scheme_config:
                authorizer = scheme_config['x-amazon-apigateway-authorizer']

                # Extract the authorizer key by removing '_authorizer' suffix if present
                authorizer_key = scheme_name.replace('_authorizer', '')

                # Check if there's a custom authorizer configuration for this scheme
                custom_authorizer = None
                if config and config.api and config.api.lambda_authorizers:
                    custom_authorizer = config.api.lambda_authorizers.get(authorizer_key)

                # Replace authorizerUri
                if 'authorizerUri' in authorizer:
                    if custom_authorizer:
                        # Use the lambda_name from configuration
                        lambda_name = custom_authorizer.lambda_name
                        authorizer['authorizerUri'] = f'arn:aws:apigateway:{aws_region}:lambda:path/2015-03-31/functions/arn:aws:lambda:{aws_region}:{aws_account}:function:{environment}-{app_name}-{lambda_name}/invocations'
                    else:
                        # Default behavior for non-configured authorizers
                        authorizer['authorizerUri'] = f'arn:aws:apigateway:{aws_region}:lambda:path/2015-03-31/functions/arn:aws:lambda:{aws_region}:{aws_account}:function:{environment}-{app_name}-authorizer/invocations'

                # Replace authorizerCredentials
                if 'authorizerCredentials' in authorizer:
                    if custom_authorizer:
                        # Use the role_name from configuration
                        role_name = custom_authorizer.role_name
                        authorizer['authorizerCredentials'] = f'arn:aws:iam::{aws_account}:role/{environment}-{app_name}-{role_name}'
                    else:
                        # Default behavior for non-configured authorizers
                        authorizer['authorizerCredentials'] = f'arn:aws:iam::{aws_account}:role/{environment}-{app_name}-authorizer-role'

    with open(output_file, "w+", encoding="utf-8") as f:
        json.dump(api_definition, f, indent=2)
