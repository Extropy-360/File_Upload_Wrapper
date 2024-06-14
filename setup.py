from setuptools import setup

setup(
    name="File_Upload_Wrapper",
    version="0.2.0",
    description="A wrapper for uploading files to the portal",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Extropy-360/File_Upload_Wrapper",
    py_modules=["file_upload_wrapper"],
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
