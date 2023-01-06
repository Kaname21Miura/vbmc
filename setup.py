# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='vbmc',
    version='0.0.0',
    description='CPU version of Voxel-based Monte Carlo simulation',
    long_description=readme,
    author='Kaname Miura',
    author_email='miukana21@gmail.com',
    install_requires=[
        'numpy','matplotlib','abc','datetime','time','json','pickle','bz2',
        'numba','functools','inspect','warnings'
    ],
    url='https://github.com/Kaname21Miura/vbmc.git',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
