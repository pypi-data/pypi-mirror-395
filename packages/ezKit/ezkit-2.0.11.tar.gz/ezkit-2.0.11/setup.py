"""setup"""

from setuptools import find_packages, setup

setup(
    name="ezKit",
    version="2.0.11",
    author="septvean",
    author_email="septvean@gmail.com",
    description="Easy Kit",
    packages=find_packages(exclude=["deprecated", "documents", "tests"]),
    include_package_data=True,
    # package_data={"ezKit": ["markdown_to_html.template"]},
    python_requires=">=3.12",
    install_requires=["loguru>=0.7"],
)
