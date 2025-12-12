from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="envrihub",
    version="0.0.13",
    description="Python library to streamline interaction with the ENVRI-Hub APIs, providing a pythonic facade to data and service access.",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="ENVRI Community",
    author_email="envri-hub-next-wp13-14@mailman.egi.eu",
    url="https://gitlab.a.incd.pt/envri-hub-next/vre-lib",
    packages=["envrihub", "envrihub.cos", "envrihub.data_access"],
    install_requires=[
        "shapely",
        "retry",
        "openapi3-parser",
        "prance",
        "pandas",
        "argopy",
        "SPARQLWrapper",
    ],  # external packages as dependencies
)
