from os import path
from setuptools import setup, find_packages

this_directory = path.dirname(__file__)
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="roleml",
    packages=find_packages(),
    package_data={"": ["*.sav", "*.json"],},
    version="0.2.2",
    install_requires=["scikit-learn == 0.23.0", "numpy >= 1.16.2", "shapely", "pandas", "joblib"],
    description="ML classifier for role in Riot API LoL matches",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Canisback",
    author_email="canisback@gmail.com",
    url="https://github.com/Canisback/roleML",
    keywords=["Riot API", "python", "machine learning", "role", "League of Legends", " classifier"],
    classifiers=[]
)
