from setuptools import setup, find_packages

setup(
    name="odd_or_even_albin",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    description="A simple library to check odd or even numbers",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Albin Mathew",
#    license="MIT",
#    url="https://github.com/yourname/odd_or_even",
)
