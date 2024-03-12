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
    name='flake8-commas-x',
    author="Peter Law",
    author_email="PeterJCLaw@gmail.com",
    maintainer="Peter Law",
    maintainer_email="PeterJCLaw@gmail.com",
    version='3.0.0.dev2',
    install_requires=['flake8>=5'],
    python_requires='>=3.8',
    url='https://github.com/PeterJCLaw/flake8-commas/',
    long_description=readme + '\n\n' + history,
    description='Flake8 lint for trailing commas.',
    packages=['flake8_commas'],
    test_suite='test',
    include_package_data=True,
    entry_points={
        'flake8.extension': [
            'C81 = flake8_commas:CommaChecker',
        ],
    },
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Quality Assurance',
        'Framework :: Flake8',
    ],
)
