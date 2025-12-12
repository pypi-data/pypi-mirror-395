"""Setup script for streamlit-app-generator."""
from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="streamlit-app-generator",
    version="0.2.0",
    author="Leandro Meyer Dal Cortivo",
    author_email="lmdcorti@gmail.com",
    description="Generate complete Streamlit applications with authentication and database templates",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/leandrodalcortivo/streamlit-app-generator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "streamlit>=1.28.0",
        "click>=8.0.0",
        "jinja2>=3.0.0",
        "pyyaml>=6.0",
        "bcrypt>=4.0.0",
        "python-dotenv>=1.0.0",
        "pydantic>=2.0.0",
    ],
    extras_require={
        "postgresql": ["psycopg2-binary>=2.9.0", "sqlalchemy>=2.0.0"],
        "mysql": ["mysql-connector-python>=8.0.0", "sqlalchemy>=2.0.0"],
        "mongodb": ["pymongo>=4.0.0"],
        "redis": ["redis>=5.0.0"],
        "oracle": ["oracledb>=2.0.0"],
        "all-databases": [
            "psycopg2-binary>=2.9.0",
            "mysql-connector-python>=8.0.0",
            "pymongo>=4.0.0",
            "redis>=5.0.0",
            "oracledb>=2.0.0",
            "sqlalchemy>=2.0.0",
        ],
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "isort>=5.12.0",
            "pre-commit>=3.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "streamlit-app-generator=streamlit_app_generator.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "streamlit_app_generator": [
            "templates/**/*",
            "templates/**/*.py",
            "templates/**/*.toml",
            "templates/**/*.md",
        ],
    },
)
