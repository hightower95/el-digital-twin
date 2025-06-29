from setuptools import setup, find_packages

setup(
    name="toolkit",
    version="0.1.0",
    description="A toolkit package",
    author="Your Name",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["loguru>=0.7.0",],
    python_requires=">=3.7",
)