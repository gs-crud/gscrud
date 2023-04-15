from setuptools import setup, find_packages
import sys
sys.path[0:0] = ['src/gscrud']


setup(
    name='gscrud',
    version='1.0',
    description='CRUD application for Google Sheet',
    author='muthugit',
    author_email='base.muthupandian@gmail.com',
    url='https://muthupandian.in',
    packages=(find_packages(where="src")),
    package_dir={"": "src"},

)
