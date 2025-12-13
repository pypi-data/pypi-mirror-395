from setuptools import setup, find_packages

setup(
    name="mctech_actuator",
    version="1.1.0",
    packages=find_packages(
        include=["mctech_actuator.*"],
        exclude=["*.tests"]
    ),
    exclude_package_data={"mctech_actuator": ["testmain.py"]},
    install_requires=["log4py", "fastapi"]
)
