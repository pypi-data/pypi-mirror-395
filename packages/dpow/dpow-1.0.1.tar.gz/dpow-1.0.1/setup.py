from setuptools import setup, find_packages

setup(
    name="dpow",
    version="1.0.1",
    description="Distributed Proof of Work library customized for QudsLab",
    author="QudsLab",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True,
    package_data={
        'dpow': ['bin/*/**'],  # Include binaries if they happen to be there
    },
)
