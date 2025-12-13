from setuptools import setup, find_packages

# setup
setup(
    name="MDUS",
    version = "0.1.5",
    author = "Takuro OGAWA",
    author_email = "polish.stream@gmail.com",
    description = "MDUS: MESSENGER's Data Using System",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url = "https://github.com/streamamz/MDUS",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib",
        "requests",
        "spiceypy",
        "KT17",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    include_package_data=True
)