from setuptools import setup, find_packages

setup(
    name="Portal-Upload-Wrapper",
    version="0.1.0",
    description="A wrapper for uploading files to the portal",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Extropy-360/Portal-Upload-Wrapper",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
