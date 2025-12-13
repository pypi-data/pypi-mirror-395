from setuptools import setup, find_packages

setup(
    name="promptlog",
    version="0.1.0",
    author="Yam",
    author_email="haoshaochun@gmail.com",
    description="A version control tool for prompts",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/hscspring/promptlog",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    install_requires=[
        "deepdiff>=5.8.1",
        "appdirs>=1.4.4",
    ],
)
