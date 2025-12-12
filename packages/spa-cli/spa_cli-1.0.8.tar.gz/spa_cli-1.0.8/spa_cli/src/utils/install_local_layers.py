import os
import tqdm
import sys
import typer
import subprocess
from glob import glob
from pathlib import Path
from shutil import copytree, rmtree

from ...globals import Config


LAYERS_VERSIONS = '1.0.0'
PACKAGE_NAME = 'layers-extras'

README = f'''
# {PACKAGE_NAME}
***

'''

LICENSE = '''Copyright (c) 2018 The Python Packaging Authority

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

MANIFEST = '''
recursive-include * *.html
'''


TEMPLATE_SETUP = '''
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='{name}',
    version='{version}',
    author="{author}",
    author_email="{author_email}",
    description="Install local layers for AWS Sam Local Development",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
)
'''

def install_layers(project_config: Config):
    global TEMPLATE_SETUP
    SETUP = TEMPLATE_SETUP.format(
        version=LAYERS_VERSIONS,
        name=PACKAGE_NAME,
        author=project_config.project.definition.author,
        author_email=project_config.project.definition.author_email
    )
    original_path = Path(os.getcwd())
    tmp_path = Path(original_path / 'tmp-extras')
    layers_path = Path(original_path / 'src/layers')

    layers = [layers_path.joinpath(layer) for layer in os.listdir(layers_path) if '__' not in layer and layers_path.joinpath(layer).is_dir()]

    LAYERS = []
    for layer in layers:
        LAYERS += [layer.joinpath('python').joinpath(lyr) for lyr in os.listdir(layer.joinpath('python')) if '__' not in lyr and layer.joinpath('python').joinpath(lyr).is_dir()]

    tmp_path = Path(original_path / 'tmp')

    def run(cmd, **kw):
        typer.echo(f"[cmd] {' '.join(cmd)}")
        return subprocess.run(cmd, check=True, **kw)

    try:
        if not tmp_path.exists():
            tmp_path.mkdir()
        for file_name, data in {'LICENSE': LICENSE, 'README.md': README, 'setup.py': SETUP}.items():

            with open(tmp_path.joinpath(file_name), 'w+') as f:
                f.write(data)
        
        with open(tmp_path.joinpath('MANIFEST.in'), 'w+') as f:
            f.write(MANIFEST)
        for layer in LAYERS:
            copytree(layer, tmp_path.joinpath(layer.name))
        os.chdir(tmp_path)
        

        run([sys.executable, "-m", "pip", "install",
            "--no-input", "--disable-pip-version-check",
            "setuptools", "wheel"])

        #os.system('pip install setuptools wheel')

        run([sys.executable, "setup.py", "sdist", "bdist_wheel"])
        # os.system(r'python setup.py sdist bdist_wheel')

        try:
            # os.system(f'pip uninstall {PACKAGE_NAME}')
            subprocess.run([sys.executable, "-m", "pip", "uninstall",
                        "-y", PACKAGE_NAME],
                    check=False)
        except Exception as details:
            typer.echo(details)
            raise OSError(f'Is not possible uninstall the package {PACKAGE_NAME}')
        #os.system(r'pip install {}'.format(glob(os.path.join('.', 'dist', '*.whl'))[0]))
        wheel_path = glob(str(Path("dist") / "*.whl"))[0]
        run([sys.executable, "-m", "pip", "install",
            "--no-input", "--disable-pip-version-check", wheel_path])
        os.chdir(original_path)
    except KeyboardInterrupt:
        typer.echo('STOP BY USER')
    finally:
        try:
            rmtree(tmp_path)
        except Exception as e:
            typer.echo(str(e))

    typer.echo(f'Se han instalado las siguientes layers: {list(map(lambda l: l.name, layers))}')

def build_layers(layers_path: Path, tmp_path: Path = Path('tmp_build_layer')):
    if os.path.exists(tmp_path):
        rmtree(tmp_path)

    if not os.path.exists(tmp_path):
        os.mkdir(tmp_path)

    for layer in tqdm.tqdm(os.listdir(layers_path)):
        layer_path = layers_path.joinpath(layer)
        if not layer_path.is_dir():
            continue  

        copytree(layer_path, tmp_path.joinpath(layer))

        layer_path_res = str(tmp_path.joinpath(layer).joinpath('python').resolve())
        req_path = str(tmp_path.joinpath(layer).joinpath('python').joinpath('requirements.txt').resolve())
        try:
            typer.echo(f'running command: pip install -r {req_path} -t {layer_path_res}')
            os.system(f'pip install -r {req_path} -t {layer_path_res}')
        except Exception as e:
            typer.echo(f"WARNING: {str(e)}", color=typer.colors.YELLOW)
