from setuptools import setup, find_packages

setup(
    name="novabrawlstars",
    version="0.1.6",
    description="Unofficial Python wrapper for the Brawl Stars API.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="NovaFenice",
    license="MIT",
    python_requires=">=3.8",
    packages=find_packages(where="."),
    install_requires=[
        "httpx", "asyncio"
    ],
    keywords=["brawl stars", "api", "python", "wrapper"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/NovaFenice/NovaBrawlStarsAPI",
)
