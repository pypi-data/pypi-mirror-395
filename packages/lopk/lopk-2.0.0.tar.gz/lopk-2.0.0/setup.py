from setuptools import setup, find_packages
import os

# 读取版本信息
with open('__init__.py', 'r', encoding='utf-8') as f:
    for line in f:
        if line.startswith('__version__'):
            version = line.split('=')[1].strip().strip('\'"')
            break
    else:
        version = '2.0.0'

# 读取README
try:
    with open('README.md', 'r', encoding='utf-8') as f:
        long_description = f.read()
except:
    long_description = "Lightweight Operational Progress Kit - A simple progress bar library"

setup(
    name="lopk",
    version=version,
    author="I-love-china",
    author_email="13709048021@163.com",
    description="Lightweight Operational Progress Kit - A simple progress bar library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/l-love-china/Lightweight-Operational-Progress-Kit",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
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
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "colorama>=0.4.4",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.9",
        ],
    },
    entry_points={
        "console_scripts": [
            "lopk-demo=LOPK11.lopk:demo",
            "lopk-info=LOPK11:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords=["progress", "bar", "terminal", "cli", "spinner", "timer"],
    project_urls={
        "Documentation": "https://github.com/your-username/lopk#readme",
        "Source": "https://github.com/your-username/lopk",
        "Tracker": "https://github.com/your-username/lopk/issues",
    },
)