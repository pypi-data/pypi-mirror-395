from setuptools import setup, find_packages

setup(
    name="fronttracker",
    version="1.1.0",
    author="Emmanuel Romero",
    author_email="romeroqe@gmail.com",
    description="Library for detection and monitoring of ocean fronts",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/romeroqe/fronttracker",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "geopy",
        "scipy",
        "scikit-learn",
        "scikit-image",
        "shapely",
        "alphashape",
        "matplotlib"
    ],
    license="CC-BY-4.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)