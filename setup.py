import setuptools

# Thank you to https://packaging.python.org/tutorials/packaging-projects/

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="spontit",
    version="1.0.7",
    author="Spontit Inc",
    author_email="info@spontit.com",
    description="Send push notifications without your app, website, or notification infrastructure.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/spontit/spontit-api-python-wrapper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
