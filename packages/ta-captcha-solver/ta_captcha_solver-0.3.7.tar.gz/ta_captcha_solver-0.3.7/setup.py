#!/usr/bin/env python

"""The setup script."""
from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

install_requirements = open("requirements.txt").readlines()

setup(
    author="Bohdan Sukhov",
    author_email="bohdan.sukhov@thoughtful.ai",
    python_requires=">=3.8",
    classifiers=[
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    description="Thoughtful Captcha Solver Package",
    entry_points={
        "console_scripts": [
            "ta_captcha_solver=ta_captcha_solver.cli:main",
        ],
    },
    install_requires=install_requirements,
    long_description=readme,
    include_package_data=True,
    keywords="ta_captcha_solver",
    name="ta_captcha_solver",
    packages=find_packages(include=["ta_captcha_solver", "ta_captcha_solver.*"]),
    test_suite="tests",
    url="https://www.thoughtful.ai/",
    version="0.3.7",
    zip_safe=False,
)
