from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="atlas_consortia_commons",
    # Test PyPi version
    # version="1.1.3",
    # Prod PyPi version
    version="1.1.6",
    author="Atlas Consortia",
    author_email="api-developers@hubmapconsortium.org",
    description="The common code supporting the web services in the consortia.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/x-atlas-consortia/commons",
    packages=[
        "atlas_consortia_commons",
        "atlas_consortia_commons.converter",
        "atlas_consortia_commons.decorator",
        "atlas_consortia_commons.file",
        "atlas_consortia_commons.object",
        "atlas_consortia_commons.rest",
        "atlas_consortia_commons.string",
        "atlas_consortia_commons.ubkg",
        "atlas_consortia_commons.url",
    ],
    package_data={"": ["*.json"]},
    include_package_data=True,
    install_requires=[
        "Flask>=3.0.3",
        "Werkzeug>=3.0.3",
        "hubmap-commons>=2.1.18",
        # For now use pinned version of jsonref due to breaking changes made in 1.0.0
        "jsonref==0.3.0",
        "jsonschema>=3.2.0",
        "neo4j>=5.20.0",
        "pytz>=2021.1",
        "property>=2.2",
        # Airflow dependes on globus_sdk==2.0.1
        "globus_sdk>=2.0.1",
        # cwltool uses prov==1.5.1
        # Will remove provenance.py and this prov dependency later
        "prov>=1.5.1",
        # It's an agreement with other collaborators to use the beblow versions
        # for requests and PyYAML
        "requests>=2.32.3",
        "PyYAML>=6.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        # "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
