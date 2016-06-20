#########################################
## Python loraRelayer v. 1.0.0
## @author: Tim van der Voord - tim@vandervoord.nl
## (C) 2016, Tim van der Voord
##
## Setup script
from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='python-loradecoder',
    version='0.1.0',
    url='https://github.com/Timvandervoord/python-loradecoder.git',
    license='GNU',
    author='timvandervoord',
    author_email='timvandervoord@gmail.com',
    description='LoRaWan1.0 packet decoder',
    long_description=long_description,
    packages=['loradecoder'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'six>=1.9.0',
        'pyaes>=1.3.0'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)