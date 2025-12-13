from setuptools import setup, find_packages

setup(
    name="arabia",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[],
    author="Moja",
    description="مكتبة عربية لتعليم Python للمبتدئين",
    long_description=open("README.md", encoding="utf-8").read(),

long_description_content_type="text/markdown",

    url="https://github.com/FoxCode-Moja/Arabia",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)