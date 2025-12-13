from setuptools import setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='thermobuilpy',
    version='0.1.2',
    description='ToDo',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Hannes Hanse',
    author_email='hannes.hanse@tu-clausthal.de',
    keywords=['milp','time series','optimization','gurobi','gurobipy'],
    readme = "README.md",
    url='https://github.com/hanneshanse/MilPython',
    install_requires=["numpy","matplotlib"],
    classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]
)