#!/usr/bin/env python3
"""
Setup configuration for talentsavvy-improveteam package.
"""

from setuptools import setup, find_packages
import os

# Read version from environment or default
VERSION = os.environ.get('PACKAGE_VERSION', '0.30.68')

# Read long description from README if it exists
long_description = ""
readme_path = os.path.join(os.path.dirname(__file__), "README.md")
if os.path.exists(readme_path):
    with open(readme_path, "r", encoding="utf-8") as fh:
        long_description = fh.read()

setup(
    name="talentsavvy-improveteam",
    version=VERSION,
    author="TalentSavvy.com",
    description="Scripts for data extraction scripts from software development systems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "."},
    packages=find_packages(where="."),
    # Include all package data files
    include_package_data=True,
    package_data={
        "common": ["config.json", "extract.sh"],
    },
    python_requires=">=3.7",
    install_requires=[
        "paramiko",
        "pytz",
        "python-dateutil",
        "pandas",
        "requests",
        "urllib3",
    ],
    py_modules=[
        "extract_azuredevops_boards",
        "extract_azuredevops_pipelines",
        "extract_azuredevops_repos",
        "extract_bitbucket_pipelines",
        "extract_bitbucket_repos",
        "extract_github",
        "extract_github_actions",
        "extract_gitlab",
        "extract_jenkins",
        "extract_jira",
        "extract_octopus",
        "sftp_upload",
    ],
    entry_points={
        "console_scripts": [
            "extract_azuredevops_boards=extract_azuredevops_boards:main",
            "extract_azuredevops_pipelines=extract_azuredevops_pipelines:main",
            "extract_azuredevops_repos=extract_azuredevops_repos:main",
            "extract_bitbucket_pipelines=extract_bitbucket_pipelines:main",
            "extract_bitbucket_repos=extract_bitbucket_repos:main",
            "extract_github=extract_github:main",
            "extract_github_actions=extract_github_actions:main",
            "extract_gitlab=extract_gitlab:main",
            "extract_jenkins=extract_jenkins:main",
            "extract_jira=extract_jira:main",
            "extract_octopus=extract_octopus:main",
            "sftp_upload=sftp_upload:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
)

