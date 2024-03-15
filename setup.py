import os

from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

service_name = os.path.basename(os.getcwd())

setup(
    name=service_name,
    version="0.1.0",
    author="Origo Dataplattform",
    author_email="dataplattform@oslo.kommune.no",
    description="Email alerts for failing pipelines",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/oslokommune/dataplatform-pipeline-alerts-email",
    packages=find_packages(),
    install_requires=[
        "boto3>=1.28.11",
        "okdata-aws>=2.1,<3",
        "okdata-sdk",
    ],
)
