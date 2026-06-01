from setuptools import setup, find_packages

setup(
    name="vehicle_insurance",
    version="0.0.1",
    author="Hima",
    author_email="himahn2004@gmail.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[],
)