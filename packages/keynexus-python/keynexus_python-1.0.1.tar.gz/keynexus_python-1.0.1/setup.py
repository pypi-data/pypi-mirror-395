from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="keynexus-python",
    version="1.0.1",
    author="KeyNexus",
    author_email="support@keynexus.es",
    description="Official Python SDK for KeyNexus License Management",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/keynexus/keynexus-python",
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
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
    ],
    keywords="license management authentication licensing drm",
    project_urls={
        "Bug Reports": "https://github.com/keynexus/keynexus-python/issues",
        "Documentation": "https://keynexus.es/docs",
        "Source": "https://github.com/keynexus/keynexus-python",
    },
)
