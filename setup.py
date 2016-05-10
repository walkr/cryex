#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def read_long_description(readme_file):
    """ Read package long description from README file """
    try:
        import pypandoc
    except (ImportError, OSError) as exception:
        print('No pypandoc or pandoc: %s' % (exception,))
        if sys.version_info.major == 3:
            handle = open(readme_file, encoding='utf-8')
        else:
            handle = open(readme_file)
        long_description = handle.read()
        handle.close()
        return long_description
    else:
        return pypandoc.convert(readme_file, 'rst')


with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'requests'
]

test_requirements = [
    'requests', 'requests_mock',
]

setup(
    name='cryex',
    version='0.1.10',
    description="Clients for Ethereum cryptocurrency exchanges",
    long_description=read_long_description('README.md') + '\n\n' + history,
    author="Tony Walker",
    author_email='walkr.walkr@gmail.com',
    url='https://github.com/walkr/cryex',
    packages=[
        'cryex', 'cryex.coins',
    ],
    package_dir={'cryex':
                 'cryex'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords='cryex',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
