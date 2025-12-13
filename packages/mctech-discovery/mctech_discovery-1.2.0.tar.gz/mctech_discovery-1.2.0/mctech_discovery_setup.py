from setuptools import setup, find_packages

setup(
    name="mctech_discovery",
    version="1.2.0",
    packages=find_packages(
        include=["mctech_discovery.*"],
        exclude=["*.tests"]
    ),
    exclude_package_data={"mctech_discovery": ["testmain.py"]},
    install_requires=["log4py", "netifaces",
                      "py_eureka_client", "httpx",
                      "mctech-actuator", "mctech-core", "websocket-client"]
)
