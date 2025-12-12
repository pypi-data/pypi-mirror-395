from setuptools import setup, find_packages
import os

# Read the README file for long description
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="ojt-data-generator",
    version="0.1.1",
    author="Kushal Kotiny",
    author_email="kushalkotiny@example.com",
    description="A powerful Python package for generating realistic fake data with 6 pre-built templates - perfect for testing, development, and prototyping",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kushalkotiny/ojt",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="fake data generator testing development faker mock data csv pandas",
    python_requires=">=3.7",
    install_requires=[
        "faker>=18.0.0",
        "pandas>=1.3.0",
    ],
    entry_points={
        "console_scripts": [
            "ojt=ojt.cli:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/kushalkotiny/ojt/issues",
        "Source": "https://github.com/kushalkotiny/ojt",
    },
)
