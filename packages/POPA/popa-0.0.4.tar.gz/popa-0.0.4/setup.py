from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="POPA",
    author="EGOR",
    description="POPA MODULE",
    version="0.0.4",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=" >= 3.6"
)