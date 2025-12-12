import setuptools 

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hyperpod_cheverification_training",
    version="100.0.0",
    author="chehaoha",
    author_email="chehaoha@amazon.com",
    description="HyperPod CHE verification training package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chehaoha/hyperpod-cheverification-training",  # Update with your actual repo URL
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    license="Apache License 2.0",
)
