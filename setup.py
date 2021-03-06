import os
from setuptools import setup, find_packages

from genericglue import VERSION


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


requirements = []

setup(
    name = "Django Generic Glue",
    version = ".".join(map(str, VERSION)),
    description = "",
    long_description = read('README.rst'),
    url = '',
    license = 'MIT',
    maintainer = 'The World Company',
    maintainer_email = 'support@ellingtoncms.com',
    packages = find_packages(exclude=['tests']),
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    install_requires = requirements,
)
