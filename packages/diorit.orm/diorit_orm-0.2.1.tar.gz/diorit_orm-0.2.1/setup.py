
from setuptools import setup, find_packages


setup(
    name='diorit.orm',
    version='0.2.1',
    packages=find_packages(include=["dioritorm", "dioritorm.*"]),
    install_requires=[
        "mysql-connector-python"
    ],
    author='bogdanAntonjuk',
    author_email='info@diorit.com.ua',
    description='Data-modeling core for application development',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
