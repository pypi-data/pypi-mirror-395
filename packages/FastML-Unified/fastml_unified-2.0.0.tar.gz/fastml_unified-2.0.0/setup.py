"""
Setup script for FastML - The unified Machine Learning Acceleration Framework
Combines FastArray, FastData, and JAX-based acceleration in one package
"""
from setuptools import setup, find_packages
import os

# Read the contents of your README file
this_directory = os.path.abspath(os.path.dirname(__file__))
readme_path = os.path.join(this_directory, '..', 'README.md')
long_description = ""
if os.path.exists(readme_path):
    with open(readme_path, encoding='utf-8') as f:
        long_description = f.read()
else:
    long_description = "FastML: The unified Machine Learning Acceleration Framework - Combining FastArray, FastData, and JAX-based acceleration with extreme compression for TPU/GPU/CPU"

setup(
    name="FastML-Unified",
    version="2.0.0",
    author="FastML Development Team",
    author_email="fastml@example.com",
    description="The unified Machine Learning Acceleration Framework with extreme compression and multi-device optimization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fastml/fastml-unified",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities"
    ],
    python_requires='>=3.8',
    install_requires=[
        "numpy>=1.21.0",
        "jax>=0.4.0",
        "jaxlib>=0.4.0", 
        "flax>=0.7.0",
        "optax>=0.1.0",
        "blosc>=1.0.0; python_implementation != 'PyPy'",
        "scipy>=1.7.0",
        "tokenizers>=0.13.0",
        "datasets>=2.0.0"
    ],
    extras_require={
        'dev': [
            'pytest>=6.0',
            'pytest-cov>=2.0',
            'mypy>=0.910',
            'black>=21.0',
            'flake8>=3.8',
        ],
        'full': [
            'torch>=1.9.0',
            'tensorflow>=2.8.0',
        ],
    },
    keywords="machine-learning ai tensor tpu gpu cpu compression fastarray fastdata jax numpy fastml unified",
    project_urls={
        "Bug Reports": "https://github.com/fastml/fastml-unified/issues",
        "Source": "https://github.com/fastml/fastml-unified",
        "Documentation": "https://fastml.readthedocs.io/",
    }
)