"""
Setup configuration for universal_agent_tools package.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="universal-agent-tools",
    version="1.1.0",
    author="Universal Agent Team",
    description="Reusable tools and utilities for Universal Agent stack",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mjdevaccount/universal_agent_tools",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[
        "universal-agent-nexus>=3.1.0",
        "langchain-openai>=0.1.0",
        "langchain-core>=0.1.0",
        "httpx>=0.25.0",
        "fastapi>=0.104.0",
        "pydantic>=2.0.0",
        "uvicorn>=0.24.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "mypy>=1.5.0",
        ],
        "qdrant": [
            "qdrant-client>=1.7.0",
        ],
        "github": [
            "PyGithub>=2.1.0",
        ],
    },
)

