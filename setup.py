# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='pycnab240',
    version='0.0.3',
    author='Trustcode',
    author_email='suporte@trustcode.com.br',
    url='https://github.com/Trust-Code/PyTrustCnab240',
    keywords=['cnab', 'cnab240', 'pycnab'],
    packages=find_packages(exclude=['*tests*']),
    include_package_data=True,
    package_data={
        'pycnab240': [
            'bancos/santander/specs/*.json',
        ],
    },
    install_requires=[
        'setuptools-git==1.1',
        'future'
    ],
    license='MIT',
    description='Lib para gerar arquivo CNAB 240 - Integração bancária',
    long_description=open('README.md', 'r').read(),
    download_url='https://github.com/Trust-Code/PyTrustCnab240',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    platforms='any',
    tests_require=[
        'mock',
    ],
)
