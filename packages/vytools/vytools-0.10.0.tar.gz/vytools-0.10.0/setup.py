#!/usr/bin/env python
import setuptools, re

try:
    with open('README.md','r') as f:
        readme = f.read()
except Exception as exc:
    readme = ''

setuptools.setup(name='vytools',
    description='Tools for working with vy',
    long_description=readme,
    long_description_content_type='text/markdown',
    license='MIT',
    author='Nate Bunderson',
    author_email='nbunderson@gmail.com',
    url='https://github.com/NateBu/vyengine',
    keywords = ["vy", "vytools"],
    classifiers = [
        "Programming Language :: Python",
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Other/Nonlisted Topic"
    ],
    python_requires='>=3.6',
    packages=setuptools.find_packages(),
    package_data = {},
    install_requires=[
        'cerberus'
    ],
    entry_points={
        'console_scripts':[]
    },
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)

