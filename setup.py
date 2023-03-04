# coding:utf-8
from pathlib import Path

from setuptools import find_packages, setup
from afuzz.settings import VERSION

with open("requirements.txt", encoding="utf-8") as req:
    requirements = [r.rstrip() for r in req.readlines()]

setup(
    name="Afuzz",
    version=VERSION,
    author="RapidDNS",
    author_email="skyj96455@gmail.com",
    description="Afuzz",
    long_description=open("README.md", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/rapiddns",
    packages=find_packages(),
    zip_safe=False,
    install_requires=requirements,
    package_data={'afuzz': ['db/*']},
    include_package_data=True,
    classifiers=[
        "Development Status :: 1 - Beta",
        "Environment :: Console",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    entry_points={"console_scripts": ["afuzz=afuzz:main"]},
    python_requires=">=3.8",
    keywords=['afuzz', 'bug bounty', 'http', 'pentesting', 'security']
)
