# coding:utf-8
from pathlib import Path

from setuptools import find_packages, setup

setup(
    name="Afuzz",
    version="0.1.8",
    author="RapidDNS",
    author_email="skyj96455@gmail.com",
    description="Afuzz",
    long_description=open("README.md", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/rapiddns",
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        "httpx==0.23.3",
        "httpx[http2]",
        "asciistuff==1.2.3",
        "prettytable==3.6.0",
        "pandas==1.5.3",
        "tldextract==3.4.0"
    ],
    package_data={'afuzz': ['db/*']},
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10"

    ],
    entry_points={"console_scripts": ["afuzz=afuzz:main"]},
    keywords=['afuzz', 'bug bounty', 'http', 'pentesting', 'security']
)
