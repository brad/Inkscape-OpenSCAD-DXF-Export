#!/usr/bin/env python
# -*- coding: utf-8 -*-

import multiprocessing
import re

from setuptools import setup


setup(
    name='inkscape-openscad-dxf-export',
    version='0.0.1',
    description='Inkscape OpenSCAD DXF Export',
    long_description=open('README.md').read(),
    author='Brad Pitcher',
    author_email='bradpitcher@gmail.com',
    url='https://github.com/brad/Inkscape-OpenSCAD-DXF-Export',
    packages=[],
    package_data={'': ['COPYING', 'README.md']},
    include_package_data=True,
    install_requires=["setuptools"],
    license='GPL',
    test_suite='nose.collector',
    tests_require='nose',
    classifiers=(
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: GNU Public License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy'
    ),
)
