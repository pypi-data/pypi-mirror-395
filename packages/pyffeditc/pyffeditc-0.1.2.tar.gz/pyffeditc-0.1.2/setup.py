from setuptools import setup, find_packages

setup(
    name="pyffeditc",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        'pywin32; platform_system=="Windows"'
    ],
    author="Peter Grønbæk Andersen",
    author_email="peter@grnbk.io",
    description="A Python wrapper for the ffeditc_unicode.exe utility.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    project_urls={
        "Homepage": "https://github.com/pgroenbaek/pyffeditc",
        "Issues": "https://github.com/pgroenbaek/pyffeditc/issues",
        "Source": "https://github.com/pgroenbaek/pyffeditc",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.6",
)