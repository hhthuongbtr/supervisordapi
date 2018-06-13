import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="supervisordapi",
    version="0.0.1",
    author="Thuong Huynh",
    author_email="hhthuongbtr@gmail.com",
    description="supervisord API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hhthuongbtr/supervisordapi.git",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
