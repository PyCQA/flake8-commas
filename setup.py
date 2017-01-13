import io
import os
from setuptools import setup

__dir__ = os.path.dirname(__file__)


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


readme = read('README.rst')
history = read('CHANGES.rst').replace('.. :changelog:', '')


setup(
    name='flake8-trailing-commas',
    author='Trevor Creech',
    version='0.1.1',
    install_requires=[
        'pep8',
    ],
    url='https://github.com/graingert/flake8-trailing-commas/',
    long_description=readme + '\n\n' + history,
    description='Flake8 lint for trailing commas.',
    packages=['flake8_commas'],
    test_suite='test',
    include_package_data=True,
    entry_points={
        'flake8.extension': [
            'flake8_commas = flake8_commas:CommaChecker',
        ],
    },
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Quality Assurance',
    ],
)
