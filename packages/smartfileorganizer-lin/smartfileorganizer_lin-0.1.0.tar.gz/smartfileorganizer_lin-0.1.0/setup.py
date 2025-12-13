"""
项目安装配置文件
兼容旧版本的 setuptools 配置
"""

from setuptools import setup

# 读取 README 文件作为长描述
try:
    with open("README.md", "r", encoding="utf-8") as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = "智能文件整理工具，自动分类下载文件"

setup(
    name="smartfileorganizer-lin",
    version="0.1.0",
    packages=["smart_file_organizer"],
    package_dir={"": "src"},
    install_requires=[
        "pyyaml>=6.0",
        "watchdog>=2.1",
    ],
    entry_points={
        "console_scripts": [
            "organize-files=smart_file_organizer.main:main",
        ],
    },
    python_requires=">=3.10",
    author="你的名字",
    author_email="你的邮箱@example.com",
    description="智能文件整理工具，自动分类下载文件",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/smart-file-organizer",
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Development Status :: 3 - Alpha",
    ],
)
