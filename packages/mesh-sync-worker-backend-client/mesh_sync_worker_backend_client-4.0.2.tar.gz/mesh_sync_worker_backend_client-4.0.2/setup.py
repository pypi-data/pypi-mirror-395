from setuptools import setup, find_packages
import os

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mesh-sync-worker-backend-client",
    version="1.0.3",
    description="Auto-generated Python client for Mesh-Sync worker-backend - provides type-safe methods for enqueueing jobs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Mesh-Sync",
    author_email="",
    url="https://github.com/Mesh-Sync/worker-backend",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Distributed Computing",
    ],
    keywords="worker job-queue bullmq client mesh-sync",
    project_urls={
        "Bug Reports": "https://github.com/Mesh-Sync/worker-backend/issues",
        "Source": "https://github.com/Mesh-Sync/worker-backend",
    },
)
