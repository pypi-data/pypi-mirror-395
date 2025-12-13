from setuptools import setup

with open("README.md", "r") as file:
    long_description = file.read()

setup(
    name="ntdrt",
    version="1.23.3",
    author="Tomáš Kolinger",
    author_email="tomas@kolinger.name",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=["ntdrt"],
    zip_safe=False
)
