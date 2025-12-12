from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.6.0'
DESCRIPTION = 'This package finds covariation patterns between interacted niche cell types from single-cell resolution spatial transcriptomics data.'
LONG_DESCRIPTION = 'A package that performs cell type annotations on spatial transcriptomics data, finds the niche interactions and covariation patterns between interacting cell types.'

# Setting up
setup(name="nico-sc-sp", #"nico-sc-sp"
    version=VERSION,
    author="Ankit Agrawal",
    author_email="<ankitplusplus@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['scanpy==1.11.2','seaborn==0.13.2','scipy==1.11.3', 'matplotlib==3.10.3','numpy==1.26.1','networkx==3.2.1','gseapy==1.1.4','numba==0.58.1','xlsxwriter==3.1.9',  'pydot==1.4.2','scikit-learn==1.3.2','pandas==2.1.1', 'KDEpy==1.1.8','leidenalg'],
    keywords=['python', 'tissue niche','niche','spatial transcriptomics','single-cell RNA sequencing','scRNAseq','scRNA-seq','MERFISH','seqFISH','STARmap','nico','niche covariation'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ]
)
