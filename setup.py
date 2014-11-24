# coding=utf-8
from distutils.core import setup
import py2exe


setup(
    console=["main.py"],
    options={
        'py2exe': {
            'includes': 'decimal',
        },
    },
)