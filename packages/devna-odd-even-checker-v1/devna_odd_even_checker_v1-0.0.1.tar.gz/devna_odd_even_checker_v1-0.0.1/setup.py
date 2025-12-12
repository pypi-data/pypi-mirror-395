from setuptools import setup, find_packages

setup(
    name="devna_odd_even_checker_v1",  # Make sure this name is unique
    version="0.0.1",
    description="A simple odd or even checker",
    author="Devna",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
)