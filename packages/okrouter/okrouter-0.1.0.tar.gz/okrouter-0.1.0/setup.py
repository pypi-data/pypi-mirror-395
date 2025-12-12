from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="okrouter", 
    version="0.1.0",
    author="OKRouter Team",
    author_email="support@okrouter.com", 
    description="The official Python client for OKRouter API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    

    url="https://okrouter.com", 

    project_urls={
        "Documentation": "https://okrouter.com/docs",
        "Source Code": "https://github.com/okrouter/okrouter-python",
        "Website": "https://okrouter.com",
    },
    
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP",
    ],
    python_requires='>=3.6',
    install_requires=[
        "requests", 
    ],
)
