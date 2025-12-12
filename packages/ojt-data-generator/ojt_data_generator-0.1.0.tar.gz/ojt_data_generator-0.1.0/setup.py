from setuptools import setup, find_packages

setup(
    name="ojt-data-generator",
    version="0.1.0",
    author="Kushal Kotiny",
    author_email="kushalkotiny@example.com",
    description="A data generator tool with multiple templates for users, employees, students, products, and more",
    long_description="OJT Data Generator - Generate fake data for testing and development with multiple templates including users, employees, students, products, bank accounts, and patients.",
    long_description_content_type="text/plain",
    url="https://github.com/kushalkotiny/ojt",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
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
)
