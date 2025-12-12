from setuptools import setup, find_packages

setup(
    name="anshika_resume", 
    version="0.0.1",
    author="Ansh",
    description="A digital experience for Anshika",
    packages=find_packages(),
    include_package_data=True, # Looks at MANIFEST.in
    install_requires=[
        'requests', # Required for your API
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)