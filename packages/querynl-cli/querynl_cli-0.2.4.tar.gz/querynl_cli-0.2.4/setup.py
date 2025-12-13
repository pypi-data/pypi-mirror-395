"""
Setup configuration for QueryNL CLI
"""

from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="querynl_cli",
    version="0.2.4",
    description="AI-powered CLI for natural language database queries and automated test data generation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="QueryNL Team",
    author_email="contact@querynl.io",
    url="https://github.com/dushshantha/QueryNL",
    project_urls={
        "Bug Tracker": "https://github.com/dushshantha/QueryNL/issues",
        "Documentation": "https://github.com/dushshantha/QueryNL/blob/main/README.md",
        "Source Code": "https://github.com/dushshantha/QueryNL",
    },
    python_requires=">=3.10",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "querynl=cli.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Topic :: Database",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    keywords="database, sql, natural-language, cli, test-data, faker, llm, ai",
)
