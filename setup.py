# coding: utf-8
import re
from parver import Version, ParseError
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

version_scope = {'__builtins__': None}
with open("seeq/addons/stictionanalyser/_version.py", "r+") as f:
    version_file = f.read()
    version_line = re.search(r"__version__ = (.*)", version_file)
    if version_line is None:
        raise ValueError(f"Invalid version. Expected __version__ = 'xx.xx.xx', but got \n{version_file}")
    version = version_line.group(1).replace(" ", "").strip('\n').strip("'").strip('"')
    print(f"version: {version}")
    try:
        Version.parse(version)
        exec(version_line.group(0), version_scope)
    except ParseError as e:
        print(str(e))
        raise

setup_args = dict(
    name='stictionanalyser',
    version=version_scope['__version__'],
    author="Timothy Essinger",
    author_email="timothy.essinger@seeq.com",
    license="Apache License 2.0",
    platforms=["Linux", "Windows"],
    description="Stiction analysis of time series data in Seeq",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Timothy716/seeq-stictionanalyser", 
    packages=setuptools.find_namespace_packages(include=['seeq.*']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'dask[complete]>=2.18.1',
        'ipyvuetify>=1.5.1',
        'matplotlib>=3.1.3',
        'memoization>=0.2.2',
        'numpy>=1.19.5',
        'pandas>=1.2.1',
        'plotly>=4.5.0',
        'python-dateutil>=2.8.1',
        'opencv-python-headless >=4.5.4.58',
        'scipy==1.6.2',
        'scikit-image',
        'tzlocal==2.0',
        'parver~=0.3.1',
        'image>=1.5.33',
    ],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        # "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)

setuptools.setup(**setup_args)
