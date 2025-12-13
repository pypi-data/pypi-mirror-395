import os
from setuptools import setup, find_packages

setup(
    name="llm-editor",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "openai",
        "PyYAML",
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": [
            "edit=llm_editor.cli:main",
        ],
    },
    author="Abhinav",
    description="A CLI tool to edit files using LLMs",
    long_description=open("README.md").read() if os.path.exists("README.md") else "",
    long_description_content_type="text/markdown",
)
