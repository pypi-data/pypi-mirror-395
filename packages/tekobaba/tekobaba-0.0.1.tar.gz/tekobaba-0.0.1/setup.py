from setuptools import setup, find_packages

setup(
    name="tekobaba",
    version="0.0.1",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "tekobaba": ["resources/*"],
    },
    description="tekobaba özel paket",
)
