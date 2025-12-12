from distutils.core import setup

packages = ['txdpy']
setup(name='txdpy',
    version='11.1.1',
    author='唐旭东',
    packages=packages,
    package_dir={'requests': 'requests'},
    install_requires=[
        "lxml","loguru","tqdm","colorama","openpyxl","pymysql","xlsxwriter","xlrd","sshtunnel","requests","fuzzywuzzy","PyMuPDF","pdfplumber","bs4","translate","natsort","six"
    ])