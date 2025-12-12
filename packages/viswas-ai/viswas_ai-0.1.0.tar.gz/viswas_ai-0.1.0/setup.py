from setuptools import setup, find_packages

setup(
    name="viswas_ai",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["requests"],
    author="Viswas",
    description="A simple AI helper library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)
