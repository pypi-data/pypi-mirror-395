import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="openemr",
    version="0.4.1",
    author="Stein van Broekhoven",
    author_email="stein@aapjeisbaas.nl",
    description="An OpenEMR api connector",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/aapjeisbaas/openemr-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests'
    ]
)