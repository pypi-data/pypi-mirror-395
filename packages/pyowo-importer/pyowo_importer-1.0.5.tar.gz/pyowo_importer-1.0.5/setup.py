from setuptools import setup, find_packages

setup(
    name='pyowo_importer',
    version='1.0.5',
    author='Aleksander Sapieha',
    packages=find_packages(),
    install_requires=[
        'pythowopp',
        'stwings_with_awwows',
    ],
)