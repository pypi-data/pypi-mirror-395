from setuptools import setup, find_packages

#Leer el contenido de README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="taikpo",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author="taielkpo",
    description="Una pruebita, papi.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://ole.com.ar"
)
