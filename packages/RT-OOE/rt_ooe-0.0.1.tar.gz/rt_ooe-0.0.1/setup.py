from setuptools import setup, find_packages

setup(
    name="RT_OOE",
    version="0.0.1",
    packages=find_packages(),
    include_package_data=True,
    description="A package to check if a number is odd or even.",
    author="Your Name",
    license="MIT",
    python_requires=">=3.7",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    keywords=["odd", "even", "number"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
