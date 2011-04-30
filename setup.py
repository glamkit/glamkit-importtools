#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
 
setup(
    name='glamkit-importtools',
    version='0.5a1',
    description='XML and MARC analysis and harvesting framework',
    author='Greg Turner',
    author_email='greg@interaction.net.au',
    url='http://github.com/glamkit/glamkit-importtools',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=['Development Status :: 4 - Beta',
                 'Environment :: Web Environment',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: BSD License',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Topic :: Utilities'],
    install_requires=['setuptools', 'lxml', 'pymarc'],
    license='BSD',
    # test_suite = "importtools.tests",
)
