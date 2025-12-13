from setuptools import setup
from mypyc.build import mypycify


setup(ext_modules=mypycify(["faster_async_lru/__init__.py", "--strict", "--pretty"]))
