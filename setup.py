from setuptools import setup, find_packages
setup(
  name = 'roleml',
  packages = find_packages(),
  package_data={
    '': ['*.sav'],
  },
  version = '0.1.8',
  description = 'ML classifier for role in Riot API LoL matches',
  author = 'Canisback',
  author_email = 'canisback@gmail.com',
  url = 'https://github.com/Canisback/roleML',
  keywords = ['Riot API', 'python', 'machine learning','role','Leaue of Legends', ' classifier'],
  classifiers = [],
  install_requires=[
    "scikit-learn",
      "numpy >= 1.16.2",
      "matplotlib",
      "pandas"
  ],
)
