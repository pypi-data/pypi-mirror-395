"""
Setup script for taskController package.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="taskController",
    version="0.2.0",
    author="Orangewood Labs",
    author_email="Yuvraj.m@orangewood.co",
    description="A Python library for pause/resume/kill control of functions across processes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yuvimehta/taskController",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "dill>=0.3.0",
    ],
    entry_points={
        'console_scripts': [
            'taskController=taskController.cli:main',
        ],
    },
    keywords="flow-control pause resume kill decorator process-control",
    project_urls={
        "Bug Reports": "https://github.com/yuvimehta/taskController/issues",
        "Source": "https://github.com/yuvimehta/taskController",
    },
)
