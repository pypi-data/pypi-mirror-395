from setuptools import setup, find_packages

setup(
    name="mctech_core",
    version="1.1.0",
    packages=find_packages(
        include=["mctech_core.*"],
        exclude=["*.tests"]
    ),
    exclude_package_data={"mctech_core": ["testmain.py"]},
    install_requires=["log4py", "pyyaml", "pyDes"]
)
