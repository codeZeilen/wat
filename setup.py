# -*- coding: utf-8 -*-
# Based on: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE.md') as f:
    license = f.read()

setup(
    name='wat',
    version='0.1.0',
    description='',
    long_description=readme,
    author='Patrick Rein',
    author_email='hi@patrickrein.de',
    url='https://github.com/codezeilen/wat',
    license=license,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Developers',
        'Topic :: System :: Shells',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10',
        'Operating System :: POSIX :: Linux'
    ],
    python_requires='>=3.10',
    entry_points={
        'console_scripts': [
            'wat = wat.wat:answer_wat',
        ],
    },
    include_package_data=True,
    package_data={"": ["*.json"]},
    packages=['wat', 'wat.pagesources']
)
