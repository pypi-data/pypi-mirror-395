from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="extract360",
    version="0.1.0",
    author="Extract360",
    author_email="contato@extract360.tech",
    description="Official Python client for the Extract360 API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://extract360.tech",
    project_urls={
        "Homepage": "https://extract360.tech",
        "Repository": "https://github.com/synkia/extract360",
        "Issues": "https://github.com/synkia/extract360/issues",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Software Development :: Libraries",
        "Topic :: Internet :: WWW/HTTP",
    ],
    python_requires=">=3.9",
    install_requires=[
        "requests>=2.31",
    ],
    keywords=["extract360", "web-scraping", "sdk", "api-client"],
)
