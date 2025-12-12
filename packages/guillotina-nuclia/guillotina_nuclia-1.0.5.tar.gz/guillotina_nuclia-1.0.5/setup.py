# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup


test_requires = [
    "async_asgi_testclient",
    "pytest>=5.0",
    "pytest-asyncio==0.18.3",
    "coverage",
    "pytest-cov",
    "pytest-docker-fixtures[pg]>=1.3.0",
    "docker",
    "aiohttp>=3.0.0,<4.0.0",
]


setup(
    name="guillotina_nuclia",
    description="nuclia support for guillotina",
    keywords="AI async guillotina nuclia",
    author="Nil Bacardit Vinyals",
    author_email="n.bacardit@iskra.cat",
    version=open("VERSION").read().strip(),
    long_description=(open("README.rst").read() + "\n" + open("CHANGELOG.rst").read()),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    url="https://github.com/guillotinaweb/guillotina_nuclia",
    license="GPL version 3",
    setup_requires=["pytest-runner"],
    zip_safe=True,
    include_package_data=True,
    package_data={"": ["*.txt", "*.rst"], "guillotina_nuclia": ["py.typed"]},
    packages=find_packages(exclude=["ez_setup"]),
    install_requires=["guillotina>=7.0.0", "nuclia>=4.9.11"],
    tests_require=test_requires,
    extras_require={"test": test_requires},
)
