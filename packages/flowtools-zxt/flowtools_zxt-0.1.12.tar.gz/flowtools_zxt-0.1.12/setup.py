from setuptools import setup, find_packages

setup(
    name="flowtools_zxt",
    version="0.1.12",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    author="zhangxutao",
    author_email="zxt0413363@163.com",
)