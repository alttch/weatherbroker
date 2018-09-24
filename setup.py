__version__ = "0.0.1"

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="weatherbroker",
    version=__version__,
    author='Altertech Group',
    author_email="pr@altertech.com",
    description="Weather broker for Python",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/alttch/weatherbroker",
    packages=setuptools.find_packages(),
    license='Apache License 2.0',
    install_requires=['requests'],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Scientific/Engineering :: Atmospheric Science"
    ),
)
