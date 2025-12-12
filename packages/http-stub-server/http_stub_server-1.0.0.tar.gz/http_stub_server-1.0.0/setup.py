"""
HTTP Stub Server - Setup Configuration
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="http-stub-server",
    version="1.0.0",
    author="Soumya Sagar",
    author_email="soumyasagar@example.com",
    description="A configurable HTTP stub server for e-commerce API testing and development",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Soumya-codr/OJTCheats",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Testing :: Mocking",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
        "Framework :: Flask",
    ],
    python_requires=">=3.8",
    install_requires=[
        "Flask>=3.0.0",
        "Flask-CORS>=4.0.0",
        "watchdog>=3.0.0",
    ],
    entry_points={
        "console_scripts": [
            "http-stub-server=server:main",
        ],
    },
    include_package_data=True,
    keywords="http stub mock api testing development e-commerce flask",
    project_urls={
        "Bug Reports": "https://github.com/Soumya-codr/OJTCheats/issues",
        "Source": "https://github.com/Soumya-codr/OJTCheats",
        "Documentation": "https://github.com/Soumya-codr/OJTCheats/blob/master/README.md",
    },
)
