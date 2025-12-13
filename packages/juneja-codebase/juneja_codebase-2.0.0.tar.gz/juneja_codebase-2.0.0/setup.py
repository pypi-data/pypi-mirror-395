from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="juneja_codebase",
    version="2.0.0",
    author="AJ",
    description="CLI tool to generate academic practical code files for Compiler Design, Data Structures, OS, and DBMS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Education",
    ],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            'juneja-codebase=juneja_codebase.main:main',
        ],
    },
    include_package_data=True,
)
