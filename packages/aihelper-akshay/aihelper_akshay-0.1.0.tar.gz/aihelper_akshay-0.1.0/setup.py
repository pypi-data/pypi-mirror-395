from setuptools import setup, find_packages

setup(
    name="aihelper_akshay",
    version="0.1.0",
    packages=find_packages(),
    description="AI helper library for Flask apps",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=["openai"],
    author="Akshay Shibu",
    python_requires=">=3.7",
)
