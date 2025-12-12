#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IoC数据SDK安装配置
"""

from setuptools import setup, find_packages
import os

# 读取README文件
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "IoC数据SDK - 提供工业物联网数据查询接口"

# 读取requirements文件
def read_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return ["PyYAML>=5.1.0"]

setup(
    name="enn-iot-oc-sdk",
    version="1.0.0",
    author="ENN Energy",
    author_email="developer@enn.com",
    description="IoC数据SDK - 提供工业物联网数据查询接口",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/enn-energy/enn-iot-oc-sdk",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
        ],
    },
    include_package_data=True,
    package_data={
        "enn_iot_oc": [
            "data/demo/source/*.json",
            "data/demo/*.yaml",
        ],
    },
    entry_points={
        "console_scripts": [
            "enn-iot-generate=main:main",
        ],
    },
    keywords="iot, industrial, data, sdk, repository, query",
    project_urls={
        "Bug Reports": "https://github.com/enn-energy/enn-iot-oc-sdk/issues",
        "Source": "https://github.com/enn-energy/enn-iot-oc-sdk",
        "Documentation": "https://github.com/enn-energy/enn-iot-oc-sdk/wiki",
    },
)