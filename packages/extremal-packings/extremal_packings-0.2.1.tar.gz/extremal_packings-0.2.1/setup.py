from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="extremal-packings",
    version="0.2.1",
    author="Fabián Henry Vilaxa",
    author_email="fabian.henry.vilaxa@alumnos.uta.cl",
    description="Análisis geométrico y espectral de configuraciones de discos unitarios tangentes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Fhv75/disk-packing-analysis",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Mathematics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.20.0",
        "scipy>=1.7.0",
        "matplotlib>=3.3.0",
        "networkx>=2.5",
        "click>=8.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=3.0",
            "black>=22.0",
            "flake8>=4.0",
            "mypy>=0.950",
        ],
    },
    entry_points={
        'console_scripts': [
            'epack=extremal_packings.cli:cli',
            'extremal-packings=extremal_packings.cli:cli',
        ],
    },
    package_data={
        "extremal_packings": ["../data/*.json"],
    },
    include_package_data=True,
)