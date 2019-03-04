from setuptools import setup, find_packages
setup(
  name = 'roleml',
  packages = find_packages(),
  version = '0.1.0',
  description = 'ML classifier for role in Riot API LoL matches',
  author = 'Canisback',
  author_email = 'canisback@gmail.com',
  url = 'https://github.com/Canisback/roleML',
  keywords = ['Riot API', 'python', 'machine learning','role','Leaue of Legends', ' classifier'],
  classifiers = [],
  install_requires=[
    "scikit-learn",
      "numpy",
      "matplotlib",
      "pandas"
  ],
)
