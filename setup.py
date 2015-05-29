#!/usr/bin/env python
# -*- coding: utf-8 -*-

import multiprocessing
import re

from setuptools import setup, find_packages


setup(
    name='inkscape-openscad-dxf',
    version='0.0.1',
    description='Inkscape OpenSCAD DXF Export',
    long_description=open('README.md').read(),
    author='Brad Pitcher',
    author_email='bradpitcher@gmail.com',
    url='https://github.com/brad/Inkscape-OpenSCAD-DXF-Export',
    packages=find_packages(exclude=['ez_setup', 'tests', 'tests.*']),
    package_data={'openscad_dxf': ['../openscad_dxf.inx']},
    include_package_data=True,
    install_requires=["setuptools"],
    license='GPL',
    test_suite='nose.collector',
    tests_require='nose',
    classifiers=(
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: PyPy'
    ),
)
