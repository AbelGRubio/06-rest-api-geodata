import os

from setuptools import setup, find_packages
from src.app import __version__
import shutil

source_dir = './src'
destination_dir = '.'

shutil.copytree (source_dir, destination_dir, dirs_exist_ok=True)

with open('requirements.txt') as f:
    requirements = f.readlines()
with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='app',
    version=__version__,
    author="app",
    author_email="app@gmail.es",
    keywords='development, setup, setuptools',
    python_requires='>=3.8',
    url='https://github.com/AbelGRubio/06-rest-api-geodata.git',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(include=['app', 'app.*']),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System:: OS Independent",],
    package_data={'validation_files': ['validation_files/*.csv']},
    include_package_data=True)

shutil.rmtree('./app')
os.remove('./__main__.py')