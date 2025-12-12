from setuptools import setup, find_packages

setup(
    name="nc_user_terminator",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
    ],
    author="bw_song",
    author_email="m132777096902@gmail.com",
    description="OAuth client wrapper for multi-tenant projects",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.8",
)
