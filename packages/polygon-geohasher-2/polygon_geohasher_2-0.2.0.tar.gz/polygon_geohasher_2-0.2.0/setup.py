from setuptools import setup, find_packages


def readme() -> str:
    with open("README.md") as f:
        return f.read()


def requirements() -> str:
    with open("requirements.txt") as f:
        return f.read()


setup(
    name="polygon-geohasher-2",
    author="Alberto Bonsanto; maintained by Jon Duckworth",
    author_email="",
    url="https://github.com/duckontheweb/polygon-geohasher",
    description="""Wrapper over Shapely that returns the set of geohashes that form a Polygon.""",
    long_description=readme(),
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(),
    package_data={"": ["py.typed"]},
    install_requires=requirements(),
    python_requires=">=3.10,<3.15",
    include_package_data=False,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
    ],
    keywords=["polygon", "geohashes"],
)
