from setuptools import setup, find_packages

setup(
    name="SocatLib",
    version="2.0.1",
    description="Async Python library for network communication using socat",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="ash404.dev",
    author_email="momoh70070@gmail.com",
    url="https://github.com/ash404/SocatLib",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
    ],
)