# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 20:25:03 2022

@author: Harley Hanes
"""

from setuptools import setup, find_packages

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name='UQLibrary',
    version='0.1.3',
    author='H. Hanes',
    author_email='hhanes@ncsu.edu',
    packages=find_packages(include=["UQLibrary", "UQLibrary.*"]),
    url='https://github.com/HarleyHanes/UQLibrary-CourseProject',
    license='LICENSE',
    description='Robust set of sensitivity and identifiability analysis methods.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        "numpy >= 1.20.0",
        "scipy >= 1.7.1",
        "matplotlib >= 3.4.3",
        "tabulate >= 0.8.9",
        "mpi4py >= 3.1.3"
    ],
    python_requires='>=3.8',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)