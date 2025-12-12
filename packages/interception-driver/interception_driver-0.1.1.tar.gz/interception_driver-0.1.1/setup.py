from setuptools import setup, find_packages
import os

long_description = ""
if os.path.exists("README.md"):
    with open("README.md", encoding="utf-8") as f:
        long_description = f.read()

setup(
    name="interception_driver",
    version="0.1.1",
    author="Ibrahim Arslan",
    author_email="ibrahimarslan226@gmail.com",
    description="Python wrapper for Interception driver (Low-level input)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    
    packages=find_packages(),
    
    include_package_data=True,
    package_data={
        "interception_driver": ["*.dll"],
    },
    
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires='>=3.6',
)