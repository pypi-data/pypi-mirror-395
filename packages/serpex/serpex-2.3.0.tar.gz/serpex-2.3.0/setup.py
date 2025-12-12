from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="serpex",
    version="2.3.0",
    author="Serpex Team",
    author_email="support@serpex.dev",
    description="Official Python SDK for Serpex SERP API - Fetch search results in JSON format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/divyeshradadiya/serpex-sdk-python",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
        "typing-extensions>=4.0.0; python_version<'3.10'",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-asyncio>=0.21.0",
            "black>=22.0.0",
            "isort>=5.10.0",
            "mypy>=0.950",
            "flake8>=4.0.0",
        ],
    },
    keywords="serp search api google search-results seo python sdk",
    project_urls={
        "Bug Reports": "https://github.com/divyeshradadiya/serpex-sdk-python/issues",
        "Source": "https://github.com/divyeshradadiya/serpex-sdk-python",
        "Documentation": "https://github.com/divyeshradadiya/serpex-sdk-python#readme",
    },
)
