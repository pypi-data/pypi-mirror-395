from setuptools import setup, find_packages

setup(
    name="ai_helpers_sandra",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["requests"],
    author="Your Name",
    description="A simple AI helper library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourname/ai_helpers",
    python_requires=">=3.8"
)
