from setuptools import setup, find_packages

setup(
    name="viswas-ai",
    version="0.1.3",  # <- increment version
    packages=find_packages(),
    install_requires=["requests"],
    author="Viswas",
    description="A simple AI helper library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)

