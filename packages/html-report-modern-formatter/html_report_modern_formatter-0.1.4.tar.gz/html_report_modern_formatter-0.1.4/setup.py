from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="html-report-modern-formatter",
    version="0.1.4",
    description="Modern HTML formatter for Behave BDD reports",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Agnaldo",
    author_email="aejvilariano128@gmail.com",
    url="https://github.com/Vilariano/html-report-modern-formatter",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "behave>=1.2.6",
        "jinja2>=3.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
