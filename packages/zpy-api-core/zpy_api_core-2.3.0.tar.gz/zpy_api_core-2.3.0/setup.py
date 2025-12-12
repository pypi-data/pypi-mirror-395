import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zpy-api-core",
    version="2.3.0",
    author="Noé Cruz | linkedin.com/in/zurckz/",
    author_email="zurckz.services@gmail.com",
    description="Helper layer for backend application development to Aws Lambda",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NoeCruzMW",
    packages=setuptools.find_packages(),
    install_requires=[
        "marshmallow>=3.23.0,<4.0.0",
        "marshmallow_objects==2.3.0",
        "requests==2.32.5",
        "Click",
        "python-dateutil",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    py_modules=["zpy.cli"],
    entry_points={
        "console_scripts": [
            "zpy = zpy.cli:cli",
        ],
    },
    python_requires=">=3.13",
)
