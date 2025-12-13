from setuptools import setup, find_packages

setup(
    name="shapeedit",
    version="0.5.0b3",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "shapeio==0.5.0b3"
    ],
    author="Peter Grønbæk Andersen",
    author_email="peter@grnbk.io",
    description="A library that provides experimental operations for modifying existing MSTS/ORTS shape files.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    project_urls={
        "Homepage": "https://github.com/pgroenbaek/shapeedit",
        "Issues": "https://github.com/pgroenbaek/shapeedit/issues",
        "Source": "https://github.com/pgroenbaek/shapeedit",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)