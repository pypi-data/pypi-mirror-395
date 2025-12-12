from setuptools import setup, find_packages

setup(
    name="fund-stack-cli",
    version="0.1.0",
    description="A comprehensive personal finance management CLI tool.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Sourashis Ghosh Roy",
    author_email="sourashis@example.com",
    url="https://github.com/ItzSouraseez/fund-stack-cli",
    packages=find_packages(),
    install_requires=[
        "requests",
        "rich",
        "google-genai"
    ],
    entry_points={
        "console_scripts": [
            "fund-stack=fund_stack_cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
