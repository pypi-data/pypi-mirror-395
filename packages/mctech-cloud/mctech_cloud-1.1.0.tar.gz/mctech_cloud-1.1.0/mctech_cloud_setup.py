from setuptools import setup, find_packages

setup(
    name="mctech_cloud",
    version="1.1.0",
    packages=find_packages(
        include=["mctech_cloud.*"],
        exclude=["*.tests"]
    ),
    exclude_package_data={"mctech_cloud": ["testmain.py"]},
    install_requires=["log4py", "fastapi", "starlette",
                      "mctech-actuator", "mctech-discovery"]
)
