from setuptools import setup, find_packages

setup(
    name="funx",
    version="1.0.2",
    author="Khiat Mohammed Abderrezzak",
    author_email="khiat.dev@gmail.com",
    license="MIT",
    description="Python utility functions for cleaner, more readable code",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/funx/",
    packages=find_packages(),
    keywords=[
        "python",
        "utilities",
        "helpers",
        "functions",
        "clean code",
        "readable code",
        "maintainable code",
        "utility library",
        "code quality",
        "developer tools",
        "productivity",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
)
