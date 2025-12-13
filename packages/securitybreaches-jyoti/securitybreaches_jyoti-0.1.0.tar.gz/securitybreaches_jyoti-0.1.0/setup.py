from setuptools import setup, find_packages

setup(
    name="securitybreaches-jyoti",
    version="0.1.0",
    author="Jyoti Rahate",
    author_email="your.email@example.com",
    description="Security Breaches documentation and resources",
    long_description="A package containing security breaches notes and documentation",
    long_description_content_type="text/plain",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
