from setuptools import setup, find_packages

setup(
    name="shade-privacy",
    version="1.0.0",
    author="Your Name or Company",
    author_email="your@email.com",
    description="Python SDK for ZK Intent API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/shade-privacy",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.28.0",
        "websockets>=11.0.0",
        "pycryptodome>=3.17.0",
    ],
)