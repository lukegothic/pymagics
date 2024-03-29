#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', ]

test_requirements = [ ]

setup(
    author="Luke Perez",
    author_email='lukegothic@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Python lib with utils to work with MTG data, retrieve data from many endpoints and provide a standarized and OOP approach to MTG objects",
    entry_points={
        'console_scripts': [
            'pymagics=pymagics.cli:main',
        ],
    },
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='pymagics',
    name='pymagics',
    packages=find_packages(include=['pymagics', 'pymagics.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/lukegothic/pymagics',
    version='0.1.28',
    zip_safe=False,
)
