#!/usr/bin/env python
from setuptools import setup

files = [
    "statuscake/library",
]

short_description = long_description = "Ansible module for statuscake.com"
try:
    with open("README.md") as f:
        long_description = f.read()
except:
    pass

setup(
    name='ansible-modules-statuscake',
    version='1.0.0',
    description=short_description,
    long_description=long_description,
    author='Rory Geoghegan',
    author_email='r.geoghegan@gmail.com',
    url='https://github.com/rgeoghegan/ansible-modules-statuscake',
    packages=files,
    install_requires = [
        'ansible>=1.9.3',
    ],
)
