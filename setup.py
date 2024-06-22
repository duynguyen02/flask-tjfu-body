from setuptools import find_packages, setup
from codecs import open
from os import path

from flask_tjfu_body import __version__, __author__

HERE = path.abspath(path.dirname(__file__))
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

SCRIPTS = [

]

PACKAGES = [
    'flask_tjfu_body'
]

REQUIRED_PACKAGES = [
    "Flask"
]

setup(
    name='flask-tjfu-body',
    packages=find_packages(include=PACKAGES),
    scripts=SCRIPTS,
    version=__version__,
    description='',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=__author__,
    url="https://github.com/duynguyen02/flask-tjfu-body",
    install_requires=REQUIRED_PACKAGES,
    keywords=[
        "Python",
        "Flask"
    ],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Operating System :: OS Independent"
    ]
)
