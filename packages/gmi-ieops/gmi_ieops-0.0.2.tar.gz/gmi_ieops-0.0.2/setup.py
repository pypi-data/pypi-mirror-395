from setuptools import setup, find_packages

sdk_packages = find_packages(where='sdk')
packages = ['gmi_ieops'] + [f'gmi_ieops.{p}' for p in sdk_packages]

setup(
    name="gmi_ieops",
    version="0.0.2",
    author="GMICloud Inc.",
    packages=packages,
    package_dir={'gmi_ieops': 'sdk'},
    python_requires=">=3.10",
    install_requires=[]
)
