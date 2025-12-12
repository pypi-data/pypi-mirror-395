from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()
    

setup(
    name='api_investment_risk',
    version='0.3.9.6',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pandas>=2.2.3",
        "requests>=2.32.3",
    ],
    long_description=description,
    long_description_content_type="text/markdown",
            
)