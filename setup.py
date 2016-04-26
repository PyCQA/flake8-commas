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


long_description = read('README.rst')

about = {}
with open(os.path.join(__dir__, 'flake8_commas', '__about__.py')) as file:
    exec(file.read(), about)


setup(
    name='flake8-commas',
    author='Trevor Creech',
    version=about['__version__'],
    install_requires=[
        'pep8',
    ],
    url='http://github.com/zedlander/flake8-commas/',
    long_description=long_description,
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
