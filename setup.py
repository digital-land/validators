from setuptools import setup, find_packages

setup(
    name='validators-ep',
    version='1.0.0',
    description='A package for validation functions',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'Flask',
        'python-magic',
    ],
)