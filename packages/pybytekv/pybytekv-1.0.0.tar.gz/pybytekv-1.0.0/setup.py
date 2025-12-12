from setuptools import setup, find_packages

setup(
    name="pybytekv",
    version="1.0.0",
    packages=find_packages(),
    description="Full-feature Python client for ByteKV server (TCP + RESP)",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="VSSCO",
    url="https://github.com/your-repo/pybytekv",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
