"""
Setup configuration for Trackify package.
"""
from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read requirements
requirements = []
with open('backend/requirements.txt', encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="trackify-pc",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A comprehensive PC activity tracking and productivity analysis system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/trackify",
    packages=find_packages(include=['trackify', 'trackify.*']),
    include_package_data=True,
    package_data={
        'trackify.backend': ['config/*.json'],
    },
    install_requires=requirements,
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business :: Scheduling",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: Microsoft :: Windows",
    ],
    entry_points={
        'console_scripts': [
            'trackify-tracker=trackify.tracker_cli:main',
            'trackify-backend=trackify.backend_cli:main',
        ],
    },
    keywords="activity tracking productivity time management windows monitoring",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/trackify/issues",
        "Source": "https://github.com/yourusername/trackify",
        "Documentation": "https://github.com/yourusername/trackify#readme",
    },
)
