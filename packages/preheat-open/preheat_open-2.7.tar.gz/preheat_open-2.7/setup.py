import setuptools

import versioneer

package_requirements_file = "requirements.txt"
docs_requirements_file = "docs/requirements.txt"
documentation_requirements = open(docs_requirements_file).read().split("\n")

setuptools.setup(
    name="preheat_open",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author="Neogrid and contributors",
    author_email="analytics@neogrid.dk",
    description="Python wrapper for Neogrid Technologies' REST API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://gitlab.com/neogrid-technologies-public/preheat-open-python",
    project_urls={
        "Bug Tracker": "https://gitlab.com/neogrid-technologies-public/preheat-open-python/-/issues",
        "Documentation": "https://preheat-open.readthedocs.io/en/latest/",
        "Source Code": "https://gitlab.com/neogrid-technologies-public/preheat-open-python",
        "Changelog": "https://gitlab.com/neogrid-technologies-public/preheat-open-python/-/blob/master/RELEASE_NOTES.md",
    },
    packages=setuptools.find_packages(),
    data_files=[("requirements", [package_requirements_file, docs_requirements_file])],
    package_data={"preheat_open": ["*.yaml", "api/*.yaml"]},
    include_package_data=True,
    python_requires=">=3.10",
    install_requires=open(package_requirements_file).read().split("\n"),
    extras_require={
        "doc": documentation_requirements,
        "dev": [
            "setuptools>=42",
            "wheel",
            "pytest",
            "pytest-cov",
            "pytest-xdist",
        ]
        + documentation_requirements,
    },
)
