# -*- coding: utf-8 -*-
# Based on: https://github.com/kennethreitz/setup.py

from setuptools import setup

with open('README.md') as f:
    readme = f.read()

with open('LICENSE.md') as f:
    license = f.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

with open('tests/requirements.txt') as f:
    tests_required = f.read().splitlines()

setup(
    name='wat-terminal',
    version='0.1.0',
    description='wat helps you find out what all the things in your Linux system are. You can ask it for information on: executables, services, bash built-ins, packages, files and folders',
    long_description=readme,
    long_description_content_type="text/markdown",
    author='Patrick Rein',
    author_email='support@patrickrein.de',
    url='https://github.com/codezeilen/wat',
    install_requires=required,
    tests_require=tests_required,
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
    packages=['wat', 'wat.pagesources']
)
