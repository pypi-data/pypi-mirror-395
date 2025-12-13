from setuptools import setup, find_packages

setup(
    name="rowsncolumns-spreadsheet",
    version="0.1.5",
    description="Python implementation of rowsncolumns spreadsheet operations",
    author="Rows & Columns",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "pydantic>=2.0.0",
        "typing-extensions>=4.0.0",
        "jsonpatch>=1.33",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "mypy>=1.0.0",
        ]
    },
)