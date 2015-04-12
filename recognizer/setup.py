import os
from setuptools import setup

def get_description():
    return ""

def get_long_description():
    return ""

def get_packages():
    return ["pytect"]

def get_classifiers():
    return [
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: Apache Software License",
    ]

setup(
    name="pytect",
    version="0.0.1",
    author="Sarat Tallamraju",
    author_email="sarattallamraju@gmail.com",
    description=get_description(),
    license="Apache License V2",
    keywords="pytect face detection recognition",
    long_description=get_long_description(),
    packages=get_packages(),
    classifiers=get_classifiers(),
)