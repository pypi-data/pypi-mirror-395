from setuptools import setup, find_packages

setup(
    name="html-report-modern-formatter",
    version="0.1.3",
    description="Modern HTML formatter for Behave BDD reports",
    author="Agnaldo Vilariano",
    author_email="aejvilariano128@gmai.com",
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
