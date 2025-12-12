import json
from setuptools import setup, find_packages

with open('../../package.json', 'r') as f:
    package_info = json.load(f)

setup(
    name='steamuck',
    version=package_info.get('version'),
    author='Steamuck Team',
    description='A support library for creating plugins with Steamuck.',
    long_description=open('../../README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Steamuck/SDK',
    packages=find_packages(),
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.11.8'
)