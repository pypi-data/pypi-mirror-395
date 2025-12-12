#!/usr/bin/env python3
# coding = utf8
"""
@ Author : ZeroSeeker
@ e-mail : zeroseeker@foxmail.com
@ GitHub : https://github.com/ZeroSeeker
@ Gitee : https://gitee.com/ZeroSeeker
"""
import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="lazyad",
    version="0.0.79",
    description="基于Python的懒人包-适用于广告投放模块",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="ZeroSeeker",
    author_email="zeroseeker@foxmail.com",
    url="https://gitee.com/ZeroSeeker/lazyad",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        # "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'lazysdk>=0.1.88',
        "xmltodict==0.14.2"
    ]
)
