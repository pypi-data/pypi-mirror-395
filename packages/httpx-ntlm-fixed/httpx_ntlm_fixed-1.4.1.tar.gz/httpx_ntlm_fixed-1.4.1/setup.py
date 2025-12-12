#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name="httpx_ntlm_fixed",
    version="1.4.1",
    packages=["httpx_ntlm"],
    install_requires=[
        "httpx>=0.24",
        "pyspnego>=0.3",
    ],
    provides=["httpx_ntlm"],
    author="LogicDaemon",
    author_email="pub-pypi@logicdaemon.ru",
    url="https://github.com/LogicDaemon/httpx-ntlm",
    description="This package allows for HTTP NTLM authentication using the HTTPX library. Fork of httpx_ntlm with fixes.",
    long_description=open('README.rst').read(),
    long_description_content_type='text/x-rst',
    license="ISC",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "License :: OSI Approved :: ISC License (ISCL)",
    ],
)
