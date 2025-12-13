from setuptools import find_packages, setup

with open("app/README.md", "r") as f:
    long_description = f.read()

setup(
    name="grammarian",
    version="0.1.21",
    description="An easy and fast tool to check english grammar",
    package_dir={"": "app"},
    packages=find_packages(where="app"),
    include_package_data=True,
    package_data={
        "grammarian.src":["*"],
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hiko667/grammarian-grammar-checker-package",  
    author="StanisławKulesza",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent"
    ],
    python_requires =">=3.13",
    extras_require = {
        "dev" : ["twine>=6.2.0"]
    }
)