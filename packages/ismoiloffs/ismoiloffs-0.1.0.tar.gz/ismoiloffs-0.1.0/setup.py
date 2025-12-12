from setuptools import setup, find_packages

setup(
    name="ismoiloffs",
    version="1.0.0",
    description="Run your remote code securely via Python package",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="ISMOILOFF",
    author_email="youremail@example.com",
    url="https://github.com/ismoiloff/ismoiloff",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "requests",
        "colorama",
        "platformdirs",   # optional if you want to use it later
        # remove 'licensing' if it is local; user must install manually
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
