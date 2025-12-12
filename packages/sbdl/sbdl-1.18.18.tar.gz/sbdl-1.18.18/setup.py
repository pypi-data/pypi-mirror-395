from setuptools import setup

setup(
  name='sbdl',
  version='1.18.18',
  description = "System Behaviour Description Language (Compiler)",
  author = "Michael A. Hicks",
  author_email = "michael@mahicks.org",
  url = "https://sbdl.dev",
  scripts=['sbdl'],
  py_modules=['sbdl','csv-to-sbdl','sbdl_server'],
  license = "Proprietary",
  python_requires='>=3.6',
  install_requires=['networkx','matplotlib','docx2txt','pandas','openpyxl','docxtpl','jinja2']
)
