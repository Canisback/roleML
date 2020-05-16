from setuptools import setup, find_packages

from os import path
this_directory = path.dirname(__file__)
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
    
    
setup(
  name = 'roleml',
  packages = find_packages(),
  package_data={
    '': ['*.sav'],
  },
  version = '0.1.16',
  description = 'ML classifier for role in Riot API LoL matches',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'Canisback',
  author_email = 'canisback@gmail.com',
  url = 'https://github.com/Canisback/roleML',
  keywords = ['Riot API', 'python', 'machine learning','role','League of Legends', ' classifier'],
  classifiers = [],
  install_requires=[
      "scikit-learn >= 0.23.0",
      "numpy >= 1.16.2",
      "shapely",
      "pandas"
  ],
)
