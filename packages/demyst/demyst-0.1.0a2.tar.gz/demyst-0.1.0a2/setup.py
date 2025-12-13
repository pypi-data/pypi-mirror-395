import os

from setuptools import find_packages, setup

# Read README if it exists
long_description = ""
if os.path.exists("README.md"):
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()

setup(
    name="demyst",
    version="1.1.0",
    author="Demyst Team",
    description="The Academic Integrity Platform for Scientific Code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Hmbown/demyst",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Quality Assurance",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.20.0",
        "PyYAML>=6.0",
        "pydantic>=2.0.0",
        "libcst>=1.0.0",
        "rich>=13.0.0",
        "langchain-core>=0.1.0",
        "mcp>=1.0.0",
    ],
    extras_require={
        "torch": ["torch>=1.9.0"],
        "jax": ["jax>=0.3.0", "jaxlib>=0.3.0"],
        "tracking": ["wandb>=0.12.0", "mlflow>=1.20.0"],
        "all": [
            "torch>=1.9.0",
            "jax>=0.3.0",
            "jaxlib>=0.3.0",
            "wandb>=0.12.0",
            "mlflow>=1.20.0",
        ],
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "demyst=demyst.cli:main",
        ],
    },
)
