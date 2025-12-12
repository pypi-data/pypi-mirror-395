#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
APT软件包快照与比较工具安装脚本
"""

import os
from setuptools import setup, find_packages

# 读取README文件
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# 读取requirements文件
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="aptbox",
    version="0.1.0",
    description="APT软件包快照与比较工具",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="fengyucn",
    author_email="fengyucn@gmail.com",
    url="https://github.com/fengyucn/aptbox",
    project_urls={
        "Bug Reports": "https://github.com/fengyucn/aptbox/issues",
        "Source": "https://github.com/fengyucn/aptbox",
        "Documentation": "https://github.com/fengyucn/aptbox/blob/main/README.md",
    },
    packages=find_packages(),
    include_package_data=True,
    install_requires=read_requirements(),
    data_files=[
        ('etc/bash_completion.d', ['completion/aptbox-completion.bash']),
    ],
    entry_points={
        'console_scripts': [
            'aptbox=aptbox.main:main',
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Developers",
        "Topic :: System :: Systems Administration",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: POSIX :: Linux",
        "Environment :: Console",
    ],
    python_requires=">=3.6",
    keywords="apt, debian, ubuntu, package management, snapshot, system administration",
    license="MIT",
)