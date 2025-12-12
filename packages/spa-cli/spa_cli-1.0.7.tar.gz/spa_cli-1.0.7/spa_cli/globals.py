from enum import Enum
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, TypeVar, Type, cast, Callable, List
import typer
import toml
import datetime
from dotenv import load_dotenv

class Constants(Enum):
    PROJECT_TEMPLATE = "https://github.com/DavidCuy/serverless-python-application-pattern.git"
    MYSQL_ENGINE = "mysql"
    POSTGRESQL_ENGINE = "postgresql"
    
    AWS_REPOSITORY = "aws"
    OTHER_REPOSITORY = "other"
    
    VALID_MODEL_TYPES = (int, str, float, datetime.datetime)
    JSON_INT_DTYPE = 'int'
    JSON_FLOAT_DTYPE = 'float'
    JSON_STRING_DTYPE = 'str'
    JSON_DATETIME_DTYPE = 'datetime'

DRIVERS = {
    Constants.MYSQL_ENGINE.value: "pymysql",
    Constants.POSTGRESQL_ENGINE.value: "psycopg2"
}

def get_driver_from_engine(engine: Constants):
    return DRIVERS.get(engine.value, None)

SQL_PORTS_DEFAULT = {
    Constants.MYSQL_ENGINE.value: "3306",
    Constants.POSTGRESQL_ENGINE.value: "5432"
}

JSON_MAPPING_VALUE = {
    Constants.JSON_INT_DTYPE.value: 'Column("{ColumnName}", Integer)',
    Constants.JSON_STRING_DTYPE.value: 'Column("{ColumnName}", String)',
    Constants.JSON_FLOAT_DTYPE.value: 'Column("{ColumnName}", Float)',
    Constants.JSON_DATETIME_DTYPE.value: 'Column("{ColumnName}", DateTime)'
}

T = TypeVar("T")

def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_str_to_list(x: Any) -> List[str]:
    assert isinstance(x, str)
    return [x]


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()

class BaseConf:
    @property
    def attrs(self) -> List[str]:
        """ Returns a list of the attributes of an object
        Returns:
            List[str]: Attributes
        """
        return list(filter(lambda prop: not str(prop).startswith('_'), self.__dict__.keys()))
    
    @classmethod
    def from_dict(cls_, obj: Any) -> 'Folders':
        assert isinstance(obj, dict)
        
        obj_dict = {}
        attributes = list(filter(lambda prop: not str(prop).startswith('_'), (cls_).__dataclass_fields__.keys()))
        for attr in attributes:
            obj_dict.update({attr: from_str(obj.get(attr))})
        return cls_(**obj_dict)
    
    def to_dict(self):
        output_dict = {}
        for attr in self.attrs:
            output_dict.update({attr: self.__getattribute__(attr)})
        return output_dict
    
    def __repr__(self) -> str:
        """ Model representation
        Returns:
            str: Model output string formatted
        """
        attr_array = [f"{attr}={self.__getattribute__(attr)}" for attr in self.attrs]
        args_format = ",".join(attr_array)
        return f"<{type(self).__name__}({args_format})>"

@dataclass
class Files(BaseConf):
    model: str
    service: str
    controller: str
    endpoint: str
    lambda_function: str
    test_lambda: str
    lambda_conf: str


@dataclass
class Folders(BaseConf):
    models: str
    services: str
    controllers: str
    lambdas: str
    root: str
    jsons: str
    layers: str

@dataclass
class Definition(BaseConf):
    name: str
    description: str
    author: str
    author_email: str
    base_api: str

@dataclass
class Project(BaseConf):
    definition: Definition
    folders: Folders

    @staticmethod
    def from_dict(obj: Any) -> 'Project':
        assert isinstance(obj, dict)
        definition = Definition.from_dict(obj.get("definition"))
        folders = Folders.from_dict(obj.get("folders"))
        return Project(definition, folders)

@dataclass
class Template(BaseConf):
    files: Files

    @staticmethod
    def from_dict(obj: Any) -> 'Template':
        assert isinstance(obj, dict)
        files = Files.from_dict(obj.get("files"))
        return Template(files)

@dataclass
class Config(BaseConf):
    project: Project
    template: Template

    @staticmethod
    def from_dict(obj: Any) -> 'Config':
        assert isinstance(obj, dict)
        project = Project.from_dict(obj.get("project"))
        template = Template.from_dict(obj.get("template"))
        return Config(project, template)


def load_config(path="spa_project.toml") -> Config:
    config_path = Path(Path.cwd() / path)
    if not config_path.exists():
        typer.echo("config file not found in the project.", color=typer.colors.YELLOW)
        load_dotenv(".env")
        app_name = os.getenv("app_name") or ""
        config_path.write_text(f"""[spa.project.definition]
name = "{app_name}"
description = ""
author = "David Cuy"
author_email = ""
base_api = "api.yaml"

[spa.template.files]
model = ".spa/templates/models/model.txt"
service = ".spa/templates/models/service.txt"
controller = ".spa/templates/models/controller.txt"
endpoint = ".spa/templates/lambda_endpoint.txt"
lambda_function = ".spa/templates/lambda.txt"
test_lambda = ".spa/templates/test_lambda_function.txt"
lambda_conf = ".spa/templates/lambda_conf.txt"

[spa.project.folders]
root = "src"
models = "src/layers/databases/python/core_db/models"
services = "src/layers/databases/python/core_db/services"
controllers = "src/layers/core/python/core_http/controllers"
jsons = ".spa/templates/json"
lambdas = "src/lambdas"
layers = "src/layers"
        """)
        typer.echo(
            f"Created config file at {config_path} in this path you can find all configuration for the project here.")
        typer.echo(f"Please add the file {config_path} to git tracking and commit it")
    try:
        toml_config = toml.loads(config_path.read_text())
    except Exception as e:
        typer.echo("Error reading the config file, please check the file format.", color=typer.colors.RED)
        raise 
    return Config.from_dict(toml_config["spa"])