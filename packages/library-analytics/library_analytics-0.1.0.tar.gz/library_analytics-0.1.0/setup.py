"""
Setup configuration for library-analytics package
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="library-analytics",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Python package for library management analytics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/library-analytics",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Framework :: Django",
        "Framework :: Django :: 4.0",
        "Framework :: Django :: 4.1",
        "Framework :: Django :: 4.2",
    ],
    python_requires=">=3.8",
    install_requires=[
        # No hard dependencies - works with or without Django
    ],
    extras_require={
        "django": ["Django>=4.0"],
    },
    keywords="library management analytics django statistics",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/library-analytics/issues",
        "Source": "https://github.com/yourusername/library-analytics",
    },
)
