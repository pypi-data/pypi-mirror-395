#!/usr/bin/env python
# coding=utf-8

from setuptools import setup
import setuptools
setup(
    name='FPC',
    version='0.88',
    description=(
        'Frank\'s Personal Conllection'
    ),
    long_description='Frank\'s Personal Conllection',
    author='Frank',
    author_email='luoziluojun@126.com',
    maintainer='Frank',
    maintainer_email='luoziluojun@126.com',
    license='BSD License',
    packages=setuptools.find_packages(),
    platforms=["all"],
    url='http://ff2.pw',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries'
    ],
)