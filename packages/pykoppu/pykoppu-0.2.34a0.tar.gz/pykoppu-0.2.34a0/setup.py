from setuptools import setup, find_packages

setup(
    name="pykoppu",
    version="0.2.34-alpha",
    packages=find_packages(),
    install_requires=[
        "brian2>=2.5",
        "networkx",
        "numpy",
        "scipy",
    ],
    extras_require={
        "doc": [
            "mkdocs-material",
            "mkdocstrings[python]",
        ],
    },
    author="KOPPU Team",
    author_email="contact@koppu.io",
    description="SDK for KOPPU (K-dimensional Organoid Probabilistic Processing Unit)",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://koppu.io",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    python_requires='>=3.8',
    keywords="organoid computing neuromorphic optimization pubo brian2",
)
