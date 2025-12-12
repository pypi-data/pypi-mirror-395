import os
from setuptools import setup


# Pass package modules files.
# From https://stackoverflow.com/a/36693250/1956471
def package_files(directory):
    paths = []
    for path, directories, filenames in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join("..", path, filename))
    return paths


readme_markdown = None
with open("README.md") as f:
    readme_markdown = f.read()

setup(
    name="tqwgp-parser",
    version="0.8.1",
    url="https://github.com/YtoTech/talk-quote-work-getpaid-parser",
    license="AGPL-3.0",
    author="Yoan Tournade",
    author_email="y@yoantournade.com",
    description="A library for parsing Talk Quote Work Get-Paid (TQWGP) text-based compliant sales and accounting documents.",
    long_description=readme_markdown,
    long_description_content_type="text/markdown",
    # TODO console_scripts?
    # https://python-packaging.readthedocs.io/en/latest/command-line-scripts.html
    scripts=["scripts/tqwgp"],
    packages=["tqwgp_parser"],
    include_package_data=True,
    package_data={
        # "tqwgp_parser": ["*.hy"],
        "tqwgp_parser": package_files("tqwgp_parser"),
    },
    zip_safe=False,
    platforms="any",
    install_requires=[
        "hy>=0.26.0",
        "toolz",
        # "hyrule",
        "pendulum",
        "toml",
        "pyyaml",
        "click",
        "babel",
    ],
)
